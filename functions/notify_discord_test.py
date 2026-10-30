# -*- coding: utf-8 -*-
"""
    Discord Notification Test
    -----------------------

    Unit tests for `main.py`

"""

import ast
import json
import logging
import os

import main
import pytest


def test_sns_get_discord_message_payload_snapshots(snapshot, monkeypatch):
    """
    Compare outputs of get_discord_message_payload() with snapshots stored

    Run `pipenv run test:updatesnapshots` to update snapshot images
    """

    monkeypatch.setenv("DISCORD_AVATAR_URL", "https://i.imgur.com/eeYUFCO_d.webp")
    monkeypatch.setenv("DISCORD_USERNAME", "main_test")

    # These are SNS messages that invoke the lambda handler; the event payload is in the
    # `message` field
    _dir = "./messages"
    messages = [f for f in os.listdir(_dir) if os.path.isfile(os.path.join(_dir, f))]

    for file in messages:
        with open(os.path.join(_dir, file), "r") as ofile:
            event = ast.literal_eval(ofile.read())

            attachments = []
            # These are as delivered wrapped in an SNS message payload so we unpack
            for record in event["Records"]:
                sns = record["Sns"]
                subject = sns["Subject"]
                message = sns["Message"]
                region = sns["TopicArn"].split(":")[3]

                attachment = main.get_discord_message_payload(
                    message=message, region=region, subject=subject
                )
                attachments.append(attachment)

            filename = os.path.basename(file)
            snapshot.assert_match(attachments, f"message_{filename}")


def test_event_get_discord_message_payload_snapshots(snapshot, monkeypatch):
    """
    Compare outputs of get_discord_message_payload() with snapshots stored

    Run `pipenv run test:updatesnapshots` to update snapshot images
    """

    monkeypatch.setenv("DISCORD_AVATAR_URL", "https://i.imgur.com/eeYUFCO_d.webp")
    monkeypatch.setenv("DISCORD_USERNAME", "main_test")

    # These are just the raw events that will be converted to JSON string and
    # sent via SNS message
    _dir = "./events"
    events = [f for f in os.listdir(_dir) if os.path.isfile(os.path.join(_dir, f))]

    for file in events:
        with open(os.path.join(_dir, file), "r") as ofile:
            event = ast.literal_eval(ofile.read())

            attachment = main.get_discord_message_payload(
                message=event, region="us-east-1", subject="bar"
            )
            attachments = [attachment]

            filename = os.path.basename(file)
            snapshot.assert_match(attachments, f"event_{filename}")


def test_environment_variables_set(monkeypatch):
    """
    Should pass since environment variables are provided
    """

    monkeypatch.setenv("DISCORD_AVATAR_URL", "https://i.imgur.com/eeYUFCO_d.webp")
    monkeypatch.setenv("DISCORD_USERNAME", "main_test")
    monkeypatch.setenv(
        "DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/HOOK_ID/HOOK_TOKEN"
    )

    with open(os.path.join("./messages/text_message.json"), "r") as efile:
        event = ast.literal_eval(efile.read())

        for record in event["Records"]:
            sns = record["Sns"]
            subject = sns["Subject"]
            message = sns["Message"]
            region = sns["TopicArn"].split(":")[3]

            main.get_discord_message_payload(
                message=message, region=region, subject=subject
            )


def test_environment_variables_missing():
    """
    Should pass since environment variables are NOT provided and
    will raise a `KeyError`
    """
    with pytest.raises(KeyError):
        # will raise before parsing/validation
        main.get_discord_message_payload(message={}, region="foo", subject="bar")


@pytest.mark.parametrize(
    "region,service,expected",
    [
        (
            "us-east-1",
            "cloudwatch",
            "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1",
        ),
        (
            "us-gov-east-1",
            "cloudwatch",
            "https://console.amazonaws-us-gov.com/cloudwatch/home?region=us-gov-east-1",
        ),
        (
            "us-east-1",
            "guardduty",
            "https://console.aws.amazon.com/guardduty/home?region=us-east-1",
        ),
        (
            "us-gov-east-1",
            "guardduty",
            "https://console.amazonaws-us-gov.com/guardduty/home?region=us-gov-east-1",
        ),
    ],
)
def test_get_service_url(region, service, expected):
    assert main.get_service_url(region=region, service=service) == expected


def test_get_service_url_exception():
    """
    Should raise error since service is not defined in enum
    """
    with pytest.raises(KeyError):
        main.get_service_url(region="us-east-1", service="athena")


def test_lambda_handler_empty_records(monkeypatch, caplog):
    """
    Should return a "no records" result and warn, without raising.

    Regression test: lambda_handler referenced `response` outside the for-loop,
    which raised UnboundLocalError when event["Records"] was empty because the
    loop body never executed and `response` was never assigned.
    """
    monkeypatch.setenv("DISCORD_AVATAR_URL", "https://i.imgur.com/eeYUFCO_d.webp")
    monkeypatch.setenv("DISCORD_USERNAME", "main_test")

    with caplog.at_level(logging.WARNING):
        result = main.lambda_handler(event={"Records": []}, context={})

    payload = json.loads(result)
    assert payload["code"] == 200
    assert payload["info"] == "No records to process"
    assert "No SNS records" in caplog.text


def test_lambda_handler_does_not_log_error_for_204(monkeypatch, caplog):
    """
    Should treat Discord's 204 No Content as a successful send.

    A successful webhook execution returns 204 No Content; 200 with a body is
    returned only when the webhook is executed with the `wait` parameter.
    """
    monkeypatch.setenv("DISCORD_AVATAR_URL", "https://i.imgur.com/eeYUFCO_d.webp")
    monkeypatch.setenv("DISCORD_USERNAME", "main_test")
    monkeypatch.setenv("DISCORD_EMOJI", ":aws:")
    monkeypatch.setenv(
        "DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/HOOK_ID/HOOK_TOKEN"
    )

    def fake_send_discord_notification(payload):
        return json.dumps({"code": 204, "info": "No Content"})

    monkeypatch.setattr(main, "send_discord_notification", fake_send_discord_notification)

    with open(os.path.join("./messages/text_message.json"), "r") as efile:
        event = ast.literal_eval(efile.read())

    with caplog.at_level(logging.DEBUG):
        response = main.lambda_handler(event=event, context={})

    assert json.loads(response)["code"] == 204
    assert not [record for record in caplog.records if record.levelno >= logging.ERROR]

# -*- coding: utf-8 -*-
"""
    Discord Notification Test
    -----------------------

    Unit tests for `main.py`

"""

import ast
import json
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


def test_lambda_handler_empty_records(monkeypatch):
    """
    Should not raise when the event has no Records.

    Regression test: lambda_handler referenced `response` outside the for-loop,
    which raised NameError when event["Records"] was empty because the loop
    body never executed and `response` was never assigned.
    """
    monkeypatch.setenv("DISCORD_AVATAR_URL", "https://i.imgur.com/eeYUFCO_d.webp")
    monkeypatch.setenv("DISCORD_USERNAME", "main_test")

    result = main.lambda_handler(event={"Records": []}, context={})

    assert json.loads(result)["code"] == 200

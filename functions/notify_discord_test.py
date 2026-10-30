# -*- coding: utf-8 -*-
"""
    Discord Notification Test
    -----------------------

    Unit tests for `main.py`

"""

import ast
import json
import os
from typing import Dict

import main
import pytest


class FakeCognitoIdentity:
    """Stand-in for the Cognito identity of the Lambda context object."""

    identity_id = "us-east-1:00000000-0000-0000-0000-000000000000"
    identity_pool_id = "us-east-1:00000000-0000-0000-0000-000000000000"


class FakeClientContextClient:
    """Stand-in for the client details of the Lambda context object."""

    installation_id = "00000000-0000-0000-0000-000000000000"
    app_title = "notify-discord-test"
    app_version_name = "1.0.0"
    app_version_code = "1"
    app_package_name = "com.example.notify_discord"


class FakeClientContext:
    """Stand-in for the client context of the Lambda context object."""

    client = FakeClientContextClient()
    custom: Dict[str, str] = {}
    env: Dict[str, str] = {}


class FakeLambdaContext:
    """Stand-in for the context object the AWS Lambda runtime passes to the handler.

    The attributes mirror the ones documented for the Lambda runtime interface
    client: https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
    """

    function_name = "notify_discord"
    function_version = "$LATEST"
    invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:notify_discord"
    memory_limit_in_mb = "128"
    aws_request_id = "00000000-0000-0000-0000-000000000000"
    log_group_name = "/aws/lambda/notify_discord"
    log_stream_name = "2024/01/01/[$LATEST]00000000000000000000000000000000"
    identity = FakeCognitoIdentity()
    client_context = FakeClientContext()

    def get_remaining_time_in_millis(self) -> int:
        return 30000


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


def test_lambda_context_protocol_matches_runtime_context():
    """
    Should satisfy the LambdaContext protocol.

    Guards the annotation of lambda_handler's `context` parameter: the object
    that the AWS Lambda runtime passes (modelled here from the documented
    runtime interface client) must satisfy the protocol, so the annotation
    cannot drift away from what the runtime actually provides.
    """
    assert isinstance(FakeLambdaContext(), main.LambdaContext)


def test_lambda_context_protocol_rejects_plain_dict():
    """
    Should not satisfy the LambdaContext protocol.

    A plain dict was the previous (incorrect) annotation for `context`; it must
    not match the protocol.
    """
    assert not isinstance({}, main.LambdaContext)


def test_lambda_handler_accepts_lambda_context(monkeypatch):
    """
    Should accept the runtime context object and return the send result.

    Exercises lambda_handler with a context object (not a dict) to prove the
    handler works with what the runtime actually passes.
    """
    monkeypatch.setenv("DISCORD_AVATAR_URL", "https://i.imgur.com/eeYUFCO_d.webp")
    monkeypatch.setenv("DISCORD_USERNAME", "main_test")
    monkeypatch.setenv("DISCORD_EMOJI", ":aws:")
    monkeypatch.setenv(
        "DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/HOOK_ID/HOOK_TOKEN"
    )

    sent = {}

    def fake_send_discord_notification(payload):
        sent["payload"] = payload
        return json.dumps({"code": 200, "info": "stubbed"})

    monkeypatch.setattr(main, "send_discord_notification", fake_send_discord_notification)

    with open(os.path.join("./messages/text_message.json"), "r") as efile:
        event = ast.literal_eval(efile.read())

    response = main.lambda_handler(event=event, context=FakeLambdaContext())

    assert json.loads(response)["code"] == 200
    assert "payload" in sent

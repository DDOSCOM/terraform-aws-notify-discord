import base64
import json
import logging
import os
import urllib.parse
import urllib.request
from enum import Enum
from typing import Any, Dict, Optional, Union, cast
from urllib.error import HTTPError

import boto3

# Set default region if not provided
REGION = os.environ.get("AWS_REGION", "us-east-1")

# Create client so its cached/frozen between invocations
KMS_CLIENT = boto3.client("kms", region_name=REGION)


class AwsService(Enum):
    """AWS service supported by function"""

    cloudwatch = "cloudwatch"
    guardduty = "guardduty"


def decrypt_url(encrypted_url: str) -> str:
    """Decrypt encrypted URL with KMS

    :param encrypted_url: URL to decrypt with KMS
    :returns: plaintext URL
    """
    try:
        decrypted_payload = KMS_CLIENT.decrypt(
            CiphertextBlob=base64.b64decode(encrypted_url)
        )
        return decrypted_payload["Plaintext"].decode()
    except Exception:
        logging.exception("Failed to decrypt URL with KMS")
        return ""


def get_service_url(region: str, service: str) -> str:
    """Get the appropriate service URL for the region

    :param region: name of the AWS region
    :param service: name of the AWS service
    :returns: AWS console url formatted for the region and service provided
    """
    try:
        service_name = AwsService[service].value
        if region.startswith("us-gov-"):
            return f"https://console.amazonaws-us-gov.com/{service_name}/home?region={region}"
        else:
            return f"https://console.aws.amazon.com/{service_name}/home?region={region}"

    except KeyError:
        print(f"Service {service} is currently not supported")
        raise


class CloudWatchAlarmState(Enum):
    """Maps CloudWatch notification state to Discord message format color"""

    OK = "1834752"
    INSUFFICIENT_DATA = "16761600"
    ALARM = "16711680"


def format_cloudwatch_alarm(message: Dict[str, Any], region: str) -> Dict[str, Any]:
    """Format CloudWatch alarm event into Discord message format

    :params message: SNS message body containing CloudWatch alarm event
    :region: AWS region where the event originated from
    :returns: formatted Discord message payload
    """

    cloudwatch_url = get_service_url(region=region, service="cloudwatch")
    alarm_name = message["AlarmName"]

    return {
        "author": {
            "name": "Cloudwatch Alarm",
            "url": cloudwatch_url,
            "icon_url": "https://i.imgur.com/llpFFJc_d.webp"
        },
        "title": alarm_name,
        "url": cloudwatch_url,
        "description": message["AlarmDescription"],
        "color": CloudWatchAlarmState[message["NewStateValue"]].value,
        "fields": [
            {
                "name": "Alarm Description",
                "value": f"`{message['AlarmDescription']}`"
            },
            {
                "name": "Alarm reason",
                "value": f"`{message['NewStateReason']}`"
            },
            {
                "name": "Old State",
                "value": f"`{message['OldStateValue']}`",
                "inline": "true"
            },
            {
                "name": "Current State",
                "value": f"`{message['NewStateValue']}`",
                "inline": "true"
            },
            {
                "name": "Link to Alarm",
                "value": f"{cloudwatch_url}#alarm:alarmFilter=ANY;name={urllib.parse.quote(alarm_name)}"
            },
        ],
        "thumbnail": {"url": "https://i.imgur.com/llpFFJc_d.webp"},
        "footer": {
            "text": f"AWS CloudWatch notification - {message['AlarmName']}"
        }
    }


class GuardDutyFindingSeverity(Enum):
    """Maps GuardDuty finding severity to Discord message format color"""

    Low = "5046016"
    Medium = "16761600"
    High = "16711680"


def format_guardduty_finding(message: Dict[str, Any], region: str) -> Dict[str, Any]:
    """
    Format GuardDuty finding event into Discord message format

    :params message: SNS message body containing GuardDuty finding event
    :params region: AWS region where the event originated from
    :returns: formatted Discord message payload
    """

    guardduty_url = get_service_url(region=region, service="guardduty")
    detail = message["detail"]
    service = detail.get("service", {})
    severity_score = detail.get("severity")

    if severity_score < 4.0:
        severity = "Low"
    elif severity_score < 7.0:
        severity = "Medium"
    else:
        severity = "High"

    return {
        "author": {
            "name": "GuardDuty Alarm",
            "url": guardduty_url,
            "icon_url": "https://i.imgur.com/V37bZBb_d.webp"
        },
        "title": f"`Severity Score {severity_score}`",
        "url": guardduty_url,
        "description": detail.get("title"),
        "color": GuardDutyFindingSeverity[severity].value,
        "fields": [
            {
                "name": "Description",
                "value": detail["description"]
            },
            {
                "name": "Finding Type",
                "value": f"`{detail['type']}`"
            },
            {
                "name": "First Seen",
                "value": f"`{service['eventFirstSeen']}`",
                "inline": "true"
            },
            {
                "name": "Last Seen",
                "value": f"`{service['eventLastSeen']}`",
                "inline": "true"
            },
            {
                "name": "Severity",
                "value": f"`{severity}`",
                "inline": "true"
            },
            {
                "name": "Count",
                "value": f"`{service['count']}`",
                "inline": "true"
            },
            {
                "name": "Link to Finding",
                "value": f"{guardduty_url}#/findings?search=id%3D{detail['id']}"
            }
        ],
        "thumbnail": {"url": "https://i.imgur.com/V37bZBb_d.webp"},
        "footer": {
            "text": f"AWS GuardDuty Finding - {detail.get('title')}"
        }
    }


def format_default(
        message: Union[str, Dict], subject: Optional[str] = None
) -> Dict[str, Any]:
    """
    Default formatter, converting event into Discord message format

    :params message: SNS message body containing message/event
    :returns: formatted Discord message payload
    """
    attachments = {
        "author": {
            "name": "AWS Notification",
            "icon_url": os.environ["DISCORD_AVATAR_URL"]
        },
        "title": subject if subject else "Message",
        "description": "A new default message",
        "color": "4607"
    }

    fields = []

    if type(message) is dict:
        for k, v in message.items():
            value = f"{json.dumps(v)}" if isinstance(v, (dict, list)) else str(v)
            fields.append({"name": k, "value": f"`{value}`", "inline": len(value) < 25})
    else:
        fields.append({"name": "Event", "value": message, "inline": "false"})

    if fields:
        attachments["fields"] = fields  # type: ignore

    return attachments


def get_discord_message_payload(
        message: Union[str, Dict], region: str, subject: Optional[str] = None
) -> Dict:
    """
    Parse notification message and format into Discord message payload

    :params message: SNS message body notification payload
    :params region: AWS region where the event originated from
    :params subject: Optional subject line for Discord notification
    :returns: Discord message payload
    """

    discord_username = os.environ["DISCORD_USERNAME"]
    discord_avatar = os.environ["DISCORD_AVATAR_URL"]

    payload = {
        "username": discord_username,
        "avatar_url": discord_avatar,
        "content": "New AWS Notification"
    }
    embeds = None

    if isinstance(message, str):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            logging.info("Not a structured payload, just a string message")

    message = cast(Dict[str, Any], message)

    if "AlarmName" in message:
        notification = format_cloudwatch_alarm(message=message, region=region)
        embeds = notification

    elif (
            isinstance(message, Dict) and message.get("detail-type") == "GuardDuty Finding"
    ):
        notification = format_guardduty_finding(
            message=message, region=message["region"]
        )
        embeds = notification

    elif "embeds" in message or "text" in message:
        payload = {**payload, **message}

    else:
        embeds = format_default(message=message, subject=subject)

    if embeds:
        payload["embeds"] = [embeds]  # type: ignore

    return payload


def send_discord_notification(payload: Dict[str, Any]) -> str:
    """
    Send notification payload to Discord

    :params payload: formatted Discord message payload
    :returns: response details from sending notification
    """

    discord_url = os.environ["DISCORD_WEBHOOK_URL"]
    if not discord_url.startswith("http"):
        discord_url = decrypt_url(discord_url)

    req = urllib.request.Request(discord_url)
    data = json.dumps(payload).encode('utf-8')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('User-agent', 'aws-lambda/3.9')
    req.add_header('Content-Length', str(len(data)))
    try:
        result = urllib.request.urlopen(req, data)
        return json.dumps({"code": result.getcode(), "info": result.info().as_string()})
    except HTTPError as e:
        # logging.error(f"{e}: result")
        return json.dumps({"code": e.getcode(), "info": e.info().as_string()})


def lambda_handler(event: Dict[str, Any], context: Dict[str, Any]) -> str:
    """
    Lambda function to parse notification events and forward to Discord

    :param event: lambda expected event object
    :param context: lambda expected context object
    :returns: none
    """

    if os.environ.get("LOG_EVENTS", "False") == "True":
        logging.info(f"Event logging enabled: `{json.dumps(event)}`")

    # Initialise the response so lambda_handler does not raise NameError when
    # event["Records"] is empty (the for-loop body never runs in that case).
    response = json.dumps({"code": 200, "info": ""})

    for record in event["Records"]:
        sns = record["Sns"]
        subject = sns["Subject"]
        message = sns["Message"]
        region = sns["TopicArn"].split(":")[3]

        payload = get_discord_message_payload(
            message=message, region=region, subject=subject
        )
        response = send_discord_notification(payload=payload)

    if json.loads(response)["code"] != 200:
        response_info = json.loads(response)["info"]
        logging.error(
            f"Error: received status `{response_info}` using event `{event}` and context `{context}`"
        )

    return response

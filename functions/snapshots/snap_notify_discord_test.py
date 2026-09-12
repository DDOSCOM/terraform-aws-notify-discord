# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_event_get_discord_message_payload_snapshots event_cloudwatch_alarm.json'] = [
    {
        'avatar_url': 'https://i.imgur.com/eeYUFCO_d.webp',
        'content': 'New AWS Notification',
        'embeds': [
            {
                'author': {
                    'icon_url': 'https://i.imgur.com/llpFFJc_d.webp',
                    'name': 'Cloudwatch Alarm',
                    'url': 'https://console.aws.amazon.com/cloudwatch/home?region=us-east-1'
                },
                'color': '16711680',
                'description': 'Example alarm description.',
                'fields': [
                    {
                        'name': 'Alarm Description',
                        'value': '`Example alarm description.`'
                    },
                    {
                        'name': 'Alarm reason',
                        'value': '`Threshold Crossed`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Old State',
                        'value': '`OK`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Current State',
                        'value': '`ALARM`'
                    },
                    {
                        'name': 'Link to Alarm',
                        'value': 'https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#alarm:alarmFilter=ANY;name=Example'
                    }
                ],
                'footer': {
                    'text': 'AWS CloudWatch notification - Example'
                },
                'thumbnail': {
                    'url': 'https://i.imgur.com/llpFFJc_d.webp'
                },
                'title': 'Example',
                'url': 'https://console.aws.amazon.com/cloudwatch/home?region=us-east-1'
            }
        ],
        'username': 'main_test'
    }
]

snapshots['test_event_get_discord_message_payload_snapshots event_guardduty_finding_high.json'] = [
    {
        'avatar_url': 'https://i.imgur.com/eeYUFCO_d.webp',
        'content': 'New AWS Notification',
        'embeds': [
            {
                'author': {
                    'icon_url': 'https://i.imgur.com/V37bZBb_d.webp',
                    'name': 'GuardDuty Alarm',
                    'url': 'https://console.aws.amazon.com/guardduty/home?region=us-east-1'
                },
                'color': '16711680',
                'description': 'SAMPLE Unprotected port on EC2 instance i-123123123 is being probed',
                'fields': [
                    {
                        'name': 'Description',
                        'value': 'EC2 instance has an unprotected port which is being probed by a known malicious host.'
                    },
                    {
                        'name': 'Finding Type',
                        'value': '`Recon:EC2 PortProbeUnprotectedPort`'
                    },
                    {
                        'inline': 'true',
                        'name': 'First Seen',
                        'value': '`2020-01-02T01:02:03Z`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Last Seen',
                        'value': '`2020-01-03T01:02:03Z`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Severity',
                        'value': '`High`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Count',
                        'value': '`1234`'
                    },
                    {
                        'name': 'Link to Finding',
                        'value': 'https://console.aws.amazon.com/guardduty/home?region=us-east-1#/findings?search=id%3Dsample-id-2'
                    }
                ],
                'footer': {
                    'text': 'AWS GuardDuty Finding - SAMPLE Unprotected port on EC2 instance i-123123123 is being probed'
                },
                'thumbnail': {
                    'url': 'https://i.imgur.com/V37bZBb_d.webp'
                },
                'title': '`Severity Score 9`',
                'url': 'https://console.aws.amazon.com/guardduty/home?region=us-east-1'
            }
        ],
        'username': 'main_test'
    }
]

snapshots['test_event_get_discord_message_payload_snapshots event_guardduty_finding_medium.json'] = [
    {
        'avatar_url': 'https://i.imgur.com/eeYUFCO_d.webp',
        'content': 'New AWS Notification',
        'embeds': [
            {
                'author': {
                    'icon_url': 'https://i.imgur.com/V37bZBb_d.webp',
                    'name': 'GuardDuty Alarm',
                    'url': 'https://console.aws.amazon.com/guardduty/home?region=us-east-1'
                },
                'color': '16761600',
                'description': 'SAMPLE Unprotected port on EC2 instance i-123123123 is being probed',
                'fields': [
                    {
                        'name': 'Description',
                        'value': 'EC2 instance has an unprotected port which is being probed by a known malicious host.'
                    },
                    {
                        'name': 'Finding Type',
                        'value': '`Recon:EC2 PortProbeUnprotectedPort`'
                    },
                    {
                        'inline': 'true',
                        'name': 'First Seen',
                        'value': '`2020-01-02T01:02:03Z`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Last Seen',
                        'value': '`2020-01-03T01:02:03Z`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Severity',
                        'value': '`Medium`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Count',
                        'value': '`1234`'
                    },
                    {
                        'name': 'Link to Finding',
                        'value': 'https://console.aws.amazon.com/guardduty/home?region=us-east-1#/findings?search=id%3Dsample-id-2'
                    }
                ],
                'footer': {
                    'text': 'AWS GuardDuty Finding - SAMPLE Unprotected port on EC2 instance i-123123123 is being probed'
                },
                'thumbnail': {
                    'url': 'https://i.imgur.com/V37bZBb_d.webp'
                },
                'title': '`Severity Score 5`',
                'url': 'https://console.aws.amazon.com/guardduty/home?region=us-east-1'
            }
        ],
        'username': 'main_test'
    }
]

snapshots['test_event_get_discord_message_payload_snapshots event_guardduty_finding_low.json'] = [
    {
        'avatar_url': 'https://i.imgur.com/eeYUFCO_d.webp',
        'content': 'New AWS Notification',
        'embeds': [
            {
                'author': {
                    'icon_url': 'https://i.imgur.com/V37bZBb_d.webp',
                    'name': 'GuardDuty Alarm',
                    'url': 'https://console.aws.amazon.com/guardduty/home?region=us-east-1'
                },
                'color': '5046016',
                'description': 'SAMPLE Unprotected port on EC2 instance i-123123123 is being probed',
                'fields': [
                    {
                        'name': 'Description',
                        'value': 'EC2 instance has an unprotected port which is being probed by a known malicious host.'
                    },
                    {
                        'name': 'Finding Type',
                        'value': '`Recon:EC2 PortProbeUnprotectedPort`'
                    },
                    {
                        'inline': 'true',
                        'name': 'First Seen',
                        'value': '`2020-01-02T01:02:03Z`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Last Seen',
                        'value': '`2020-01-03T01:02:03Z`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Severity',
                        'value': '`Low`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Count',
                        'value': '`1234`'
                    },
                    {
                        'name': 'Link to Finding',
                        'value': 'https://console.aws.amazon.com/guardduty/home?region=us-east-1#/findings?search=id%3Dsample-id-2'
                    }
                ],
                'footer': {
                    'text': 'AWS GuardDuty Finding - SAMPLE Unprotected port on EC2 instance i-123123123 is being probed'
                },
                'thumbnail': {
                    'url': 'https://i.imgur.com/V37bZBb_d.webp'
                },
                'title': '`Severity Score 2`',
                'url': 'https://console.aws.amazon.com/guardduty/home?region=us-east-1'
            }
        ],
        'username': 'main_test'
    }
]

snapshots['test_sns_get_discord_message_payload_snapshots message_cloudwatch_alarm.json'] = [
    {
        'avatar_url': 'https://i.imgur.com/eeYUFCO_d.webp',
        'content': 'New AWS Notification',
        'embeds': [
            {
                'author': {
                    'icon_url': 'https://i.imgur.com/llpFFJc_d.webp',
                    'name': 'Cloudwatch Alarm',
                    'url': 'https://console.aws.amazon.com/cloudwatch/home?region=us-east-1'
                },
                'color': '1834752',
                'description': 'App is reporting "A JPA error occurred(Unable to build EntityManagerFactory)"',
                'fields': [
                    {
                        'name': 'Alarm Description',
                        'value': '`App is reporting "A JPA error occurred(Unable to build EntityManagerFactory)"`'
                    },
                    {
                        'name': 'Alarm reason',
                        'value': '`Threshold Crossed: 1 datapoint [1.0 (12/02/19 15:44:00)] was not less than the threshold (1.0).`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Old State',
                        'value': '`ALARM`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Current State',
                        'value': '`OK`'
                    },
                    {
                        'name': 'Link to Alarm',
                        'value': 'https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#alarm:alarmFilter=ANY;name=DBMigrationRequired'
                    }
                ],
                'footer': {
                    'text': 'AWS CloudWatch notification - DBMigrationRequired'
                },
                'thumbnail': {
                    'url': 'https://i.imgur.com/llpFFJc_d.webp'
                },
                'title': 'DBMigrationRequired',
                'url': 'https://console.aws.amazon.com/cloudwatch/home?region=us-east-1'
            }
        ],
        'username': 'main_test'
    }
]

snapshots['test_sns_get_discord_message_payload_snapshots message_dms_notification.json'] = [
    {
        'avatar_url': 'https://i.imgur.com/eeYUFCO_d.webp',
        'content': 'New AWS Notification',
        'embeds': [
            {
                'author': {
                    'icon_url': 'https://i.imgur.com/eeYUFCO_d.webp',
                    'name': 'AWS Notification'
                },
                'color': '4607',
                'description': 'A new default message',
                'fields': [
                    {
                        'inline': True,
                        'name': 'Event Source',
                        'value': '`replication-task`'
                    },
                    {
                        'inline': True,
                        'name': 'Event Time',
                        'value': '`2019-02-12 15:45:24.091`'
                    },
                    {
                        'inline': False,
                        'name': 'Identifier Link',
                        'value': '`https://console.aws.amazon.com/dms/home?region=us-east-1#tasks:ids=hello-world`'
                    },
                    {
                        'inline': True,
                        'name': 'SourceId',
                        'value': '`hello-world`'
                    },
                    {
                        'inline': False,
                        'name': 'Event ID',
                        'value': '`http://docs.aws.amazon.com/dms/latest/userguide/CHAP_Events.html#DMS-EVENT-0079 `'
                    },
                    {
                        'inline': False,
                        'name': 'Event Message',
                        'value': '`Replication task has stopped.`'
                    }
                ],
                'title': 'DMS Notification Message'
            }
        ],
        'username': 'main_test'
    }
]

snapshots['test_sns_get_discord_message_payload_snapshots message_glue_notification.json'] = [
    {
        'avatar_url': 'https://i.imgur.com/eeYUFCO_d.webp',
        'content': 'New AWS Notification',
        'embeds': [
            {
                'author': {
                    'icon_url': 'https://i.imgur.com/eeYUFCO_d.webp',
                    'name': 'AWS Notification'
                },
                'color': '4607',
                'description': 'A new default message',
                'fields': [
                    {
                        'inline': True,
                        'name': 'version',
                        'value': '`0`'
                    },
                    {
                        'inline': False,
                        'name': 'id',
                        'value': '`ad3c3da1-148c-d5da-9a6a-79f1bc9a8a2e`'
                    },
                    {
                        'inline': True,
                        'name': 'detail-type',
                        'value': '`Glue Job State Change`'
                    },
                    {
                        'inline': True,
                        'name': 'source',
                        'value': '`aws.glue`'
                    },
                    {
                        'inline': True,
                        'name': 'account',
                        'value': '`000000000000`'
                    },
                    {
                        'inline': True,
                        'name': 'time',
                        'value': '`2021-06-18T12:34:06Z`'
                    },
                    {
                        'inline': True,
                        'name': 'region',
                        'value': '`us-east-2`'
                    },
                    {
                        'inline': True,
                        'name': 'resources',
                        'value': '`[]`'
                    },
                    {
                        'inline': False,
                        'name': 'detail',
                        'value': '`{"jobName": "test_job", "severity": "ERROR", "state": "FAILED", "jobRunId": "jr_ca2144d747b45ad412d3c66a1b6934b6b27aa252be9a21a95c54dfaa224a1925", "message": "SystemExit: 1"}`'
                    }
                ],
                'title': 'Message'
            }
        ],
        'username': 'main_test'
    }
]

snapshots['test_sns_get_discord_message_payload_snapshots message_guardduty_finding.json'] = [
    {
        'avatar_url': 'https://i.imgur.com/eeYUFCO_d.webp',
        'content': 'New AWS Notification',
        'embeds': [
            {
                'author': {
                    'icon_url': 'https://i.imgur.com/V37bZBb_d.webp',
                    'name': 'GuardDuty Alarm',
                    'url': 'https://console.amazonaws-us-gov.com/guardduty/home?region=us-gov-east-1'
                },
                'color': '16711680',
                'description': 'SAMPLE Unprotected port on EC2 instance i-123123123 is being probed',
                'fields': [
                    {
                        'name': 'Description',
                        'value': 'EC2 instance has an unprotected port which is being probed by a known malicious host.'
                    },
                    {
                        'name': 'Finding Type',
                        'value': '`Recon:EC2 PortProbeUnprotectedPort`'
                    },
                    {
                        'inline': 'true',
                        'name': 'First Seen',
                        'value': '`2020-01-02T01:02:03Z`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Last Seen',
                        'value': '`2020-01-03T01:02:03Z`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Severity',
                        'value': '`High`'
                    },
                    {
                        'inline': 'true',
                        'name': 'Count',
                        'value': '`1234`'
                    },
                    {
                        'name': 'Link to Finding',
                        'value': 'https://console.amazonaws-us-gov.com/guardduty/home?region=us-gov-east-1#/findings?search=id%3Dsample-id-2'
                    }
                ],
                'footer': {
                    'text': 'AWS GuardDuty Finding - SAMPLE Unprotected port on EC2 instance i-123123123 is being probed'
                },
                'thumbnail': {
                    'url': 'https://i.imgur.com/V37bZBb_d.webp'
                },
                'title': '`Severity Score 9`',
                'url': 'https://console.amazonaws-us-gov.com/guardduty/home?region=us-gov-east-1'
            }
        ],
        'username': 'main_test'
    }
]

snapshots['test_sns_get_discord_message_payload_snapshots message_text_message.json'] = [
    {
        'avatar_url': 'https://i.imgur.com/eeYUFCO_d.webp',
        'content': 'New AWS Notification',
        'embeds': [
            {
                'author': {
                    'icon_url': 'https://i.imgur.com/eeYUFCO_d.webp',
                    'name': 'AWS Notification'
                },
                'color': '4607',
                'description': 'A new default message',
                'fields': [
                    {
                        'inline': 'false',
                        'name': 'Event',
                        'value': '''This
is
a typical multi-line
message from SNS!

Have a ~good~ amazing day! :)'''
                    }
                ],
                'title': 'All Fine'
            }
        ],
        'username': 'main_test'
    }
]

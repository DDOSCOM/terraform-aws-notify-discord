# AWS Notify Discord Terraform module

This module creates an SNS topic (or uses an existing one) and an AWS Lambda function that sends notifications to
Discord using the [incoming webhooks API](https://discord.com/developers/docs/resources/webhook).

Start by setting up
an [incoming webhook integration](https://support.discord.com/hc/en-us/articles/228383668-Introducci%C3%B3n-a-los-webhook)
in your Discord space.

## Supported Features

- AWS Lambda runtime Python 3.10
- Create new SNS topic or use existing one
- Support plaintext and encrypted version of Discord webhook URL
- Most of Discord message options are customizable
- Various event types are supported, even generic messages:
    - AWS CloudWatch Alarms
    - AWS CloudWatch LogMetrics Alarms
    - AWS GuardDuty Findings

## Usage

```hcl
module "notify_discord" {
  source = "github.com/DDOSCOM/terraform-aws-notify-discord"

  sns_topic_name = "discord-topic"

  discord_webhook_url = "https://discord.com/api/webhooks/XXX/XXXXXXXX"
  discord_username    = "aws"
  discord_avatar_url  = "https://i.imgur.com/eeYUFCO_d.webp"
}
```

## Use existing SNS topic or create new

If you want to subscribe the AWS Lambda Function created by this module to an existing SNS topic you should
specify `create_sns_topic = false` as an argument and specify the name of existing SNS topic name in `sns_topic_name`.

## Local Development and Testing

See the [functions](https://github.com/DDOSCOM/terraform-aws-notify-discord/tree/master/functions) for further
details.

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Requirements

| Name                                                                      | Version   |
|---------------------------------------------------------------------------|-----------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | > = 1.1.3 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws)                   | > = 3.61  |

## Providers

| Name                                              | Version  |
|---------------------------------------------------|----------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | > = 3.61 |

## Modules

| Name                                                   | Source                           | Version |
|--------------------------------------------------------|----------------------------------|---------|
| <a name="module_lambda"></a> [lambda](#module\_lambda) | terraform-aws-modules/lambda/aws | 2.34.0  |

## Resources

| Name                                                                                                                                              | Type        |
|---------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| [aws_cloudwatch_log_group.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group)               | resource    |
| [aws_sns_topic.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic)                                       | resource    |
| [aws_sns_topic_subscription.sns_notify_discord](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sns_topic_subscription) | resource    |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity)                     | data source |
| [aws_iam_policy_document.lambda](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document)              | data source |
| [aws_partition.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/partition)                                 | data source |
| [aws_region.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region)                                       | data source |

## Inputs

| Name                                                                                                                                                           | Description                                                                                                                                                         | Type           | Default          | Required |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|------------------|:--------:|
| <a name="input_cloudwatch_log_group_kms_key_id"></a> [cloudwatch\_log\_group\_kms\_key\_id](#input\_cloudwatch\_log\_group\_kms\_key\_id)                      | The ARN of the KMS Key to use when encrypting log data for Lambda                                                                                                   | `string`       | `null`           |    no    |
| <a name="input_cloudwatch_log_group_retention_in_days"></a> [cloudwatch\_log\_group\_retention\_in\_days](#input\_cloudwatch\_log\_group\_retention\_in\_days) | Specifies the number of days you want to retain log events in log group for Lambda.                                                                                 | `number`       | `0`              |    no    |
| <a name="input_cloudwatch_log_group_tags"></a> [cloudwatch\_log\_group\_tags](#input\_cloudwatch\_log\_group\_tags)                                            | Additional tags for the Cloudwatch log group                                                                                                                        | `map(string)`  | `{}`             |    no    |
| <a name="input_create"></a> [create](#input\_create)                                                                                                           | Whether to create all resources                                                                                                                                     | `bool`         | `true`           |    no    |
| <a name="input_create_sns_topic"></a> [create\_sns\_topic](#input\_create\_sns\_topic)                                                                         | Whether to create new SNS topic                                                                                                                                     | `bool`         | `true`           |    no    |
| <a name="input_iam_policy_path"></a> [iam\_policy\_path](#input\_iam\_policy\_path)                                                                            | Path of policies to that should be added to IAM role for Lambda Function                                                                                            | `string`       | `null`           |    no    |
| <a name="input_iam_role_boundary_policy_arn"></a> [iam\_role\_boundary\_policy\_arn](#input\_iam\_role\_boundary\_policy\_arn)                                 | The ARN of the policy that is used to set the permissions boundary for the role                                                                                     | `string`       | `null`           |    no    |
| <a name="input_iam_role_name_prefix"></a> [iam\_role\_name\_prefix](#input\_iam\_role\_name\_prefix)                                                           | A unique role name beginning with the specified prefix                                                                                                              | `string`       | `"lambda"`       |    no    |
| <a name="input_iam_role_path"></a> [iam\_role\_path](#input\_iam\_role\_path)                                                                                  | Path of IAM role to use for Lambda Function                                                                                                                         | `string`       | `null`           |    no    |
| <a name="input_iam_role_tags"></a> [iam\_role\_tags](#input\_iam\_role\_tags)                                                                                  | Additional tags for the IAM role                                                                                                                                    | `map(string)`  | `{}`             |    no    |
| <a name="input_kms_key_arn"></a> [kms\_key\_arn](#input\_kms\_key\_arn)                                                                                        | ARN of the KMS key used for decrypting discord webhook url                                                                                                            | `string`       | `""`             |    no    |
| <a name="input_lambda_description"></a> [lambda\_description](#input\_lambda\_description)                                                                     | The description of the Lambda function                                                                                                                              | `string`       | `null`           |    no    |
| <a name="input_lambda_function_name"></a> [lambda\_function\_name](#input\_lambda\_function\_name)                                                             | The name of the Lambda function to create                                                                                                                           | `string`       | `"notify_discord"` |    no    |
| <a name="input_lambda_function_s3_bucket"></a> [lambda\_function\_s3\_bucket](#input\_lambda\_function\_s3\_bucket)                                            | S3 bucket to store artifacts                                                                                                                                        | `string`       | `null`           |    no    |
| <a name="input_lambda_function_store_on_s3"></a> [lambda\_function\_store\_on\_s3](#input\_lambda\_function\_store\_on\_s3)                                    | Whether to store produced artifacts on S3 or locally.                                                                                                               | `bool`         | `false`          |    no    |
| <a name="input_lambda_function_tags"></a> [lambda\_function\_tags](#input\_lambda\_function\_tags)                                                             | Additional tags for the Lambda function                                                                                                                             | `map(string)`  | `{}`             |    no    |
| <a name="input_lambda_function_vpc_security_group_ids"></a> [lambda\_function\_vpc\_security\_group\_ids](#input\_lambda\_function\_vpc\_security\_group\_ids) | List of security group ids when Lambda Function should run in the VPC.                                                                                              | `list(string)` | `null`           |    no    |
| <a name="input_lambda_function_vpc_subnet_ids"></a> [lambda\_function\_vpc\_subnet\_ids](#input\_lambda\_function\_vpc\_subnet\_ids)                           | List of subnet ids when Lambda Function should run in the VPC. Usually private or intra subnets.                                                                    | `list(string)` | `null`           |    no    |
| <a name="input_lambda_role"></a> [lambda\_role](#input\_lambda\_role)                                                                                          | IAM role attached to the Lambda Function. If this is set then a role will not be created for you.                                                                   | `string`       | `""`             |    no    |
| <a name="input_log_events"></a> [log\_events](#input\_log\_events)                                                                                             | Boolean flag to enabled/disable logging of incoming events                                                                                                          | `bool`         | `false`          |    no    |
| <a name="input_recreate_missing_package"></a> [recreate\_missing\_package](#input\_recreate\_missing\_package)                                                 | Whether to recreate missing Lambda package if it is missing locally or not                                                                                          | `bool`         | `true`           |    no    |
| <a name="input_reserved_concurrent_executions"></a> [reserved\_concurrent\_executions](#input\_reserved\_concurrent\_executions)                               | The amount of reserved concurrent executions for this lambda function. A value of 0 disables lambda from being triggered and -1 removes any concurrency limitations | `number`       | `-1`             |    no    |
| <a name="input_discord_avatar_url"></a> [discord\_avatar\_url](#input\_discord\_avatar\_url)                                                                         | The avatar that will appear on discord messages                                                                                                                       | `string`       | n/a              |   yes    |
| <a name="input_discord_username"></a> [discord\_username](#input\_discord\_username)                                                                                 | The username that will appear on discord messages                                                                                                                     | `string`       | n/a              |   yes    |
| <a name="input_discord_webhook_url"></a> [discord\_webhook\_url](#input\_discord\_webhook\_url)                                                                      | The URL of discord webhook                                                                                                                                            | `string`       | n/a              |   yes    |
| <a name="input_sns_topic_kms_key_id"></a> [sns\_topic\_kms\_key\_id](#input\_sns\_topic\_kms\_key\_id)                                                         | ARN of the KMS key used for enabling SSE on the topic                                                                                                               | `string`       | `""`             |    no    |
| <a name="input_sns_topic_name"></a> [sns\_topic\_name](#input\_sns\_topic\_name)                                                                               | The name of the SNS topic to create                                                                                                                                 | `string`       | n/a              |   yes    |
| <a name="input_sns_topic_tags"></a> [sns\_topic\_tags](#input\_sns\_topic\_tags)                                                                               | Additional tags for the SNS topic                                                                                                                                   | `map(string)`  | `{}`             |    no    |
| <a name="input_subscription_filter_policy"></a> [subscription\_filter\_policy](#input\_subscription\_filter\_policy)                                           | (Optional) A valid filter policy that will be used in the subscription to filter messages seen by the target resource.                                              | `string`       | `null`           |    no    |
| <a name="input_tags"></a> [tags](#input\_tags)                                                                                                                 | A map of tags to add to all resources                                                                                                                               | `map(string)`  | `{}`             |    no    |

## Outputs

| Name                                                                                                                                                                         | Description                                                                                                 |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| <a name="output_lambda_cloudwatch_log_group_arn"></a> [lambda\_cloudwatch\_log\_group\_arn](#output\_lambda\_cloudwatch\_log\_group\_arn)                                    | The Amazon Resource Name (ARN) specifying the log group                                                     |
| <a name="output_lambda_iam_role_arn"></a> [lambda\_iam\_role\_arn](#output\_lambda\_iam\_role\_arn)                                                                          | The ARN of the IAM role used by Lambda function                                                             |
| <a name="output_lambda_iam_role_name"></a> [lambda\_iam\_role\_name](#output\_lambda\_iam\_role\_name)                                                                       | The name of the IAM role used by Lambda function                                                            |
| <a name="output_notify_discord_lambda_function_arn"></a> [notify\_discord\_lambda\_function\_arn](#output\_notify\_discord\_lambda\_function\_arn)                                 | The ARN of the Lambda function                                                                              |
| <a name="output_notify_discord_lambda_function_invoke_arn"></a> [notify\_discord\_lambda\_function\_invoke\_arn](#output\_notify\_discord\_lambda\_function\_invoke\_arn)          | The ARN to be used for invoking Lambda function from API Gateway                                            |
| <a name="output_notify_discord_lambda_function_last_modified"></a> [notify\_discord\_lambda\_function\_last\_modified](#output\_notify\_discord\_lambda\_function\_last\_modified) | The date Lambda function was last modified                                                                  |
| <a name="output_notify_discord_lambda_function_name"></a> [notify\_discord\_lambda\_function\_name](#output\_notify\_discord\_lambda\_function\_name)                              | The name of the Lambda function                                                                             |
| <a name="output_notify_discord_lambda_function_version"></a> [notify\_discord\_lambda\_function\_version](#output\_notify\_discord\_lambda\_function\_version)                     | Latest published version of your Lambda function                                                            |
| <a name="output_discord_topic_arn"></a> [discord\_topic\_arn](#output\_discord\_topic\_arn)                                                                                        | The ARN of the SNS topic from which messages will be sent to discord                                          |
| <a name="output_this_discord_topic_arn"></a> [this\_discord\_topic\_arn](#output\_this\_discord\_topic\_arn)                                                                       | The ARN of the SNS topic from which messages will be sent to discord (backward compatibility for version 4.x) |

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->

## Authors

Module is maintained by [Santiago Hurtado](https://github.com/MefistoBaal) with help
from [these awesome contributors](https://github.com/DDOSCOM/terraform-aws-notify-discord/graphs/contributors)
.

## License

Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See
LICENSE for full details.

output "discord_topic_arn" {
  description = "The ARN of the SNS topic from which messages will be sent to Discord"
  value       = module.notify_discord.discord_topic_arn
}

output "notify_discord_lambda_function_name" {
  description = "The name of the Lambda function"
  value       = module.notify_discord.notify_discord_lambda_function_name
}

output "notify_discord_lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = module.notify_discord.notify_discord_lambda_function_arn
}

output "kms_key_arn" {
  description = "The ARN of the KMS key used to encrypt the Discord webhook URL"
  value       = aws_kms_key.this.arn
}

output "cloudwatch_alarm_arn" {
  description = "The ARN of the example CloudWatch alarm"
  value       = aws_cloudwatch_metric_alarm.this.arn
}

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

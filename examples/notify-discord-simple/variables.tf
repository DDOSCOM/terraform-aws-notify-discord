variable "aws_region" {
  description = "AWS region to deploy the example resources into"
  type        = string
  default     = "us-east-1"
}

variable "sns_topic_name" {
  description = "The name of the SNS topic to create"
  type        = string
  default     = "discord-topic"
}

variable "discord_webhook_url" {
  description = "The URL of the Discord incoming webhook. Create one at Discord > Channel Settings > Integrations > Webhooks."
  type        = string
}

variable "discord_username" {
  description = "The username that will appear on Discord messages"
  type        = string
  default     = "aws"
}

variable "discord_avatar_url" {
  description = "The avatar that will appear on Discord messages"
  type        = string
  default     = "https://i.imgur.com/eeYUFCO_d.webp"
}

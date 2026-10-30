provider "aws" {
  region = var.aws_region
}

module "notify_discord" {
  source = "../.."

  sns_topic_name = var.sns_topic_name

  discord_webhook_url = var.discord_webhook_url
  discord_username    = var.discord_username
  discord_avatar_url  = var.discord_avatar_url
}

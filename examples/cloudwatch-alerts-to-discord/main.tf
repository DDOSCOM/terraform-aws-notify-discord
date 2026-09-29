provider "aws" {
  region = var.aws_region
}

# KMS key used to encrypt the Discord webhook URL at rest. The Lambda decrypts
# it at runtime (DISCORD_WEBHOOK_URL does not start with "http" in that case).
resource "aws_kms_key" "this" {
  description             = "KMS key to encrypt the Discord webhook URL for the notify-discord module"
  deletion_window_in_days = 7
}

# Encrypt the Discord webhook URL with KMS. The ciphertext_blob is base64
# encoded, which is exactly what the Lambda's decrypt_url() expects.
resource "aws_kms_ciphertext" "webhook_url" {
  key_id    = aws_kms_key.this.key_id
  plaintext = var.discord_webhook_url
}

module "notify_discord" {
  source = "../.."

  sns_topic_name = var.sns_topic_name

  # Pass the KMS-encrypted webhook URL (not the plaintext one).
  discord_webhook_url = aws_kms_ciphertext.webhook_url.ciphertext_blob
  kms_key_arn         = aws_kms_key.this.arn

  discord_username   = var.discord_username
  discord_avatar_url = var.discord_avatar_url
}

# An example CloudWatch alarm that publishes to the module's SNS topic, which
# forwards the alert to Discord.
resource "aws_cloudwatch_metric_alarm" "this" {
  alarm_name          = var.alarm_name
  alarm_description   = "Example CloudWatch alarm that sends notifications to Discord via the notify-discord module"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80

  alarm_actions = [module.notify_discord.discord_topic_arn]
  ok_actions    = [module.notify_discord.discord_topic_arn]
}

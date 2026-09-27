# notify-discord-simple

A minimal example that creates an SNS topic and a Lambda function which
forwards notifications to a Discord channel via an incoming webhook.

## Usage

Create an incoming webhook in your Discord channel
(*Channel Settings → Integrations → Webhooks*) and copy the webhook URL.

```bash
cd examples/notify-discord-simple

terraform init
terraform apply \
  -var discord_webhook_url="https://discord.com/api/webhooks/XXX/XXXXXXXX"
```

Publish a message to the SNS topic to trigger a Discord notification:

```bash
aws sns publish \
  --topic-arn "$(terraform output -raw discord_topic_arn)" \
  --message "Hello from AWS" \
  --subject "Test message"
```

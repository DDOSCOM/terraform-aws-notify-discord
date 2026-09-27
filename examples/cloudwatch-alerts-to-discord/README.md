# cloudwatch-alerts-to-discord

An end-to-end example that sends AWS CloudWatch alarm notifications to a
Discord channel, keeping the Discord webhook URL encrypted with KMS at rest.

It provisions:

- a KMS key,
- the `notify-discord` module (an SNS topic + Lambda) configured with the
  KMS-encrypted webhook URL,
- an example CloudWatch metric alarm that publishes ALARM and OK transitions
  to the module's SNS topic.

## Usage

Create an incoming webhook in your Discord channel
(*Channel Settings → Integrations → Webhooks*) and copy the webhook URL.

```bash
cd examples/cloudwatch-alerts-to-discord

terraform init
terraform apply \
  -var discord_webhook_url="https://discord.com/api/webhooks/XXX/XXXXXXXX"
```

The webhook URL is encrypted with KMS and only stored in ciphertext form in
the Lambda environment variables. The Lambda decrypts it at runtime using the
KMS key.

To trigger the alarm manually for testing, force it into the ALARM state:

```bash
aws cloudwatch set-alarm-state \
  --alarm-name "$(terraform output -raw cloudwatch_alarm_arn | cut -d: -f7)" \
  --state-value ALARM \
  --state-reason "Manual test" \
  --state-reason-data '{"reason":"Manual test"}'
```

## Cleanup

```bash
terraform destroy \
  -var discord_webhook_url="https://discord.com/api/webhooks/XXX/XXXXXXXX"
```

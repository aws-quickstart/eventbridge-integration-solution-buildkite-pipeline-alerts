# eventbridge-integration-solution-buildkite-pipeline-alerts
## Amazon EventBridge Integration Solution for Buildkite Pipeline Alerts

This Quick Start demonstrates two types of integrations to receive Buildkite pipeline alerts through Amazon EventBridge. It can be configured to send pipeline alerts in one of two ways:
- As text messages through Amazon Simple Notification Service (SNS).
- As messages sent to a webhook endpoint (ex: Chime, Slack) by an AWS Lambda function.

This solution enables your Buildkite Amazon EventBridge Partner event bus to trigger a rule that evaluates all events and sends alerts for matched events (in the example, 'Build Finished' events). You can use this as a starter project to extend for any scenario that requires customizing your Buildkite pipeline alerts.

Sending text message alerts with Amazon SNS:
![Quick Start architecture for EventBridge Integration Solution for Buildkite pipeline alerts & SNS](https://github.com/aws-quickstart/eventbridge-integration-solution-buildkite-pipeline-alerts/raw/master/images/arch-eventbridge-buildkite-sns.png)

Sending alerts to a webhook endpoint with AWS Lambda:
![Quick Start architecture for EventBridge Integration Solution for Buildkite pipeline alerts & Lambda](https://github.com/aws-quickstart/eventbridge-integration-solution-buildkite-pipeline-alerts/raw/master/images/arch-eventbridge-lambda-webhook.png)

To post feedback, submit feature ideas, or report bugs, use the **Issues** section of [this GitHub repo](https://github.com/aws-quickstart/eventbridge-buildkite-pipeline-alerts).

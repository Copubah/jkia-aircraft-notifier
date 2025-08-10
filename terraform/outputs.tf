output "sns_topic_arn" {
  description = "ARN of the SNS topic for aircraft landing notifications"
  value       = aws_sns_topic.aircraft_landing.arn
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.landing_notifier.function_name
}

output "eventbridge_rule_name" {
  description = "Name of the EventBridge rule"
  value       = aws_cloudwatch_event_rule.landing_check.name
}output "
dynamodb_table_name" {
  description = "Name of the DynamoDB table storing arrivals"
  value       = aws_dynamodb_table.jkia_arrivals.name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table storing arrivals"
  value       = aws_dynamodb_table.jkia_arrivals.arn
}
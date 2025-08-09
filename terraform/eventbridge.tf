resource "aws_cloudwatch_event_rule" "landing_check" {
  name                = "jkia-landing-check"
  description         = "Trigger Lambda to check for aircraft landings at JKIA"
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.landing_check.name
  target_id = "TriggerLambda"
  arn       = aws_lambda_function.landing_notifier.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.landing_notifier.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.landing_check.arn
}




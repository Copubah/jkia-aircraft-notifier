resource "aws_sns_topic" "aircraft_landing" {
  name = "jkia-aircraft-landing"
}

resource "aws_sns_topic_subscription" "email_sub" {
  topic_arn = aws_sns_topic.aircraft_landing.arn
  protocol  = "email"
  endpoint  = var.notification_email
}


variable "notification_email" {
  description = "Email address to receive aircraft landing notifications"
  type        = string
}

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}
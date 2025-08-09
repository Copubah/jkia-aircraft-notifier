variable "aws_region" {
  description = "AWS region to deploy NBO resources"
  type        = string
  default     = "us-east-1"
}

variable "notification_email" {
  description = "Email address to receive aircraft landing alerts"
  type        = string
  default     = "copubah@gmail.com"
}

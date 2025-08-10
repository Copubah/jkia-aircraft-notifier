# DynamoDB table to store aircraft arrivals
resource "aws_dynamodb_table" "jkia_arrivals" {
  name           = "jkia-arrivals"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "arrival_id"

  attribute {
    name = "arrival_id"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  # Global Secondary Index for querying by date
  global_secondary_index {
    name     = "date-timestamp-index"
    hash_key = "date"
    range_key = "timestamp"
  }

  tags = {
    Name        = "JKIA Arrivals"
    Environment = "production"
    Project     = "jkia-aircraft-notifier"
  }
}
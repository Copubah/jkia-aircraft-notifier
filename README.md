# JKIA Aircraft Landing Notifier ✈️

Real-time aircraft landing notifications for Nairobi's Jomo Kenyatta International Airport (JKIA) using AWS serverless architecture and the OpenSky Network API.

![Architecture Diagram](./docs/architecture.png)

## 🎯 Overview

This serverless application monitors aircraft activity around JKIA and sends instant email notifications when aircraft land or are detected in the landing pattern. Built entirely on AWS using Infrastructure as Code (Terraform) for reliable, scalable, and cost-effective monitoring.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌─────────────┐
│   EventBridge   │───▶│    Lambda    │───▶│  OpenSky API    │    │     SNS     │
│  (5 min timer)  │    │   Function   │    │   (Aircraft     │    │   Topic     │
└─────────────────┘    └──────┬───────┘    │    States)      │    └──────┬──────┘
                              │            └─────────────────┘           │
                              ▼                                          ▼
                       ┌──────────────┐                          ┌─────────────┐
                       │ CloudWatch   │                          │    Email    │
                       │    Logs      │                          │ Notification│
                       └──────────────┘                          └─────────────┘
```

### Components

- **Amazon EventBridge**: Triggers Lambda function every 5 minutes
- **AWS Lambda**: Fetches aircraft data and processes landing detection
- **OpenSky Network API**: Provides real-time aircraft position data
- **Amazon SNS**: Delivers email notifications
- **CloudWatch Logs**: Monitors function execution and debugging

## 🚀 Features

- ✅ **Real-time Monitoring**: Checks aircraft positions every 5 minutes
- ✅ **Smart Detection**: Identifies aircraft landing based on altitude and ground status
- ✅ **Email Notifications**: Instant alerts with flight details
- ✅ **Serverless Architecture**: No infrastructure management required
- ✅ **Cost Effective**: Runs for less than $1/month
- ✅ **Infrastructure as Code**: Fully automated deployment with Terraform
- ✅ **Comprehensive Logging**: Full observability and debugging capabilities

## 📋 Prerequisites

- **AWS Account** with appropriate permissions
- **AWS CLI** configured with credentials
- **Terraform** >= 1.0 installed
- **Valid email address** for notifications

### Required AWS Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:*",
        "events:*",
        "sns:*",
        "iam:*",
        "logs:*"
      ],
      "Resource": "*"
    }
  ]
}
```

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone <your-repository-url>
cd jkia-aircraft-notifier
```

### 2. Configure Email
Edit `variables.tf` to set your notification email:
```hcl
variable "notification_email" {
  description = "Email address to receive aircraft landing alerts"
  type        = string
  default     = "your-email@example.com"  # Change this
}
```

### 3. Deploy Infrastructure
```bash
# Make deployment script executable
chmod +x deploy.sh

# Deploy the infrastructure
./deploy.sh
```

### 4. Confirm Email Subscription
- Check your email inbox for AWS SNS confirmation
- Click the confirmation link to activate notifications

## 📊 Monitoring & Testing

### View Real-time Logs
```bash
# Follow logs in real-time
aws logs tail /aws/lambda/jkia-landing-notifier --follow

# View recent logs
aws logs tail /aws/lambda/jkia-landing-notifier --since 1h
```

### Test Lambda Function
```bash
# Manual test
aws lambda invoke --function-name jkia-landing-notifier response.json
cat response.json
```

### Send Test Notification
```bash
# Test SNS email delivery
aws sns publish \
  --topic-arn $(terraform output -raw sns_topic_arn) \
  --subject "Test JKIA Notification" \
  --message "Test message to verify email notifications are working!"
```

### Check Infrastructure Status
```bash
# Verify Lambda function
aws lambda get-function --function-name jkia-landing-notifier

# Check EventBridge rule
aws events describe-rule --name jkia-landing-check

# Verify SNS subscription
aws sns list-subscriptions-by-topic --topic-arn $(terraform output -raw sns_topic_arn)
```

## 📧 Sample Notification

```
Subject: ✈️ Aircraft Landing Alert - JKIA

🛬 AIRCRAFT LANDING NOTIFICATION

Flight: KQ101
Location: Near Jomo Kenyatta International Airport (JKIA)
Status: Aircraft on ground
Velocity: 15 m/s
Detection Time: 14:30 UTC

This aircraft appears to have recently landed or is landing at JKIA.

This is an automated notification from your JKIA Aircraft Landing Notifier.
```

## ⚙️ Configuration

### Adjust Check Frequency
Modify `terraform/eventbridge.tf`:
```hcl
resource "aws_cloudwatch_event_rule" "landing_check" {
  name                = "jkia-landing-check"
  description         = "Trigger Lambda to check for aircraft landings at JKIA"
  schedule_expression = "rate(10 minutes)"  # Change from 5 to 10 minutes
}
```

### Change Detection Area
Modify `lambda/lambda_function.py`:
```python
# Expand detection area around JKIA
lamin, lamax = -1.6, -1.0  # latitude range (wider)
lomin, lomax = 36.6, 37.3  # longitude range (wider)
```

### Customize Landing Detection Logic
```python
# Modify detection criteria in lambda_function.py
if on_ground or (altitude and altitude < 200 and velocity and velocity < 100):
    # Adjust altitude and velocity thresholds
```

## 💰 Cost Breakdown

| Service | Usage | Monthly Cost |
|---------|-------|--------------|
| AWS Lambda | 8,640 invocations (5min intervals) | ~$0.20 |
| Amazon SNS | Variable (per notification) | ~$0.50 |
| Amazon EventBridge | 8,640 rule evaluations | Free Tier |
| CloudWatch Logs | Log storage and queries | ~$0.10 |
| **Total** | | **~$0.80/month** |

## 🔧 Troubleshooting

### No Notifications Received
1. **Check email subscription status**:
   ```bash
   aws sns list-subscriptions-by-topic --topic-arn $(terraform output -raw sns_topic_arn)
   ```
   Look for `"SubscriptionArn"` - should NOT say `"PendingConfirmation"`

2. **Verify Lambda execution**:
   ```bash
   aws logs tail /aws/lambda/jkia-landing-notifier --since 30m
   ```

3. **Test SNS manually**:
   ```bash
   aws sns publish --topic-arn $(terraform output -raw sns_topic_arn) --message "Test"
   ```

### API Connection Issues
- OpenSky Network API has rate limits
- Check logs for timeout errors
- Consider increasing check interval during high-traffic periods

### Too Many Notifications
- Adjust detection criteria in Lambda function
- Increase EventBridge schedule interval
- Add cooldown logic to prevent duplicate notifications

### Lambda Function Errors
```bash
# Check for import errors or runtime issues
aws lambda invoke --function-name jkia-landing-notifier response.json
cat response.json
```

## 🔄 Updates & Maintenance

### Update Lambda Code
```bash
# After modifying lambda/lambda_function.py
terraform apply -auto-approve
```

### Update Infrastructure
```bash
# After modifying Terraform files
terraform plan
terraform apply
```

### View Terraform State
```bash
terraform show
terraform output
```

## 🧹 Cleanup

To remove all resources and stop charges:
```bash
terraform destroy
```

## 📁 Project Structure

```
jkia-aircraft-notifier/
├── README.md                 # This file
├── deploy.sh                 # Deployment script
├── main.tf                   # Root Terraform configuration
├── variables.tf              # Input variables
├── outputs.tf                # Output values
├── docs/
│   └── architecture.png      # Architecture diagram
├── lambda/
│   ├── lambda_function.py    # Main Lambda function
│   ├── requirements.txt      # Python dependencies
│   └── lambda_package.zip    # Deployment package (auto-generated)
└── terraform/
    ├── eventbridge.tf        # EventBridge configuration
    ├── iam.tf               # IAM roles and policies
    ├── lambda.tf            # Lambda function configuration
    ├── sns.tf               # SNS topic and subscription
    ├── variables.tf         # Module variables
    └── outputs.tf           # Module outputs
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenSky Network](https://opensky-network.org/) for providing free aircraft tracking data
- [AWS](https://aws.amazon.com/) for serverless infrastructure
- [Terraform](https://terraform.io/) for Infrastructure as Code

## 📞 Support

If you encounter issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review CloudWatch logs for detailed error information
3. Open an issue in this repository
4. Contact the maintainer

---

**Happy Flight Tracking! ✈️**
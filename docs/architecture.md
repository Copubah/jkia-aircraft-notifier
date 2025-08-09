# JKIA Aircraft Landing Notifier - Architecture

## System Architecture Diagram

```
                    ┌─────────────────────────────────────────────────────────────┐
                    │                    AWS Cloud                                │
                    │                                                             │
    ┌───────────────┼─────────────────────────────────────────────────────────────┼───────────────┐
    │               │                                                             │               │
    │   ┌───────────▼──────────┐              ┌─────────────────────────────────▼─────────────┐ │
    │   │     EventBridge      │              │              Lambda Function                   │ │
    │   │                      │              │                                                │ │
    │   │  ┌─────────────────┐ │              │  ┌──────────────────────────────────────────┐ │ │
    │   │  │ Scheduled Rule  │ │──────────────┼─▶│        jkia-landing-notifier             │ │ │
    │   │  │                 │ │   Triggers   │  │                                          │ │ │
    │   │  │ rate(5 minutes) │ │   every      │  │  • Fetch aircraft data from OpenSky     │ │ │
    │   │  └─────────────────┘ │   5 minutes  │  │  • Filter aircraft near JKIA            │ │ │
    │   └─────────────────────┘              │  │  • Detect landing patterns               │ │ │
    │                                        │  │  • Send notifications via SNS            │ │ │
    │                                        │  └──────────────────────────────────────────┘ │ │
    │                                        └─────────────────────────────────────────────────┘ │
    │                                                           │                                 │
    │                                                           │ API Call                        │
    │                                                           ▼                                 │
    │   ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
    │   │                          External API                                               │ │
    │   │                                                                                     │ │
    │   │  ┌─────────────────────────────────────────────────────────────────────────────┐  │ │
    │   │  │                    OpenSky Network API                                      │  │ │
    │   │  │                                                                             │  │ │
    │   │  │  • Real-time aircraft position data                                        │  │ │
    │   │  │  • Global flight tracking                                                  │  │ │
    │   │  │  • Free tier available                                                     │  │ │
    │   │  │  • Returns aircraft states (position, altitude, velocity, ground status)  │  │ │
    │   │  └─────────────────────────────────────────────────────────────────────────────┘  │ │
    │   └─────────────────────────────────────────────────────────────────────────────────────┘ │
    │                                                           │                                 │
    │                                                           │ Returns aircraft data           │
    │                                                           ▼                                 │
    │   ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
    │   │                        Notification Service                                         │ │
    │   │                                                                                     │ │
    │   │  ┌─────────────────────────────────────────────────────────────────────────────┐  │ │
    │   │  │                         Amazon SNS                                          │  │ │
    │   │  │                                                                             │  │ │
    │   │  │  ┌─────────────────┐              ┌─────────────────────────────────────┐  │  │ │
    │   │  │  │   SNS Topic     │              │         Email Subscription          │  │  │ │
    │   │  │  │                 │──────────────┼─▶                                   │  │  │ │
    │   │  │  │ jkia-aircraft-  │   Delivers   │  • Protocol: email                  │  │  │ │
    │   │  │  │    landing      │   messages   │  • Endpoint: user@example.com       │  │  │ │
    │   │  │  └─────────────────┘              │  • Status: Confirmed                │  │  │ │
    │   │  │                                   └─────────────────────────────────────┘  │  │ │
    │   │  └─────────────────────────────────────────────────────────────────────────────┘  │ │
    │   └─────────────────────────────────────────────────────────────────────────────────────┘ │
    │                                                           │                                 │
    │                                                           │ Email notification              │
    │                                                           ▼                                 │
    └───────────────────────────────────────────────────────────────────────────────────────────┘
                                                                │
                                                                ▼
                                            ┌─────────────────────────────────┐
                                            │           End User              │
                                            │                                 │
                                            │  📧 Receives email notification │
                                            │     when aircraft land at JKIA │
                                            └─────────────────────────────────┘
```

## Data Flow

1. **EventBridge Trigger**: Every 5 minutes, EventBridge triggers the Lambda function
2. **API Request**: Lambda calls OpenSky Network API to get aircraft positions near JKIA
3. **Data Processing**: Lambda filters and analyzes aircraft data to detect landings
4. **Notification**: If landings detected, Lambda publishes message to SNS topic
5. **Email Delivery**: SNS delivers email notification to subscribed user

## Component Details

### EventBridge Rule
- **Name**: `jkia-landing-check`
- **Schedule**: `rate(5 minutes)`
- **Target**: Lambda function
- **Status**: ENABLED

### Lambda Function
- **Name**: `jkia-landing-notifier`
- **Runtime**: Python 3.12
- **Memory**: 128 MB
- **Timeout**: 30 seconds
- **Environment Variables**: SNS_TOPIC_ARN

### OpenSky Network API
- **Endpoint**: `https://opensky-network.org/api/states/all`
- **Parameters**: Bounding box around JKIA coordinates
- **Rate Limits**: Free tier limitations apply
- **Data Format**: JSON array of aircraft states

### SNS Topic
- **Name**: `jkia-aircraft-landing`
- **Type**: Standard topic
- **Subscription**: Email protocol
- **Delivery**: Immediate

### IAM Roles & Policies
- **Lambda Execution Role**: Basic execution + SNS publish permissions
- **EventBridge Permissions**: Lambda invoke permissions
- **CloudWatch Logs**: Automatic log group creation

## Security Considerations

- Lambda function uses least-privilege IAM role
- No sensitive data stored in environment variables
- API calls use HTTPS encryption
- Email notifications contain no sensitive flight data
- All AWS services communicate within VPC when applicable

## Monitoring & Observability

- **CloudWatch Logs**: All Lambda executions logged
- **CloudWatch Metrics**: Lambda duration, errors, invocations
- **SNS Delivery Status**: Email delivery confirmation
- **EventBridge Metrics**: Rule execution success/failure

## Scalability & Performance

- **Serverless Architecture**: Automatically scales with demand
- **Stateless Design**: No persistent storage required
- **API Rate Limiting**: Handles OpenSky API limitations gracefully
- **Error Handling**: Robust retry and error recovery mechanisms
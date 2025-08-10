# Today's Arrivals Tracking

This enhanced version of the JKIA Aircraft Landing Notifier now includes the ability to track and query all aircraft arrivals for the current day.

## New Features

### 🗄️ **Persistent Storage**
- All detected aircraft arrivals are now stored in a DynamoDB table
- Data includes flight callsign, detection time, altitude, ground status, and velocity
- Automatic deduplication prevents duplicate entries for the same flight

### 📊 **Query Today's Arrivals**
- Query all arrivals detected today via Lambda function
- Programmatic access to historical data for the current day
- JSON response with detailed flight information

### 🖥️ **Dashboard Interface**
- HTML dashboard to visualize today's arrivals
- Real-time statistics and flight details
- Auto-refresh functionality

## Usage

### Query Today's Arrivals (Command Line)

```bash
# Using the Python script
./query_todays_arrivals.py

# Using AWS CLI directly
aws lambda invoke \
  --function-name jkia-landing-notifier \
  --payload '{"query_type": "todays_arrivals"}' \
  response.json && cat response.json
```

### Query Today's Arrivals (Programmatically)

```python
import boto3
import json

lambda_client = boto3.client('lambda')
response = lambda_client.invoke(
    FunctionName='jkia-landing-notifier',
    Payload=json.dumps({'query_type': 'todays_arrivals'})
)

result = json.loads(response['Payload'].read())
arrivals_data = json.loads(result['body'])
print(f"Total arrivals today: {arrivals_data['total_arrivals']}")
```

### View Dashboard

Open `arrivals_dashboard.html` in your web browser to see a visual representation of today's arrivals. 

**Note**: The dashboard currently shows mock data. To connect it to your live Lambda function, you'll need to:
1. Create an API Gateway endpoint
2. Connect it to your Lambda function  
3. Update the JavaScript to call your API endpoint

## Data Structure

### DynamoDB Table Schema

```json
{
  "arrival_id": "2024-01-15#KQ101#14",  // Composite key: date#callsign#hour
  "date": "2024-01-15",                 // Date of arrival
  "timestamp": "2024-01-15T14:30:15Z",  // Full timestamp
  "callsign": "KQ101",                  // Flight callsign
  "altitude": 0,                        // Altitude in meters
  "on_ground": true,                    // Ground status
  "velocity": 12.5,                     // Velocity in m/s
  "detection_time": "14:30:15 UTC"      // Human-readable time
}
```

### Query Response Format

```json
{
  "status": "success",
  "query_type": "todays_arrivals",
  "date": "2024-01-15",
  "total_arrivals": 12,
  "arrivals": [
    {
      "callsign": "KQ101",
      "time": "14:30:15 UTC",
      "altitude": 0.0,
      "on_ground": true,
      "velocity": 12.5
    }
  ],
  "timestamp": "2024-01-15T15:00:00Z"
}
```

## Deployment

The enhanced system includes a new DynamoDB table and updated Lambda permissions. Deploy using:

```bash
# Deploy the updated infrastructure
./deploy.sh

# Verify the DynamoDB table was created
aws dynamodb describe-table --table-name jkia-arrivals

# Test the query functionality
./query_todays_arrivals.py
```

## Cost Impact

The addition of DynamoDB storage adds minimal cost:

| Service | Additional Monthly Cost |
|---------|------------------------|
| DynamoDB | ~$0.25 (pay-per-request) |
| Lambda | No change |
| **Total Additional** | **~$0.25/month** |

## Monitoring

### View Stored Arrivals

```bash
# Query DynamoDB directly for today's arrivals
aws dynamodb query \
  --table-name jkia-arrivals \
  --index-name date-timestamp-index \
  --key-condition-expression "#date = :date" \
  --expression-attribute-names '{"#date": "date"}' \
  --expression-attribute-values '{":date": {"S": "'$(date +%Y-%m-%d)'"}}'
```

### Check Lambda Logs

```bash
# View logs for both regular monitoring and query requests
aws logs tail /aws/lambda/jkia-landing-notifier --follow
```

## Troubleshooting

### No Data Returned
1. **Check if arrivals are being detected**: Review Lambda logs for aircraft detection
2. **Verify DynamoDB permissions**: Ensure Lambda has read/write access to the table
3. **Check date format**: Ensure queries use YYYY-MM-DD format

### DynamoDB Errors
1. **Table not found**: Verify the table was created during deployment
2. **Access denied**: Check IAM permissions for Lambda role
3. **Throttling**: Consider switching to provisioned capacity for high-volume usage

### Query Script Issues
1. **AWS credentials**: Ensure AWS CLI is configured with proper credentials
2. **Lambda permissions**: Verify you have permission to invoke the Lambda function
3. **Function name**: Confirm the Lambda function name matches your deployment

## Future Enhancements

- **Historical data retention**: Implement data archival for long-term storage
- **API Gateway integration**: Create REST API for web dashboard connectivity  
- **Real-time updates**: Add WebSocket support for live dashboard updates
- **Analytics**: Add daily/weekly/monthly arrival statistics
- **Flight details**: Integrate with additional APIs for more flight information
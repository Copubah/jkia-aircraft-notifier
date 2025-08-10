#!/usr/bin/env python3
"""
Script to query today's aircraft arrivals at JKIA
"""

import boto3
import json
from datetime import datetime, timezone

def query_todays_arrivals():
    """Query Lambda function for today's arrivals"""
    lambda_client = boto3.client('lambda')
    
    try:
        # Invoke Lambda function with query parameter
        response = lambda_client.invoke(
            FunctionName='jkia-landing-notifier',
            InvocationType='RequestResponse',
            Payload=json.dumps({
                'query_type': 'todays_arrivals'
            })
        )
        
        # Parse response
        payload = json.loads(response['Payload'].read())
        result = json.loads(payload['body'])
        
        if result['status'] == 'success':
            print(f"\n🛬 JKIA Arrivals for {result['date']}")
            print("=" * 50)
            print(f"Total arrivals detected: {result['total_arrivals']}")
            
            if result['arrivals']:
                print("\nFlight Details:")
                print("-" * 50)
                for arrival in result['arrivals']:
                    status = "✅ On Ground" if arrival['on_ground'] else f"🛬 Landing ({arrival['altitude']}m)"
                    print(f"Flight: {arrival['callsign']:<12} | Time: {arrival['time']:<12} | Status: {status}")
                    print(f"         {'':12} | Velocity: {arrival['velocity']:.1f} m/s")
                    print()
            else:
                print("\nNo arrivals detected today yet.")
                
        else:
            print(f"Error: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"Error querying arrivals: {e}")

if __name__ == "__main__":
    query_todays_arrivals()
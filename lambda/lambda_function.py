import os
import json
import requests
import boto3
from datetime import datetime, timezone
from decimal import Decimal

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE', 'jkia-arrivals')
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

def store_arrival(aircraft_data):
    """Store aircraft arrival in DynamoDB"""
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)
        now = datetime.now(timezone.utc)
        
        item = {
            'date': now.strftime('%Y-%m-%d'),
            'timestamp': now.isoformat(),
            'callsign': aircraft_data.get('callsign', 'Unknown'),
            'altitude': Decimal(str(aircraft_data.get('altitude', 0))) if aircraft_data.get('altitude') else Decimal('0'),
            'on_ground': aircraft_data.get('on_ground', False),
            'velocity': Decimal(str(aircraft_data.get('velocity', 0))) if aircraft_data.get('velocity') else Decimal('0'),
            'detection_time': now.strftime('%H:%M:%S UTC')
        }
        
        # Use composite key to avoid duplicates (date + callsign + hour)
        item['arrival_id'] = f"{item['date']}#{aircraft_data.get('callsign', 'Unknown')}#{now.strftime('%H')}"
        
        table.put_item(Item=item)
        print(f"Stored arrival for {aircraft_data.get('callsign')} in DynamoDB")
        return True
    except Exception as e:
        print(f"Error storing arrival in DynamoDB: {e}")
        return False

def get_todays_arrivals():
    """Get all arrivals for today from DynamoDB"""
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        
        response = table.query(
            IndexName='date-timestamp-index',
            KeyConditionExpression='#date = :date',
            ExpressionAttributeNames={'#date': 'date'},
            ExpressionAttributeValues={':date': today}
        )
        
        return response.get('Items', [])
    except Exception as e:
        print(f"Error querying today's arrivals: {e}")
        return []

def lambda_handler(event, context):
    print(f"Starting JKIA landing check at {datetime.now(timezone.utc)}")
    
    # Check for arrivals in the last 10 minutes to avoid duplicates
    now = int(datetime.now(timezone.utc).timestamp())
    ten_min_ago = now - (10 * 60)
    
    print(f"Checking flights between {ten_min_ago} and {now}")

    # Use states API to get current aircraft positions near JKIA
    # JKIA coordinates: -1.3192, 36.9278 (lat, lon)
    # Bounding box: roughly 20km around JKIA
    lamin, lamax = -1.5, -1.1  # latitude range
    lomin, lomax = 36.7, 37.2  # longitude range
    
    url = f"https://opensky-network.org/api/states/all?lamin={lamin}&lomin={lomin}&lamax={lamax}&lomax={lomax}"
    
    try:
        print(f"Calling OpenSky API: {url}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if not data or 'states' not in data or not data['states']:
            print("No aircraft currently detected near JKIA")
            print(f"API Response: {data}")
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "status": "success",
                    "aircraft_checked": 0,
                    "landings_detected": 0,
                    "notifications_sent": 0,
                    "message": "No aircraft currently near JKIA",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
            }
        
        aircraft_states = data['states']
        print(f"Retrieved {len(aircraft_states)} aircraft near JKIA from OpenSky API")
        
        # Filter for aircraft that appear to be landing (low altitude, low velocity)
        # OpenSky states format: [icao24, callsign, origin_country, time_position, last_contact, 
        #                        longitude, latitude, baro_altitude, on_ground, velocity, ...]
        landed_aircraft = []
        for state in aircraft_states:
            if len(state) >= 9:
                callsign = state[1]
                altitude = state[7]  # barometric altitude in meters
                on_ground = state[8]
                velocity = state[9] if len(state) > 9 else None
                
                # Consider aircraft as "landing" if on ground or very low altitude with low speed
                if on_ground or (altitude and altitude < 100 and velocity and velocity < 50):
                    landed_aircraft.append({
                        'callsign': callsign.strip() if callsign else 'Unknown',
                        'altitude': altitude,
                        'on_ground': on_ground,
                        'velocity': velocity
                    })
        
        print(f"Found {len(landed_aircraft)} aircraft that appear to have landed")
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Error fetching from OpenSky API: {e}"
        print(error_msg)
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": error_msg})
        }

    # If this is a query request, return today's arrivals
    if event.get('query_type') == 'todays_arrivals':
        todays_arrivals = get_todays_arrivals()
        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "success",
                "query_type": "todays_arrivals",
                "date": datetime.now(timezone.utc).strftime('%Y-%m-%d'),
                "total_arrivals": len(todays_arrivals),
                "arrivals": [
                    {
                        "callsign": item.get('callsign'),
                        "time": item.get('detection_time'),
                        "altitude": float(item.get('altitude', 0)),
                        "on_ground": item.get('on_ground'),
                        "velocity": float(item.get('velocity', 0))
                    } for item in todays_arrivals
                ],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }, default=str)
        }

    notifications_sent = 0
    for aircraft in landed_aircraft:
        try:
            callsign = aircraft.get("callsign", "Unknown")
            altitude = aircraft.get("altitude")
            on_ground = aircraft.get("on_ground")
            velocity = aircraft.get("velocity")
            
            # Store the arrival in DynamoDB
            store_arrival(aircraft)
            
            # Create detailed message
            status = "on ground" if on_ground else f"at {altitude}m altitude"
            subject = f"✈️ Aircraft Landing Alert - JKIA"
            message = f"""
🛬 AIRCRAFT LANDING NOTIFICATION

Flight: {callsign}
Location: Near Jomo Kenyatta International Airport (JKIA)
Status: Aircraft {status}
Velocity: {velocity} m/s
Detection Time: {datetime.now(timezone.utc).strftime('%H:%M UTC')}

This aircraft appears to have recently landed or is landing at JKIA.

This is an automated notification from your JKIA Aircraft Landing Notifier.
            """.strip()
            
            # Send notification
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=subject,
                Message=message
            )
            notifications_sent += 1
            print(f"Sent notification for aircraft {callsign}")
            
        except Exception as e:
            print(f"Error sending notification for aircraft {aircraft}: {e}")

    result = {
        "statusCode": 200,
        "body": json.dumps({
            "status": "success",
            "aircraft_checked": len(aircraft_states) if 'aircraft_states' in locals() else 0,
            "landings_detected": len(landed_aircraft),
            "notifications_sent": notifications_sent,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    }
    
    print(f"Completed check: {result['body']}")
    return result

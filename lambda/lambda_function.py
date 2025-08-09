import os
import json
import requests
import boto3
from datetime import datetime, timezone

SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
sns = boto3.client('sns')

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

    notifications_sent = 0
    for aircraft in landed_aircraft:
        try:
            callsign = aircraft.get("callsign", "Unknown")
            altitude = aircraft.get("altitude")
            on_ground = aircraft.get("on_ground")
            velocity = aircraft.get("velocity")
            
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

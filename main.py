import os
import requests
import sys
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class CONFIG:
    # Coordinates: "latitude,longitude"
    START_COORD = os.getenv("START_COORD")
    DESTINATION_COORD = os.getenv("DESTINATION_COORD")
    
    TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    MY_CHAT_ID = os.getenv("MY_CHAT_ID")
    
    TOMTOM_URL = "https://api.tomtom.com/routing/1/calculateRoute/{}:{}/json"

def get_traffic_data():
    if not CONFIG.TOMTOM_API_KEY:
        print("Error: TOMTOM_API_KEY not set")
        sys.exit(1)
        
    url = CONFIG.TOMTOM_URL.format(CONFIG.START_COORD, CONFIG.DESTINATION_COORD)
    params = {
        "key": CONFIG.TOMTOM_API_KEY,
        "maxAlternatives": 1,
        "traffic": "true",
        "routeType": "fastest",
        "language": "en-US",
        "instructionsType": "text"
    }
    
    response = requests.get(url, params=params, timeout=10)
    if response.status_code != 200:
        print(f"Error fetching traffic data: {response.text}")
        sys.exit(1)
        
    return response.json()

def send_telegram_message(message):
    if not CONFIG.TELEGRAM_TOKEN or not CONFIG.MY_CHAT_ID:
        print("Error: TELEGRAM_TOKEN or MY_CHAT_ID not set")
        sys.exit(1)
        
    url = f"https://api.telegram.org/bot{CONFIG.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CONFIG.MY_CHAT_ID,
        "text": message
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Error sending Telegram message: {response.text}")
    else:
        print("Telegram message sent successfully.")

def format_time(seconds):
    minutes = seconds // 60
    return f"{minutes} min"

def format_distance(meters):
    kilometers = meters / 1000
    return f"{kilometers:.1f} km"

def get_route_name(route):
    # Try to find the major road from guidance instructions
    guidance = route.get("guidance", {})
    instructions = guidance.get("instructions", [])
    
    # Collect unique street names with significant travel time/distance if possible
    # For now, let's grab the street name with the longest distance or just the first major highway
    
    road_names = []
    for instr in instructions:
        street = instr.get("street")
        if street and street not in road_names:
            road_names.append(street)
            # Limit to first 2 roads to keep names concise
            if len(road_names) >= 2:
                break
            
    # Heuristic: return the first 2 unique major roads found
    if road_names:
        return " via " + ", ".join(road_names)
    
    return ""

def main():
    data = get_traffic_data()
    
    routes = data.get("routes", [])
    if not routes:
        print("No routes found.")
        return

    # Primary Route (Index 0)
    primary_route = routes[0]
    primary_summary = primary_route["summary"]
    primary_time = primary_summary["travelTimeInSeconds"]
    primary_delay = primary_summary.get("trafficDelayInSeconds", 0)
    primary_distance = primary_summary["lengthInMeters"]
    primary_name = "Primary Route" + get_route_name(primary_route)
    
    print(f"{primary_name}: {format_distance(primary_distance)}, {format_time(primary_time)} (Delay: {format_time(primary_delay)})")

    # Check logic: Delay > 5 minutes (300 seconds)
    if primary_delay > 300:
        message = f"⚠️ Traffic Alert!\n\n{primary_name}\nDistance: {format_distance(primary_distance)}\nDelay: {format_time(primary_delay)}\nTotal Time: {format_time(primary_time)}"
        
        # Check Alternative Route if available
        if len(routes) > 1:
            alt_route = routes[1]
            alt_summary = alt_route["summary"]
            alt_time = alt_summary["travelTimeInSeconds"]
            alt_distance = alt_summary["lengthInMeters"]
            alt_name = "Alternative Route" + get_route_name(alt_route)
            
            message += f"\n\n{alt_name}\nDistance: {format_distance(alt_distance)}\nTime: {format_time(alt_time)}"
            
            if alt_time < primary_time:
                saved_time = primary_time - alt_time
                message += f"\n\n✅ RECOMMENDATION: Take {alt_name}! It is faster by {format_time(saved_time)}."
            else:
                 message += f"\n\n{primary_name} is still the fastest despite the delay."
        else:
             message += "\n\nNo alternative route available."
             
        send_telegram_message(message)
    else:
        print("Traffic is normal. No alert sent.")

if __name__ == "__main__":
    main()

import psycopg2
from dotenv import load_dotenv
import os
import random
import time
import requests
from datetime import datetime

load_dotenv()

def get_connection():
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return connection

def generate_traffic_reading(road_id):
    vehicle_count = random.randint(50, 500)
    avg_speed = round(random.uniform(10, 60), 2)
    
    if avg_speed < 20:
        congestion_level = "High"
    elif avg_speed < 40:
        congestion_level = "Medium"
    else:
        congestion_level = "Low"
    
    recorded_at = datetime.now()
    
    return (road_id, recorded_at, vehicle_count, avg_speed, congestion_level)

def maybe_generate_accident(road_id):
    chance = random.randint(1, 100)

    if chance <= 10:  # 10% chance
        severity = random.choice(["Minor", "Major", "Fatal"])
        occurred_at = datetime.now()
        return (road_id, occurred_at, severity)
    else:
        return None


def fetch_weather(city="Jaipur"):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    temperature = data["main"]["temp"]
    condition = data["weather"][0]["main"]
    visibility = data.get("visibility", 10000) / 1000  # meters ko km mein convert kiya

    recorded_at = datetime.now()

    return (recorded_at, temperature, condition, visibility)

def insert_traffic_reading(data):
    connection = get_connection()
    cursor = connection.cursor()
    
    query = """
        INSERT INTO traffic_readings (road_id, recorded_at, vehicle_count, avg_speed, congestion_level)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, data)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print("Data inserted:", data)

def insert_weather(data):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO weather (recorded_at, temperature, condition, visibility)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, data)

    connection.commit()
    cursor.close()
    connection.close()

    print("Weather inserted:", data)

def insert_accident(data):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO accidents (road_id, occurred_at, severity)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, data)

    connection.commit()
    cursor.close()
    connection.close()

    print("Accident inserted:", data)

if __name__ == "__main__":
        road_ids = [1, 2]  # humare roads table mein jo road_id hain
    
while True:
        for road_id in road_ids:
            data = generate_traffic_reading(road_id)
            insert_traffic_reading(data)

            accident_data = maybe_generate_accident(road_id)
            if accident_data:
                insert_accident(accident_data)

        weather_data = fetch_weather("Jaipur")
        insert_weather(weather_data)

        print("Waiting 10 seconds before next collection...\n")
        time.sleep(10)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return connection

@app.get("/")
def home():
    return {"message": "Smart City Traffic API is running!"}

@app.get("/roads")
def get_roads(state: str = None, city: str = None):
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT road_id, road_name, latitude, longitude, road_type, city, state FROM roads WHERE 1=1"
    params = []

    if state:
        query += " AND state = %s"
        params.append(state)
    if city:
        query += " AND city = %s"
        params.append(city)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    roads = []
    for row in rows:
        roads.append({
            "road_id": row[0],
            "road_name": row[1],
            "latitude": float(row[2]),
            "longitude": float(row[3]),
            "road_type": row[4],
            "city": row[5],
            "state": row[6]
        })
    return roads

@app.get("/states")
def get_states():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT state FROM roads ORDER BY state;")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    return [row[0] for row in rows]


@app.get("/cities")
def get_cities(state: str = None):
    connection = get_connection()
    cursor = connection.cursor()

    if state:
        cursor.execute("SELECT DISTINCT city FROM roads WHERE state = %s ORDER BY city;", (state,))
    else:
        cursor.execute("SELECT DISTINCT city FROM roads ORDER BY city;")

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    return [row[0] for row in rows]

@app.get("/traffic-summary")
def get_traffic_summary():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT road_id, avg_speed, avg_vehicle_count, total_readings, last_updated FROM road_traffic_summary;")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    summary = []
    for row in rows:
        summary.append({
            "road_id": row[0],
            "avg_speed": float(row[1]),
            "avg_vehicle_count": float(row[2]),
            "total_readings": row[3],
            "last_updated": row[4].isoformat()
        })
    return summary

@app.get("/accidents")
def get_accidents():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT accident_id, road_id, occurred_at, severity FROM accidents;")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    accidents = []
    for row in rows:
        accidents.append({
            "accident_id": row[0],
            "road_id": row[1],
            "occurred_at": row[2].isoformat(),
            "severity": row[3]
        })
    return accidents

@app.get("/weather-latest")
def get_weather_latest(city: str = "Jaipur"):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT temperature, condition, visibility, recorded_at FROM weather WHERE city = %s ORDER BY recorded_at DESC LIMIT 1;",
        (city,)
    )
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if row:
        return {
            "temperature": float(row[0]),
            "condition": row[1],
            "visibility": float(row[2]),
            "recorded_at": row[3].isoformat()
        }
    return None
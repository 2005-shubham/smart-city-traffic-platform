import pandas as pd
from dotenv import load_dotenv
import os
import psycopg2

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

def extract_traffic_data():
    connection = get_connection()
    query = "SELECT * FROM traffic_readings;"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

def transform_traffic_data(df):
    summary = df.groupby("road_id").agg(
        avg_speed=("avg_speed", "mean"),
        avg_vehicle_count=("vehicle_count", "mean"),
        total_readings=("reading_id", "count")
    ).reset_index()

    summary["avg_speed"] = summary["avg_speed"].round(2)
    summary["avg_vehicle_count"] = summary["avg_vehicle_count"].round(0)

    return summary

def load_summary_data(summary_df):
    connection = get_connection()
    cursor = connection.cursor()

    for _, row in summary_df.iterrows():
        query = """
            INSERT INTO road_traffic_summary (road_id, avg_speed, avg_vehicle_count, total_readings, last_updated)
            VALUES (%s, %s, %s, %s, NOW())
            ON CONFLICT (road_id) 
            DO UPDATE SET 
                avg_speed = EXCLUDED.avg_speed,
                avg_vehicle_count = EXCLUDED.avg_vehicle_count,
                total_readings = EXCLUDED.total_readings,
                last_updated = NOW();
        """
        cursor.execute(query, (
            int(row["road_id"]),
            float(row["avg_speed"]),
            float(row["avg_vehicle_count"]),
            int(row["total_readings"])
        ))

    connection.commit()
    cursor.close()
    connection.close()
    print("Summary data loaded successfully!")

if __name__ == "__main__":
    traffic_df = extract_traffic_data()
    summary_df = transform_traffic_data(traffic_df)
    load_summary_data(summary_df)
    print(summary_df)
    
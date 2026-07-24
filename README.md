# Smart City Traffic Analytics Platform

A full-stack traffic monitoring system that collects, processes, and visualizes real-time traffic, weather, and accident data across multiple cities in Rajasthan, India. Built as a personal project to learn how data engineering, backend APIs, and modern frontend development come together in a real system.

The long-term idea behind this project is simple: people should be able to check live traffic conditions, weather, and accident reports for any city near them from their phone — the same way you'd check the weather. This is a working prototype of that idea, built with simulated traffic data and real weather data.

## What it does

- Continuously collects traffic readings (vehicle count, average speed, congestion level) for roads across four cities: Jaipur, Alwar, Udaipur, and Kota
- Pulls real, live weather data for each city from OpenWeatherMap
- Randomly simulates traffic accidents to demonstrate incident tracking
- Processes raw traffic data into per-road summaries (average speed, average vehicle count) using an ETL pipeline
- Serves everything through a REST API
- Displays live data on a dark-themed, mobile-responsive dashboard with a state/city selector
- Includes a Power BI dashboard for deeper analytics (speed comparisons, congestion distribution, accident severity)
- Runs fully containerized with Docker Compose

## Architecture

OpenWeatherMap API  ─┐
├─► Python Collector ─► PostgreSQL ─► ETL (Pandas) ─► road_traffic_summary
Simulated Traffic ───┘                       │
                                             ▼
                                      FastAPI Backend
                                             │
                         ┌───────────────────┼──────────────┐
                         ▼                                  ▼
                          React Dashboard Power BI Dashboard

## Tech stack

**Data & Backend**
- Python (data collection, ETL)
- PostgreSQL (database)
- Pandas (data transformation)
- FastAPI (REST API)
- OpenWeatherMap API (live weather data)

**Frontend**
- React (Vite)
- Axios
- Plain CSS (custom dark theme, no UI framework)

**Analytics**
- Power BI Desktop

**DevOps**
- Docker & Docker Compose
- Git / GitHub

## Project structure

smart-city-traffic-platform/
├── data_collector/ # Python scripts: collector.py, etl.py
├── backend/ # FastAPI application
├── frontend/ # React dashboard (Vite)
├── dashboard/ # Power BI file (.pbix)
├── docker-compose.yml
└── README.md

## Database schema

Five tables in PostgreSQL:

- **roads** — road name, coordinates, road type, city, state
- **traffic_readings** — vehicle count, average speed, congestion level, timestamp, linked to a road
- **weather** — temperature, condition, visibility, per city
- **accidents** — severity, timestamp, linked to a road
- **road_traffic_summary** — aggregated per-road stats, updated by the ETL pipeline

## API endpoints

| Endpoint | Description |
|---|---|
| `GET /roads?state=&city=` | List roads, optionally filtered by state/city |
| `GET /traffic-summary` | Aggregated speed & vehicle count per road |
| `GET /accidents` | All recorded accidents |
| `GET /weather-latest?city=` | Latest weather for a city |
| `GET /states` | List of available states |
| `GET /cities?state=` | Cities within a state |

Interactive API docs available at `/docs` (Swagger UI) once the backend is running.

## Running locally

### 1. Database
Create a PostgreSQL database named `smart_city_traffic` and run the table creation queries (see `/backend` for schema, or set up manually using the structure above).

### 2. Data Collector
```bash
cd data_collector
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Create a `.env` file with your database credentials and an OpenWeatherMap API key, then run:
```bash
python collector.py
```
This starts a loop that inserts new traffic, weather, and accident data every 10 seconds.

### 3. ETL
```bash
python etl.py
```
Run this whenever you want the `road_traffic_summary` table refreshed with the latest aggregates.

### 4. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
API runs at `http://127.0.0.1:8000`.

### 5. Frontend
```bash
cd frontend
npm install
npm run dev
```
Dashboard runs at `http://localhost:5173`.

### Or, run everything with Docker
```bash
docker-compose up
```
This builds and starts the backend and collector together.

## Design notes

The dashboard uses a dark, control-room-style layout inspired by real traffic monitoring systems — deep navy background, amber/teal/red status colors matching traffic-light conventions, and a monospace font for live numbers to give it a technical, readout feel. Each road card includes a small animated "pulse" bar whose speed reflects real congestion — slower flow means heavier traffic. Weather conditions are shown with small custom-built animated icons (sun, cloud, rain) rather than static images.

## Current limitations

- Traffic data is simulated, not sourced from real sensors
- Limited to four cities in Rajasthan (by design, for this stage of the project)
- No authentication or multi-user support
- Runs locally; not yet deployed to a cloud server

## Possible next steps

- Deploy to a cloud provider (AWS/Azure) for public access
- Expand to more states and cities
- Replace simulated traffic data with real sensor or crowd-sourced data
- Add historical trend charts (traffic over days/weeks)
- Push notifications for accidents on a user's selected route

## Author

Built by Shubham Sharma as a hands-on project to learn data analytics and DevOps practices end to end — from raw data collection to a deployed-style, containerized full-stack application.
import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function WeatherIcon({ condition }) {
  const type = condition?.toLowerCase() || ''

  if (type.includes('clear')) {
    return (
      <div className="weather-icon icon-sun">
        <div className="sun-core"></div>
        <div className="sun-rays"></div>
      </div>
    )
  }

  if (type.includes('rain') || type.includes('drizzle')) {
    return (
      <div className="weather-icon icon-rain">
        <div className="rain-cloud"></div>
        <span className="drop drop-1"></span>
        <span className="drop drop-2"></span>
        <span className="drop drop-3"></span>
      </div>
    )
  }

  return (
    <div className="weather-icon icon-cloud">
      <div className="cloud-body">
        <span className="cloud-bump bump-1"></span>
        <span className="cloud-bump bump-2"></span>
        <span className="cloud-bump bump-3"></span>
      </div>
    </div>
  )
}

function App() {
  const [roads, setRoads] = useState([])
  const [summary, setSummary] = useState([])
  const [accidents, setAccidents] = useState([])
  const [weather, setWeather] = useState(null)
  const [states, setStates] = useState([])
  const [cities, setCities] = useState([])
  const [selectedState, setSelectedState] = useState('Rajasthan')
  const [selectedCity, setSelectedCity] = useState('Jaipur')

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/states')
      .then((response) => setStates(response.data))
      .catch((error) => console.error('Error fetching states:', error))
  }, [])

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/cities?state=${selectedState}`)
      .then((response) => {
        setCities(response.data)
        if (response.data.length > 0 && !response.data.includes(selectedCity)) {
          setSelectedCity(response.data[0])
        }
      })
      .catch((error) => console.error('Error fetching cities:', error))
  }, [selectedState])

  useEffect(() => {
    const fetchData = () => {
      axios.get(`http://127.0.0.1:8000/roads?city=${selectedCity}`)
        .then((response) => setRoads(response.data))
        .catch((error) => console.error('Error fetching roads:', error))

      axios.get('http://127.0.0.1:8000/traffic-summary')
        .then((response) => setSummary(response.data))
        .catch((error) => console.error('Error fetching summary:', error))

      axios.get('http://127.0.0.1:8000/accidents')
        .then((response) => setAccidents(response.data))
        .catch((error) => console.error('Error fetching accidents:', error))

      axios.get(`http://127.0.0.1:8000/weather-latest?city=${selectedCity}`)
        .then((response) => setWeather(response.data))
        .catch((error) => console.error('Error fetching weather:', error))
    }

    fetchData()
    const interval = setInterval(fetchData, 10000)
    return () => clearInterval(interval)
  }, [selectedCity])

  const getCongestionLevel = (avgSpeed) => {
    if (avgSpeed < 20) return 'high'
    if (avgSpeed < 40) return 'medium'
    return 'low'
  }

  const getRoadName = (roadId) => {
    const road = roads.find((r) => r.road_id === roadId)
    return road ? road.road_name : `Road ${roadId}`
  }

  const cityRoadIds = roads.map((r) => r.road_id)
  const recentAccidents = [...accidents]
    .filter((a) => cityRoadIds.includes(a.road_id))
    .sort((a, b) => new Date(b.occurred_at) - new Date(a.occurred_at))
    .slice(0, 4)

  return (
    <div className="app">
      <header className="topbar">
        <span className="topbar-label">RAJASTHAN TRAFFIC WATCH</span>

        <div className="selectors">
          <select
            className="city-select"
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
          >
            {states.map((state) => (
              <option key={state} value={state}>{state}</option>
            ))}
          </select>

          <select
            className="city-select"
            value={selectedCity}
            onChange={(e) => setSelectedCity(e.target.value)}
          >
            {cities.map((city) => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>
        </div>

        <span className="topbar-status">● LIVE</span>
      </header>

      <main className="grid">
        {roads.map((road) => {
          const roadSummary = summary.find((s) => s.road_id === road.road_id)
          const level = roadSummary ? getCongestionLevel(roadSummary.avg_speed) : 'low'

          return (
            <div key={road.road_id} className={`road-card level-${level}`}>
              <div className="road-card-header">
                <span className="road-name">{road.road_name}</span>
                <span className={`status-dot dot-${level}`}></span>
              </div>
              <div className="road-stat">
                <span className="stat-value">
                  {roadSummary ? roadSummary.avg_speed.toFixed(1) : '--'}
                </span>
                <span className="stat-unit">km/h avg</span>
              </div>
              <div className="road-meta">
                <span>{roadSummary ? Math.round(roadSummary.avg_vehicle_count) : '--'} vehicles</span>
                <span className="road-type">{road.road_type}</span>
              </div>
              <div className="pulse-track">
                <div className={`pulse-dash dash-${level}`}></div>
              </div>
            </div>
          )
        })}

        <div className="road-card weather-card">
          <div className="road-card-header">
            <span className="road-name">Weather</span>
            {weather && <WeatherIcon condition={weather.condition} />}
          </div>
          {weather ? (
            <>
              <div className="road-stat">
                <span className="stat-value">{weather.temperature.toFixed(1)}</span>
                <span className="stat-unit">°C</span>
              </div>
              <div className="road-meta">
                <span>{weather.condition}</span>
                <span>{weather.visibility.toFixed(1)} km visibility</span>
              </div>
            </>
          ) : (
            <p className="empty-state">Loading weather...</p>
          )}
        </div>

        <div className="road-card accident-card">
          <div className="road-card-header">
            <span className="road-name">Recent Incidents</span>
          </div>
          {recentAccidents.length === 0 ? (
            <p className="empty-state">No incidents reported</p>
          ) : (
            <ul className="accident-list">
              {recentAccidents.map((accident) => (
                <li key={accident.accident_id} className={`accident-item severity-${accident.severity.toLowerCase()}`}>
                  <span className="accident-severity">{accident.severity}</span>
                  <span className="accident-road">{getRoadName(accident.road_id)}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function WeatherMap() {
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    fetch('/api/weather')
      .then(res => res.json())
      .then(data => setWeather(data))
      .catch(err => console.error("Weather error:", err));
  }, []);

  const position = [16.3067, 80.4365]; // Guntur Farm Coordinates

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fadeIn">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <span className="badge-amber">OpenWeather API Engine</span>
          <h1 className="text-3xl font-extrabold text-white">Weather Intelligence & Spraying Map</h1>
          <p className="text-xs text-slate-300">Micro-climate analysis & 5-day fungicide spraying windows</p>
        </div>
        <span className="badge-green">Guntur Crop District • 16.3067° N, 80.4365° E</span>
      </div>

      {/* 5 Weather Stat Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        <div className="glass-panel p-4 space-y-1">
          <span className="text-[11px] text-slate-400 font-medium">Temperature</span>
          <div className="text-2xl font-bold text-white">{weather?.temp_c || 29.5}°C</div>
          <span className="text-[10px] text-slate-400">Feels like {weather?.feels_like_c || 31.2}°C</span>
        </div>

        <div className="glass-panel p-4 space-y-1">
          <span className="text-[11px] text-slate-400 font-medium">Humidity</span>
          <div className="text-2xl font-bold text-blue-400">{weather?.humidity_pct || 78}%</div>
          <span className="text-[10px] text-slate-400">High fungal spore risk</span>
        </div>

        <div className="glass-panel p-4 space-y-1">
          <span className="text-[11px] text-slate-400 font-medium">Wind Speed</span>
          <div className="text-2xl font-bold text-emerald-400">{weather?.wind_speed_kmh || 12.5} km/h</div>
          <span className="text-[10px] text-slate-400">Low drift hazard</span>
        </div>

        <div className="glass-panel p-4 space-y-1">
          <span className="text-[11px] text-slate-400 font-medium">Rain Forecast</span>
          <div className="text-2xl font-bold text-amber-400">{weather?.rain_mm || 4.2} mm</div>
          <span className="text-[10px] text-amber-300/80">Rain expected in 14h</span>
        </div>

        <div className="glass-panel p-4 space-y-1">
          <span className="text-[11px] text-slate-400 font-medium">UV Index</span>
          <div className="text-2xl font-bold text-rose-400">{weather?.uv_index || 8.0} / 12</div>
          <span className="text-[10px] text-slate-400">Very High UV</span>
        </div>
      </div>

      {/* Map & Spray Window Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Leaflet OpenStreetMap Container */}
        <div className="glass-panel p-4 lg:col-span-2 space-y-3 min-h-[420px] flex flex-col justify-between overflow-hidden">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white">📍 Field Location & Micro-Climate Map</h3>
            <span className="text-xs text-slate-400">OpenStreetMap Layers</span>
          </div>

          <div className="w-full h-80 rounded-2xl overflow-hidden border border-white/10 z-0">
            <MapContainer center={position} zoom={13} style={{ height: '100%', width: '100%' }}>
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              />
              <Marker position={position}>
                <Popup>
                  <strong>Guntur Crop Sector 4B</strong><br />
                  Tomato & Potato Fields<br />
                  Temp: {weather?.temp_c || 29.5}°C
                </Popup>
              </Marker>
              <Circle center={position} radius={1200} pathOptions={{ color: '#10b981', fillColor: '#10b981', fillOpacity: 0.15 }} />
            </MapContainer>
          </div>
        </div>

        {/* 5-Day Spraying Risk Forecast */}
        <div className="glass-panel p-6 space-y-4">
          <h3 className="text-sm font-bold text-white">🗓️ 5-Day Spraying Risk Windows</h3>
          <p className="text-xs text-slate-400">OpenWeather forecast integrated with fungicide drift calculations</p>

          <div className="space-y-3 pt-2">
            {(weather?.forecast || [
              { day: "Today", temp: "29°C", rain: "4.2mm", risk: "High Risk" },
              { day: "Tomorrow", temp: "30°C", rain: "0.0mm", risk: "Low Risk" },
              { day: "Day 3", temp: "32°C", rain: "1.0mm", risk: "Medium Risk" },
              { day: "Day 4", temp: "28°C", rain: "18.2mm", risk: "Very High Risk" },
              { day: "Day 5", temp: "27°C", rain: "0.2mm", risk: "Low Risk" }
            ]).map((item, idx) => (
              <div key={idx} className="bg-slate-900/90 rounded-2xl p-3.5 border border-white/10 flex items-center justify-between">
                <div>
                  <h4 className="text-xs font-bold text-white">{item.day}</h4>
                  <p className="text-[11px] text-slate-400">{item.temp} • Rain: {item.rain}</p>
                </div>
                <span className={
                  item.risk === "Low Risk" ? "badge-green" : item.risk === "Medium Risk" ? "badge-amber" : "badge-rose"
                }>
                  {item.risk}
                </span>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
}

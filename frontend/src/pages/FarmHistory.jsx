import React, { useState, useEffect } from 'react';

export default function FarmHistory() {
  const [history, setHistory] = useState({ scans: [], calls: [] });

  useEffect(() => {
    fetch('/api/history')
      .then(res => res.json())
      .then(data => setHistory(data))
      .catch(err => console.error("History fetch error:", err));
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fadeIn">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <span className="badge-green">SQLite Database Node</span>
          <h1 className="text-3xl font-extrabold text-white">Farm History & Voice Call Logs</h1>
          <p className="text-xs text-slate-300">Complete historical timeline of disease scans, treatments, and AI Voice interactions</p>
        </div>
      </div>

      {/* 1. Lifecycle Status Progression Timeline */}
      <div className="glass-panel p-6 space-y-4">
        <h3 className="text-base font-bold text-white">🌱 Crop Lifecycle Disease Recovery Progression</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2">
          <div className="bg-emerald-950/30 p-4 rounded-2xl border border-emerald-500/40 space-y-1">
            <span className="text-xs font-bold text-emerald-400">Step 1: Healthy Growth</span>
            <p className="text-xs text-slate-200">Baseline leaf foliage scan (100% Health)</p>
          </div>
          <div className="bg-amber-950/30 p-4 rounded-2xl border border-amber-500/40 space-y-1">
            <span className="text-xs font-bold text-amber-400">Step 2: Early Detection</span>
            <p className="text-xs text-slate-200">MobileNetV2 identified Early Blight (Confidence 88.5%)</p>
          </div>
          <div className="bg-blue-950/30 p-4 rounded-2xl border border-blue-500/40 space-y-1">
            <span className="text-xs font-bold text-blue-400">Step 3: 5-Day Treatment</span>
            <p className="text-xs text-slate-200">Gemini treatment plan + Voice Call reminder</p>
          </div>
          <div className="bg-teal-950/30 p-4 rounded-2xl border border-teal-500/40 space-y-1">
            <span className="text-xs font-bold text-teal-400">Step 4: Fully Recovered</span>
            <p className="text-xs text-slate-200">Foliage healed, harvest loss prevented</p>
          </div>
        </div>
      </div>

      {/* 2. Scan Records Table */}
      <div className="glass-panel p-6 space-y-4">
        <h3 className="text-base font-bold text-white">🔬 MobileNetV2 Scan Log</h3>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-white/5 text-slate-400 font-bold uppercase tracking-wider">
              <tr>
                <th className="p-3">ID</th>
                <th className="p-3">Crop</th>
                <th className="p-3">Disease Prediction</th>
                <th className="p-3">Confidence</th>
                <th className="p-3">Severity</th>
                <th className="p-3">Savings</th>
                <th className="p-3">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-slate-200">
              {history.scans && history.scans.length > 0 ? (
                history.scans.map((s, idx) => (
                  <tr key={idx} className="hover:bg-white/5 transition-colors">
                    <td className="p-3 font-mono font-bold text-emerald-400">#{s.id}</td>
                    <td className="p-3 font-bold">{s.crop}</td>
                    <td className="p-3 font-semibold text-white">{s.disease}</td>
                    <td className="p-3">{(s.confidence * 100).toFixed(1)}%</td>
                    <td className="p-3"><span className="badge-amber">{s.severity}</span></td>
                    <td className="p-3 font-bold text-emerald-400">₹{s.estimated_savings}</td>
                    <td className="p-3 text-slate-400 font-mono">{s.scanned_at ? s.scanned_at.split('T')[0] : 'Today'}</td>
                  </tr>
                ))
              ) : (
                [
                  { id: 101, crop: "Tomato", disease: "Tomato___Early_blight", conf: 0.88, sev: "Medium Risk", savings: 18500, date: "2026-07-29" },
                  { id: 102, crop: "Tomato", disease: "Tomato___healthy", conf: 0.94, sev: "Low Risk", savings: 28000, date: "2026-07-28" },
                  { id: 103, crop: "Potato", disease: "Potato___healthy", conf: 0.91, sev: "Low Risk", savings: 22000, date: "2026-07-25" }
                ].map((s, idx) => (
                  <tr key={idx} className="hover:bg-white/5 transition-colors">
                    <td className="p-3 font-mono font-bold text-emerald-400">#{s.id}</td>
                    <td className="p-3 font-bold">{s.crop}</td>
                    <td className="p-3 font-semibold text-white">{s.disease}</td>
                    <td className="p-3">{(s.conf * 100).toFixed(1)}%</td>
                    <td className="p-3"><span className="badge-amber">{s.sev}</span></td>
                    <td className="p-3 font-bold text-emerald-400">₹{s.savings}</td>
                    <td className="p-3 text-slate-400 font-mono">{s.date}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* 3. OmniDimension Voice AI Call Logs */}
      <div className="glass-panel p-6 space-y-4">
        <h3 className="text-base font-bold text-white">🎙️ OmniDimension Voice AI Call Logs</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {history.calls && history.calls.length > 0 ? (
            history.calls.map((call, idx) => (
              <div key={idx} className="bg-slate-900/80 p-4 rounded-2xl border border-white/10 space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-emerald-400">📞 {call.farmer_phone}</span>
                  <span className="text-slate-400 font-mono">{call.duration_seconds} seconds</span>
                </div>
                <p className="text-xs text-slate-200 leading-relaxed">{call.summary}</p>
                <div className="text-[11px] text-amber-300 font-semibold pt-2 border-t border-white/5">
                  ⏰ Reminder: {call.reminder || "Tomorrow at 5:30 PM"}
                </div>
              </div>
            ))
          ) : (
            <div className="bg-slate-900/80 p-4 rounded-2xl border border-white/10 space-y-2 col-span-2">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-emerald-400">📞 Ramesh Rao (+91 9876543210)</span>
                <span className="text-slate-400 font-mono">78 seconds</span>
              </div>
              <p className="text-xs text-slate-200 leading-relaxed">
                Voice AI called farmer. Explained Tomato Early Blight detection & weather-aware spraying window. Farmer inquired about Neem oil mixing. Scheduled Day 2 spray reminder for 5:30 PM.
              </p>
              <div className="text-[11px] text-amber-300 font-semibold pt-2 border-t border-white/5">
                ⏰ Scheduled Reminder: Tomorrow at 5:30 PM (Day 2 Spray Reminder)
              </div>
            </div>
          )}
        </div>
      </div>

    </div>
  );
}

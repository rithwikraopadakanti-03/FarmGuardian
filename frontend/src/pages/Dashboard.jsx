import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, PieChart, Pie, Cell } from 'recharts';
import { translations } from '../i18n/translations';

export default function Dashboard({ currentLang, onOpenVoiceModal }) {
  const t = translations[currentLang]?.dashboard || translations.en.dashboard;

  const [weather, setWeather] = useState(null);
  const [history, setHistory] = useState({ scans: [], calls: [] });

  useEffect(() => {
    // Fetch live weather from API
    fetch('/api/weather')
      .then(res => res.json())
      .then(data => setWeather(data))
      .catch(err => console.error("Weather fetch error:", err));

    // Fetch history from API
    fetch('/api/history')
      .then(res => res.json())
      .then(data => setHistory(data))
      .catch(err => console.error("History fetch error:", err));
  }, []);

  // Yield Comparison Data for Recharts
  const yieldData = [
    { month: 'Jan', Healthy: 100, Predicted: 92 },
    { month: 'Feb', Healthy: 100, Predicted: 88 },
    { month: 'Mar', Healthy: 100, Predicted: 75 },
    { month: 'Apr', Healthy: 100, Predicted: 84 },
    { month: 'May', Healthy: 100, Predicted: 95 },
  ];

  // Disease Distribution Pie Chart Data
  const pieData = [
    { name: 'Healthy', value: 55, color: '#10b981' },
    { name: 'Early Blight', value: 30, color: '#f59e0b' },
    { name: 'Late Blight', value: 15, color: '#f43f5e' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fadeIn">
      
      {/* Header Banner */}
      <div className="glass-panel p-6 sm:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 relative overflow-hidden">
        <div className="absolute -right-10 -bottom-10 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="badge-green">🟢 Live Intelligence Node</span>
            <span className="text-xs text-slate-400 font-mono">Guntur Sector 4B • Andhra Pradesh</span>
          </div>
          <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight">
            {t.welcome}
          </h1>
          <p className="text-sm text-slate-300 max-w-xl mt-1">
            Real-time MobileNetV2 ML Diagnostics, OpenWeather Spraying Risk Alerts, and Gemini Agronomist Planning.
          </p>
        </div>

        {/* Quick Actions */}
        <div className="flex items-center gap-3 w-full md:w-auto">
          <Link to="/detect" className="glass-button text-sm w-full md:w-auto justify-center">
            🔬 {t.newScan}
          </Link>
          <button onClick={onOpenVoiceModal} className="glass-button-secondary text-sm w-full md:w-auto justify-center">
            📞 {t.triggerVoice}
          </button>
        </div>
      </div>

      {/* 4 Core KPI Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        
        {/* Farm Health Score Gauge */}
        <div className="glass-panel p-5 space-y-3">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-400">
            <span>{t.healthScore}</span>
            <span className="text-emerald-400 font-bold">92/100</span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">92%</span>
            <span className="text-xs text-emerald-400 font-medium">↑ 4.2% this week</span>
          </div>
          <div className="w-full h-2.5 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-emerald-500 to-teal-400 rounded-full" style={{ width: '92%' }} />
          </div>
        </div>

        {/* Today's Weather */}
        <div className="glass-panel p-5 space-y-3">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-400">
            <span>{t.todayWeather}</span>
            <span className="text-blue-400 font-mono">{weather?.city || "Guntur"}</span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{weather?.temp_c || 29.5}°C</span>
            <span className="text-xs text-slate-300">💧 {weather?.humidity_pct || 78}% Hum</span>
          </div>
          <div className="text-xs text-amber-400 font-medium truncate">
            ⚠️ {weather?.spraying_risk || "Medium Spraying Risk"}
          </div>
        </div>

        {/* Recovery Rate */}
        <div className="glass-panel p-5 space-y-3">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-400">
            <span>{t.recoveryRate}</span>
            <span className="text-emerald-400 font-bold">88.5%</span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">88.5%</span>
            <span className="text-xs text-slate-400">Target 85%</span>
          </div>
          <div className="w-full h-2.5 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-teal-400 to-blue-500 rounded-full" style={{ width: '88.5%' }} />
          </div>
        </div>

        {/* Financial Savings */}
        <div className="glass-panel p-5 space-y-3">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-400">
            <span>{t.financialSavings}</span>
            <span className="text-emerald-400 font-bold">₹18,500</span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-emerald-400">₹18.5k</span>
            <span className="text-xs text-slate-400">ROI 14.2x</span>
          </div>
          <p className="text-[11px] text-slate-400">Based on early MobileNetV2 disease detection</p>
        </div>

      </div>

      {/* Analytics Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Yield Loss Prediction Chart (Recharts) */}
        <div className="glass-panel p-6 lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-white">{t.yieldPrediction}</h3>
              <p className="text-xs text-slate-400">Comparing ideal harvest yield against predicted recovery yield</p>
            </div>
            <span className="badge-green">AI Forecast</span>
          </div>

          <div className="h-64 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={yieldData}>
                <defs>
                  <linearGradient id="healthyGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="predGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="month" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Area type="monotone" dataKey="Healthy" stroke="#10b981" fillOpacity={1} fill="url(#healthyGrad)" />
                <Area type="monotone" dataKey="Predicted" stroke="#3b82f6" fillOpacity={1} fill="url(#predGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Disease Distribution Pie Chart */}
        <div className="glass-panel p-6 space-y-4">
          <h3 className="text-base font-bold text-white">{t.diseaseDistribution}</h3>
          <p className="text-xs text-slate-400">Classification distribution across field scans</p>

          <div className="h-48 w-full flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={75}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '8px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="space-y-2 pt-2">
            {pieData.map((item, idx) => (
              <div key={idx} className="flex items-center justify-between text-xs font-medium">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-slate-300">{item.name}</span>
                </div>
                <span className="text-white font-bold">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Recent Scans Table / Cards */}
      <div className="glass-panel p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-white">{t.recentScans}</h3>
          <Link to="/history" className="text-xs text-emerald-400 font-semibold hover:underline">
            View All History →
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {history.scans && history.scans.length > 0 ? (
            history.scans.slice(0, 3).map((scan, idx) => (
              <div key={idx} className="bg-slate-900/80 rounded-2xl p-4 border border-white/10 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-white">{scan.crop}</span>
                  <span className="badge-green">{scan.severity}</span>
                </div>
                <h4 className="text-sm font-semibold text-emerald-400">{scan.disease}</h4>
                <div className="flex justify-between text-[11px] text-slate-400 pt-2 border-t border-white/5">
                  <span>Confidence: {(scan.confidence * 100).toFixed(1)}%</span>
                  <span>Est. Savings: ₹{scan.estimated_savings}</span>
                </div>
              </div>
            ))
          ) : (
            [
              { crop: "Tomato", disease: "Tomato___healthy", conf: 0.88, sev: "Low Risk", savings: 28000 },
              { crop: "Tomato", disease: "Tomato___Early_blight", conf: 0.86, sev: "Medium Risk", savings: 18500 },
              { crop: "Potato", disease: "Potato___healthy", conf: 0.94, sev: "Low Risk", savings: 22000 }
            ].map((scan, idx) => (
              <div key={idx} className="bg-slate-900/80 rounded-2xl p-4 border border-white/10 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-white">{scan.crop}</span>
                  <span className="badge-green">{scan.sev}</span>
                </div>
                <h4 className="text-sm font-semibold text-emerald-400">{scan.disease}</h4>
                <div className="flex justify-between text-[11px] text-slate-400 pt-2 border-t border-white/5">
                  <span>Confidence: {(scan.conf * 100).toFixed(1)}%</span>
                  <span>Est. Savings: ₹{scan.savings}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

    </div>
  );
}

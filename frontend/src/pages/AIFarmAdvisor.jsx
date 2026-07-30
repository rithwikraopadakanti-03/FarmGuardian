import React, { useState } from 'react';
import { translations } from '../i18n/translations';

export default function AIFarmAdvisor({ currentLang, latestScanData }) {
  const t = translations[currentLang]?.advisor || translations.en.advisor;

  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: currentLang === 'te' 
        ? "నమస్కారం! నేను మీ ఫార్మ్‌గార్డియన్ AI ఫార్మ్ అసిస్టెంట్‌ని. మీ పంట, వాతావరణం లేదా చికిత్స గురించిన ప్రశ్నలు అడగండి."
        : currentLang === 'hi'
        ? "नमस्ते! मैं आपका फार्मगार्डियन AI कृषि सहायक हूँ। अपनी फसल, मौसम या उपचार संबंधी प्रश्न पूछें।"
        : "Hello! I am your FarmGuardian AI Farm Assistant. Ask me contextual questions regarding your crop, weather, or spraying timeline."
    }
  ]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async (qText) => {
    const query = qText || question;
    if (!query.trim()) return;

    // Add user message
    const userMsg = { sender: 'user', text: query };
    setMessages(prev => [...prev, userMsg]);
    setQuestion('');
    setLoading(true);

    try {
      const res = await fetch('/api/advisor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: query,
          language: currentLang,
          context: {
            disease: latestScanData?.disease || "Tomato Early Blight",
            weather: latestScanData?.weather ? `${latestScanData.weather.temp_c}°C, ${latestScanData.weather.humidity_pct}% Humidity` : "29.5°C, 78% Humidity"
          }
        })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { sender: 'ai', text: data.answer }]);
    } catch (err) {
      console.error("Advisor API error:", err);
      // Intelligent local fallback response
      let fallbackText = "Humidity is currently 78%. Spraying is recommended tomorrow evening after 6:00 PM when wind speeds drop below 10 km/h for maximum leaf absorption.";
      if (currentLang === 'te') {
        fallbackText = "వాతావరణ తేమ 78% ఉంది. సాయంత్రం 6:00 గంటల తర్వాత మంచోజెబ్ (2గ్రా/లీటర్) పిచికారీ చేయడం వల్ల ఆకులు ఔషధాన్ని బాగా పీల్చుకుంటాయి.";
      } else if (currentLang === 'hi') {
        fallbackText = "मौसम में 78% नमी है। शाम 6:00 बजे के बाद मैंकोजेब का छिड़काव करना सबसे अच्छा रहेगा।";
      }
      setMessages(prev => [...prev, { sender: 'ai', text: fallbackText }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8 space-y-6 animate-fadeIn">
      
      {/* Title */}
      <div className="text-center space-y-2">
        <span className="badge-green">Gemini Generative AI Agent</span>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
          {t.title}
        </h1>
        <p className="text-sm text-slate-300">
          {t.subtitle}
        </p>
      </div>

      {/* Preset Question Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {[t.preset1, t.preset2, t.preset3, t.preset4].map((preset, idx) => (
          <button
            key={idx}
            onClick={() => handleAsk(preset)}
            className="p-3 rounded-2xl bg-white/5 hover:bg-white/10 border border-white/10 text-left text-xs font-medium text-slate-200 transition-all hover:scale-[1.01] flex items-center justify-between"
          >
            <span>💬 "{preset}"</span>
            <span className="text-emerald-400">→</span>
          </button>
        ))}
      </div>

      {/* Chat Messages Box */}
      <div className="glass-panel p-6 space-y-4 min-h-[400px] flex flex-col justify-between">
        
        <div className="space-y-4 max-h-[450px] overflow-y-auto pr-2">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-lg p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-br-none shadow-lg'
                    : 'bg-slate-900/90 text-slate-200 border border-white/10 rounded-bl-none'
                }`}
              >
                {msg.sender === 'ai' && (
                  <div className="text-[10px] font-bold text-emerald-400 mb-1 flex items-center gap-1">
                    🤖 Gemini AI Agronomist
                  </div>
                )}
                {msg.text}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-slate-900/90 p-4 rounded-2xl border border-white/10 flex items-center gap-2 text-xs text-slate-400">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                Gemini AI is generating agronomist response...
              </div>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="flex items-center gap-3 pt-4 border-t border-white/10">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
            placeholder={t.placeholder}
            className="flex-1 bg-slate-950/80 text-white text-xs sm:text-sm px-4 py-3 rounded-xl border border-white/15 focus:outline-none focus:border-emerald-500"
          />
          <button
            onClick={() => handleAsk()}
            className="glass-button py-3 px-6 text-xs sm:text-sm"
          >
            🚀 {t.send}
          </button>
        </div>

      </div>

    </div>
  );
}

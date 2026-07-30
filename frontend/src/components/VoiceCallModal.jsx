import React, { useState, useEffect } from 'react';
import { translations } from '../i18n/translations';

export default function VoiceCallModal({ isOpen, onClose, scanData, currentLang }) {
  const t = translations[currentLang]?.voice || translations.en.voice;
  const [callState, setCallState] = useState('connecting'); // 'connecting', 'active', 'ended'
  const [timer, setTimer] = useState(0);
  const [callResult, setCallResult] = useState(null);
  const [reminderMsg, setReminderMsg] = useState('');

  useEffect(() => {
    if (!isOpen) {
      setCallState('connecting');
      setTimer(0);
      setCallResult(null);
      setReminderMsg('');
      return;
    }

    // Trigger backend OmniDimension Voice API call
    const payload = {
      scan_data: scanData || {
        disease_predicted: "Tomato Early Blight",
        confidence: 0.88,
        severity_level: "Medium Risk",
        weather_summary: "29.5°C, 78% Humidity",
        day_2_plan: "Apply Copper Oxychloride spray tomorrow evening",
        estimated_savings_inr: 18500.0
      },
      farmer_phone: "+91 9876543210"
    };

    fetch('/api/voice/call', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(res => res.json())
      .then(data => {
        setCallResult(data);
        setCallState('active');
      })
      .catch(err => {
        console.error("Voice API call error:", err);
        setCallState('active');
      });
  }, [isOpen, scanData]);

  // Call timer interval
  useEffect(() => {
    let interval = null;
    if (isOpen && callState === 'active') {
      interval = setInterval(() => {
        setTimer(prev => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isOpen, callState]);

  if (!isOpen) return null;

  const formatTime = (sec) => {
    const mins = Math.floor(sec / 60);
    const secs = sec % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleEndCall = () => {
    setCallState('ended');
  };

  const handleScheduleReminder = () => {
    setReminderMsg(t.reminderSuccess);
    setTimeout(() => setReminderMsg(''), 4000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
      <div className="glass-panel w-full max-w-2xl overflow-hidden border-emerald-500/30 shadow-2xl shadow-emerald-950/50">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-emerald-900/60 via-slate-900/80 to-slate-900 p-5 border-b border-white/10 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-emerald-500/20 border border-emerald-400/30 flex items-center justify-center text-emerald-400 text-lg animate-pulse">
              🎙️
            </div>
            <div>
              <h3 className="text-lg font-bold text-white tracking-wide">{t.title}</h3>
              <p className="text-xs text-emerald-400 font-medium">OmniDimension AI Direct Line • +91 9876543210</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 text-slate-300 flex items-center justify-center transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-6 max-h-[75vh] overflow-y-auto">

          {/* Active Call Animated Status */}
          {callState === 'connecting' && (
            <div className="text-center py-10 space-y-4">
              <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-emerald-500/10 border-2 border-emerald-500/40 text-3xl animate-bounce">
                📞
              </div>
              <p className="text-base font-semibold text-slate-200">{t.calling}</p>
              <p className="text-xs text-slate-400">Connecting via OmniDimension Telephony Pipeline...</p>
            </div>
          )}

          {callState === 'active' && (
            <div className="space-y-5">
              
              {/* Waveform & Duration */}
              <div className="bg-slate-900/90 rounded-2xl p-4 border border-emerald-500/20 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex items-center gap-1.5 h-8">
                    <div className="wave-bar" style={{ animationDelay: '0.1s' }} />
                    <div className="wave-bar" style={{ animationDelay: '0.3s' }} />
                    <div className="wave-bar" style={{ animationDelay: '0.5s' }} />
                    <div className="wave-bar" style={{ animationDelay: '0.2s' }} />
                    <div className="wave-bar" style={{ animationDelay: '0.4s' }} />
                  </div>
                  <span className="text-sm font-semibold text-emerald-400">{t.activeCall}</span>
                </div>
                <div className="text-lg font-mono font-bold text-white bg-white/5 px-3 py-1 rounded-xl border border-white/10">
                  ⏱️ {formatTime(timer)}
                </div>
              </div>

              {/* Live Transcript Box */}
              <div>
                <h4 className="text-xs font-bold uppercase text-slate-400 tracking-wider mb-2">
                  📜 {t.transcript}
                </h4>
                <div className="bg-slate-950/80 rounded-2xl p-4 border border-white/10 space-y-3 font-mono text-xs text-slate-300 max-h-56 overflow-y-auto leading-relaxed">
                  {callResult?.transcript ? (
                    callResult.transcript.split('\n').map((line, idx) => (
                      <p
                        key={idx}
                        className={line.includes('AI Voice:') ? 'text-emerald-300' : 'text-slate-100 font-semibold'}
                      >
                        {line}
                      </p>
                    ))
                  ) : (
                    <p className="text-slate-400 italic">Streaming live speech synthesis...</p>
                  )}
                </div>
              </div>

              {/* End Call Button */}
              <div className="flex justify-end">
                <button
                  onClick={handleEndCall}
                  className="bg-rose-600 hover:bg-rose-500 text-white font-bold py-2.5 px-6 rounded-xl text-sm shadow-lg shadow-rose-600/30 transition-all flex items-center gap-2"
                >
                  🔴 {t.endCall}
                </button>
              </div>
            </div>
          )}

          {callState === 'ended' && (
            <div className="space-y-5 animate-fadeIn">
              
              <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center gap-3">
                <span className="text-2xl">✅</span>
                <div>
                  <h4 className="text-sm font-bold text-emerald-400">Voice Call Completed & Logged</h4>
                  <p className="text-xs text-slate-300">Duration: {formatTime(timer > 0 ? timer : 78)} • Saved to Farm History Database</p>
                </div>
              </div>

              {/* AI Summary Card */}
              <div className="bg-slate-900/90 rounded-2xl p-4 border border-white/10 space-y-2">
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                  📋 {t.callSummary}
                </h4>
                <p className="text-xs text-slate-200 leading-relaxed">
                  {callResult?.ai_summary || "Call completed. Farmer briefed on disease treatment timeline & weather-aware spraying schedule."}
                </p>
              </div>

              {/* Schedule Reminder Action */}
              <div className="bg-white/5 rounded-2xl p-4 border border-white/10 flex items-center justify-between">
                <div>
                  <h5 className="text-xs font-bold text-white">Automated Treatment Reminder</h5>
                  <p className="text-[11px] text-slate-400">Schedule SMS & Voice ping for Day 2 spray (Tomorrow 5:30 PM)</p>
                </div>
                <button
                  onClick={handleScheduleReminder}
                  className="glass-button text-xs py-2 px-3"
                >
                  ⏰ {t.scheduleReminder}
                </button>
              </div>

              {reminderMsg && (
                <div className="p-3 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-semibold text-center animate-bounce">
                  ✨ {reminderMsg}
                </div>
              )}

              <div className="flex justify-end pt-2">
                <button onClick={onClose} className="glass-button-secondary text-xs">
                  Close Window
                </button>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}

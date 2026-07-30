import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { translations } from '../i18n/translations';

export default function Navbar({ currentLang, setLanguage, onOpenVoiceModal }) {
  const location = useLocation();
  const t = translations[currentLang]?.nav || translations.en.nav;

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="sticky top-0 z-50 backdrop-blur-md bg-[#0a0f1d]/80 border-b border-white/10 px-4 lg:px-8 py-3 transition-all">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 p-0.5 shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
            <div className="w-full h-full bg-[#0a0f1d] rounded-[10px] flex items-center justify-center">
              <span className="text-emerald-400 font-bold text-xl">🌱</span>
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-100 to-slate-400">
                FarmGuardian
              </span>
              <span className="bg-emerald-500/10 text-emerald-400 text-[10px] font-bold px-2 py-0.5 rounded-full border border-emerald-500/20">
                AI PRO 2.0
              </span>
            </div>
            <p className="text-[11px] text-slate-400 -mt-1 hidden sm:block">
              {translations[currentLang]?.tagline || "Commercial Farm Intelligence Platform"}
            </p>
          </div>
        </Link>

        {/* Navigation Links */}
        <div className="hidden md:flex items-center gap-1 bg-white/5 p-1.5 rounded-2xl border border-white/10">
          <Link
            to="/dashboard"
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
              isActive('/dashboard') || isActive('/')
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shadow-sm'
                : 'text-slate-300 hover:text-white hover:bg-white/5'
            }`}
          >
            📊 {t.dashboard}
          </Link>
          <Link
            to="/detect"
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
              isActive('/detect')
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shadow-sm'
                : 'text-slate-300 hover:text-white hover:bg-white/5'
            }`}
          >
            🔬 {t.detection}
          </Link>
          <Link
            to="/advisor"
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
              isActive('/advisor')
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shadow-sm'
                : 'text-slate-300 hover:text-white hover:bg-white/5'
            }`}
          >
            🤖 {t.advisor}
          </Link>
          <Link
            to="/weather"
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
              isActive('/weather')
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shadow-sm'
                : 'text-slate-300 hover:text-white hover:bg-white/5'
            }`}
          >
            🌤️ {t.weather}
          </Link>
          <Link
            to="/history"
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
              isActive('/history')
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shadow-sm'
                : 'text-slate-300 hover:text-white hover:bg-white/5'
            }`}
          >
            📜 {t.history}
          </Link>
        </div>

        {/* Right Controls: Multi-Language & Voice Call Button */}
        <div className="flex items-center gap-3">
          
          {/* Language Selector Selector */}
          <div className="relative">
            <select
              value={currentLang}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-slate-800/90 text-slate-200 text-xs font-semibold px-3 py-2 rounded-xl border border-white/15 focus:outline-none focus:border-emerald-500 cursor-pointer shadow-inner"
            >
              <option value="en">🌐 EN (English)</option>
              <option value="te">🇮🇳 TE (తెలుగు)</option>
              <option value="hi">🇮🇳 HI (हिन्दी)</option>
            </select>
          </div>

          {/* CALL FARMER Shortcut */}
          <button
            onClick={onOpenVoiceModal}
            className="glass-button text-xs py-2 px-3 sm:px-4 flex items-center gap-2 shadow-emerald-500/20 animate-pulse"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-300 animate-ping" />
            <span>📞 {t.callFarmer}</span>
          </button>

        </div>
      </div>
    </nav>
  );
}

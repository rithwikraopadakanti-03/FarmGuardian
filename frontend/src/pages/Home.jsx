import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { Leaf, ShieldCheck, TrendingUp, BookOpen, Search, ArrowRight, Activity, Globe } from 'lucide-react';
import { LanguageContext } from '../context/LanguageContext';

const Home = () => {
  const { t } = useContext(LanguageContext);

  const features = [
    { icon: <Search size={24} className="text-green-400" />, title: t('home.features.disease_detection'), desc: t('home.features.disease_detection_desc') },
    { icon: <Activity size={24} className="text-blue-400" />, title: t('home.features.severity_assessment'), desc: t('home.features.severity_assessment_desc') },
    { icon: <TrendingUp size={24} className="text-yellow-400" />, title: t('home.features.yield_prediction'), desc: t('home.features.yield_prediction_desc') },
    { icon: <ShieldCheck size={24} className="text-purple-400" />, title: t('home.features.treatment_advice'), desc: t('home.features.treatment_advice_desc') },
    { icon: <BookOpen size={24} className="text-orange-400" />, title: t('home.features.field_reports'), desc: t('home.features.field_reports_desc') },
    { icon: <Globe size={24} className="text-teal-400" />, title: t('home.features.multilingual'), desc: t('home.features.multilingual_desc') }
  ];

  return (
    <div className="min-h-screen relative overflow-hidden flex flex-col">
      {/* Background Decorative Elements */}
      <div className="hero-bg-circle bg-green-500/20 w-96 h-96 -top-20 -left-20 animate-pulse-glow"></div>
      <div className="hero-bg-circle bg-blue-500/20 w-96 h-96 top-40 -right-20"></div>
      
      {/* Navbar (Simplified for Home) */}
      <nav className="relative z-10 flex items-center justify-between p-6 lg:px-12">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center text-white shadow-lg">
            <Leaf size={24} />
          </div>
          <span className="text-2xl font-bold font-heading text-white">
            Farm<span className="text-green-400">Guardian</span>
          </span>
        </div>
        <div className="flex gap-4">
          <Link to="/login" className="btn-secondary"><span>{t('nav.login')}</span></Link>
          <Link to="/register" className="btn-primary"><span>{t('nav.register')}</span></Link>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative z-10 flex-1 flex flex-col items-center justify-center text-center px-4 sm:px-6 lg:px-8 mt-12 mb-20 animate-fade-in-up">
        <h1 className="text-5xl md:text-7xl font-bold font-heading mb-6 tracking-tight leading-tight">
          {t('home.hero_title').split('AI')[0]} <span className="gradient-text">AI</span>
        </h1>
        <p className="text-lg md:text-xl text-slate-300 max-w-2xl mb-10 leading-relaxed">
          {t('home.hero_subtitle')}
        </p>
        <div className="flex flex-col sm:flex-row gap-4">
          <Link to="/login" className="btn-primary px-8 py-4 text-lg group">
            <span>{t('home.cta_detect')}</span>
            <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
          </Link>
          <a href="#features" className="btn-secondary px-8 py-4 text-lg">
            <span>{t('home.cta_learn')}</span>
          </a>
        </div>
      </div>

      {/* Stats Section */}
      <div className="relative z-10 bg-slate-900/50 border-y border-slate-700/50 py-12 mb-24">
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div className="px-4 animate-fade-in-up delay-100">
            <div className="text-3xl font-bold text-green-400 mb-2">96%+</div>
            <div className="text-sm text-slate-400 uppercase tracking-wider">{t('home.stats.accuracy')}</div>
          </div>
          <div className="px-4 animate-fade-in-up delay-200">
            <div className="text-3xl font-bold text-blue-400 mb-2">38</div>
            <div className="text-sm text-slate-400 uppercase tracking-wider">{t('home.stats.diseases')}</div>
          </div>
          <div className="px-4 animate-fade-in-up delay-300">
            <div className="text-3xl font-bold text-yellow-400 mb-2">3</div>
            <div className="text-sm text-slate-400 uppercase tracking-wider">{t('home.stats.languages')}</div>
          </div>
          <div className="px-4 animate-fade-in-up delay-400">
            <div className="text-3xl font-bold text-purple-400 mb-2">24/7</div>
            <div className="text-sm text-slate-400 uppercase tracking-wider">{t('home.stats.farmers')}</div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div id="features" className="relative z-10 max-w-7xl mx-auto px-4 pb-24">
        <div className="text-center mb-16 animate-fade-in-up">
          <h2 className="text-4xl font-bold font-heading mb-4">{t('home.features.title')}</h2>
          <p className="text-slate-400 max-w-2xl mx-auto">{t('home.features.subtitle')}</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, idx) => (
            <div key={idx} className="glass-card p-8 animate-fade-in-up delay-100">
              <div className="w-12 h-12 rounded-lg bg-slate-800/50 border border-slate-700 flex items-center justify-center mb-6">
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold font-heading mb-3">{feature.title}</h3>
              <p className="text-slate-400 leading-relaxed">{feature.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;

import React, { useState, useContext, useEffect } from 'react';
import { Activity, ShieldAlert, Sprout, FolderArchive, Search } from 'lucide-react';
import { Link } from 'react-router-dom';
import { LanguageContext } from '../context/LanguageContext';
import { AuthContext } from '../context/AuthContext';

const Dashboard = () => {
  const { t } = useContext(LanguageContext);
  const { user } = useContext(AuthContext);
  const [scanHistory, setScanHistory] = useState([]);

  // Load scan history from localStorage
  useEffect(() => {
    try {
      const saved = localStorage.getItem('farmguardian_scans');
      if (saved) {
        setScanHistory(JSON.parse(saved));
      }
    } catch (e) {
      console.error('Failed to load scan history', e);
    }
  }, []);

  const totalScans = scanHistory.length;
  const healthyScans = scanHistory.filter(s => s.disease?.toLowerCase().includes('healthy')).length;
  const diseasedScans = totalScans - healthyScans;
  const highRiskScans = scanHistory.filter(s => s.risk_level === 'High').length;

  const stats = [
    { title: t('dashboard.total_scans'), value: totalScans.toString(), icon: <FolderArchive className="text-blue-400" />, cls: 'stat-card-blue' },
    { title: t('dashboard.healthy_plants'), value: healthyScans.toString(), icon: <Sprout className="text-green-400" />, cls: 'stat-card-green' },
    { title: t('dashboard.diseased_plants'), value: diseasedScans.toString(), icon: <Activity className="text-yellow-400" />, cls: 'stat-card-yellow' },
    { title: t('dashboard.risk_alerts'), value: highRiskScans.toString(), icon: <ShieldAlert className="text-red-400" />, cls: 'stat-card-red' },
  ];

  return (
    <div className="space-y-8 animate-fade-in-up">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold font-heading">{t('dashboard.title')}</h1>
          <p className="text-slate-400 mt-1">{t('dashboard.welcome')}{user?.isGuest ? ' Guest' : ''}</p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, idx) => (
          <div key={idx} className={`glass p-6 rounded-2xl flex items-center justify-between ${stat.cls}`}>
            <div>
              <div className="text-sm text-slate-400 uppercase tracking-wider mb-2">{stat.title}</div>
              <div className="text-3xl font-bold">{stat.value}</div>
            </div>
            <div className="w-12 h-12 rounded-xl bg-slate-800/50 flex items-center justify-center border border-slate-700">
              {stat.icon}
            </div>
          </div>
        ))}
      </div>

      {/* Empty State or Recent Scans */}
      {totalScans === 0 ? (
        <div className="glass-card p-12 text-center">
          <div className="w-20 h-20 rounded-full bg-green-500/10 flex items-center justify-center text-green-400 mx-auto mb-6">
            <Search size={36} />
          </div>
          <h3 className="text-2xl font-bold font-heading mb-3">{t('dashboard.no_scans')}</h3>
          <p className="text-slate-400 mb-8 max-w-md mx-auto">
            Upload a leaf image on the Disease Detection page to get started with your first analysis.
          </p>
          <Link to="/detect" className="btn-primary px-8 py-3">
            <span>{t('nav.detect')}</span>
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Recent Scans List */}
          <div className="glass-card p-6">
            <h3 className="text-lg font-semibold mb-4">{t('dashboard.recent_scans')}</h3>
            <div className="space-y-3">
              {scanHistory.slice(-10).reverse().map((scan, idx) => (
                <div key={idx} className="flex justify-between items-center p-4 glass rounded-xl">
                  <div>
                    <div className="font-medium">{scan.disease?.replace(/_/g, ' ')}</div>
                    <div className="text-sm text-slate-400">
                      {t('detection.confidence')}: {(scan.confidence * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    {scan.severity_level && scan.severity_level !== 'Healthy' && (
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        scan.risk_level === 'High' ? 'bg-red-500/20 text-red-400' :
                        scan.risk_level === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                        'bg-green-500/20 text-green-400'
                      }`}>
                        {scan.severity_level}
                      </span>
                    )}
                    {scan.disease?.toLowerCase().includes('healthy') && (
                      <span className="px-3 py-1 rounded-full text-xs font-semibold bg-green-500/20 text-green-400">
                        {t('common.healthy')}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;

import React, { useContext } from 'react';
import { AlertTriangle, CheckCircle, Info, ShieldAlert, Sprout } from 'lucide-react';
import { LanguageContext } from '../context/LanguageContext';

const PredictionCard = ({ result }) => {
  const { t } = useContext(LanguageContext);

  if (!result) return null;

  const isHealthy = result.disease.toLowerCase().includes('healthy');
  
  const getSeverityClass = (level) => {
    switch(level) {
      case 'Mild': return 'severity-mild';
      case 'Moderate': return 'severity-moderate';
      case 'Severe': return 'severity-severe';
      default: return 'bg-green-500/20 text-green-400 border-green-500/30';
    }
  };

  const getRiskClass = (level) => {
    switch(level) {
      case 'Low': return 'risk-low';
      case 'Medium': return 'risk-medium';
      case 'High': return 'risk-high';
      default: return 'risk-low';
    }
  };

  const confidencePercent = (result.confidence * 100).toFixed(1);

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* Main Result */}
      <div className={`glass-card p-6 border ${isHealthy ? 'border-green-500/30' : 'border-red-500/30'}`}>
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2">
              {isHealthy ? <CheckCircle className="text-green-400" /> : <AlertTriangle className="text-red-400" />}
              <span className="text-sm font-semibold tracking-wider uppercase text-slate-400">
                {t('detection.results_title')}
              </span>
            </div>
            <h2 className="text-2xl font-bold font-heading mb-1">
              {result.disease.replace(/_/g, ' ').replace('___', ' - ')}
            </h2>
          </div>
          
          <div className="text-right">
            <div className="text-3xl font-bold gradient-text">{confidencePercent}%</div>
            <div className="text-sm text-slate-400">{t('detection.confidence')}</div>
          </div>
        </div>

        {/* Confidence Bar */}
        <div className="mt-6">
          <div className="progress-bar">
            <div 
              className="progress-fill bg-gradient-to-r from-green-500 to-green-300" 
              style={{ width: `${confidencePercent}%` }}
            ></div>
          </div>
        </div>
      </div>

      {!isHealthy && (
        <>
          {/* Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className={`glass p-4 text-center rounded-xl border ${getSeverityClass(result.severity_level)}`}>
              <div className="text-sm uppercase tracking-wider mb-1 opacity-80">{t('detection.severity')}</div>
              <div className="text-xl font-bold">{result.severity_level} ({result.severity_score}%)</div>
            </div>
            
            <div className={`glass p-4 text-center rounded-xl border ${getRiskClass(result.risk_level)}`}>
              <div className="flex items-center justify-center gap-2 text-sm uppercase tracking-wider mb-1 opacity-80">
                <ShieldAlert size={16} /> {t('detection.risk_level')}
              </div>
              <div className="text-xl font-bold">{result.risk_level}</div>
            </div>
            
            <div className="glass p-4 text-center rounded-xl border border-yellow-500/30 text-yellow-400 bg-yellow-500/10">
              <div className="text-sm uppercase tracking-wider mb-1 opacity-80">{t('detection.yield_loss')}</div>
              <div className="text-xl font-bold">{result.yield_loss_range}</div>
            </div>
          </div>

          {/* Recommendations */}
          {result.recommendations && (
            <div className="glass-card p-6">
              <h3 className="text-lg font-bold font-heading mb-4 flex items-center gap-2">
                <Info className="text-blue-400" />
                {t('detection.recommendations')}
              </h3>
              
              <div className="space-y-6">
                {result.recommendations.immediate_actions && (
                  <div>
                    <h4 className="text-red-400 font-semibold mb-2">{t('detection.immediate_actions')}</h4>
                    <ul className="list-disc list-inside text-slate-300 space-y-1">
                      {result.recommendations.immediate_actions.map((act, i) => <li key={i}>{act}</li>)}
                    </ul>
                  </div>
                )}
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {result.recommendations.organic_treatments && (
                    <div>
                      <h4 className="text-green-400 font-semibold mb-2 flex items-center gap-2">
                        <Sprout size={16} /> {t('detection.organic_treatments')}
                      </h4>
                      <ul className="list-disc list-inside text-slate-300 space-y-1">
                        {result.recommendations.organic_treatments.map((act, i) => <li key={i}>{act}</li>)}
                      </ul>
                    </div>
                  )}
                  
                  {result.recommendations.chemical_treatments && (
                    <div>
                      <h4 className="text-blue-400 font-semibold mb-2">{t('detection.chemical_treatments')}</h4>
                      <ul className="list-disc list-inside text-slate-300 space-y-1">
                        {result.recommendations.chemical_treatments.map((act, i) => <li key={i}>{act}</li>)}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </>
      )}

      {isHealthy && (
        <div className="glass-card p-6 text-center border-green-500/30 bg-green-500/5">
          <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center text-green-400 mx-auto mb-4">
            <Sprout size={32} />
          </div>
          <h3 className="text-xl font-bold text-green-400 mb-2">Great news!</h3>
          <p className="text-slate-300">No diseases detected. Your crop appears to be healthy.</p>
        </div>
      )}
    </div>
  );
};

export default PredictionCard;

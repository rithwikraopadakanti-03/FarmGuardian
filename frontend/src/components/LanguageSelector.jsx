import React, { useContext } from 'react';
import { LanguageContext } from '../context/LanguageContext';
import { Globe } from 'lucide-react';

const LanguageSelector = () => {
  const { language, changeLanguage, t } = useContext(LanguageContext);

  const languages = [
    { code: 'en', label: 'English' },
    { code: 'te', label: 'తెలుగు (Telugu)' },
    { code: 'hi', label: 'हिंदी (Hindi)' }
  ];

  return (
    <div className="glass-light p-6">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 rounded-lg bg-blue-500/20 text-blue-400">
          <Globe size={24} />
        </div>
        <h3 className="text-lg font-semibold">{t('settings.select_language')}</h3>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {languages.map((lang) => (
          <button
            key={lang.code}
            onClick={() => changeLanguage(lang.code)}
            className={`p-4 rounded-xl border transition-all duration-300 text-left ${
              language === lang.code
                ? 'bg-green-500/20 border-green-500/50 text-white'
                : 'bg-slate-800/50 border-slate-700 hover:border-slate-500 text-slate-300'
            }`}
          >
            <span className="font-medium text-lg">{lang.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default LanguageSelector;

import React, { createContext, useState, useEffect } from 'react';
import enTranslations from '../i18n/en.json';
import teTranslations from '../i18n/te.json';
import hiTranslations from '../i18n/hi.json';

export const LanguageContext = createContext(null);

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(localStorage.getItem('language') || 'en');
  const [translations, setTranslations] = useState(enTranslations);

  useEffect(() => {
    localStorage.setItem('language', language);
    switch (language) {
      case 'te':
        setTranslations(teTranslations);
        break;
      case 'hi':
        setTranslations(hiTranslations);
        break;
      case 'en':
      default:
        setTranslations(enTranslations);
        break;
    }
  }, [language]);

  const changeLanguage = (lang) => {
    setLanguage(lang);
  };

  // Helper to get nested translation value
  const t = (keyString) => {
    const keys = keyString.split('.');
    let result = translations;
    for (const key of keys) {
      if (result && result[key] !== undefined) {
        result = result[key];
      } else {
        return keyString; // Fallback to key if not found
      }
    }
    return result;
  };

  return (
    <LanguageContext.Provider value={{ language, changeLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

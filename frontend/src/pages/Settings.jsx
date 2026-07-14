import React, { useContext } from 'react';
import LanguageSelector from '../components/LanguageSelector';
import { LanguageContext } from '../context/LanguageContext';
import { AuthContext } from '../context/AuthContext';
import { User, Bell, Palette, Info } from 'lucide-react';

const Settings = () => {
  const { t } = useContext(LanguageContext);
  const { user } = useContext(AuthContext);

  return (
    <div className="max-w-3xl mx-auto space-y-8 animate-fade-in-up">
      <div>
        <h1 className="text-3xl font-bold font-heading mb-2">{t('settings.title')}</h1>
      </div>

      <div className="space-y-6">
        {/* Profile Section */}
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-6 pb-4 border-b border-slate-700/50">
            <User className="text-blue-400" size={24} />
            <h2 className="text-xl font-bold font-heading">{t('settings.profile')}</h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-slate-400 mb-1">Account Type</label>
              <div className="font-medium">
                {user?.isGuest ? 'Guest User' : 'Registered Farmer'}
              </div>
            </div>
            {!user?.isGuest && (
              <button className="btn-secondary text-sm">Update Profile Details</button>
            )}
          </div>
        </div>

        {/* Language Section */}
        <LanguageSelector />

        {/* Info Section */}
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-4">
            <Info className="text-purple-400" size={24} />
            <h2 className="text-xl font-bold font-heading">{t('settings.about')}</h2>
          </div>
          <p className="text-slate-400 mb-2">
            FarmGuardian AI is an intelligent crop disease detection platform built to help farmers protect their yields.
          </p>
          <div className="text-sm font-medium text-slate-500">
            {t('settings.version')}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;

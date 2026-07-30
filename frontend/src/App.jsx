import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import VoiceCallModal from './components/VoiceCallModal';

// Pages
import Dashboard from './pages/Dashboard';
import DiseaseDetection from './pages/DiseaseDetection';
import AIFarmAdvisor from './pages/AIFarmAdvisor';
import WeatherMap from './pages/WeatherMap';
import FarmHistory from './pages/FarmHistory';

const App = () => {
  const [currentLang, setLanguage] = useState('en');
  const [isVoiceModalOpen, setIsVoiceModalOpen] = useState(false);
  const [latestScanData, setLatestScanData] = useState(null);

  const handleOpenVoiceModal = () => setIsVoiceModalOpen(true);
  const handleCloseVoiceModal = () => setIsVoiceModalOpen(false);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#0a0f1d] text-slate-100 flex flex-col font-sans">
        
        {/* Startup Glassmorphism Navbar */}
        <Navbar
          currentLang={currentLang}
          setLanguage={setLanguage}
          onOpenVoiceModal={handleOpenVoiceModal}
        />

        {/* Main Content Workspace */}
        <main className="flex-1 py-4">
          <Routes>
            <Route
              path="/"
              element={
                <Dashboard
                  currentLang={currentLang}
                  onOpenVoiceModal={handleOpenVoiceModal}
                />
              }
            />
            <Route
              path="/dashboard"
              element={
                <Dashboard
                  currentLang={currentLang}
                  onOpenVoiceModal={handleOpenVoiceModal}
                />
              }
            />
            <Route
              path="/detect"
              element={
                <DiseaseDetection
                  currentLang={currentLang}
                  onOpenVoiceModal={handleOpenVoiceModal}
                  setLatestScanData={setLatestScanData}
                />
              }
            />
            <Route
              path="/advisor"
              element={
                <AIFarmAdvisor
                  currentLang={currentLang}
                  latestScanData={latestScanData}
                />
              }
            />
            <Route
              path="/weather"
              element={<WeatherMap />}
            />
            <Route
              path="/history"
              element={<FarmHistory />}
            />

            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </main>

        {/* Global Interactive OmniDimension Voice AI Call Portal Modal */}
        <VoiceCallModal
          isOpen={isVoiceModalOpen}
          onClose={handleCloseVoiceModal}
          scanData={latestScanData}
          currentLang={currentLang}
        />

        {/* Startup Footer */}
        <footer className="border-t border-white/10 py-6 text-center text-xs text-slate-400 bg-[#0a0f1d]/90">
          <p>© 2026 FarmGuardian AI Farm Intelligence Platform • Powered by MobileNetV2 ML, Gemini GenAI, OpenWeather & OmniDimension Voice AI</p>
        </footer>

      </div>
    </BrowserRouter>
  );
};

export default App;

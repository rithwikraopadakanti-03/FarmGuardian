import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { LanguageProvider } from './context/LanguageContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import DiseaseDetection from './pages/DiseaseDetection';
import FieldHealthReport from './pages/FieldHealthReport';
import Settings from './pages/Settings';

const AppLayout = ({ children }) => {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Sidebar />
      <main className="md:ml-64 pt-16 min-h-screen p-4 sm:p-6 lg:p-8">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
};

const App = () => {
  return (
    <BrowserRouter>
      <LanguageProvider>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <AppLayout><Dashboard /></AppLayout>
              </ProtectedRoute>
            } />
            <Route path="/detect" element={
              <ProtectedRoute>
                <AppLayout><DiseaseDetection /></AppLayout>
              </ProtectedRoute>
            } />
            <Route path="/report" element={
              <ProtectedRoute>
                <AppLayout><FieldHealthReport /></AppLayout>
              </ProtectedRoute>
            } />
            <Route path="/settings" element={
              <ProtectedRoute>
                <AppLayout><Settings /></AppLayout>
              </ProtectedRoute>
            } />
            
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </LanguageProvider>
    </BrowserRouter>
  );
};

export default App;

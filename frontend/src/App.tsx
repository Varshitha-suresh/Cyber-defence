import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { MainLayout } from './layouts/MainLayout';

// Pages
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { DashboardPage } from './pages/DashboardPage';
import { DeviceSecurityPage } from './pages/DeviceSecurityPage';
import { NetworkSecurityPage } from './pages/NetworkSecurityPage';
import { PhishingAnalyzerPage } from './pages/PhishingAnalyzerPage';
import { CredentialSecurityPage } from './pages/CredentialSecurityPage';
import { BehaviouralSecurityPage } from './pages/BehaviouralSecurityPage';
import { RecommendationsPage } from './pages/RecommendationsPage';
import { RiskHistoryPage } from './pages/RiskHistoryPage';
import { SecurityEventsPage } from './pages/SecurityEventsPage';
import { SettingsPage } from './pages/SettingsPage';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Landing & Auth */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected Application Routes */}
          <Route
            element={
              <ProtectedRoute>
                <MainLayout />
              </ProtectedRoute>
            }
          >
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/device" element={<DeviceSecurityPage />} />
            <Route path="/network" element={<NetworkSecurityPage />} />
            <Route path="/phishing" element={<PhishingAnalyzerPage />} />
            <Route path="/credentials" element={<CredentialSecurityPage />} />
            <Route path="/behaviour" element={<BehaviouralSecurityPage />} />
            <Route path="/recommendations" element={<RecommendationsPage />} />
            <Route path="/history" element={<RiskHistoryPage />} />
            <Route path="/events" element={<SecurityEventsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { NotificationProvider } from './context/NotificationContext';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import HomePage from './pages/HomePage';
import LoginRegisterPage from './pages/LoginRegisterPage';
import AuthCallback from './pages/AuthCallback';
import AdminDashboard from './pages/AdminDashboard';
import ProfilePage from './pages/ProfilePage';
import VerifyEmailPage from './pages/VerifyEmailPage'; // <-- استيراد جديد
import AccountActivatedPage from './pages/AccountActivatedPage'; // <-- استيراد جديد

function App() {
  return (
    <NotificationProvider>
      <div className="bg-gray-50 min-h-screen">
        <Navbar />
        <main className="py-8">
          <Routes>
            {/* --- مسارات عامة --- */}
            <Route path="/login" element={<LoginRegisterPage />} />
            <Route path="/auth/callback" element={<AuthCallback />} />
            <Route path="/verify-email" element={<VerifyEmailPage />} />
            <Route path="/activate/:token" element={<AccountActivatedPage />} />

            {/* --- مسارات محمية --- */}
            <Route
              path="/"
              element={
                <ProtectedRoute allowedRoles={['user', 'admin', 'manager']}>
                  <HomePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute allowedRoles={['admin', 'manager']}>
                  <AdminDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute allowedRoles={['user', 'admin', 'manager']}>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </main>
      </div>
    </NotificationProvider>
  );
}

export default App;
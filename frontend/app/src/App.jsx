import React, { useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import HomePage from './pages/HomePage';
import LoginRegisterPage from './pages/LoginRegisterPage';
import AuthCallback from './pages/AuthCallback';
import AdminDashboard from './pages/AdminDashboard';
import ProfilePage from './pages/ProfilePage';
import VerifyEmailPage from './pages/VerifyEmailPage';
import AccountActivatedPage from './pages/AccountActivatedPage';

function App() {
  const navigate = useNavigate();

  useEffect(() => {
    const redirectPath = sessionStorage.getItem('redirect');
    if (redirectPath) {
      sessionStorage.removeItem('redirect');
      // قم بإزالة المسار الأساسي قبل التوجيه
      const path = redirectPath.replace('/restaurant-management', '');
      navigate(path, { replace: true });
    }
  }, [navigate]);

  return (
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
  );
}

export default App;
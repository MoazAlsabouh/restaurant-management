import React from 'react';
import { Navigate } from 'react-router-dom';

// دالة بسيطة لفك تشفير التوكن (JWT)
const decodeToken = (token) => {
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch {
        return null;
    }
};

const ProtectedRoute = ({ children, allowedRoles }) => {
    const token = localStorage.getItem('authToken');

    if (!token) {
        // إذا لم يكن هناك توكن، أعده لصفحة التسجيل
        return <Navigate to="/login" replace />;
    }

    const userData = decodeToken(token);

    if (!userData || !allowedRoles.includes(userData.role)) {
        // إذا كان الدور غير مسموح به، أعده للصفحة الرئيسية
        return <Navigate to="/" replace />;
    }

    return children;
};

export default ProtectedRoute;

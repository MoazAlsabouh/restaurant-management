import { useState, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import { useNotification } from '../context/NotificationContext';

// قراءة رابط الخادم الخلفي من متغيرات البيئة
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

const useApi = () => {
    const [loading, setLoading] = useState(false);
    const { showNotification } = useNotification();
    const location = useLocation();

    const request = useCallback(async (url, method = 'GET', body = null, showError = true) => {
        setLoading(true);

        // بناء الرابط الكامل
        const fullUrl = `${API_BASE_URL}${url}`;

        const token = localStorage.getItem('authToken');
        const headers = { 'Content-Type': 'application/json' };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const options = { method, headers };
        if (body) {
            options.body = JSON.stringify(body);
        }

        try {
            const response = await fetch(fullUrl, options); // استخدام الرابط الكامل
            const data = await response.json();

            if (!response.ok) {
                if (response.status === 401 && location.pathname !== '/login') {
                    localStorage.removeItem('authToken');
                    window.location.href = '/login';
                    throw new Error('انتهت صلاحية الجلسة. الرجاء تسجيل الدخول مرة أخرى.');
                }
                throw new Error(data.error || data.message || 'حدث خطأ ما.');
            }

            return data;
        } catch (err) {
            if (showError && err.message !== 'انتهت صلاحية الجلسة. الرجاء تسجيل الدخول مرة أخرى.') {
                 showNotification(err.message, 'error');
            }
            throw err;
        } finally {
            setLoading(false);
        }
    }, [showNotification, location.pathname]);

    return { loading, request };
};

export default useApi;
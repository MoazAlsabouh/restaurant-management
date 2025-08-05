import { useState, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import { useNotification } from '../context/NotificationContext';

const useApi = () => {
    const [loading, setLoading] = useState(false);
    const { showNotification } = useNotification();
    const location = useLocation();

    const request = useCallback(async (url, method = 'GET', body = null) => {
        setLoading(true);

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
            const response = await fetch(url, options);

            if (!response.ok) {
                if (response.status === 401 && location.pathname !== '/login') {
                    localStorage.removeItem('authToken');
                    window.location.href = '/login';
                    throw new Error('انتهت صلاحية الجلسة. الرجاء تسجيل الدخول مرة أخرى.');
                }
                const data = await response.json();
                throw new Error(data.error || data.message || 'حدث خطأ ما.');
            }

            if (response.status === 204) {
                return null;
            }

            return await response.json();
        } catch (err) {
            if (err.message !== 'انتهت صلاحية الجلسة. الرجاء تسجيل الدخول مرة أخرى.') {
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
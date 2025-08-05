import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import useApi from '../hooks/useApi';
import { useNotification } from '../context/NotificationContext';

export default function VerifyEmailPage() {
    const navigate = useNavigate();
    const location = useLocation();
    const { loading, request } = useApi();
    const { showNotification } = useNotification();
    const [formData, setFormData] = useState({
        email: location.state?.email || '',
        code: ''
    });

    useEffect(() => {
        if (location.state?.email) {
            setFormData(prev => ({ ...prev, email: location.state.email }));
        }
    }, [location.state]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = await request('/api/v1/auth/verify-email', 'POST', formData);
            showNotification(data.message || 'تم التحقق بنجاح! يمكنك الآن تسجيل الدخول.');
            navigate('/login');
        } catch (err) { /* ... */ }
    };

    return (
        <div className="bg-gray-100 flex items-center justify-center min-h-screen font-sans py-12" dir="rtl">
            <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-xl shadow-lg">
                <div className="text-center">
                    <h1 className="text-3xl font-bold text-gray-800">التحقق من البريد الإلكتروني</h1>
                    <p className="text-gray-500 mt-2">لقد أرسلنا رمزًا إلى بريدك الإلكتروني. الرجاء إدخاله أدناه.</p>
                </div>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-700">البريد الإلكتروني</label>
                        <input type="email" id="email" name="email" value={formData.email} onChange={handleInputChange} required className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
                    </div>
                    <div>
                        <label htmlFor="code" className="block text-sm font-medium text-gray-700">رمز التحقق</label>
                        <input type="text" id="code" name="code" value={formData.code} onChange={handleInputChange} required className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
                    </div>
                    <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700">
                        {loading ? 'جاري التحقق...' : 'تحقق'}
                    </button>
                </form>
            </div>
        </div>
    );
}
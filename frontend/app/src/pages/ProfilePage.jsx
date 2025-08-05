import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import useApi from '../hooks/useApi';
import { useNotification } from '../context/NotificationContext';

export default function ProfilePage() {
    const navigate = useNavigate();
    const { loading, request } = useApi();
    const { showNotification } = useNotification();
    const [user, setUser] = useState(null);
    const [infoData, setInfoData] = useState({ full_name: '', email: '', username: '' });
    const [passwordData, setPasswordData] = useState({ old_password: '', new_password: '' });
    const [usernameError, setUsernameError] = useState('');

    const fetchProfile = useCallback(async () => {
        try {
            const data = await request('/api/v1/profile/');
            setUser(data.user);
            setInfoData({ full_name: data.user.full_name, email: data.user.email, username: data.user.username });
        } catch (err) { /* ... */ }
    }, [request]);

    useEffect(() => { fetchProfile(); }, [fetchProfile]);

    const handleInfoUpdate = async (e) => {
        e.preventDefault();
        try {
            const data = await request('/api/v1/profile/update', 'PUT', { full_name: infoData.full_name, email: infoData.email });
            showNotification(data.message || 'تم تحديث المعلومات بنجاح');
            fetchProfile();
        } catch (err) { /* ... */ }
    };

    const handleUsernameUpdate = async (e) => {
        e.preventDefault();
        setUsernameError('');
        try {
            const data = await request('/api/v1/profile/update-username', 'PUT', { username: infoData.username }, false);
            showNotification(data.message || 'تم تحديث اسم المستخدم بنجاح');
            fetchProfile();
        } catch (err) {
            if (err.message === "اسم المستخدم مستخدم بالفعل") {
                setUsernameError(err.message);
            } else {
                showNotification(err.message, 'error');
            }
        }
    };

    const handlePasswordUpdate = async (e) => {
        e.preventDefault();
        try {
            const data = await request('/api/v1/profile/update-password', 'POST', passwordData);
            showNotification(data.message || 'تم تحديث كلمة المرور بنجاح');
            setPasswordData({ old_password: '', new_password: '' });
        } catch (err) { /* ... */ }
    };

    const handleDeleteAccount = async () => {
        if (window.confirm('هل أنت متأكد من تعطيل حسابك؟ سيتم تسجيل خروجك.')) {
            try {
                await request('/api/v1/profile/delete', 'DELETE');
                localStorage.removeItem('authToken');
                navigate('/login');
            } catch (err) { /* ... */ }
        }
    };

    if (loading && !user) return <div className="text-center p-8">جاري تحميل الملف الشخصي...</div>;

    return (
        <div className="container mx-auto p-8 max-w-4xl" dir="rtl">
            <h1 className="text-3xl font-bold mb-8">ملفي الشخصي</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* تحديث المعلومات */}
                <div className="bg-white p-6 rounded-lg shadow-md space-y-6">
                    <form onSubmit={handleInfoUpdate} className="space-y-4">
                        <h2 className="text-2xl font-semibold mb-4">تحديث المعلومات الشخصية</h2>
                        <div>
                            <label htmlFor="full_name" className="block text-sm font-medium text-gray-700">الاسم الكامل</label>
                            <input type="text" id="full_name" value={infoData.full_name || ''} onChange={(e) => setInfoData({...infoData, full_name: e.target.value})} className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
                        </div>
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-700">البريد الإلكتروني</label>
                            <input type="email" id="email" value={infoData.email || ''} onChange={(e) => setInfoData({...infoData, email: e.target.value})} className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
                        </div>
                        <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700">حفظ المعلومات</button>
                    </form>
                    <hr/>
                    <form onSubmit={handleUsernameUpdate} className="space-y-4">
                        <h2 className="text-2xl font-semibold mb-4">تحديث اسم المستخدم</h2>
                        <div>
                            <label htmlFor="username" className="block text-sm font-medium text-gray-700">اسم المستخدم</label>
                            <input type="text" id="username" value={infoData.username || ''} onChange={(e) => { setInfoData({...infoData, username: e.target.value}); setUsernameError(''); }} className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm ${usernameError ? 'border-red-500' : 'border-gray-300'}`} />
                            {usernameError && <p className="text-red-500 text-xs mt-1">{usernameError}</p>}
                        </div>
                        <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700">حفظ اسم المستخدم</button>
                    </form>
                </div>

                {/* تغيير كلمة المرور */}
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h2 className="text-2xl font-semibold mb-4">تغيير كلمة المرور</h2>
                    <form onSubmit={handlePasswordUpdate} className="space-y-4">
                        <div>
                            <label htmlFor="old_password"  className="block text-sm font-medium text-gray-700">كلمة المرور القديمة</label>
                            <input type="password" id="old_password" value={passwordData.old_password} onChange={(e) => setPasswordData({...passwordData, old_password: e.target.value})} className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
                        </div>
                        <div>
                            <label htmlFor="new_password"  className="block text-sm font-medium text-gray-700">كلمة المرور الجديدة</label>
                            <input type="password" id="new_password" value={passwordData.new_password} onChange={(e) => setPasswordData({...passwordData, new_password: e.target.value})} className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm" />
                        </div>
                        <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700">تحديث كلمة المرور</button>
                    </form>
                </div>
            </div>

            {/* منطقة الخطر */}
            <div className="mt-12 bg-red-50 border-l-4 border-red-400 p-4">
                <div className="flex">
                    <div className="py-1">
                        <h3 className="font-bold text-red-800">منطقة الخطر</h3>
                        <p className="text-sm text-red-700 mt-2">
                            تعطيل حسابك هو إجراء لا يمكن التراجع عنه. سيتم تسجيل خروجك ولن تتمكن من الوصول إلى حسابك مرة أخرى.
                        </p>
                        <button onClick={handleDeleteAccount} disabled={loading} className="mt-4 bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700">
                            تعطيل حسابي
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
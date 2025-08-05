import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import useApi from '../hooks/useApi';
import { useNotification } from '../context/NotificationContext';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

const SpinnerIcon = () => ( <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"> <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle> <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path> </svg> );
const GoogleIcon = () => ( <svg className="w-5 h-5" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="google" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 488 512"> <path fill="currentColor" d="M488 261.8C488 403.3 381.5 512 244 512 109.8 512 0 402.2 0 256S109.8 0 244 0c73.2 0 136 29.3 182.3 75.3l-63.6 62.1C337.3 114.6 295.6 96 244 96c-88.6 0-160.2 71.6-160.2 160s71.6 160 160.2 160c92.8 0 140.3-68.8 143.9-105.4H244v-75.5h243.1c1.6 10.3 2.9 20.9 2.9 31.8z"></path> </svg> );
const FacebookIcon = () => ( <svg className="w-5 h-5" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="facebook-f" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"> <path fill="currentColor" d="M279.14 288l14.22-92.66h-88.91v-60.13c0-25.35 12.42-50.06 52.24-50.06h40.42V6.26S260.43 0 225.36 0c-73.22 0-121.08 44.38-121.08 124.72v70.62H22.89V288h81.39v224h100.17V288z"></path> </svg> );
const GithubIcon = () => ( <svg className="w-5 h-5" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="github" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512"> <path fill="currentColor" d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3.3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.3-6.2-10.1-27.8 2.3-57.4 0 0 21.9-7.1 71.6 26.3 20.9-5.9 43.1-8.8 66.1-8.8 22.9 0 45.2 2.9 66.1 8.8 49.7-33.3 71.6-26.3 71.6-26.3 12.4 29.6 4.6 51.2 2.3 57.4 16 17.6 23.6 31.4 23.6 58.9 0 96.5-58.6 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"></path> </svg> );

export default function LoginRegisterPage() {
    const navigate = useNavigate();
    const location = useLocation();
    const { loading, request } = useApi();
    const { showNotification } = useNotification();
    const [view, setView] = useState('login');
    const [formData, setFormData] = useState({
        full_name: '', username: '', email: '', password: '', code: '', new_password: ''
    });
    const [validationErrors, setValidationErrors] = useState({});
    const [oauthError, setOauthError] = useState(null);

    useEffect(() => {
        if (location.state?.oauthError) {
            setOauthError(location.state.oauthError);
        }
    }, [location.state]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({ ...prevState, [name]: value }));
        setValidationErrors(prev => ({...prev, [name]: null}));
        setOauthError(null);
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setValidationErrors({});
        try {
            const { full_name, username, email, password } = formData;
            const data = await request('/api/v1/auth/register', 'POST', { full_name, username, email, password }, false);
            showNotification(data.message || 'تم التسجيل بنجاح!');
            navigate('/verify-email', { state: { email: formData.email } });
        } catch (err) {
            if (err.message === "البريد الإلكتروني مستخدم مسبقًا") {
                setValidationErrors(prev => ({ ...prev, email: err.message }));
            } else if (err.message === "اسم المستخدم مستخدم مسبقًا") {
                setValidationErrors(prev => ({ ...prev, username: err.message }));
            } else {
                showNotification(err.message, 'error');
            }
        }
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const { email, password } = formData;
            const data = await request('/api/v1/auth/login', 'POST', { email, password });
            localStorage.setItem('authToken', data.token);
            navigate('/');
        } catch (err) {
            if (err.message === 'يرجى تأكيد بريدك الإلكتروني أولاً') {
                navigate('/verify-email', { state: { email: formData.email } });
            }
        }
    };

    const handleRequestReset = async (e) => {
        e.preventDefault();
        try {
            const { email } = formData;
            const data = await request('/api/v1/auth/request-password-reset', 'POST', { email });
            showNotification(data.message);
            setView('resetPassword');
        } catch (err) { /* ... */ }
    };

    const handleResetPassword = async (e) => {
        e.preventDefault();
        try {
            const { email, code, new_password } = formData;
            const data = await request('/api/v1/auth/reset-password', 'POST', { email, code, new_password });
            showNotification(data.message);
            setView('login');
        } catch (err) { /* ... */ }
    };

    const handleSocialLogin = (provider) => {
        window.location.href = `${API_BASE_URL}/api/v1/auth/login/${provider}`;
    };

    const renderForm = () => {
        if (view === 'register') {
            return (
                <>
                    <h1 className="text-3xl font-bold text-center text-gray-800">إنشاء حساب جديد</h1>
                    <form onSubmit={handleRegister} className="space-y-4">
                        <div><label htmlFor="full_name">الاسم الكامل</label><input type="text" id="full_name" name="full_name" onChange={handleInputChange} required className="w-full px-4 py-2 mt-1 border rounded-lg" /></div>
                        <div>
                            <label htmlFor="username">اسم المستخدم</label>
                            <input type="text" id="username" name="username" onChange={handleInputChange} required className={`w-full px-4 py-2 mt-1 border rounded-lg ${validationErrors.username ? 'border-red-500' : ''}`} />
                            {validationErrors.username && <p className="text-red-500 text-xs mt-1">{validationErrors.username}</p>}
                        </div>
                        <div>
                            <label htmlFor="email">البريد الإلكتروني</label>
                            <input type="email" id="email" name="email" onChange={handleInputChange} required className={`w-full px-4 py-2 mt-1 border rounded-lg ${validationErrors.email ? 'border-red-500' : ''}`} />
                            {validationErrors.email && <p className="text-red-500 text-xs mt-1">{validationErrors.email}</p>}
                        </div>
                        <div><label htmlFor="password">كلمة المرور</label><input type="password" id="password" name="password" onChange={handleInputChange} required className="w-full px-4 py-2 mt-1 border rounded-lg" /></div>
                        <button type="submit" disabled={loading} className="w-full flex justify-center items-center px-4 py-3 font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700">{loading ? <SpinnerIcon /> : 'إنشاء حساب'}</button>
                    </form>
                    <button onClick={() => setView('login')} className="text-sm text-blue-600 hover:underline">هل لديك حساب بالفعل؟ قم بتسجيل الدخول</button>
                </>
            );
        }

        if (view === 'forgotPassword') {
            return (
                <>
                    <h1 className="text-3xl font-bold text-center text-gray-800">إعادة تعيين كلمة المرور</h1>
                    <form onSubmit={handleRequestReset} className="space-y-6">
                        <div><label htmlFor="email">البريد الإلكتروني</label><input type="email" id="email" name="email" onChange={handleInputChange} required className="w-full px-4 py-2 mt-1 border rounded-lg" /></div>
                        <button type="submit" disabled={loading} className="w-full flex justify-center items-center px-4 py-3 font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700">{loading ? <SpinnerIcon /> : 'إرسال الرمز'}</button>
                    </form>
                    <button onClick={() => setView('login')} className="text-sm text-blue-600 hover:underline">العودة لتسجيل الدخول</button>
                </>
            );
        }

        if (view === 'resetPassword') {
            return (
                <>
                    <h1 className="text-3xl font-bold text-center text-gray-800">إدخال الرمز</h1>
                    <form onSubmit={handleResetPassword} className="space-y-4">
                        <div><label htmlFor="email">البريد الإلكتروني</label><input type="email" id="email" name="email" onChange={handleInputChange} required className="w-full px-4 py-2 mt-1 border rounded-lg" /></div>
                        <div><label htmlFor="code">الرمز</label><input type="text" id="code" name="code" onChange={handleInputChange} required className="w-full px-4 py-2 mt-1 border rounded-lg" /></div>
                        <div><label htmlFor="new_password">كلمة المرور الجديدة</label><input type="password" id="new_password" name="new_password" onChange={handleInputChange} required className="w-full px-4 py-2 mt-1 border rounded-lg" /></div>
                        <button type="submit" disabled={loading} className="w-full flex justify-center items-center px-4 py-3 font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700">{loading ? <SpinnerIcon /> : 'تعيين كلمة المرور'}</button>
                    </form>
                    <button onClick={() => setView('login')} className="text-sm text-blue-600 hover:underline">العودة لتسجيل الدخول</button>
                </>
            );
        }

        return ( // Default view is 'login'
            <>
                <h1 className="text-3xl font-bold text-center text-gray-800">تسجيل الدخول</h1>
                {oauthError && (
                    <div className="p-4 text-sm rounded-lg text-center bg-yellow-100 text-yellow-800">
                        {oauthError}
                    </div>
                )}
                <form onSubmit={handleLogin} className="space-y-6">
                    <div><label htmlFor="email">البريد الإلكتروني</label><input type="email" id="email" name="email" onChange={handleInputChange} required className="w-full px-4 py-2 mt-1 border rounded-lg" /></div>
                    <div><label htmlFor="password">كلمة المرور</label><input type="password" id="password" name="password" onChange={handleInputChange} required className="w-full px-4 py-2 mt-1 border rounded-lg" /></div>
                    <div className="text-right"><button type="button" onClick={() => setView('forgotPassword')} className="text-sm text-blue-600 hover:underline">هل نسيت كلمة المرور؟</button></div>
                    <button type="submit" disabled={loading} className="w-full flex justify-center items-center px-4 py-3 font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700">{loading ? <SpinnerIcon /> : 'دخول'}</button>
                </form>
                <button onClick={() => setView('register')} className="text-sm text-blue-600 hover:underline">ليس لديك حساب؟ قم بإنشاء واحد</button>
            </>
        );
    };

    return (
        <div className="bg-gray-100 flex items-center justify-center min-h-screen font-sans py-12" dir="rtl">
            <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-xl shadow-lg">
                {renderForm()}
                <div className="relative flex py-2 items-center">
                    <div className="flex-grow border-t border-gray-300"></div>
                    <span className="flex-shrink mx-4 text-gray-400 text-sm">أو عبر</span>
                    <div className="flex-grow border-t border-gray-300"></div>
                </div>
                <div className="grid grid-cols-3 gap-3">
                    <button onClick={() => handleSocialLogin('google')} type="button" className="inline-flex w-full justify-center items-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-red-500 hover:text-white transition duration-300"> <GoogleIcon /> </button>
                    <button onClick={() => handleSocialLogin('facebook')} type="button" className="inline-flex w-full justify-center items-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-blue-600 hover:text-white transition duration-300"> <FacebookIcon /> </button>
                    <button onClick={() => handleSocialLogin('github')} type="button" className="inline-flex w-full justify-center items-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-800 hover:text-white transition duration-300"> <GithubIcon /> </button>
                </div>
            </div>
        </div>
    );
}
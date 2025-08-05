import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

const decodeToken = (token) => {
    try { return JSON.parse(atob(token.split('.')[1])); } catch (e) { return null; }
};

const Navbar = () => {
    const navigate = useNavigate();
    const location = useLocation(); // لمراقبة التغيرات في الرابط
    const [user, setUser] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('authToken');
        if (token) {
            setUser(decodeToken(token));
        } else {
            setUser(null);
        }
    }, [location.pathname]); // أعد التحقق عند تغير الصفحة

    const handleLogout = () => {
        localStorage.removeItem('authToken');
        setUser(null);
        navigate('/login');
    };

    return (
        <nav className="bg-white shadow-md" dir="rtl">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center">
                        <Link to="/" className="text-2xl font-bold text-blue-600">مطعمي</Link>
                    </div>
                    <div className="flex items-center space-x-4 space-x-reverse">
                        <Link to="/" className="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">الرئيسية</Link>
                        {user && ['admin', 'manager'].includes(user.role) && (
                            <Link to="/dashboard" className="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">لوحة التحكم</Link>
                        )}
                        {user ? (
                            <>
                                <Link to="/profile" className="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">ملفي الشخصي</Link>
                                <button onClick={handleLogout} className="bg-red-500 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-red-600">
                                    تسجيل الخروج
                                </button>
                            </>
                        ) : (
                            <Link to="/login" className="bg-blue-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
                                تسجيل الدخول
                            </Link>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
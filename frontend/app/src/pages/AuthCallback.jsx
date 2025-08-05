import React, { useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';

export default function AuthCallback() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();

    useEffect(() => {
        const token = searchParams.get('token');
        const error = searchParams.get('error');

        if (token) {
            localStorage.setItem('authToken', token);
            navigate('/');
        } else if (error) {
            // إعادة التوجيه إلى صفحة الدخول مع تمرير الخطأ
            navigate('/login', { state: { oauthError: error } });
        } else {
            // في حالة عدم وجود أي منهما، أعده إلى صفحة التسجيل
            navigate('/login', { state: { oauthError: 'حدث خطأ غير متوقع أثناء المصادقة.' } });
        }
    }, [searchParams, navigate]);

    return (
        <div className="flex items-center justify-center min-h-screen">
            <p>جاري المصادقة...</p>
        </div>
    );
}
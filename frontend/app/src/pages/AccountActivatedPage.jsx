import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

export default function AccountActivatedPage() {
    const { token } = useParams();
    const [message, setMessage] = useState('جاري تفعيل حسابك...');
    const [isSuccess, setIsSuccess] = useState(false);

    useEffect(() => {
        const activate = async () => {
            try {
                const response = await fetch(`/api/v1/auth/activate/${token}`);
                const data = await response.json();
                setMessage(data.message || 'حدث خطأ ما.');
                if (response.ok) {
                    setIsSuccess(true);
                }
            } catch (err) {
                setMessage('فشل الاتصال بالخادم.');
            }
        };
        activate();
    }, [token]);

    return (
        <div className="text-center p-12">
            <h1 className={`text-3xl font-bold mb-4 ${isSuccess ? 'text-green-600' : 'text-red-600'}`}>
                {message}
            </h1>
            {isSuccess && (
                <Link to="/login" className="text-blue-500 hover:underline">
                    اضغط هنا لتسجيل الدخول
                </Link>
            )}
        </div>
    );
}
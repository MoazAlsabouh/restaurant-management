import React, { useEffect, useState } from 'react';
import useApi from '../hooks/useApi';

export default function HomePage() {
    const [items, setItems] = useState([]);
    const { loading, error, request } = useApi();

    useEffect(() => {
        const fetchData = async () => {
            try {
                // المسار الصحيح لعرض الأصناف
                const data = await request('/api/v1/food_items/detail');
                // المفتاح الصحيح من الخادم هو 'food_items'
                setItems(data.food_items || []);
            } catch (err) { /* يتم التعامل مع الخطأ في الخطاف */ }
        };
        fetchData();
    }, [request]);

    return (
        <div className="container mx-auto p-8" dir="rtl">
            <h1 className="text-4xl font-bold text-center mb-12">قائمة طعامنا</h1>
            {loading && <p className="text-center">جاري التحميل...</p>}
            {error && <p className="text-center text-red-500">حدث خطأ: {error}</p>}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {items.map(item => (
                    <div key={item.id} className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow border-t-4 border-blue-500">
                        <h3 className="text-2xl font-bold text-gray-800">{item.name}</h3>
                        <p className="text-gray-600 mt-2">النوع: {item.type}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}
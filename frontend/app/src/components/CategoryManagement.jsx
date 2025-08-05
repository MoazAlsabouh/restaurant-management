import React, { useEffect, useState, useCallback } from 'react';
import useApi from '../hooks/useApi';
import { useNotification } from '../context/NotificationContext';

export default function CategoryManagement() {
    const [categories, setCategories] = useState([]);
    const [newCategory, setNewCategory] = useState({ type: '' });
    const { loading, request } = useApi();
    const { showNotification } = useNotification();

    const fetchCategories = useCallback(async () => {
        try {
            const data = await request('/api/v1/food_category/detail');
            setCategories(data.food_items || []);
        } catch (err) { /* ... */ }
    }, [request]);

    useEffect(() => { fetchCategories(); }, [fetchCategories]);

    const handleCreate = async (e) => {
        e.preventDefault();
        try {
            await request('/api/v1/food_category/', 'POST', newCategory);
            showNotification('تمت إضافة الفئة بنجاح');
            setNewCategory({ type: '' });
            fetchCategories();
        } catch (err) { /* ... */ }
    };

    const handleDelete = async (id) => {
        if (window.confirm('هل أنت متأكد؟')) {
            try {
                await request(`/api/v1/food_category/${id}`, 'DELETE');
                showNotification('تم حذف الفئة بنجاح');
                fetchCategories();
            } catch (err) { /* ... */ }
        }
    };

    return (
        <div>
            <h2 className="text-2xl font-semibold mb-6">إدارة فئات الطعام</h2>
            <form onSubmit={handleCreate} className="mb-8 p-4 bg-gray-50 rounded-lg flex gap-4 items-center">
                <input type="text" value={newCategory.type} onChange={(e) => setNewCategory({ type: e.target.value })} placeholder="اسم الفئة الجديدة (مثال: مقبلات)" className="p-2 border rounded flex-grow" required />
                <button type="submit" className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600">إضافة فئة</button>
            </form>

            {loading && <p>جاري التحميل...</p>}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {categories.map(cat => (
                    <div key={cat.id} className="bg-white p-4 rounded-lg shadow flex justify-between items-center">
                        <p className="font-bold">{cat.type}</p>
                        <button onClick={() => handleDelete(cat.id)} className="text-red-500 hover:text-red-700">حذف</button>
                    </div>
                ))}
            </div>
        </div>
    );
}
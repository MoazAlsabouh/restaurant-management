import React, { useEffect, useState, useCallback } from 'react';
import useApi from '../hooks/useApi';
import { useNotification } from '../context/NotificationContext';

// مكون النافذة المنبثقة للتعديل
const EditItemModal = ({ item, categories, isOpen, onClose, onSave, loading }) => {
    const [editedItem, setEditedItem] = useState(item);

    useEffect(() => {
        setEditedItem(item);
    }, [item]);

    if (!isOpen || !editedItem) return null;

    const handleChange = (e) => {
        const { name, value } = e.target;
        setEditedItem(prev => ({ ...prev, [name]: value }));
    };

    const handleSave = (e) => {
        e.preventDefault();
        onSave(editedItem);
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50" dir="rtl">
            <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
                <h2 className="text-2xl font-bold mb-6">تعديل الصنف</h2>
                <form onSubmit={handleSave}>
                    <div className="mb-4">
                        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">اسم الصنف</label>
                        <input type="text" name="name" id="name" value={editedItem.name} onChange={handleChange} className="w-full p-2 border rounded-lg" required />
                    </div>
                    <div className="mb-6">
                        <label htmlFor="food_category_id" className="block text-sm font-medium text-gray-700 mb-1">الفئة</label>
                        <select name="food_category_id" id="food_category_id" value={editedItem.food_category_id} onChange={handleChange} className="w-full p-2 border rounded-lg" required>
                            {categories.map(cat => <option key={cat.id} value={cat.id}>{cat.type}</option>)}
                        </select>
                    </div>
                    <div className="flex justify-end gap-4">
                        <button type="button" onClick={onClose} className="px-4 py-2 rounded-lg text-gray-600 bg-gray-100 hover:bg-gray-200">إلغاء</button>
                        <button type="submit" disabled={loading} className="px-4 py-2 rounded-lg text-white bg-blue-600 hover:bg-blue-700">{loading ? 'جاري الحفظ...' : 'حفظ التغييرات'}</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default function ItemManagement() {
    const [items, setItems] = useState([]);
    const [categories, setCategories] = useState([]);
    const [newItem, setNewItem] = useState({ name: '', food_category_id: '' });
    const [editingItem, setEditingItem] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const { loading, request } = useApi();
    const { showNotification } = useNotification();

    const fetchData = useCallback(async () => {
        try {
            const [itemsData, categoriesData] = await Promise.all([
                request('/api/v1/food_items/detail'),
                request('/api/v1/food_category/detail')
            ]);
            setItems(itemsData.food_items || []);
            setCategories(categoriesData.food_items || []);
            if (categoriesData.food_items?.length > 0) {
                setNewItem(prev => ({ name: '', food_category_id: categoriesData.food_items[0].id }));
            } else {
                setNewItem({ name: '', food_category_id: '' });
            }
        } catch (err) { /* ... */ }
    }, [request]);

    useEffect(() => { fetchData(); }, [fetchData]);

    const handleCreate = async (e) => {
        e.preventDefault();
        if (!newItem.food_category_id) {
            showNotification('الرجاء إضافة فئة أولاً قبل إضافة صنف.', 'error');
            return;
        }
        try {
            await request('/api/v1/food_items/', 'POST', { name: newItem.name, food_category_id: newItem.food_category_id });
            showNotification('تمت إضافة الصنف بنجاح');
            setNewItem({ name: '', food_category_id: categories[0]?.id || '' });
            fetchData();
        } catch (err) { /* ... */ }
    };

    const handleDelete = async (id) => {
        if (window.confirm('هل أنت متأكد؟')) {
            try {
                await request(`/api/v1/food_items/${id}`, 'DELETE');
                showNotification('تم حذف الصنف بنجاح');
                fetchData();
            } catch (err) { /* ... */ }
        }
    };

    const handleUpdate = async (itemToUpdate) => {
        try {
            await request(`/api/v1/food_items/${itemToUpdate.id}`, 'PATCH', {
                name: itemToUpdate.name,
                food_category_id: itemToUpdate.food_category_id
            });
            showNotification('تم تحديث الصنف بنجاح');
            setIsModalOpen(false);
            setEditingItem(null);
            fetchData();
        } catch (err) { /* ... */ }
    };

    const openEditModal = (item) => {
        const categoryId = categories.find(c => c.type === item.type)?.id;
        setEditingItem({ ...item, food_category_id: categoryId || (categories.length > 0 ? categories[0].id : '') });
        setIsModalOpen(true);
    };

    return (
        <div>
            <EditItemModal 
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                item={editingItem}
                categories={categories}
                onSave={handleUpdate}
                loading={loading}
            />
            <h2 className="text-2xl font-semibold mb-6">إدارة أصناف الطعام</h2>

            {categories.length === 0 ? (
                <div className="p-4 text-center bg-yellow-50 text-yellow-800 rounded-lg">
                    الرجاء الذهاب إلى "إدارة فئات الطعام" وإضافة فئة واحدة على الأقل قبل إضافة الأصناف.
                </div>
            ) : (
                <form onSubmit={handleCreate} className="mb-8 p-4 bg-gray-50 rounded-lg grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
                    <input type="text" name="name" value={newItem.name} onChange={(e) => setNewItem({...newItem, name: e.target.value})} placeholder="اسم الصنف الجديد (مثال: بيتزا)" className="p-2 border rounded col-span-1" required />
                    <select name="food_category_id" value={newItem.food_category_id} onChange={(e) => setNewItem({...newItem, food_category_id: e.target.value})} className="p-2 border rounded col-span-1" required>
                        {categories.map(cat => <option key={cat.id} value={cat.id}>{cat.type}</option>)}
                    </select>
                    <button type="submit" className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 col-span-1">إضافة صنف</button>
                </form>
            )}

            {loading && !isModalOpen && <p>جاري التحميل...</p>}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {items.map(item => (
                    <div key={item.id} className="bg-white p-4 rounded-lg shadow flex justify-between items-center">
                        <div>
                            <p className="font-bold">{item.name}</p>
                            <p className="text-sm text-gray-500">{item.type}</p>
                        </div>
                        <div className="flex gap-2">
                            <button onClick={() => openEditModal(item)} className="text-blue-500 hover:text-blue-700">تعديل</button>
                            <button onClick={() => handleDelete(item.id)} className="text-red-500 hover:text-red-700">حذف</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

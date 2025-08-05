import React, { useEffect, useState, useCallback } from 'react';
import useApi from '../hooks/useApi';
import { useNotification } from '../context/NotificationContext';

const decodeToken = (token) => {
    try { return JSON.parse(atob(token.split('.')[1])); } catch (e) { return null; }
};

// مكون النافذة المنبثقة لتغيير الدور
const RoleChangeModal = ({ user, isOpen, onClose, onSave, loading }) => {
    const [newRole, setNewRole] = useState(user ? user.role : 'user');
    if (!isOpen || !user) return null;
    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50" dir="rtl">
            <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-sm">
                <h2 className="text-2xl font-bold mb-6">تغيير دور: {user.email}</h2>
                <div className="mb-6">
                    <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-1">الدور الجديد</label>
                    <select id="role" value={newRole} onChange={(e) => setNewRole(e.target.value)} className="w-full p-2 border rounded-lg">
                        <option value="user">User</option>
                        <option value="admin">Admin</option>
                    </select>
                </div>
                <div className="flex justify-end gap-4">
                    <button type="button" onClick={onClose} className="px-4 py-2 rounded-lg text-gray-600 bg-gray-100 hover:bg-gray-200">إلغاء</button>
                    <button onClick={() => onSave(user.id, newRole)} disabled={loading} className="px-4 py-2 rounded-lg text-white bg-blue-600 hover:bg-blue-700">{loading ? 'جاري الحفظ...' : 'حفظ'}</button>
                </div>
            </div>
        </div>
    );
};

// مكون النافذة المنبثقة لتغيير اسم المستخدم
const UsernameChangeModal = ({ user, isOpen, onClose, onSave, loading }) => {
    const [newUsername, setNewUsername] = useState(user ? user.username : '');
    if (!isOpen || !user) return null;
    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50" dir="rtl">
            <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-sm">
                <h2 className="text-2xl font-bold mb-6">تغيير اسم المستخدم لـ: {user.full_name}</h2>
                <div className="mb-6">
                    <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">اسم المستخدم الجديد</label>
                    <input id="username" type="text" value={newUsername} onChange={(e) => setNewUsername(e.target.value)} className="w-full p-2 border rounded-lg" />
                </div>
                <div className="flex justify-end gap-4">
                    <button type="button" onClick={onClose} className="px-4 py-2 rounded-lg text-gray-600 bg-gray-100 hover:bg-gray-200">إلغاء</button>
                    <button onClick={() => onSave(user.id, newUsername)} disabled={loading} className="px-4 py-2 rounded-lg text-white bg-blue-600 hover:bg-blue-700">{loading ? 'جاري الحفظ...' : 'حفظ'}</button>
                </div>
            </div>
        </div>
    );
};

export default function UserManagement() {
    const [users, setUsers] = useState([]);
    const [filters, setFilters] = useState({ email: '', role: '', is_active: '', full_name: '', username: '' });
    const [currentUserRole, setCurrentUserRole] = useState(null);
    const [isRoleModalOpen, setIsRoleModalOpen] = useState(false);
    const [isUsernameModalOpen, setIsUsernameModalOpen] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);
    const { loading, request } = useApi();
    const { showNotification } = useNotification();

    useEffect(() => {
        const token = localStorage.getItem('authToken');
        if (token) {
            setCurrentUserRole(decodeToken(token)?.role);
        }
    }, []);

    const fetchUsers = useCallback(async (currentFilters) => {
        try {
            const params = new URLSearchParams();
            if (currentFilters.email) params.append('email', currentFilters.email);
            if (currentFilters.role) params.append('role', currentFilters.role);
            if (currentFilters.is_active !== '') params.append('is_active', currentFilters.is_active);
            if (currentFilters.full_name) params.append('full_name', currentFilters.full_name);
            if (currentFilters.username) params.append('username', currentFilters.username);

            const queryString = params.toString();
            const url = `/api/v1/admin/users${queryString ? `?${queryString}` : ''}`;
            const data = await request(url);
            setUsers(data.users || []);
        } catch (err) { /* ... */ }
    }, [request]);

    useEffect(() => {
        fetchUsers(filters);
    }, [fetchUsers]);

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters(prev => ({ ...prev, [name]: value }));
    };

    const handleSearch = (e) => {
        e.preventDefault();
        fetchUsers(filters);
    };

    const handleReset = () => {
        const initialFilters = { email: '', role: '', is_active: '', full_name: '', username: '' };
        setFilters(initialFilters);
        fetchUsers(initialFilters);
    };

    const handleUpdateRole = async (userId, newRole) => {
        try {
            const data = await request(`/api/v1/admin/user/${userId}/role`, 'PATCH', { role: newRole });
            showNotification(data.message || 'تم تحديث الدور بنجاح');
            setIsRoleModalOpen(false);
            fetchUsers(filters);
        } catch (err) { /* ... */ }
    };

    const handleUpdateUsername = async (userId, newUsername) => {
        try {
            const data = await request(`/api/v1/admin/user/${userId}/username`, 'PATCH', { username: newUsername });
            showNotification(data.message || 'تم تحديث اسم المستخدم بنجاح');
            setIsUsernameModalOpen(false);
            fetchUsers(filters);
        } catch (err) { /* ... */ }
    };

    const handleToggleActive = async (userId) => {
        try {
            const data = await request(`/api/v1/admin/user/${userId}/toggle-active`, 'PUT');
            showNotification(data.message || 'تم تحديث حالة المستخدم بنجاح');
            fetchUsers(filters);
        } catch(err) { /* ... */ }
    };

    const handleDeleteUser = async (userId) => {
        if(window.confirm('هل أنت متأكد من حذف هذا المستخدم؟')) {
            try {
                await request(`/api/v1/admin/user/${userId}`, 'DELETE');
                showNotification('تم حذف المستخدم بنجاح');
                fetchUsers(filters);
            } catch(err) { /* ... */ }
        }
    };

    const openRoleModal = (user) => {
        setSelectedUser(user);
        setIsRoleModalOpen(true);
    };

    const openUsernameModal = (user) => {
        setSelectedUser(user);
        setIsUsernameModalOpen(true);
    };

    return (
        <div>
            {selectedUser && (
                <>
                    <RoleChangeModal 
                        isOpen={isRoleModalOpen}
                        onClose={() => setIsRoleModalOpen(false)}
                        user={selectedUser}
                        onSave={handleUpdateRole}
                        loading={loading}
                    />
                    <UsernameChangeModal 
                        isOpen={isUsernameModalOpen}
                        onClose={() => setIsUsernameModalOpen(false)}
                        user={selectedUser}
                        onSave={handleUpdateUsername}
                        loading={loading}
                    />
                </>
            )}
            <h2 className="text-2xl font-semibold mb-6">إدارة المستخدمين</h2>
            <form onSubmit={handleSearch} className="mb-8 p-4 bg-gray-50 rounded-lg grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 items-end">
                <input type="text" name="full_name" value={filters.full_name} onChange={handleFilterChange} placeholder="بحث بالاسم الكامل..." className="p-2 border rounded col-span-1" />
                <input type="text" name="username" value={filters.username} onChange={handleFilterChange} placeholder="بحث باسم المستخدم..." className="p-2 border rounded col-span-1" />
                <input type="text" name="email" value={filters.email} onChange={handleFilterChange} placeholder="بحث بالبريد..." className="p-2 border rounded col-span-1" />
                <select name="role" value={filters.role} onChange={handleFilterChange} className="p-2 border rounded col-span-1">
                    <option value="">كل الأدوار</option>
                    <option value="user">User</option>
                    <option value="admin">Admin</option>
                    <option value="manager">Manager</option>
                </select>
                <select name="is_active" value={filters.is_active} onChange={handleFilterChange} className="p-2 border rounded col-span-1">
                    <option value="">كل الحالات</option>
                    <option value="true">نشط</option>
                    <option value="false">غير نشط</option>
                </select>
                <div className="flex gap-2 col-span-1">
                    <button type="submit" className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 flex-grow">بحث</button>
                    <button type="button" onClick={handleReset} className="bg-gray-500 text-white p-2 rounded hover:bg-gray-600">إعادة تعيين</button>
                </div>
            </form>

            {loading && <p>جاري تحميل المستخدمين...</p>}
            <div className="bg-white shadow-md rounded-lg overflow-x-auto">
                <table className="min-w-full leading-normal">
                    <thead>
                        <tr>
                            <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">الاسم الكامل</th>
                            <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">اسم المستخدم</th>
                            <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">البريد الإلكتروني</th>
                            <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">الدور</th>
                            <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">الحالة</th>
                            <th className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">إجراءات</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(user => (
                            <tr key={user.id}>
                                <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">{user.full_name}</td>
                                <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                                    <div className="flex items-center justify-between">
                                        <span>{user.username}</span>
                                        <button onClick={() => openUsernameModal(user)} className="text-yellow-600 hover:text-yellow-900 text-xs">تغيير</button>
                                    </div>
                                </td>
                                <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">{user.email}</td>
                                <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                                    <div className="flex items-center justify-between">
                                        <span>{user.role}</span>
                                        {currentUserRole === 'manager' && user.role !== 'manager' && (
                                            <button onClick={() => openRoleModal(user)} className="text-green-600 hover:text-green-900 text-xs">تغيير</button>
                                        )}
                                    </div>
                                </td>
                                <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                                    <div className="flex items-center justify-between">
                                        <span className={`relative inline-block px-3 py-1 font-semibold leading-tight ${user.is_active ? 'text-green-900' : 'text-red-900'}`}>
                                            <span aria-hidden className={`absolute inset-0 ${user.is_active ? 'bg-green-200' : 'bg-red-200'} opacity-50 rounded-full`}></span>
                                            <span className="relative">{user.is_active ? 'نشط' : 'غير نشط'}</span>
                                        </span>
                                        <button onClick={() => handleToggleActive(user.id)} className="text-indigo-600 hover:text-indigo-900 text-xs">تبديل</button>
                                    </div>
                                </td>
                                <td className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                                    <button onClick={() => handleDeleteUser(user.id)} className="text-red-600 hover:text-red-900">حذف</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
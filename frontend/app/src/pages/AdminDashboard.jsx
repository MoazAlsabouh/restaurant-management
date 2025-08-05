import React, { useState } from 'react';
import UserManagement from '../components/UserManagement';
import CategoryManagement from '../components/CategoryManagement';
import ItemManagement from '../components/ItemManagement';

export default function AdminDashboard() {
    const [activeTab, setActiveTab] = useState('users');

    const renderContent = () => {
        switch (activeTab) {
            case 'users': return <UserManagement />;
            case 'categories': return <CategoryManagement />;
            case 'items': return <ItemManagement />;
            default: return <UserManagement />;
        }
    };

    const TabButton = ({ tabName, title }) => (
        <button
            onClick={() => setActiveTab(tabName)}
            className={`px-6 py-3 font-semibold rounded-t-lg transition-colors duration-300 ${
                activeTab === tabName
                    ? 'bg-white text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-500 hover:text-blue-600'
            }`}
        >
            {title}
        </button>
    );

    return (
        <div className="container mx-auto p-4 sm:p-8" dir="rtl">
            <div className="bg-white rounded-lg shadow-lg">
                <div className="flex border-b">
                    <TabButton tabName="users" title="إدارة المستخدمين" />
                    <TabButton tabName="categories" title="إدارة فئات الطعام" />
                    <TabButton tabName="items" title="إدارة الأصناف" />
                </div>
                <div className="p-6">
                    {renderContent()}
                </div>
            </div>
        </div>
    );
}

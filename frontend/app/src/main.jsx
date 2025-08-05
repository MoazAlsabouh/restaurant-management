import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
// 1. تأكد من استيراد BrowserRouter
import { BrowserRouter } from 'react-router-dom'
import { NotificationProvider } from './context/NotificationContext'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* 2. استخدام BrowserRouter مع تحديد المسار الأساسي */}
    <BrowserRouter basename="/restaurant-management/">
      <NotificationProvider>
        <App />
      </NotificationProvider>
    </BrowserRouter>
  </React.StrictMode>,
)

import { Navigate, Route, Routes } from 'react-router-dom';
import DashboardLayout from '../components/layout/DashboardLayout';
import LoginPage from '../features/auth/LoginPage';
import RegisterPage from '../features/auth/RegisterPage';
import CartPage from '../features/cart/CartPage';
import DashboardPage from '../features/dashboard/DashboardPage';
import NotificationsPage from '../features/notifications/NotificationsPage';
import OrdersPage from '../features/orders/OrdersPage';
import PaymentsPage from '../features/payments/PaymentsPage';
import ProductsPage from '../features/products/ProductsPage';
import ProtectedRoute from './ProtectedRoute';

const AppRoutes = () => (
  <Routes>
    <Route path="/login" element={<LoginPage />} />
    <Route path="/register" element={<RegisterPage />} />
    <Route path="/" element={<ProtectedRoute><DashboardLayout><DashboardPage /></DashboardLayout></ProtectedRoute>} />
    <Route path="/products" element={<ProtectedRoute><DashboardLayout><ProductsPage /></DashboardLayout></ProtectedRoute>} />
    <Route path="/cart" element={<ProtectedRoute><DashboardLayout><CartPage /></DashboardLayout></ProtectedRoute>} />
    <Route path="/orders" element={<ProtectedRoute><DashboardLayout><OrdersPage /></DashboardLayout></ProtectedRoute>} />
    <Route path="/payments" element={<ProtectedRoute><DashboardLayout><PaymentsPage /></DashboardLayout></ProtectedRoute>} />
    <Route path="/notifications" element={<ProtectedRoute><DashboardLayout><NotificationsPage /></DashboardLayout></ProtectedRoute>} />
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>
);

export default AppRoutes;

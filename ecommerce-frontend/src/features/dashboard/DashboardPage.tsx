import { useEffect, useState } from 'react';
import { Bell, CreditCard, Package, Plus, Receipt, ShoppingCart } from 'lucide-react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { getProducts } from '../../api/productApi';
import { getCart, getOrders } from '../../api/orderApi';
import { getMyPayments } from '../../api/paymentApi';
import { getNotifications } from '../../api/notificationApi';
import Card from '../../components/common/Card';
import Loader from '../../components/common/Loader';
import { getErrorMessage } from '../../utils/format';

type Stats = { products: number; cart: number; orders: number; payments: number; notifications: number };

const DashboardPage = () => {
  const [stats, setStats] = useState<Stats>({ products: 0, cart: 0, orders: 0, payments: 0, notifications: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const [products, cart, orders, payments, notifications] = await Promise.allSettled([
          getProducts(), getCart(), getOrders(), getMyPayments(), getNotifications()
        ]);
        setStats({
          products: products.status === 'fulfilled' ? products.value.length : 0,
          cart: cart.status === 'fulfilled' ? cart.value.items?.length ?? 0 : 0,
          orders: orders.status === 'fulfilled' ? orders.value.length : 0,
          payments: payments.status === 'fulfilled' ? payments.value.length : 0,
          notifications: notifications.status === 'fulfilled' ? notifications.value.length : 0
        });
      } catch (error) {
        toast.error(getErrorMessage(error));
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, []);

  const cards = [
    { label: 'Products', value: stats.products, icon: Package, color: 'bg-blue-50 text-blue-700' },
    { label: 'Cart Items', value: stats.cart, icon: ShoppingCart, color: 'bg-purple-50 text-purple-700' },
    { label: 'Orders', value: stats.orders, icon: Receipt, color: 'bg-orange-50 text-orange-700' },
    { label: 'Payments', value: stats.payments, icon: CreditCard, color: 'bg-green-50 text-green-700' },
    { label: 'Notifications', value: stats.notifications, icon: Bell, color: 'bg-pink-50 text-pink-700' }
  ];

  if (loading) return <Loader />;

  return (
    <section className="space-y-6">
      <div className="rounded-3xl bg-slate-900 p-8 text-white shadow-soft">
        <p className="text-sm uppercase tracking-widest text-blue-200">Industry-level practice project</p>
        <h1 className="mt-3 text-3xl font-bold">Smart E-Commerce Microservice Dashboard</h1>
        <p className="mt-2 max-w-2xl text-slate-300">Complete frontend flow connected with auth, product, order, payment and notification services.</p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            to="/products"
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-4 py-2.5 text-sm font-semibold text-slate-900 transition hover:bg-blue-50"
          >
            <Plus className="h-4 w-4" /> Add Product
          </Link>
          <Link
            to="/products"
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-slate-800 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-700"
          >
            <Package className="h-4 w-4" /> Manage Products
          </Link>
        </div>
      </div>
      <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-5">
        {cards.map(({ label, value, icon: Icon, color }) => (
          <Card key={label}>
            <div className={`mb-4 inline-flex rounded-2xl p-3 ${color}`}><Icon className="h-6 w-6" /></div>
            <p className="text-sm text-slate-500">{label}</p>
            <h2 className="mt-1 text-3xl font-bold text-slate-900">{value}</h2>
          </Card>
        ))}
      </div>
    </section>
  );
};

export default DashboardPage;

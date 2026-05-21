import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { getOrders } from '../../api/orderApi';
import { processPayment } from '../../api/paymentApi';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import EmptyState from '../../components/common/EmptyState';
import Loader from '../../components/common/Loader';
import type { Order } from '../../types/order';
import { formatCurrency, formatDate, getErrorMessage } from '../../utils/format';

const OrdersPage = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [payingId, setPayingId] = useState<string | null>(null);

  const loadOrders = async () => {
    setLoading(true);
    try { setOrders(await getOrders()); } catch (error) { toast.error(getErrorMessage(error)); } finally { setLoading(false); }
  };
  useEffect(() => { void loadOrders(); }, []);

  const pay = async (order: Order) => {
    const orderId = order.order_id || order.id;
    setPayingId(orderId);
    try {
      await processPayment({ order_id: orderId, amount: Number(order.total_amount ?? order.total ?? 0), payment_method: 'fake_card' });
      toast.success('Fake payment processed');
      await loadOrders();
    } catch (error) { toast.error(getErrorMessage(error)); } finally { setPayingId(null); }
  };

  if (loading) return <Loader />;
  if (!orders.length) return <EmptyState title="No orders found" message="Create an order from your cart." />;

  return (
    <section className="space-y-5">
      <div><h1 className="text-2xl font-bold text-slate-900">Orders</h1><p className="text-sm text-slate-500">Order history from order-service.</p></div>
      <div className="grid gap-4">
        {orders.map((order) => {
          const id = order.order_id || order.id;
          return <Card key={id} className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
            <div><h3 className="font-bold text-slate-900">Order #{id}</h3><p className="text-sm text-slate-500">Created: {formatDate(order.created_at)}</p></div>
            <div className="flex flex-wrap items-center gap-3"><span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-semibold">{order.status}</span><b>{formatCurrency(order.total_amount ?? order.total ?? 0)}</b><Button loading={payingId === id} onClick={() => pay(order)}>Process Payment</Button></div>
          </Card>;
        })}
      </div>
    </section>
  );
};

export default OrdersPage;

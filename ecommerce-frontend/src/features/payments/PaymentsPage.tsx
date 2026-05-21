import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { getMyPayments } from '../../api/paymentApi';
import Card from '../../components/common/Card';
import EmptyState from '../../components/common/EmptyState';
import Loader from '../../components/common/Loader';
import type { Payment } from '../../types/payment';
import { formatCurrency, formatDate, getErrorMessage } from '../../utils/format';

const PaymentsPage = () => {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try { setPayments(await getMyPayments()); } catch (error) { toast.error(getErrorMessage(error)); } finally { setLoading(false); }
    };
    void load();
  }, []);

  if (loading) return <Loader />;
  if (!payments.length) return <EmptyState title="No payments found" message="Process payment from order page." />;

  return (
    <section className="space-y-5">
      <div><h1 className="text-2xl font-bold text-slate-900">Payments</h1><p className="text-sm text-slate-500">Payment status from payment-service.</p></div>
      <div className="grid gap-4">
        {payments.map((payment) => <Card key={payment.payment_id || payment.id} className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
          <div><h3 className="font-bold text-slate-900">Payment #{payment.payment_id || payment.id}</h3><p className="text-sm text-slate-500">Order: {payment.order_id} • {formatDate(payment.created_at)}</p></div>
          <div className="flex items-center gap-3"><span className="rounded-full bg-green-50 px-3 py-1 text-sm font-semibold text-green-700">{payment.status}</span><b>{formatCurrency(payment.amount ?? 0)}</b></div>
        </Card>)}
      </div>
    </section>
  );
};

export default PaymentsPage;

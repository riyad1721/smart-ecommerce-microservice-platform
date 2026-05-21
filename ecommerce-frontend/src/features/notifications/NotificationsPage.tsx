import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { getNotifications } from '../../api/notificationApi';
import Card from '../../components/common/Card';
import EmptyState from '../../components/common/EmptyState';
import Loader from '../../components/common/Loader';
import type { Notification } from '../../types/notification';
import { formatDate, getErrorMessage } from '../../utils/format';

const NotificationsPage = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try { setNotifications(await getNotifications()); } catch (error) { toast.error(getErrorMessage(error)); } finally { setLoading(false); }
    };
    void load();
  }, []);

  if (loading) return <Loader />;
  if (!notifications.length) return <EmptyState title="No notifications found" message="Notification logs will appear after order/payment events." />;

  return (
    <section className="space-y-5">
      <div><h1 className="text-2xl font-bold text-slate-900">Notifications</h1><p className="text-sm text-slate-500">Notification logs from notification-service.</p></div>
      <div className="grid gap-4">
        {notifications.map((notification) => <Card key={notification.notification_id || notification.id}>
          <div className="flex flex-col justify-between gap-2 md:flex-row md:items-start"><div><h3 className="font-bold text-slate-900">{notification.title || notification.type || 'Notification'}</h3><p className="mt-1 text-sm text-slate-600">{notification.message}</p></div><span className="text-xs text-slate-400">{formatDate(notification.created_at)}</span></div>
        </Card>)}
      </div>
    </section>
  );
};

export default NotificationsPage;

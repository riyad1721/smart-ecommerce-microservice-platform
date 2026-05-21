import { Bell, CreditCard, Home, Package, Receipt, ShoppingCart } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import clsx from 'clsx';

const items = [
  { to: '/', label: 'Dashboard', icon: Home },
  { to: '/products', label: 'Products', icon: Package },
  { to: '/cart', label: 'Cart', icon: ShoppingCart },
  { to: '/orders', label: 'Orders', icon: Receipt },
  { to: '/payments', label: 'Payments', icon: CreditCard },
  { to: '/notifications', label: 'Notifications', icon: Bell }
];

const Sidebar = () => (
  <aside className="h-full w-72 border-r border-slate-200 bg-white p-4">
    <div className="mb-6 rounded-2xl bg-slate-900 p-5 text-white">
      <p className="text-xs uppercase tracking-widest text-slate-300">Microservice Platform</p>
      <h2 className="mt-2 text-xl font-bold">Frontend Dashboard</h2>
    </div>
    <nav className="space-y-1">
      {items.map(({ to, label, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          className={({ isActive }) => clsx('flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold transition', isActive ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-100')}
          end={to === '/'}
        >
          <Icon className="h-5 w-5" />
          {label}
        </NavLink>
      ))}
    </nav>
  </aside>
);

export default Sidebar;

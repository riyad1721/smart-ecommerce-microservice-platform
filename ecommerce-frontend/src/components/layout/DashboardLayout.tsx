import { useState, type ReactNode } from 'react';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

const DashboardLayout = ({ children }: { children: ReactNode }) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar onMenuClick={() => setOpen(true)} />
      <div className="flex">
        <div className="hidden h-[calc(100vh-4rem)] lg:block lg:sticky lg:top-16"><Sidebar /></div>
        {open && (
          <div className="fixed inset-0 z-40 lg:hidden">
            <button className="absolute inset-0 bg-slate-900/40" onClick={() => setOpen(false)} />
            <div className="relative h-full"><Sidebar /></div>
          </div>
        )}
        <main className="w-full p-4 lg:p-8">{children}</main>
      </div>
    </div>
  );
};

export default DashboardLayout;

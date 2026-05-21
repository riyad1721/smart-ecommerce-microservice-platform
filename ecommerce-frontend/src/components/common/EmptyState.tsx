import { Inbox } from 'lucide-react';

const EmptyState = ({ title = 'No data found', message = 'Data will appear here when available.' }: { title?: string; message?: string }) => (
  <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-8 text-center text-slate-500">
    <Inbox className="mx-auto mb-3 h-10 w-10 text-slate-400" />
    <h3 className="text-base font-semibold text-slate-700">{title}</h3>
    <p className="mt-1 text-sm">{message}</p>
  </div>
);

export default EmptyState;

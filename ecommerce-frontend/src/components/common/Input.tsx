import type { InputHTMLAttributes } from 'react';
import clsx from 'clsx';

type Props = InputHTMLAttributes<HTMLInputElement> & { label?: string; error?: string };

const Input = ({ label, error, className, ...props }: Props) => (
  <label className="block">
    {label && <span className="mb-1.5 block text-sm font-semibold text-slate-700">{label}</span>}
    <input className={clsx('w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100', className)} {...props} />
    {error && <span className="mt-1 block text-xs text-red-600">{error}</span>}
  </label>
);

export default Input;

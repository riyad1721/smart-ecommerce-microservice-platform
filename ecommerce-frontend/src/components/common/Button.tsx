import type { ButtonHTMLAttributes, ReactNode } from 'react';
import clsx from 'clsx';

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  loading?: boolean;
};

const styles = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700',
  secondary: 'bg-slate-900 text-white hover:bg-slate-800',
  danger: 'bg-red-600 text-white hover:bg-red-700',
  ghost: 'bg-slate-100 text-slate-700 hover:bg-slate-200'
};

const Button = ({ children, variant = 'primary', loading, className, disabled, ...props }: Props) => (
  <button
    className={clsx('inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-60', styles[variant], className)}
    disabled={disabled || loading}
    {...props}
  >
    {loading ? 'Loading...' : children}
  </button>
);

export default Button;

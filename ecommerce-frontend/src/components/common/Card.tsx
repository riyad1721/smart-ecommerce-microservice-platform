import type { HTMLAttributes, ReactNode } from 'react';
import clsx from 'clsx';

type Props = HTMLAttributes<HTMLDivElement> & { children: ReactNode };

const Card = ({ children, className, ...props }: Props) => (
  <div className={clsx('rounded-2xl border border-slate-200 bg-white p-5 shadow-soft', className)} {...props}>
    {children}
  </div>
);

export default Card;

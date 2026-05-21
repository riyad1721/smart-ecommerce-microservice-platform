const Loader = ({ label = 'Loading data...' }: { label?: string }) => (
  <div className="flex items-center justify-center rounded-2xl bg-white p-10 text-slate-500 shadow-soft">
    <div className="mr-3 h-5 w-5 animate-spin rounded-full border-2 border-slate-300 border-t-blue-600" />
    {label}
  </div>
);

export default Loader;

export const formatCurrency = (value: number | string | undefined) => {
  const amount = Number(value ?? 0);
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
};

export const formatDate = (value?: string) => {
  if (!value) return 'N/A';
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric', month: 'short', day: '2-digit', hour: '2-digit', minute: '2-digit'
  }).format(new Date(value));
};

export const getErrorMessage = (error: unknown): string => {
  if (typeof error === 'object' && error !== null && 'response' in error) {
    const err = error as { response?: { data?: { detail?: string; message?: string } } };
    return err.response?.data?.detail || err.response?.data?.message || 'Something went wrong';
  }
  return 'Something went wrong';
};

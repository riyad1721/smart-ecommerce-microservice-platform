export type Payment = {
  id: string;
  payment_id?: string;
  order_id: string;
  status: string;
  amount?: number;
  payment_method?: string;
  created_at?: string;
};

export type ProcessPaymentPayload = {
  order_id: string;
  amount?: number;
  currency?: string;
  force_result?: string;
  payment_method?: string;
};

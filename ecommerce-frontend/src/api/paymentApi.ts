import axiosClient from './axiosClient';
import type { Payment, ProcessPaymentPayload } from '../types/payment';

const BASE_URL = import.meta.env.VITE_PAYMENT_SERVICE as string;

export const processPayment = async (payload: ProcessPaymentPayload) => {
  const { data: payment } = await axiosClient.post<Payment>(`${BASE_URL}/payments`, {
    order_id: payload.order_id,
    amount: payload.amount ?? 0,
    currency: payload.currency ?? 'USD',
  });

  const { data } = await axiosClient.post<Payment>(
    `${BASE_URL}/payments/${payment.id}/process`,
    { force_result: payload.force_result }
  );

  return data;
};
export const getPaymentById = async (id: string) => {
  const { data } = await axiosClient.get<Payment>(`${BASE_URL}/payments/${id}`);
  return data;
};
export const getPaymentsByOrder = async (orderId: string) => {
  const { data } = await axiosClient.get<Payment>(`${BASE_URL}/payments/order/${orderId}`);
  return data;
};
export const getMyPayments = async () => {
  const { data } = await axiosClient.get<Payment[]>(`${BASE_URL}/payments`);
  return data;
};

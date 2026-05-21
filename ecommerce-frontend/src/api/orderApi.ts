import axiosClient from './axiosClient';
import type { Cart } from '../types/cart';
import type { Order } from '../types/order';

const BASE_URL = import.meta.env.VITE_ORDER_SERVICE as string;

export const addToCart = async (payload: { product_id: string; quantity: number }) => {
  const { data } = await axiosClient.post(`${BASE_URL}/cart/items`, payload);
  return data;
};
export const getCart = async () => {
  const { data } = await axiosClient.get<Cart>(`${BASE_URL}/cart`);
  return data;
};
export const removeCartItem = async (itemId: string) => {
  const { data } = await axiosClient.delete(`${BASE_URL}/cart/items/${itemId}`);
  return data;
};
export const createOrder = async () => {
  const { data } = await axiosClient.post<Order>(`${BASE_URL}/orders`);
  return data;
};
export const getOrders = async () => {
  const { data } = await axiosClient.get<Order[]>(`${BASE_URL}/orders`);
  return data;
};
export const getOrderById = async (id: string) => {
  const { data } = await axiosClient.get<Order>(`${BASE_URL}/orders/${id}`);
  return data;
};

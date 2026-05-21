import axiosClient from './axiosClient';
import type { Category, Product, ProductPayload } from '../types/product';

const BASE_URL = import.meta.env.VITE_PRODUCT_SERVICE as string;

export const getProducts = async () => {
  const { data } = await axiosClient.get<Product[]>(`${BASE_URL}/products`);
  return data;
};
export const getProductById = async (id: string) => {
  const { data } = await axiosClient.get<Product>(`${BASE_URL}/products/${id}`);
  return data;
};
export const searchProducts = async (query: string) => {
  const { data } = await axiosClient.get<Product[]>(`${BASE_URL}/products/search/by-name`, {
    params: { name: query },
  });
  return data;
};
export const getCategories = async () => {
  const { data } = await axiosClient.get<Category[]>(`${BASE_URL}/categories`);
  return data;
};
export const createProduct = async (payload: ProductPayload) => {
  const { data } = await axiosClient.post<Product>(`${BASE_URL}/products`, payload);
  return data;
};
export const updateProduct = async (id: string | number, payload: Partial<ProductPayload>) => {
  const { data } = await axiosClient.put<Product>(`${BASE_URL}/products/${id}`, payload);
  return data;
};
export const deleteProduct = async (id: string | number) => {
  const { data } = await axiosClient.delete(`${BASE_URL}/products/${id}`);
  return data;
};

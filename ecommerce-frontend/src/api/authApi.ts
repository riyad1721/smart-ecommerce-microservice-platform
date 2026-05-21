import axiosClient from './axiosClient';

const AUTH_BASE_URL = import.meta.env.VITE_AUTH_SERVICE;

export type RegisterPayload = {
  full_name: string;
  email: string;
  password: string;
};

export type LoginPayload = {
  email: string;
  password: string;
};

export const registerApi = (data: RegisterPayload) => {
  return axiosClient.post(`${AUTH_BASE_URL}/auth/register`, data);
};

export const loginApi = (data: LoginPayload) => {
  return axiosClient.post(`${AUTH_BASE_URL}/auth/login`, data);
};
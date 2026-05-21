import axios, { AxiosError } from 'axios';
import { getToken, clearAuth } from '../utils/token';

const axiosClient = axios.create({
  headers: { 'Content-Type': 'application/json' },
  timeout: 15000
});

axiosClient.interceptors.request.use((config) => {
  const token = getToken();
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

axiosClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      clearAuth();
      if (window.location.pathname !== '/login') window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default axiosClient;

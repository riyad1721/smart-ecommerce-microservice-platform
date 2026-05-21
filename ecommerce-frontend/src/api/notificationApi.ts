import axiosClient from './axiosClient';
import type { Notification } from '../types/notification';

const BASE_URL = import.meta.env.VITE_NOTIFICATION_SERVICE as string;

export const getNotifications = async () => {
  const { data } = await axiosClient.get<Notification[]>(`${BASE_URL}/notifications`);
  return data;
};
export const getNotificationById = async (id: string) => {
  const { data } = await axiosClient.get<Notification>(`${BASE_URL}/notifications/${id}`);
  return data;
};
export const getNotificationsByUser = async (userId: string) => {
  const { data } = await axiosClient.get<Notification[]>(`${BASE_URL}/notifications/user/${userId}`);
  return data;
};

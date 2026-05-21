import { useMemo } from 'react';
import { authStore } from '../features/auth/authStore';

export const useAuth = () => useMemo(() => ({
  isAuthenticated: authStore.isAuthenticated(),
  user: authStore.getUser(),
  logout: authStore.logout
}), []);

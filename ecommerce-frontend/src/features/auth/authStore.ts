import type { AuthResponse, AuthUser } from '../../types/auth';
import { clearAuth, getToken, getUser, saveToken, saveUser } from '../../utils/token';

export const authStore = {
  isAuthenticated: () => Boolean(getToken()),
  getUser: () => getUser<AuthUser>(),
  setAuth: (response: AuthResponse) => {
    saveToken(response.access_token);
    if (response.user) saveUser(response.user);
  },
  logout: () => clearAuth()
};

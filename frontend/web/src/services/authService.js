import apiService from './apiService';

const authService = {
  login: async (email, password, totpCode = null) => {
    const response = await apiService.post('/api/v1/auth/login', {
      email,
      password,
      ...(totpCode && { totp_code: totpCode }),
    });

    if (response.access_token) {
      localStorage.setItem('auth_token', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
      return true;
    }
    return false;
  },

  register: async (userData) => {
    const response = await apiService.post('/api/v1/auth/register', userData);

    if (response.access_token) {
      localStorage.setItem('auth_token', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
      return true;
    }
    return false;
  },

  logout: () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
  },

  isLoggedIn: () => {
    return localStorage.getItem('auth_token') !== null;
  },

  getCurrentUser: () => {
    const userJson = localStorage.getItem('user');
    return userJson ? JSON.parse(userJson) : null;
  },

  getToken: () => {
    return localStorage.getItem('auth_token');
  },
};

export default authService;

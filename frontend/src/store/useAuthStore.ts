import { create } from 'zustand';
import { api, setAuthToken } from '../api/api';

export interface User {
  id: number;
  telegram_id: number | null;
  email: string | null;
  is_email_verified: boolean;
  balance: number;
  language: string;
  orders: any[];
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  
  login: (token: string) => {
    localStorage.setItem('token', token);
    setAuthToken(token);
    set({ token, isAuthenticated: true });
    get().fetchUser();
  },
  
  logout: () => {
    localStorage.removeItem('token');
    setAuthToken(null);
    set({ user: null, token: null, isAuthenticated: false });
  },
  
  fetchUser: async () => {
    const token = get().token;
    if (!token) return;
    
    setAuthToken(token);
    try {
      const response = await api.get('/users/me');
      set({ user: response.data, isAuthenticated: true });
    } catch (error) {
      console.error("Failed to fetch user:", error);
      get().logout();
    }
  }
}));

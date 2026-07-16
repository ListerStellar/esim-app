import { create } from 'zustand';
import type { Language } from '../locales';

interface AppState {
  language: Language;
  setLanguage: (lang: Language) => void;
}

export const useAppStore = create<AppState>((set) => ({
  language: (localStorage.getItem('language') as Language) || 'en',
  setLanguage: (lang: Language) => {
    localStorage.setItem('language', lang);
    set({ language: lang });
  }
}));

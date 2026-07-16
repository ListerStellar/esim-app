import { Link, useLocation } from 'react-router-dom';
import { Home, User as UserIcon, BookOpen, HelpCircle } from 'lucide-react';
import { useAuthStore } from '../store/useAuthStore';
import { useAppStore } from '../store/useAppStore';
import { t } from '../locales';
import type { Language } from '../locales';
import { motion } from 'framer-motion';

const LanguageSwitcher = () => {
  const { language, setLanguage } = useAppStore();
  const langs: {code: Language, flag: string}[] = [
    { code: 'en', flag: '🇬🇧' },
    { code: 'ru', flag: '🇷🇺' },
    { code: 'uk', flag: '🇺🇦' },
    { code: 'cs', flag: '🇨🇿' },
  ];

  return (
    <div className="flex items-center gap-2 bg-black/30 px-3 py-1.5 rounded-full border border-white/10">
      {langs.map(l => (
        <button 
          key={l.code}
          onClick={() => setLanguage(l.code)}
          className={`text-lg transition-transform ${language === l.code ? 'scale-125 opacity-100' : 'opacity-50 hover:opacity-80 grayscale'}`}
        >
          {l.flag}
        </button>
      ))}
    </div>
  );
};

export const Navbar = () => {
  const { pathname } = useLocation();
  const { isAuthenticated } = useAuthStore();
  const { language } = useAppStore();

  return (
    <>
      {/* Desktop Header */}
      <motion.header layoutRoot className="hidden md:flex justify-between items-center py-4 px-8 glass-panel fixed top-6 left-6 right-6 z-50 bg-black/20 backdrop-blur-xl border-white/10">
        <Link to="/" className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-300">
          ADVANCE eSIM
        </Link>
        <nav className="flex gap-2 items-center">
          <div className="mr-4"><LanguageSwitcher /></div>
          
          <Link to="/catalog" className={`relative font-medium transition-colors hover:text-white px-4 py-2 rounded-full text-slate-200`}>
            {pathname === '/catalog' && <motion.div layoutId="nav-pill" className="absolute inset-0 bg-black/30 rounded-full border border-white/10 -z-10" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} />}
            {t(language, 'nav_catalog')}
          </Link>
          
          <Link to="/how-to-install" className={`relative font-medium transition-colors hover:text-white px-4 py-2 rounded-full text-slate-200`}>
            {pathname === '/how-to-install' && <motion.div layoutId="nav-pill" className="absolute inset-0 bg-black/30 rounded-full border border-white/10 -z-10" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} />}
            {t(language, 'profile_how_to_install')}
          </Link>
          
          <Link to="/support" className={`relative font-medium transition-colors hover:text-white px-4 py-2 rounded-full text-slate-200`}>
            {pathname === '/support' && <motion.div layoutId="nav-pill" className="absolute inset-0 bg-black/30 rounded-full border border-white/10 -z-10" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} />}
            {t(language, 'support_title')}
          </Link>
          
          <Link to={isAuthenticated ? "/profile" : "/login"} className={`relative font-medium transition-colors hover:text-white px-4 py-2 rounded-full text-slate-200`}>
            {(pathname === '/profile' || pathname === '/login') && <motion.div layoutId="nav-pill" className="absolute inset-0 bg-black/30 rounded-full border border-white/10 -z-10" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} />}
            {isAuthenticated ? t(language, 'nav_profile') : t(language, 'nav_login')}
          </Link>
        </nav>
      </motion.header>

      {/* Mobile Language Switcher Floating */}
      <div className="md:hidden fixed top-4 right-4 z-50">
        <LanguageSwitcher />
      </div>

      {/* Mobile Bottom Navigation */}
      <motion.nav layoutRoot className="md:hidden fixed bottom-0 left-0 w-full glass-panel rounded-none rounded-t-3xl border-b-0 py-2 px-4 z-50 flex justify-between items-center pb-safe">
        <Link to="/" className={`relative flex flex-col items-center justify-center p-3 rounded-full transition-colors hover:text-white text-slate-300`}>
          {pathname === '/' && <motion.div layoutId="mobile-nav-pill" className="absolute inset-0 bg-black/30 rounded-full border border-white/10 -z-10" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} />}
          <Home size={24} strokeWidth={pathname === '/' ? 2.5 : 2} />
        </Link>
        
        <Link to="/catalog" className={`relative flex flex-col items-center justify-center p-3 rounded-full transition-colors hover:text-white text-slate-300`}>
          {pathname === '/catalog' && <motion.div layoutId="mobile-nav-pill" className="absolute inset-0 bg-black/30 rounded-full border border-white/10 -z-10" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} />}
          <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={pathname === '/catalog' ? "2.5" : "2"}><path strokeLinecap="round" strokeLinejoin="round" d="M3 3h18v18H3V3zm7 0v18m7-18v18M3 10h18M3 17h18"/></svg>
        </Link>
        
        <Link to="/how-to-install" className={`relative flex flex-col items-center justify-center p-3 rounded-full transition-colors hover:text-white text-slate-300`}>
          {pathname === '/how-to-install' && <motion.div layoutId="mobile-nav-pill" className="absolute inset-0 bg-black/30 rounded-full border border-white/10 -z-10" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} />}
          <BookOpen size={24} strokeWidth={pathname === '/how-to-install' ? 2.5 : 2} />
        </Link>
        
        <Link to="/support" className={`relative flex flex-col items-center justify-center p-3 rounded-full transition-colors hover:text-white text-slate-300`}>
          {pathname === '/support' && <motion.div layoutId="mobile-nav-pill" className="absolute inset-0 bg-black/30 rounded-full border border-white/10 -z-10" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} />}
          <HelpCircle size={24} strokeWidth={pathname === '/support' ? 2.5 : 2} />
        </Link>
        
        <Link to={isAuthenticated ? "/profile" : "/login"} className={`relative flex flex-col items-center justify-center p-3 rounded-full transition-colors hover:text-white text-slate-300`}>
          {(pathname === '/profile' || pathname === '/login') && <motion.div layoutId="mobile-nav-pill" className="absolute inset-0 bg-black/30 rounded-full border border-white/10 -z-10" transition={{ type: "spring", bounce: 0.2, duration: 0.6 }} />}
          <UserIcon size={24} strokeWidth={pathname === '/profile' || pathname === '/login' ? 2.5 : 2} />
        </Link>
      </motion.nav>
    </>
  );
};

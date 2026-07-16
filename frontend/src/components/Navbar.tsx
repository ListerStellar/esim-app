import { useState, useRef, useEffect } from 'react';
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

  const mobilePaths = ['/', '/catalog', '/how-to-install', '/support', isAuthenticated ? '/profile' : '/login'];
  // Handle case where logged in user goes to /login, they might be redirected to /profile
  const normalizedPathname = (pathname === '/login' && isAuthenticated) ? '/profile' : pathname;
  const activeMobileIndex = mobilePaths.indexOf(normalizedPathname);

  // Desktop pill measurements
  const desktopRefs = useRef<(HTMLAnchorElement | null)[]>([]);
  const [desktopPillStyle, setDesktopPillStyle] = useState({ left: 0, width: 0, opacity: 0, snap: true });
  const wasDesktopVisible = useRef(false);

  useEffect(() => {
    const desktopPaths = ['/catalog', '/how-to-install', '/support', isAuthenticated ? '/profile' : '/login'];
    const desktopIndex = desktopPaths.indexOf(normalizedPathname);

    if (desktopIndex !== -1 && desktopRefs.current[desktopIndex]) {
      const el = desktopRefs.current[desktopIndex];
      if (el) {
        setDesktopPillStyle({
          left: el.offsetLeft,
          width: el.offsetWidth,
          opacity: 1,
          snap: !wasDesktopVisible.current
        });
        wasDesktopVisible.current = true;
      }
    } else {
      setDesktopPillStyle(prev => ({ ...prev, opacity: 0, snap: false }));
      wasDesktopVisible.current = false;
    }
  }, [pathname, isAuthenticated, language, normalizedPathname]);

  return (
    <>
      {/* Desktop Header */}
      <header className="hidden md:flex justify-between items-center py-4 px-8 glass-panel fixed top-6 left-6 right-6 z-50 bg-black/20 backdrop-blur-xl border-white/10">
        <Link to="/" className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-300">
          ADVANCE eSIM
        </Link>
        <nav className="flex gap-2 items-center relative">
          <div className="mr-4"><LanguageSwitcher /></div>
          
          <motion.div 
            className="absolute top-1 bottom-1 bg-black/30 rounded-full border border-white/10 pointer-events-none origin-center"
            initial={false}
            animate={{ 
              left: desktopPillStyle.left, 
              width: desktopPillStyle.width, 
              opacity: desktopPillStyle.opacity,
              scale: desktopPillStyle.opacity === 1 ? 1 : 0.8
            }}
            transition={{ 
              left: desktopPillStyle.snap ? { duration: 0 } : { type: "spring", bounce: 0.2, duration: 0.6 },
              width: desktopPillStyle.snap ? { duration: 0 } : { type: "spring", bounce: 0.2, duration: 0.6 },
              opacity: { duration: 0.15 },
              scale: { duration: 0.2 }
            }}
          />

          <Link ref={el => { desktopRefs.current[0] = el; }} to="/catalog" className={`relative font-medium transition-colors hover:text-white px-4 py-2 rounded-full text-slate-200 z-10`}>
            {t(language, 'nav_catalog')}
          </Link>
          
          <Link ref={el => { desktopRefs.current[1] = el; }} to="/how-to-install" className={`relative font-medium transition-colors hover:text-white px-4 py-2 rounded-full text-slate-200 z-10`}>
            {t(language, 'profile_how_to_install')}
          </Link>
          
          <Link ref={el => { desktopRefs.current[2] = el; }} to="/support" className={`relative font-medium transition-colors hover:text-white px-4 py-2 rounded-full text-slate-200 z-10`}>
            {t(language, 'support_title')}
          </Link>
          
          <Link ref={el => { desktopRefs.current[3] = el; }} to={isAuthenticated ? "/profile" : "/login"} className={`relative font-medium transition-colors hover:text-white px-4 py-2 rounded-full text-slate-200 z-10`}>
            {isAuthenticated ? t(language, 'nav_profile') : t(language, 'nav_login')}
          </Link>
        </nav>
      </header>

      {/* Mobile Language Switcher Floating */}
      <div className="md:hidden fixed top-4 right-4 z-50">
        <LanguageSwitcher />
      </div>

      {/* Mobile Bottom Navigation */}
      <nav className="md:hidden fixed bottom-0 left-0 w-full glass-panel rounded-none rounded-t-3xl border-b-0 py-2 px-2 z-50 pb-safe">
        <div className="grid grid-cols-5 relative w-full h-full">
          {/* Active Pill Background */}
          <motion.div 
            className="absolute top-1 bottom-1 bg-black/30 rounded-full border border-white/10 pointer-events-none origin-center"
            initial={false}
            animate={{
              x: `${Math.max(0, activeMobileIndex) * 100}%`,
              width: '20%',
              opacity: activeMobileIndex !== -1 ? 1 : 0,
              scale: activeMobileIndex !== -1 ? 1 : 0.8
            }}
            transition={{ 
              x: { type: "spring", bounce: 0.2, duration: 0.6 },
              opacity: { duration: 0.15 },
              scale: { duration: 0.2 }
            }}
          />
          
          <Link to="/" className="relative flex flex-col items-center justify-center p-3 transition-colors hover:text-white text-slate-300 z-10">
            <Home size={24} strokeWidth={pathname === '/' ? 2.5 : 2} />
          </Link>
          
          <Link to="/catalog" className="relative flex flex-col items-center justify-center p-3 transition-colors hover:text-white text-slate-300 z-10">
            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={pathname === '/catalog' ? "2.5" : "2"}><path strokeLinecap="round" strokeLinejoin="round" d="M3 3h18v18H3V3zm7 0v18m7-18v18M3 10h18M3 17h18"/></svg>
          </Link>
          
          <Link to="/how-to-install" className="relative flex flex-col items-center justify-center p-3 transition-colors hover:text-white text-slate-300 z-10">
            <BookOpen size={24} strokeWidth={pathname === '/how-to-install' ? 2.5 : 2} />
          </Link>
          
          <Link to="/support" className="relative flex flex-col items-center justify-center p-3 transition-colors hover:text-white text-slate-300 z-10">
            <HelpCircle size={24} strokeWidth={pathname === '/support' ? 2.5 : 2} />
          </Link>
          
          <Link to={isAuthenticated ? "/profile" : "/login"} className="relative flex flex-col items-center justify-center p-3 transition-colors hover:text-white text-slate-300 z-10">
            <UserIcon size={24} strokeWidth={pathname === '/profile' || pathname === '/login' ? 2.5 : 2} />
          </Link>
        </div>
      </nav>
    </>
  );
};

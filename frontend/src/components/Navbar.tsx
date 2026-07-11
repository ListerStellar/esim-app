import { Link, useLocation } from 'react-router-dom';
import { Home, User as UserIcon, BookOpen, HelpCircle } from 'lucide-react';
import { useAuthStore } from '../store/useAuthStore';

export const Navbar = () => {
  const { pathname } = useLocation();
  const { isAuthenticated } = useAuthStore();

  return (
    <>
      {/* Desktop Header */}
      <header className="hidden md:flex justify-between items-center py-4 px-8 glass-panel fixed top-6 left-6 right-6 z-50 bg-black/20 backdrop-blur-xl border-white/10">
        <Link to="/" className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-300">
          ADVANCE eSIM
        </Link>
        <nav className="flex gap-6 items-center">
          <Link to="/catalog" className={`font-medium transition-colors hover:text-blue-400 ${pathname === '/catalog' ? 'text-blue-400' : 'text-slate-300'}`}>
            Catalog
          </Link>
          <Link to="/how-to-install" className={`font-medium transition-colors hover:text-blue-400 ${pathname === '/how-to-install' ? 'text-blue-400' : 'text-slate-300'}`}>
            How to use
          </Link>
          <Link to="/support" className={`font-medium transition-colors hover:text-blue-400 ${pathname === '/support' ? 'text-blue-400' : 'text-slate-300'}`}>
            Support
          </Link>
          <Link to={isAuthenticated ? "/profile" : "/login"} className={`font-medium transition-colors hover:text-blue-400 ${pathname === '/profile' ? 'text-blue-400' : 'text-slate-300'}`}>
            {isAuthenticated ? 'Profile' : 'Sign In'}
          </Link>
        </nav>
      </header>

      {/* Mobile Bottom Navigation */}
      <nav className="md:hidden fixed bottom-0 left-0 w-full glass-panel rounded-none rounded-t-3xl border-b-0 py-3 px-6 z-50 flex justify-around items-center pb-safe">
        <Link to="/" className={`flex flex-col items-center gap-1 ${pathname === '/' ? 'text-blue-400' : 'text-slate-400'}`}>
          <Home size={24} strokeWidth={pathname === '/' ? 2.5 : 2} />
          <span className="text-[10px] font-medium">Home</span>
        </Link>
        <Link to="/catalog" className={`flex flex-col items-center gap-1 ${pathname === '/catalog' ? 'text-blue-400' : 'text-slate-400'}`}>
          <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={pathname === '/catalog' ? "2.5" : "2"}><path strokeLinecap="round" strokeLinejoin="round" d="M3 3h18v18H3V3zm7 0v18m7-18v18M3 10h18M3 17h18"/></svg>
          <span className="text-[10px] font-medium">Plans</span>
        </Link>
        <Link to="/how-to-install" className={`flex flex-col items-center gap-1 ${pathname === '/how-to-install' ? 'text-blue-400' : 'text-slate-400'}`}>
          <BookOpen size={24} strokeWidth={pathname === '/how-to-install' ? 2.5 : 2} />
          <span className="text-[10px] font-medium">Guide</span>
        </Link>
        <Link to="/support" className={`flex flex-col items-center gap-1 ${pathname === '/support' ? 'text-blue-400' : 'text-slate-400'}`}>
          <HelpCircle size={24} strokeWidth={pathname === '/support' ? 2.5 : 2} />
          <span className="text-[10px] font-medium">Support</span>
        </Link>
        <Link to={isAuthenticated ? "/profile" : "/login"} className={`flex flex-col items-center gap-1 ${pathname === '/profile' ? 'text-blue-400' : 'text-slate-400'}`}>
          <UserIcon size={24} strokeWidth={pathname === '/profile' ? 2.5 : 2} />
          <span className="text-[10px] font-medium">{isAuthenticated ? 'Profile' : 'Sign In'}</span>
        </Link>
      </nav>
    </>
  );
};

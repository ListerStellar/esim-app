import { useState, useEffect, useRef } from 'react';
import { api } from '../api/api';
import { useAuthStore } from '../store/useAuthStore';
import { useNavigate } from 'react-router-dom';

// Minimal Telegram Login Widget component
const TelegramLoginWidget = ({ onAuth }: { onAuth: (user: any) => void }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    
    // Check if script already exists
    if (containerRef.current.querySelector('script')) return;

    (window as any).onTelegramAuth = (user: any) => {
      onAuth(user);
    };

    const botName = import.meta.env.VITE_TELEGRAM_BOT_NAME || 'samplebot'; // Replace with valid default or env

    const script = document.createElement('script');
    script.src = 'https://telegram.org/js/telegram-widget.js?22';
    script.setAttribute('data-telegram-login', botName); 
    script.setAttribute('data-size', 'large');
    script.setAttribute('data-onauth', 'onTelegramAuth(user)');
    script.setAttribute('data-request-access', 'write');
    script.async = true;

    containerRef.current.appendChild(script);
  }, [onAuth]);

  return <div ref={containerRef} className="flex justify-center" />;
};

export const Login = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  
  const { login } = useAuthStore();
  const navigate = useNavigate();

  const handleEmailAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (!isLogin && password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    try {
      if (isLogin) {
        // OAuth2PasswordRequestForm needs form data URL encoded
        const params = new URLSearchParams();
        params.append('username', email);
        params.append('password', password);
        
        const res = await api.post('/auth/token', params, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        login(res.data.access_token);
        navigate('/profile');
      } else {
        const res = await api.post('/auth/register', { email, password });
        login(res.data.access_token);
        navigate('/profile');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Authentication failed');
    }
  };

  const handleOAuth = (provider: 'google' | 'apple') => {
    window.location.href = `/api/auth/${provider}/login`;
  };

  const handleTelegramAuth = async (user: any) => {
    try {
      const res = await api.post('/auth/telegram', user);
      login(res.data.access_token);
      navigate('/profile');
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Telegram auth failed');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-120px)] px-4 mt-6">
      <div className="glass-panel p-8 w-full max-w-md">
        
        <div className="flex bg-black/30 rounded-xl p-1 mb-8">
          <button 
            type="button"
            className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors ${isLogin ? 'bg-blue-600/80 text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
            onClick={() => setIsLogin(true)}
          >
            Sign In
          </button>
          <button 
            type="button"
            className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors ${!isLogin ? 'bg-blue-600/80 text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
            onClick={() => setIsLogin(false)}
          >
            Register
          </button>
        </div>

        {error && <div className="bg-red-500/20 text-red-200 p-3 rounded-xl mb-4 text-sm text-center">{error}</div>}
        
        <form onSubmit={handleEmailAuth} className="space-y-4 mb-8">
          <div>
            <input 
              type="email" 
              placeholder="Email" 
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors placeholder:text-slate-500"
              required
            />
          </div>
          <div>
            <input 
              type="password" 
              placeholder="Password" 
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors placeholder:text-slate-500"
              required
            />
          </div>
          {!isLogin && (
            <div>
              <input 
                type="password" 
                placeholder="Confirm Password" 
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
                className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors placeholder:text-slate-500"
                required
              />
            </div>
          )}
          <button type="submit" className="glass-button w-full py-3">
            {isLogin ? 'Sign In' : 'Create Account'}
          </button>
        </form>

        <div className="relative mb-8">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-white/10"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-[#0f172a] text-slate-400 rounded-full">Or continue with</span>
          </div>
        </div>

        <div className="space-y-3">
          <button type="button" onClick={() => handleOAuth('google')} className="glass-button-secondary w-full py-3">
            <svg className="w-5 h-5" viewBox="0 0 24 24"><path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" /><path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" /><path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" /><path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" /></svg>
            Google
          </button>
          <button type="button" onClick={() => handleOAuth('apple')} className="glass-button-secondary w-full py-3">
            <svg className="w-5 h-5" viewBox="0 0 24 24"><path fill="currentColor" d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.04 2.26-.79 3.59-.79 2.45.02 3.91 1.25 4.7 2.4-3.87 2-3.1 7.28.62 8.68-.8 1.96-2.12 3.8-3.99 5.88zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
            Apple
          </button>
          <div className="pt-2">
            <TelegramLoginWidget onAuth={handleTelegramAuth} />
          </div>
        </div>
      </div>
    </div>
  );
};

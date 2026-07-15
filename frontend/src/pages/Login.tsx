import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/useAuthStore';
import { z } from 'zod';
import { api } from '../api/api';

const authSchema = z.object({
  email: z.string()
    .min(1, 'Email is required')
    .email('Invalid email format')
    .regex(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, 'Please enter a valid email domain (e.g. .com)'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/^[\x20-\x7E]+$/, 'Password can only contain standard characters (a-z, A-Z, 0-9 and special symbols)')
});

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

    if (!isLogin) {
      if (password !== confirmPassword) {
        setError('Passwords do not match');
        return;
      }

      try {
        authSchema.parse({ email, password });
      } catch (err) {
        if (err instanceof z.ZodError) {
          setError(err.errors[0].message);
          return;
        }
      }
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
            <svg className="w-5 h-5" viewBox="0 0 384 512"><path fill="currentColor" d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z" /></svg>
            Apple
          </button>
          <div className="relative overflow-hidden rounded-xl">
            <button type="button" className="glass-button-secondary w-full py-3 flex justify-center items-center gap-2">
              <svg className="w-5 h-5" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.96-.64-.34-1 .22-1.57.14-.15 2.65-2.43 2.7-2.63.01-.03.01-.13-.05-.18-.06-.05-.15-.03-.21-.02-.09.02-1.5 1-4.24 2.85-.4.28-.76.41-1.09.4-.36 0-1.04-.2-1.55-.37-.62-.2-1.12-.3-1.08-.63.02-.17.27-.35.75-.54 2.92-1.27 4.86-2.11 5.83-2.51 2.77-1.15 3.35-1.36 3.73-1.36.08 0 .27.02.39.11.1.08.13.19.14.28-.01.07.01.21 0 .2z" /></svg>
              Telegram
            </button>
            <div className="absolute inset-0 z-20 flex items-center justify-center cursor-pointer" style={{ opacity: 0.01 }}>
              <div className="transform scale-[3] origin-center cursor-pointer w-full h-full flex items-center justify-center">
                <TelegramLoginWidget onAuth={handleTelegramAuth} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

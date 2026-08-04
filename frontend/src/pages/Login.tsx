import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/useAuthStore';
import { useAppStore } from '../store/useAppStore';
import { t } from '../locales';
import { TelegramLoginWidget } from '../components/TelegramLoginWidget';
import { z } from 'zod';
import { api } from '../api/api';
import { ArrowRight } from 'lucide-react';

const authSchema = z.object({
  email: z.string()
    .min(1, 'Email is required')
    .email('Invalid email format')
    .regex(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, 'Please enter a valid email domain (e.g. .com)'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/^[\x20-\x7E]+$/, 'Password can only contain standard characters (a-z, A-Z, 0-9 and special symbols)')
});

export const Login = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const { language } = useAppStore();
  const { login } = useAuthStore();
  const navigate = useNavigate();

  const handleEmailAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!isLogin) {
      if (password !== confirmPassword) {
        setError(t(language, 'login_passwords_not_match'));
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
        if (res.data.detail === 'verification_required') {
          setSuccess('Registration successful! Please check your email inbox (and spam folder) to verify your account.');
          setIsLogin(true);
          return;
        }
        login(res.data.access_token);
        navigate('/profile');
      }
    } catch (err: any) {
      if (err.response?.status === 429) {
        setError(t(language, 'login_too_many_attempts'));
        return;
      }
      let detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        detail = detail[0].msg;
      }
      setError(detail || err.message || t(language, 'login_auth_failed'));
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
      if (err.response?.status === 429) {
        setError(t(language, 'login_too_many_attempts'));
        return;
      }
      let detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        detail = detail[0].msg;
      }
      setError(detail || err.message || t(language, 'login_telegram_failed'));
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
            {t(language, 'login_sign_in')}
          </button>
          <button
            type="button"
            className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors ${!isLogin ? 'bg-blue-600/80 text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
            onClick={() => setIsLogin(false)}
          >
            {t(language, 'login_register')}
          </button>
        </div>

        {error && <div className="bg-red-500/20 text-red-200 p-3 rounded-xl mb-4 text-sm text-center">{error}</div>}
        {success && <div className="bg-green-500/20 text-green-200 p-3 rounded-xl mb-4 text-sm text-center">{success}</div>}

        <form onSubmit={handleEmailAuth} className="space-y-4 mb-8">
          <div>
            <input
              type="email"
              placeholder={t(language, 'login_email')}
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors placeholder:text-slate-500"
              required
            />
          </div>
          <div>
            <input
              type="password"
              placeholder={t(language, 'login_password')}
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
                placeholder={t(language, 'login_confirm_password')}
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
                className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 outline-none focus:border-blue-500 transition-colors placeholder:text-slate-500"
                required
              />
            </div>
          )}
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-500 text-white font-medium py-3 rounded-xl transition-colors shadow flex justify-center items-center gap-2"
          >
            {isLogin ? t(language, 'login_sign_in') : t(language, 'login_register')} <ArrowRight size={18} />
          </button>
        </form>

        <div className="flex items-center mb-8">
          <div className="flex-grow border-t border-white/10"></div>
          <span className="px-4 text-sm text-slate-500">{t(language, 'login_or_social')}</span>
          <div className="flex-grow border-t border-white/10"></div>
        </div>

        <div className="space-y-4">
          <button type="button" onClick={() => handleOAuth('google')} className="glass-button-secondary w-full py-3">
            <svg className="w-5 h-5" viewBox="0 0 24 24"><path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" /><path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" /><path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" /><path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" /></svg>
            {t(language, 'login_continue_google')}
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

import { useEffect, useState } from 'react';
import { useAuthStore } from '../store/useAuthStore';
import { useNavigate } from 'react-router-dom';
import { LogOut } from 'lucide-react';
import { QRCodeModal } from '../components/QRCodeModal';
import { TelegramLoginWidget } from '../components/TelegramLoginWidget';
import { useAppStore } from '../store/useAppStore';
import { t } from '../locales';
import { api } from '../api/api';

export const Profile = () => {
  const { language } = useAppStore();
  const { user, logout, fetchUser, isAuthenticated } = useAuthStore();
  const navigate = useNavigate();
  const [selectedOrderQr, setSelectedOrderQr] = useState<any>(null);
  
  const [showEmailForm, setShowEmailForm] = useState(false);
  const [linkEmail, setLinkEmail] = useState('');
  const [linkPassword, setLinkPassword] = useState('');
  const [linkMessage, setLinkMessage] = useState<{type: 'error'|'success', text: string} | null>(null);

  const handleLinkTelegram = async (tgUser: any) => {
    try {
      await api.post('/users/me/link/telegram', tgUser);
      setLinkMessage({ type: 'success', text: t(language, 'profile_link_tg_success') });
      fetchUser();
    } catch (err: any) {
      setLinkMessage({ type: 'error', text: err.response?.data?.detail || err.message || t(language, 'profile_link_tg_error') });
    }
  };

  const handleLinkEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/users/me/link/email', { email: linkEmail, password: linkPassword });
      setLinkMessage({ type: 'success', text: t(language, 'profile_link_email_success') });
      setShowEmailForm(false);
      fetchUser();
    } catch (err: any) {
      setLinkMessage({ type: 'error', text: err.response?.data?.detail || err.message || t(language, 'profile_link_email_error') });
    }
  };

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    } else {
      fetchUser();
    }
  }, [isAuthenticated]);

  if (!user) return <div className="text-center mt-20">Loading...</div>;

  return (
    <div className="pb-24 pt-6 px-4 max-w-4xl mx-auto min-h-[calc(100vh-64px)]">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-indigo-100">
          {t(language, 'profile_title')}
        </h2>
        <button onClick={() => { logout(); navigate('/'); }} className="glass-button-secondary px-4 py-2 text-sm text-red-300 hover:text-red-200 flex items-center gap-2">
          <LogOut size={16} /> {t(language, 'profile_logout')}
        </button>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mb-8">
        <div className="glass-panel p-6 flex flex-col justify-center items-center">
          <div className="text-slate-400 mb-1 text-sm uppercase tracking-wider">{t(language, 'profile_balance')}</div>
          <div className="text-4xl font-black text-blue-300">€{user.balance.toFixed(2)}</div>
        </div>
        <div className="glass-panel p-6 md:col-span-2">
          <div className="text-slate-400 mb-1 text-sm uppercase tracking-wider">{t(language, 'profile_details')}</div>
          <div className="grid grid-cols-2 gap-4 mt-3">
            <div>
              <div className="text-xs text-slate-500">ID / Telegram</div>
              <div className="font-medium">
                {user.id} / {user.telegram_id ? user.telegram_id : '—'}
              </div>
              {!user.telegram_id && (
                <div className="mt-2 relative overflow-hidden rounded-xl">
                  <button type="button" className="bg-white/10 hover:bg-white/20 transition-colors w-full py-2 flex justify-center items-center gap-2 rounded-xl text-sm">
                    <svg className="w-4 h-4" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.96-.64-.34-1 .22-1.57.14-.15 2.65-2.43 2.7-2.63.01-.03.01-.13-.05-.18-.06-.05-.15-.03-.21-.02-.09.02-1.5 1-4.24 2.85-.4.28-.76.41-1.09.4-.36 0-1.04-.2-1.55-.37-.62-.2-1.12-.3-1.08-.63.02-.17.27-.35.75-.54 2.92-1.27 4.86-2.11 5.83-2.51 2.77-1.15 3.35-1.36 3.73-1.36.08 0 .27.02.39.11.1.08.13.19.14.28-.01.07.01.21 0 .2z" /></svg>
                    {t(language, 'profile_link_telegram')}
                  </button>
                  <div className="absolute inset-0 z-20 flex items-center justify-center cursor-pointer" style={{ opacity: 0.01 }}>
                    <div className="transform scale-[3] origin-center cursor-pointer w-full h-full flex items-center justify-center">
                      <TelegramLoginWidget onAuth={handleLinkTelegram} />
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div>
              <div className="text-xs text-slate-500">Email</div>
              <div className="font-medium break-all">{user.email || '—'}</div>
              {!user.email && !showEmailForm && (
                <button 
                  onClick={() => setShowEmailForm(true)}
                  className="mt-2 text-xs bg-white/10 hover:bg-white/20 px-3 py-1 rounded transition-colors"
                >
                  {t(language, 'profile_link_email')}
                </button>
              )}
            </div>
          </div>
          
          {showEmailForm && (
            <form onSubmit={handleLinkEmailSubmit} className="mt-4 p-4 bg-black/20 rounded-xl space-y-3">
              <div className="text-sm font-medium">{t(language, 'profile_link_email_desc')}</div>
              <input 
                type="email" 
                placeholder={t(language, 'login_email')} 
                value={linkEmail} 
                onChange={e => setLinkEmail(e.target.value)}
                className="w-full bg-white/5 border border-white/10 rounded px-3 py-2 text-sm outline-none"
                required 
              />
              <input 
                type="password" 
                placeholder={t(language, 'login_password')} 
                value={linkPassword} 
                onChange={e => setLinkPassword(e.target.value)}
                className="w-full bg-white/5 border border-white/10 rounded px-3 py-2 text-sm outline-none"
                required 
              />
              <div className="flex gap-2">
                <button type="submit" className="flex-1 bg-blue-600 hover:bg-blue-500 text-white rounded py-2 text-sm transition-colors">
                  {t(language, 'profile_link')}
                </button>
                <button type="button" onClick={() => setShowEmailForm(false)} className="flex-1 bg-white/10 hover:bg-white/20 rounded py-2 text-sm transition-colors">
                  {t(language, 'profile_cancel')}
                </button>
              </div>
            </form>
          )}

          {linkMessage && (
            <div className={`mt-4 p-3 rounded-xl text-sm text-center ${linkMessage.type === 'error' ? 'bg-red-500/20 text-red-200' : 'bg-green-500/20 text-green-200'}`}>
              {linkMessage.text}
            </div>
          )}
        </div>
      </div>

      <h3 className="text-xl font-bold mb-4">{t(language, 'profile_my_esims')}</h3>
      {user.orders && user.orders.length > 0 ? (
        <div className="space-y-4">
          {user.orders.map((o: any) => (
            <div key={o.id} className="glass-panel p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-3 mb-1">
                  <span className="font-bold text-lg">{o.country_name}</span>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${o.status === 'activated' ? 'bg-green-500/20 text-green-300' : 'bg-yellow-500/20 text-yellow-300'}`}>
                    {o.status.toUpperCase()}
                  </span>
                </div>
                <div className="text-slate-400">
                  {o.data_gb} {t(language, 'catalog_gb')} {t(language, 'catalog_days').toLowerCase()} {o.duration_days}
                </div>
              </div>
              
              {o.status === 'activated' && (
                <button 
                  onClick={() => setSelectedOrderQr(o)}
                  className="glass-button px-4 py-2 text-sm"
                >
                  {t(language, 'profile_view_qr')}
                </button>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div className="glass-panel p-8 text-center text-slate-400">
          {t(language, 'profile_no_orders')}
        </div>
      )}

      {/* QR Code Modal */}
      <QRCodeModal 
        isOpen={!!selectedOrderQr}
        onClose={() => setSelectedOrderQr(null)}
        qrCodeBase64={selectedOrderQr?.esim_qr_code}
        iccid={selectedOrderQr?.esim_iccid}
        activationCode={selectedOrderQr?.esim_activation_code}
      />
    </div>
  );
};

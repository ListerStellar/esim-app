import { useEffect, useState } from 'react';
import { useAuthStore } from '../store/useAuthStore';
import { useNavigate } from 'react-router-dom';
import { LogOut } from 'lucide-react';
import { QRCodeModal } from '../components/QRCodeModal';
import { useAppStore } from '../store/useAppStore';
import { t } from '../locales';

export const Profile = () => {
  const { language } = useAppStore();
  const { user, logout, fetchUser, isAuthenticated } = useAuthStore();
  const navigate = useNavigate();
  const [selectedOrderQr, setSelectedOrderQr] = useState<any>(null);

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
              <div className="text-xs text-slate-500">ID</div>
              <div className="font-medium">{user.id} {user.telegram_id ? `(TG: ${user.telegram_id})` : ''}</div>
            </div>
            <div>
              <div className="text-xs text-slate-500">Email</div>
              <div className="font-medium break-all">{user.email || '—'}</div>
            </div>
          </div>
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

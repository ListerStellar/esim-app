import { useEffect, useState } from 'react';
import { api } from '../api/api';
import { useAuthStore } from '../store/useAuthStore';
import { useNavigate } from 'react-router-dom';
import { X, CreditCard, Wallet } from 'lucide-react';
import { QRCodeModal } from '../components/QRCodeModal';
import { useAppStore } from '../store/useAppStore';
import { t } from '../locales';

interface Plan {
  plan_id: string;
  country_code: string;
  country_name: string;
  data_gb: number;
  duration_days: number;
  price_eur: number;
}

export const Catalog = () => {
  const [countries, setCountries] = useState<string[]>([]);
  const [names, setNames] = useState<Record<string, string>>({});
  const [selectedCountry, setSelectedCountry] = useState<string | null>(null);
  const [plans, setPlans] = useState<Plan[]>([]);
  
  // Payment Modal state
  const [paymentPlan, setPaymentPlan] = useState<Plan | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  
  // QR Modal state
  const [qrData, setQrData] = useState<any>(null);

  const { language } = useAppStore();
  const { isAuthenticated, user } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        const res = await api.get('/catalog/countries');
        setCountries(res.data.countries);
        setNames(res.data.names);
      } catch (e) {
        console.error(e);
      }
    };
    fetchCountries();
  }, []);

  useEffect(() => {
    if (!selectedCountry) return;
    const fetchPlans = async () => {
      try {
        const res = await api.get(`/catalog/plans/${selectedCountry}`);
        setPlans(res.data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchPlans();
  }, [selectedCountry]);

  const initiatePayment = (plan: Plan) => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    setPaymentPlan(plan);
  };

  const handlePayWithBalance = async () => {
    if (!paymentPlan) return;
    setIsProcessing(true);
    try {
      const res = await api.post('/transactions/buy_with_balance', { plan_id: paymentPlan.plan_id });
      setPaymentPlan(null);
      useAuthStore.getState().fetchUser();
      
      // Show QR Modal
      setQrData(res.data);
    } catch (e: any) {
      alert(t(language, 'catalog_payment_failed') + ' ' + (e.response?.data?.detail || e.message));
    } finally {
      setIsProcessing(false);
    }
  };

  const handlePayWithStripe = async () => {
    if (!paymentPlan) return;
    setIsProcessing(true);
    try {
      const redirectUrl = window.location.origin + '/payment-success';
      const res = await api.post('/transactions/buy_with_stripe', { 
        plan_id: paymentPlan.plan_id,
        redirect_url: redirectUrl
      });
      
      if (res.data.payment_url) {
        window.location.href = res.data.payment_url;
      } else if (res.data.mock) {
        // Mock Stripe payment returned QR directly
        setPaymentPlan(null);
        useAuthStore.getState().fetchUser();
        setQrData(res.data);
      }
    } catch (e: any) {
      alert(t(language, 'catalog_payment_failed') + ' ' + (e.response?.data?.detail || e.message));
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="pb-24 pt-6 px-4 max-w-4xl mx-auto min-h-[calc(100vh-64px)] relative">
      <h2 className="text-3xl font-extrabold mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-indigo-100">
        {t(language, 'catalog_choose_country')}
      </h2>
      
      {!selectedCountry ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {countries.map(c => (
            <button
              key={c}
              onClick={() => setSelectedCountry(c)}
              className="glass-panel p-6 flex flex-col items-center justify-center gap-3 transition-transform hover:scale-105 active:scale-95"
            >
              <img src={`https://flagcdn.com/w80/${c.toLowerCase()}.png`} alt={names[c] || c} className="w-16 h-12 object-cover rounded-lg shadow-md mb-2" />
              <div className="font-semibold text-center">{names[c] || c}</div>
            </button>
          ))}
        </div>
      ) : (
        <div className="animate-in fade-in slide-in-from-bottom-4 duration-300">
          <button 
            onClick={() => setSelectedCountry(null)}
            className="mb-6 text-blue-300 hover:text-blue-100 flex items-center gap-2"
          >
            ← {t(language, 'catalog_back')}
          </button>
          <h3 className="text-2xl font-bold mb-6">{t(language, 'catalog_plans_for')} {names[selectedCountry]}</h3>
          <div className="grid sm:grid-cols-2 gap-4">
            {plans.map(p => (
              <div key={p.plan_id} className="glass-panel p-6 flex flex-col justify-between">
                <div>
                  <div className="text-3xl font-black mb-1">{p.data_gb} {t(language, 'catalog_gb')}</div>
                  <div className="text-slate-300 mb-4">{p.duration_days} {t(language, 'catalog_days')}</div>
                </div>
                <div className="flex items-center justify-between mt-4">
                  <div className="text-xl font-bold text-blue-200">€{p.price_eur}</div>
                  <button onClick={() => initiatePayment(p)} className="glass-button px-6 py-2">
                    {t(language, 'catalog_buy')}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Payment Selection Modal */}
      {paymentPlan && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="glass-panel p-6 w-full max-w-md relative animate-in zoom-in-95 duration-200">
            <button 
              onClick={() => !isProcessing && setPaymentPlan(null)}
              className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors"
              disabled={isProcessing}
            >
              <X size={24} />
            </button>
            <h3 className="text-2xl font-bold mb-2">{t(language, 'catalog_select_payment')}</h3>
            <p className="text-slate-400 mb-6">
              {t(language, 'catalog_you_are_buying', { country: paymentPlan.country_name, gb: paymentPlan.data_gb, price: paymentPlan.price_eur })}
            </p>
            
            <div className="space-y-3">
              <button
                onClick={handlePayWithBalance}
                disabled={isProcessing || (user?.balance || 0) < paymentPlan.price_eur}
                className="w-full flex items-center justify-between p-4 rounded-xl border border-white/10 hover:bg-white/5 transition-colors disabled:opacity-50 disabled:cursor-not-allowed group"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400">
                    <Wallet size={20} />
                  </div>
                  <div className="text-left">
                    <div className="font-bold">{t(language, 'catalog_pay_balance')}</div>
                    <div className="text-sm text-slate-400">{t(language, 'catalog_available')} €{(user?.balance || 0).toFixed(2)}</div>
                  </div>
                </div>
                {(user?.balance || 0) < paymentPlan.price_eur && (
                  <span className="text-xs text-red-400 font-medium">{t(language, 'catalog_insufficient')}</span>
                )}
              </button>
              
              <button
                onClick={handlePayWithStripe}
                disabled={isProcessing}
                className="w-full flex items-center gap-3 p-4 rounded-xl border border-white/10 hover:bg-white/5 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-400">
                  <CreditCard size={20} />
                </div>
                <div className="text-left font-bold">{t(language, 'catalog_pay_card')}</div>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* QR Code Modal */}
      <QRCodeModal 
        isOpen={!!qrData}
        onClose={() => setQrData(null)}
        qrCodeBase64={qrData?.qr_code_base64}
        iccid={qrData?.iccid}
        activationCode={qrData?.activation_code}
      />
    </div>
  );
};

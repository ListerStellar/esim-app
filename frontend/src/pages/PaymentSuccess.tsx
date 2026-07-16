import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { api } from '../api/api';
import { QRCodeModal } from '../components/QRCodeModal';
import { CheckCircle2, Loader2, XCircle } from 'lucide-react';
import { useAuthStore } from '../store/useAuthStore';
import { useAppStore } from '../store/useAppStore';
import { t } from '../locales';

export const PaymentSuccess = () => {
  const { language } = useAppStore();
  const [searchParams] = useSearchParams();
  const orderId = searchParams.get('order_id');
  const navigate = useNavigate();
  
  const [status, setStatus] = useState<'checking' | 'success' | 'error'>('checking');
  const [qrData, setQrData] = useState<any>(null);
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    if (!orderId) {
      setStatus('error');
      setErrorMsg('No order ID provided.');
      return;
    }

    let intervalId: any;
    let attempts = 0;
    const maxAttempts = 12; // 1 minute max (12 * 5s)

    const checkPayment = async () => {
      try {
        attempts++;
        const res = await api.get(`/transactions/check_payment/${orderId}`);
        if (res.data.status === 'activated' || res.data.success === true && res.data.qr_code_base64) {
          clearInterval(intervalId);
          setStatus('success');
          setQrData(res.data);
          useAuthStore.getState().fetchUser();
        } else if (res.data.status === 'failed') {
          clearInterval(intervalId);
          setStatus('error');
          setErrorMsg('Payment failed or cancelled.');
        } else if (attempts >= maxAttempts) {
          clearInterval(intervalId);
          setStatus('error');
          setErrorMsg('Payment confirmation took too long. Please check your profile later.');
        }
        // otherwise status is likely 'paid' or 'pending' and we keep polling
      } catch (e: any) {
        clearInterval(intervalId);
        setStatus('error');
        setErrorMsg('Error checking payment: ' + (e.response?.data?.detail || e.message));
      }
    };

    checkPayment();
    intervalId = setInterval(checkPayment, 5000);

    return () => clearInterval(intervalId);
  }, [orderId]);

  return (
    <div className="pb-24 pt-6 px-4 max-w-md mx-auto min-h-[calc(100vh-64px)] flex flex-col items-center justify-center relative">
      <div className="glass-panel p-8 w-full flex flex-col items-center text-center animate-in zoom-in-95 duration-300">
        
        {status === 'checking' && (
          <>
            <Loader2 size={64} className="text-blue-400 animate-spin mb-6" />
            <h2 className="text-2xl font-bold mb-2">{t(language, 'payment_checking')}</h2>
            <p className="text-slate-400">
              {t(language, 'payment_checking_desc')}
            </p>
          </>
        )}

        {status === 'success' && (
          <>
            <CheckCircle2 size={64} className="text-green-400 mb-6" />
            <h2 className="text-2xl font-bold mb-2">{t(language, 'payment_success_title')}</h2>
            <p className="text-slate-400 mb-6">
              {t(language, 'payment_success_subtitle')}
            </p>
            <div className="flex gap-4 w-full">
              <button 
                onClick={() => setQrData({...qrData, isOpen: true})}
                className="glass-button w-full py-3"
              >
                {t(language, 'profile_view_qr')}
              </button>
              <button 
                onClick={() => navigate('/profile')}
                className="glass-button-secondary w-full py-3"
              >
                {t(language, 'payment_success_btn')}
              </button>
            </div>
          </>
        )}

        {status === 'error' && (
          <>
            <XCircle size={64} className="text-red-400 mb-6" />
            <h2 className="text-2xl font-bold mb-2">{t(language, 'payment_error_title')}</h2>
            <p className="text-slate-400 mb-6">
              {errorMsg}
            </p>
            <button 
              onClick={() => navigate('/profile')}
              className="glass-button-secondary w-full py-3"
            >
              {t(language, 'payment_go_profile')}
            </button>
          </>
        )}
      </div>

      <QRCodeModal 
        isOpen={status === 'success' && !!qrData?.isOpen}
        onClose={() => setQrData({...qrData, isOpen: false})}
        qrCodeBase64={qrData?.qr_code_base64}
        iccid={qrData?.iccid}
        activationCode={qrData?.activation_code}
      />
    </div>
  );
};

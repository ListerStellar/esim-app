import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { api } from '../api/api';
import { CheckCircle2, XCircle, Loader2 } from 'lucide-react';

export const VerifyEmail = () => {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      setStatus('error');
      setMessage('Invalid verification link.');
      return;
    }

    const verifyToken = async () => {
      try {
        const res = await api.post('/auth/verify-email', { refresh_token: token });
        setStatus('success');
        setMessage(res.data.detail || 'Email successfully verified!');
        // Automatically redirect to login after 3 seconds
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      } catch (err: any) {
        setStatus('error');
        setMessage(err.response?.data?.detail || 'Failed to verify email. The link may be expired.');
      }
    };

    verifyToken();
  }, [token, navigate]);

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-120px)] px-4 mt-6">
      <div className="glass-panel p-8 w-full max-w-md flex flex-col items-center text-center">
        {status === 'loading' && (
          <>
            <Loader2 className="w-16 h-16 text-blue-500 animate-spin mb-6" />
            <h2 className="text-2xl font-bold text-white mb-2">Verifying...</h2>
            <p className="text-slate-400">Please wait while we verify your email address.</p>
          </>
        )}
        
        {status === 'success' && (
          <>
            <CheckCircle2 className="w-16 h-16 text-green-500 mb-6" />
            <h2 className="text-2xl font-bold text-white mb-2">Success!</h2>
            <p className="text-slate-400 mb-6">{message}</p>
            <p className="text-sm text-slate-500">Redirecting to login...</p>
          </>
        )}
        
        {status === 'error' && (
          <>
            <XCircle className="w-16 h-16 text-red-500 mb-6" />
            <h2 className="text-2xl font-bold text-white mb-2">Verification Failed</h2>
            <p className="text-slate-400 mb-8">{message}</p>
            <button 
              onClick={() => navigate('/login')}
              className="bg-blue-600 hover:bg-blue-500 text-white font-medium py-3 px-8 rounded-xl transition-colors shadow"
            >
              Back to Login
            </button>
          </>
        )}
      </div>
    </div>
  );
};

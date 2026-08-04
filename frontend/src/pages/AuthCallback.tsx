import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuthStore } from '../store/useAuthStore';

export const AuthCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login } = useAuthStore();

  useEffect(() => {
    const accessToken = searchParams.get('access_token');
    
    if (accessToken) {
      login(accessToken);
      navigate('/profile', { replace: true });
    } else {
      navigate('/login', { replace: true });
    }
  }, [searchParams, login, navigate]);

  return (
    <div className="flex items-center justify-center min-h-[50vh]">
      <div className="animate-pulse text-blue-400">Authenticating...</div>
    </div>
  );
};

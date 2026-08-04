import { useEffect, useRef } from 'react';

export const TelegramLoginWidget = ({ onAuth }: { onAuth: (user: any) => void }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    
    containerRef.current.innerHTML = '';
    
    (window as any).onTelegramAuth = (user: any) => {
      onAuth(user);
    };

    const script = document.createElement('script');
    script.src = 'https://telegram.org/js/telegram-widget.js?22';
    // Import bot username from env or use fallback
    script.setAttribute('data-telegram-login', import.meta.env.VITE_TELEGRAM_BOT_USERNAME || 'esim_advance_bot');
    script.setAttribute('data-size', 'large');
    script.setAttribute('data-onauth', 'onTelegramAuth(user)');
    script.setAttribute('data-request-access', 'write');
    script.async = true;

    containerRef.current.appendChild(script);
  }, [onAuth]);

  return <div ref={containerRef} className="flex justify-center" />;
};

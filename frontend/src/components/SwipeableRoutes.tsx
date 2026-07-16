import { useState } from 'react';
import type { TouchEvent, ReactNode } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/useAuthStore';

interface SwipeableRoutesProps {
  children: ReactNode;
}

export const SwipeableRoutes = ({ children }: SwipeableRoutesProps) => {
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);
  
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const { isAuthenticated } = useAuthStore();
  
  // The ordered tabs for mobile navigation
  const mobilePaths = ['/', '/catalog', '/how-to-install', '/support', isAuthenticated ? '/profile' : '/login'];
  
  const minSwipeDistance = 75; 
  
  const handleTouchStart = (e: TouchEvent) => {
    // Only handle single touch
    if (e.targetTouches.length !== 1) return;
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };
  
  const handleTouchMove = (e: TouchEvent) => {
    if (e.targetTouches.length !== 1) return;
    setTouchEnd(e.targetTouches[0].clientX);
  };
  
  const handleTouchEnd = (e: TouchEvent) => {
    if (!touchStart || !touchEnd) return;
    
    // Ignore swipes that started on inputs or buttons if we want to be safe, 
    // but a global swipe is usually fine as long as distance is large enough.
    const target = e.target as HTMLElement;
    if (['INPUT', 'TEXTAREA', 'BUTTON'].includes(target.tagName) || target.closest('button')) {
      return;
    }

    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;
    
    if (isLeftSwipe || isRightSwipe) {
      const normalizedPathname = (pathname === '/login' && isAuthenticated) ? '/profile' : pathname;
      const currentIndex = mobilePaths.indexOf(normalizedPathname);
      
      if (currentIndex === -1) return; // not on a main tab
      
      if (isLeftSwipe && currentIndex < mobilePaths.length - 1) {
        // Swipe left -> go right
        navigate(mobilePaths[currentIndex + 1]);
      } else if (isRightSwipe && currentIndex > 0) {
        // Swipe right -> go left
        navigate(mobilePaths[currentIndex - 1]);
      }
    }
  };

  return (
    <div 
      onTouchStart={handleTouchStart} 
      onTouchMove={handleTouchMove} 
      onTouchEnd={handleTouchEnd}
      className="flex-grow flex flex-col w-full h-full"
    >
      {children}
    </div>
  );
};

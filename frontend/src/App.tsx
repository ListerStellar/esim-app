import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Landing } from './pages/Landing';
import { Catalog } from './pages/Catalog';
import { HowToInstall } from './pages/HowToInstall';
import { Support } from './pages/Support';
import { Login } from './pages/Login';
import { Profile } from './pages/Profile';
import { PaymentSuccess } from './pages/PaymentSuccess';
import { VerifyEmail } from './pages/VerifyEmail';
import { AuthCallback } from './pages/AuthCallback';
import { useEffect } from 'react';
import { useAuthStore } from './store/useAuthStore';
import { SwipeableRoutes } from './components/SwipeableRoutes';

function App() {
  const { fetchUser, isAuthenticated } = useAuthStore();

  useEffect(() => {
    if (isAuthenticated) {
      fetchUser();
    }
  }, [isAuthenticated]);

  return (
    <BrowserRouter>
      <div className="fixed inset-0 bg-app-bg -z-50 pointer-events-none"></div>
      <div className="min-h-screen flex flex-col relative z-0">
        <Navbar />
        <main className="flex-grow pt-12 pb-24 md:pt-28 md:pb-8 flex flex-col">
          <SwipeableRoutes>
            <Routes>
              <Route path="/" element={<Landing />} />
              <Route path="/catalog" element={<Catalog />} />
              <Route path="/how-to-install" element={<HowToInstall />} />
              <Route path="/support" element={<Support />} />
              <Route path="/login" element={<Login />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/payment-success" element={<PaymentSuccess />} />
              <Route path="/verify-email" element={<VerifyEmail />} />
              <Route path="/auth-callback" element={<AuthCallback />} />
            </Routes>
          </SwipeableRoutes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;

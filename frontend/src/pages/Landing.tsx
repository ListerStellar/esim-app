import { Link } from 'react-router-dom';

export const Landing = () => {
  return (
    <div className="relative min-h-[calc(100vh-64px)] flex flex-col justify-center items-center px-6 pb-24 text-center">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0 w-full h-full -top-24 md:-top-28 -z-10 overflow-hidden pointer-events-none">
        <img 
          src="/hero.png" 
          alt="Abstract Globe and SIM" 
          className="w-full h-full object-cover opacity-60 blur-3xl [mask-image:radial-gradient(ellipse_at_center,black_40%,transparent_80%)] md:[mask-image:radial-gradient(ellipse_at_center,black_40%,transparent_80%)]"
        />
      </div>

      <div className="relative z-10 max-w-3xl mx-auto space-y-8">
        <h1 className="text-5xl md:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-300 to-indigo-100 drop-shadow-lg">
          ADVANCE eSIM
        </h1>
        
        <p className="text-xl md:text-2xl text-blue-100/90 font-light max-w-2xl mx-auto">
          Instant mobile internet in over 50+ countries. 
          Connect globally without roaming charges.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mt-8">
          <Link to="/catalog" className="glass-button px-10 py-4 text-lg font-bold w-full sm:w-auto">
            View eSIM Plans
          </Link>
          <Link to="/how-to-install" className="glass-button-secondary px-8 py-4 text-lg font-medium w-full sm:w-auto">
            How it works
          </Link>
        </div>

        <div className="grid grid-cols-3 gap-6 pt-16">
          <div>
            <div className="text-4xl font-black text-blue-400 mb-2">50+</div>
            <div className="text-sm text-slate-300 uppercase tracking-wider">Countries</div>
          </div>
          <div>
            <div className="text-4xl font-black text-blue-400 mb-2">⚡️</div>
            <div className="text-sm text-slate-300 uppercase tracking-wider">Instant Setup</div>
          </div>
          <div>
            <div className="text-4xl font-black text-blue-400 mb-2">3x</div>
            <div className="text-sm text-slate-300 uppercase tracking-wider">Cheaper</div>
          </div>
        </div>
      </div>
    </div>
  );
};

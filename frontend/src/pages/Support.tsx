export const Support = () => {
  return (
    <div className="pb-24 pt-6 px-4 max-w-2xl mx-auto min-h-[calc(100vh-64px)] flex flex-col justify-center items-center text-center">
      <div className="glass-panel p-10 w-full">
        <div className="text-5xl mb-6">💬</div>
        <h2 className="text-3xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-indigo-100">
          Support
        </h2>
        <p className="text-slate-300 mb-2">
          Working hours: 9:00–21:00 (CET)
        </p>
        <p className="text-slate-400 text-sm mb-8">
          Average response time is 30 minutes.
        </p>
        <a 
          href="https://t.me/esim_support" 
          target="_blank" 
          rel="noopener noreferrer"
          className="glass-button px-8 py-3 w-full sm:w-auto inline-flex"
        >
          Contact on Telegram
        </a>
      </div>
    </div>
  );
};

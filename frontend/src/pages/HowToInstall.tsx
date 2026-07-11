export const HowToInstall = () => {
  return (
    <div className="pb-24 pt-6 px-4 max-w-2xl mx-auto min-h-[calc(100vh-64px)]">
      <h2 className="text-3xl font-extrabold mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-indigo-100">
        How to install eSIM
      </h2>

      <div className="space-y-6">
        <div className="glass-panel p-8">
          <h3 className="text-xl font-bold mb-4 text-blue-200">iPhone (iOS 12.1+)</h3>
          <ol className="list-decimal list-inside space-y-2 text-slate-300">
            <li>Open <b>Settings</b> &rarr; <b>Cellular</b></li>
            <li>Tap <b>Add Cellular Plan</b> or <b>Add eSIM</b></li>
            <li>Scan the QR Code provided in your Profile</li>
          </ol>
        </div>

        <div className="glass-panel p-8">
          <h3 className="text-xl font-bold mb-4 text-blue-200">Android</h3>
          <ol className="list-decimal list-inside space-y-2 text-slate-300">
            <li>Open <b>Settings</b> &rarr; <b>Connections</b> &rarr; <b>SIM Manager</b></li>
            <li>Tap <b>Add Mobile Plan</b> or <b>Add eSIM</b></li>
            <li>Scan the QR Code provided in your Profile</li>
          </ol>
        </div>

        <div className="glass-panel p-8 border-yellow-500/30 bg-yellow-500/5">
          <h3 className="text-lg font-bold mb-2 text-yellow-300 flex items-center gap-2">
            ⚠️ Important
          </h3>
          <ul className="list-disc list-inside space-y-1 text-yellow-100/70 text-sm">
            <li>Your phone must support eSIM functionality.</li>
            <li>Your device must be unlocked from the carrier.</li>
            <li>Wi-Fi or mobile data is required during the activation process.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

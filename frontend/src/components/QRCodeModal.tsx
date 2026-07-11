import { X } from 'lucide-react';

interface QRCodeModalProps {
  isOpen: boolean;
  onClose: () => void;
  qrCodeBase64?: string;
  iccid?: string;
  activationCode?: string;
}

export const QRCodeModal = ({ isOpen, onClose, qrCodeBase64, iccid, activationCode }: QRCodeModalProps) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="glass-panel p-6 w-full max-w-sm flex flex-col items-center relative animate-in zoom-in-95 duration-200">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors"
        >
          <X size={24} />
        </button>
        
        <h3 className="text-xl font-bold mb-4">Install Your eSIM</h3>
        
        {qrCodeBase64 ? (
          <div className="bg-white p-2 rounded-xl mb-6 shadow-xl">
            <img 
              src={`data:image/png;base64,${qrCodeBase64}`} 
              alt="eSIM QR Code" 
              className="w-48 h-48"
            />
          </div>
        ) : (
          <div className="w-48 h-48 bg-slate-800 rounded-xl mb-6 flex items-center justify-center text-slate-500">
            No QR Code
          </div>
        )}

        <div className="w-full space-y-3 text-sm">
          <div>
            <div className="text-slate-400 mb-1">ICCID</div>
            <div className="font-mono bg-black/20 p-2 rounded text-center border border-white/5 break-all text-[11px]">
              {iccid || '—'}
            </div>
          </div>
          <div>
            <div className="text-slate-400 mb-1">Activation Code</div>
            <div className="font-mono bg-black/20 p-2 rounded text-center border border-white/5 break-all text-[11px]">
              {activationCode || '—'}
            </div>
          </div>
        </div>

        <p className="text-slate-400 text-xs mt-6 text-center">
          Go to Settings &gt; Cellular &gt; Add eSIM on your device and scan this QR code.
        </p>
      </div>
    </div>
  );
};

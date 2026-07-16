import { useAppStore } from '../store/useAppStore';
import { t } from '../locales';

export const HowToInstall = () => {
  const { language } = useAppStore();
  return (
    <div className="pb-24 pt-6 px-4 max-w-2xl mx-auto min-h-[calc(100vh-64px)]">
      <h2 className="text-3xl font-extrabold mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-indigo-100">
        {t(language, 'install_title')}
      </h2>

      <div className="space-y-6">
        <div className="glass-panel p-8">
          <h3 className="text-xl font-bold mb-4 text-blue-200">{t(language, 'install_iphone')}</h3>
          <ul className="list-none space-y-2 text-slate-300">
            <li>{t(language, 'install_iphone_1')}</li>
            <li>{t(language, 'install_iphone_2')}</li>
            <li>{t(language, 'install_iphone_3')}</li>
          </ul>
        </div>

        <div className="glass-panel p-8">
          <h3 className="text-xl font-bold mb-4 text-blue-200">{t(language, 'install_android')}</h3>
          <ul className="list-none space-y-2 text-slate-300">
            <li>{t(language, 'install_android_1')}</li>
            <li>{t(language, 'install_android_2')}</li>
            <li>{t(language, 'install_android_3')}</li>
          </ul>
        </div>

        <div className="glass-panel p-8 border-yellow-500/30 bg-yellow-500/5">
          <h3 className="text-lg font-bold mb-2 text-yellow-300 flex items-center gap-2">
            ⚠️ {t(language, 'install_important')}
          </h3>
          <ul className="list-none space-y-1 text-yellow-100/70 text-sm">
            <li>{t(language, 'install_important_1')}</li>
            <li>{t(language, 'install_important_2')}</li>
            <li>{t(language, 'install_important_3')}</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

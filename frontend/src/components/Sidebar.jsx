import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import { Leaf, LayoutDashboard, Search, FileText, Settings as SettingsIcon } from 'lucide-react';
import { LanguageContext } from '../context/LanguageContext';

const Sidebar = () => {
  const { t } = useContext(LanguageContext);

  const navItems = [
    { path: '/dashboard', icon: <LayoutDashboard size={20} />, label: t('nav.dashboard') },
    { path: '/detect', icon: <Search size={20} />, label: t('nav.detect') },
    { path: '/report', icon: <FileText size={20} />, label: t('nav.report') },
    { path: '/settings', icon: <SettingsIcon size={20} />, label: t('nav.settings') },
  ];

  return (
    <aside className="w-64 h-screen fixed left-0 top-0 pt-20 border-r border-slate-700/50 bg-slate-900/50 backdrop-blur-xl z-30 hidden md:block">
      <div className="flex flex-col gap-2 p-4">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                isActive
                  ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`
            }
          >
            {item.icon}
            <span className="font-medium">{item.label}</span>
          </NavLink>
        ))}
      </div>
    </aside>
  );
};

export default Sidebar;

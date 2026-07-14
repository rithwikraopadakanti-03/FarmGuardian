import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Leaf, LogOut } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import { LanguageContext } from '../context/LanguageContext';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const { t } = useContext(LanguageContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="fixed top-0 left-0 w-full z-40 bg-slate-900/80 backdrop-blur-xl border-b border-slate-700/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center text-white shadow-lg shadow-green-500/20 group-hover:shadow-green-500/40 transition-all duration-300">
            <Leaf size={24} />
          </div>
          <span className="text-xl font-bold font-heading text-white tracking-tight">
            Farm<span className="text-green-400">Guardian</span>
          </span>
        </Link>

        <div className="flex items-center gap-4">
          {user ? (
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors"
            >
              <LogOut size={18} />
              <span className="hidden sm:block text-sm font-medium">{t('nav.logout')}</span>
            </button>
          ) : (
            <Link to="/login" className="btn-primary py-2 px-4 text-sm">
              <span>{t('nav.login')}</span>
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

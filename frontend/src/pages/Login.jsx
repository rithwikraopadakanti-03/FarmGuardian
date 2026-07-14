import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Leaf, LogIn, ArrowRight } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import { LanguageContext } from '../context/LanguageContext';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login, guestLogin } = useContext(AuthContext);
  const { t } = useContext(LanguageContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (err) {
      setError(t('common.error') + ': Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  const handleGuest = async () => {
    setLoading(true);
    try {
      await guestLogin();
      navigate('/dashboard');
    } catch (err) {
      setError(t('common.error'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden">
      <div className="hero-bg-circle bg-green-500/20 w-96 h-96 -top-20 -left-20"></div>
      
      <div className="glass-card w-full max-w-md p-8 relative z-10 animate-scale-in">
        <div className="flex flex-col items-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center text-white shadow-lg mb-4">
            <Leaf size={28} />
          </div>
          <h2 className="text-3xl font-bold font-heading text-white mb-2">{t('auth.login_title')}</h2>
          <p className="text-slate-400">{t('auth.login_subtitle')}</p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/50 text-red-400 text-sm text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">{t('auth.username')}</label>
            <input
              type="text"
              required
              className="input-field"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">{t('auth.password')}</label>
            <input
              type="password"
              required
              className="input-field"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button type="submit" disabled={loading} className="btn-primary w-full justify-center mt-2">
            {loading ? <div className="spinner w-5 h-5 border-2"></div> : (
              <>
                <LogIn size={18} />
                <span>{t('auth.login_btn')}</span>
              </>
            )}
          </button>
        </form>

        <div className="mt-8 relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-slate-700/50"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-4 bg-slate-900/50 text-slate-400">{t('auth.or')}</span>
          </div>
        </div>

        <button 
          onClick={handleGuest}
          disabled={loading}
          className="w-full mt-8 btn-secondary justify-center group"
        >
          <span>{t('auth.guest_mode')}</span>
          <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
        </button>

        <p className="mt-8 text-center text-sm text-slate-400">
          {t('auth.no_account')} <Link to="/register" className="text-green-400 hover:text-green-300 font-medium">{t('auth.register_btn')}</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;

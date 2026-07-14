import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Leaf, UserPlus } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import { LanguageContext } from '../context/LanguageContext';

const Register = () => {
  const [formData, setFormData] = useState({ username: '', email: '', password: '', confirm: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { register } = useContext(AuthContext);
  const { t } = useContext(LanguageContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (formData.password !== formData.confirm) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    try {
      await register(formData.username, formData.email, formData.password);
      navigate('/dashboard');
    } catch (err) {
      setError(t('common.error') + ': Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => setFormData({...formData, [e.target.name]: e.target.value});

  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden">
      <div className="hero-bg-circle bg-blue-500/20 w-96 h-96 -bottom-20 -right-20"></div>
      
      <div className="glass-card w-full max-w-md p-8 relative z-10 animate-scale-in">
        <div className="flex flex-col items-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center text-white shadow-lg mb-4">
            <Leaf size={28} />
          </div>
          <h2 className="text-3xl font-bold font-heading text-white mb-2">{t('auth.register_title')}</h2>
          <p className="text-slate-400">{t('auth.register_subtitle')}</p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/50 text-red-400 text-sm text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">{t('auth.username')}</label>
            <input type="text" name="username" required className="input-field" onChange={handleChange} />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">{t('auth.email')}</label>
            <input type="email" name="email" required className="input-field" onChange={handleChange} />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">{t('auth.password')}</label>
            <input type="password" name="password" required className="input-field" onChange={handleChange} />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">{t('auth.confirm_password')}</label>
            <input type="password" name="confirm" required className="input-field" onChange={handleChange} />
          </div>

          <button type="submit" disabled={loading} className="btn-primary w-full justify-center mt-4">
            {loading ? <div className="spinner w-5 h-5 border-2"></div> : (
              <>
                <UserPlus size={18} />
                <span>{t('auth.register_btn')}</span>
              </>
            )}
          </button>
        </form>

        <p className="mt-8 text-center text-sm text-slate-400">
          {t('auth.have_account')} <Link to="/login" className="text-green-400 hover:text-green-300 font-medium">{t('auth.login_btn')}</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;

import React, { createContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const isGuest = localStorage.getItem('isGuest') === 'true';
    if (token) {
      setUser({ token, isGuest });
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      const response = await authAPI.login({ username, password });
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      localStorage.removeItem('isGuest');
      setUser({ token: access_token, isGuest: false });
      return true;
    } catch (error) {
      console.error('Login failed', error);
      throw error;
    }
  };

  const register = async (username, email, password) => {
    try {
      const response = await authAPI.register({ username, email, password });
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      localStorage.removeItem('isGuest');
      setUser({ token: access_token, isGuest: false });
      return true;
    } catch (error) {
      console.error('Registration failed', error);
      throw error;
    }
  };

  const guestLogin = async () => {
    try {
      const response = await authAPI.guestLogin();
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      localStorage.setItem('isGuest', 'true');
      setUser({ token: access_token, isGuest: true });
      return true;
    } catch (error) {
      console.error('Guest login failed', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('isGuest');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, guestLogin, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

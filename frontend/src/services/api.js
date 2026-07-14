import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

// Add a request interceptor to include the auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  guestLogin: () => api.post('/auth/guest'),
};

export const predictAPI = {
  predictDisease: (formData) => api.post('/predict/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  analyzeSeverity: (formData) => api.post('/severity/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
};

export const reportAPI = {
  generateFieldReport: (formData) => api.post('/field-report/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
};

export const healthAPI = {
  check: () => api.get('/health/'),
};

export default api;

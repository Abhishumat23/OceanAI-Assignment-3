import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
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

// Auth API
export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => {
    const formData = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);
    return api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getMe: () => api.get('/api/auth/me'),
};

// Projects API
export const projectsAPI = {
  getAll: () => api.get('/api/projects'),
  getById: (id) => api.get(`/api/projects/${id}`),
  create: (data) => api.post('/api/projects', data),
  update: (id, data) => api.put(`/api/projects/${id}`, data),
  delete: (id) => api.delete(`/api/projects/${id}`),
  generateContent: (id) => api.post(`/api/projects/${id}/generate`),
};

// Sections API
export const sectionsAPI = {
  update: (id, data) => api.put(`/api/sections/${id}`, data),
  refine: (id, data) => api.post(`/api/sections/${id}/refine`, data),
  addFeedback: (id, data) => api.post(`/api/sections/${id}/feedback`, data),
  getRefinements: (id) => api.get(`/api/sections/${id}/refinements`),
};

// Export API
export const exportAPI = {
  exportDocument: (id) => {
    return api.get(`/api/export/${id}`, {
      responseType: 'blob',
    });
  },
};

export default api;

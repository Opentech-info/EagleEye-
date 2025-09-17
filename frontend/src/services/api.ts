import axios, { AxiosInstance } from 'axios';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
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

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      // Don't redirect here - let the AuthContext handle it
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials: { username: string; password: string }) =>
    api.post('/auth/login', credentials),
  
  register: (userData: {
    username: string;
    email: string;
    password: string;
    full_name?: string;
  }) => api.post('/auth/register', userData),
  
  getProfile: () => api.get('/auth/profile'),
  
  updateProfile: (profileData: any) => api.put('/auth/profile', profileData),
};

// YouTube API
export const youtubeAPI = {
  search: (query: string, limit: number = 20) =>
    api.post('/youtube/search', { query, limit }),
  
  getVideoInfo: (url: string) =>
    api.post('/youtube/info', { url }),
  
  download: (data: {
    url: string;
    quality?: string;
    type?: 'video' | 'audio' | 'video+audio';
  }) => api.post('/youtube/download', data),
};

// Torrent API
export const torrentAPI = {
  search: (query: string) =>
    api.post('/torrent/search', { query }),
  
  getPopular: (category: string = 'movies') =>
    api.get(`/torrent/popular?category=${category}`),
  
  launch: () => api.post('/torrent/launch'),
};

// Media API
export const mediaAPI = {
  stream: (data: { url: string; type?: 'video' | 'audio' }) =>
    api.post('/media/stream', data),
  
  getFormats: (url: string) =>
    api.post('/media/formats', { url }),
};

// Downloads API
export const downloadsAPI = {
  getAll: () => api.get('/downloads'),
  
  delete: (downloadId: number) => api.delete(`/downloads/${downloadId}`),
  
  downloadFile: (downloadId: number) =>
    api.get(`/downloads/${downloadId}/file`, { responseType: 'blob' }),
};

// System API
export const systemAPI = {
  getInfo: () => api.get('/system/info'),
  
  health: () => api.get('/health'),
};

// Export the main api instance
export default api;

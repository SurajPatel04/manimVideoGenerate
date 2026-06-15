import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || import.meta.env.VITE_BACKEND_URL || '';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 seconds timeout
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

let isRefreshing = false;
let failedQueue: any[] = [];

const processQueue = (error: any) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve();
    }
  });
  failedQueue = [];
};

export const refreshToken = async (): Promise<void> => {
  if (isRefreshing) {
    return new Promise(function (resolve, reject) {
      failedQueue.push({ resolve, reject });
    });
  }

  isRefreshing = true;
  try {
    await api.post("/api/user/refresh");
    processQueue(null);
  } catch (err) {
    processQueue(err);
    if (
      !window.location.pathname.includes("/login") &&
      !window.location.pathname.includes("/signup")
    ) {
      // Clear legacy local storage just in case
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
      
      window.location.href = "/login";
    }
    return Promise.reject(err);
  } finally {
    isRefreshing = false;
  }
};

// Response interceptor to handle common errors and token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Prevent infinite loops if the refresh endpoint itself fails with 401
    if (originalRequest.url === "/api/user/refresh") {
      return Promise.reject(error);
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        await refreshToken();
        // Retry original request
        return api(originalRequest);
      } catch (err) {
        return Promise.reject(err);
      }
    }

    if (error.response) {
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      console.error('Network Error:', error.request);
    } else {
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;

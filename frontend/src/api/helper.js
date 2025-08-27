// axios wrapper
import axios from 'axios';

const BACKEND_URL = import.meta.env.BACKEND_API_URL || '';
const API_URL = `${BACKEND_URL}/api`;
console.log('BACKEND_URL', API_URL);

const api = axios.create({
  baseURL: API_URL,
});

// Function to set auth token in headers
export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

// Helper function to check if user has valid tokens
export const hasValidTokens = () => {
  const accessToken = localStorage.getItem('access_token');
  const refreshToken = localStorage.getItem('refresh_token');
  return !!(accessToken && refreshToken);
};

// Function to clear all tokens
const clearTokens = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  setAuthToken(null);
};

// Function to refresh access token
const refreshAccessToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  
  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  try {
    const response = await axios.post('/api/users/refresh', {}, {
      headers: { Authorization: `Bearer ${refreshToken}` }
    });

    // Store new tokens
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('refresh_token', response.data.refresh_token);
    
    // Update axios headers with new access token
    setAuthToken(response.data.access_token);
    
    return response.data.access_token;
  } catch (error) {
    // Refresh failed, clear tokens
    clearTokens();
    throw error;
  }
};

// Helper function to manually clear tokens (for logout)
export const clearAllTokens = clearTokens;

// Attach access token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

// Add interceptor to handle token expiration and refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Check if error is 401 and we haven't already tried to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Try to refresh the token
        const newAccessToken = await refreshAccessToken();
        
        // Retry the original request with new token
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
        return api.request(originalRequest);
        
      } catch (refreshError) {
        // Refresh failed, redirect to login
        console.error('Token refresh failed:', refreshError);
        clearTokens();
        
        // Only redirect if we're not already on the login page
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
        
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export async function callApi(endpointWithMethod, data = null) {
  const [method, endpoint] = endpointWithMethod.split(':');
  
  const config = {};
  let response;
  try {
    if (method.toLowerCase() === 'get' || method.toLowerCase() === 'delete') {
      // For GET or DELETE, data is treated as query params
      config.params = data;
      response = await api.request({ method, url: endpoint, ...config });
    } else {
      // For POST, PUT, PATCH, data is the request body
      response = await api.request({ method, url: endpoint, data, ...config });
    }
    return response.data;
  } catch (error) {
    // You can customize error handling here
    console.error('API error:', error);
    throw error;
  }
}

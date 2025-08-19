import React, { createContext, useState, useContext, useEffect } from 'react';
import { callApi } from '../api/helper';
import { loginUser, registerUser } from '../api/actions'; // Import both functions

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('access_token'));

  // Set token in axios headers when token changes
  useEffect(() => {
    if (token) {
      // Add token to axios defaults
      import('../api/helper').then(({ setAuthToken }) => {
        setAuthToken(token);
      });
    }
  }, [token]);

  // Check if user is logged in on app start
  useEffect(() => {
    const checkAuth = async () => {
      const storedAccessToken = localStorage.getItem('access_token');
      const storedRefreshToken = localStorage.getItem('refresh_token');
      
      if (storedAccessToken && storedRefreshToken) {
        try {
          setToken(storedAccessToken);
          // Verify token is still valid by fetching user data
          const userData = await callApi('get:/users/me');
          setUser(userData);
          console.log('Auth check successful:', userData);
        } catch (error) {
          console.error('Auth check failed:', error);
          
          // If it's a 401, let the refresh token interceptor handle it
          if (error.response?.status === 401) {
            // The interceptor will try to refresh the token
            // If refresh fails, it will clear tokens and redirect
            console.log('Token expired, refresh interceptor will handle it');
          } else {
            // For other errors (403, 500, etc.), clear tokens
            console.log('Clearing tokens due to non-401 error');
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            setToken(null);
            setUser(null);
          }
        }
      } else {
        console.log('No stored tokens found');
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const response = await loginUser(email, password); // Use your existing function
      
      // Store both tokens
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
      setToken(response.access_token);
      setUser(response.user);
      
      return { success: true, user: response.user };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  };

  const register = async (username, email, password) => {
    try {
      const response = await registerUser(username, email, password); // Use your existing function
      return { success: true, message: 'Registration successful' };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Registration failed' };
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setToken(null);
    setUser(null);
  };

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

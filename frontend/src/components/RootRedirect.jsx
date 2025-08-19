import React, { useEffect } from 'react';
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';
import HomePage from '../pages/HomePage/HomePage';

const RootRedirect = () => {
  const { isAuthenticated, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading) {
      console.log("auth value:", isAuthenticated)
      if (isAuthenticated) {
        // User is logged in, redirect to /home
        navigate('/home', { replace: true });
      }
      // If not authenticated, stay on current page (shows HomePage)
    }
  }, [isAuthenticated, loading, navigate]);

  // Show loading while checking auth status
  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        Loading...
      </div>
    );
  }

  // If not authenticated, show the public HomePage
  return <HomePage />;
};

export default RootRedirect;

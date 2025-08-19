import React from 'react';
import { useAuth } from '../../components/AuthContext'; // Adjust path as needed
import { useNavigate } from 'react-router-dom';

const MainApp = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    // Call logout from auth context
    logout();
    
    // Optional: Navigate to login page (though ProtectedRoute will handle this)
    navigate('/login');
    
    console.log('User logged out successfully');
  };

  return (
    <div className="main-app-container">
      <h1>Welcome to the Main Application!</h1>
      {user && <p>Hello, {user.username}!</p>}
      <p>This is where your main content will go after successful login.</p>
      <button onClick={handleLogout} className="logout-button">
        Logout
      </button>
    </div>
  );
};

export default MainApp;

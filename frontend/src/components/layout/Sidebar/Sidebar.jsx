import React, { useState } from 'react';
import SidebarOptions from './SidebarOptions';
import './Sidebar.scss';
import { useAuth } from '../../AuthContext';
import { MoreVertical, CircleFadingPlus  } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Sidebar = ({ sidebar, currentPath }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [showLogoutPopup, setShowLogoutPopup] = useState(false);

  console.log("image came:", user?.profile_image)
  
  const handlePost = () => {
    console.log('Post button clicked');
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
    console.log('User logged out successfully');
  };

  const toggleLogoutPopup = () => {
    setShowLogoutPopup(!showLogoutPopup);
  };

  return (
    <div className="sidebar">
      <div className="logo">
        <h1 className="logo-text">CookNet</h1>
      </div>
      <nav className="navigation">
        {sidebar.map((sidebarOptions, index) => (
          <SidebarOptions key={index} {...sidebarOptions} currentPath={currentPath} />
        ))}
        <div className='bottom-nav'>
          <button onClick={handlePost}><CircleFadingPlus size={16} />Create Post</button>
          <div className='profile-section'>
            <div className='profile-container'>
              <div className='profile-info'>
                <img src={user.profile_image} alt={user.username} className='profile-image' referrerPolicy="no-referrer" />
                <p className='profile-username'>{user?.username}</p>
              </div>
              <div className='more-options-container'>
                <MoreVertical 
                  size={20} 
                  className='more-options-icon' 
                  onClick={toggleLogoutPopup} 
                />
              </div>
            </div>
            {showLogoutPopup && (
              <div className='logout-button-container'>
                <button onClick={handleLogout}>Logout</button>
              </div>
            )}
          </div>
        </div>
      </nav>
    </div>
  );
};

export default Sidebar;

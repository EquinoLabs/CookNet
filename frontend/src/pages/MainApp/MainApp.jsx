import React, { useState, useEffect } from 'react';
import { useAuth } from '../../components/AuthContext';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/layout/Navbar/Navbar';
import Sidebar from '../../components/layout/Sidebar/Sidebar';
import Feed from '../../components/mainapp/Feed/Feed';
import Communities from '../../components/mainapp/Communities/Communities';
import PersonalDashboard from '../../components/mainapp/PersonalDashboard.jsx/PersonalDashboard';
import SavedRecipes from '../../components/mainapp/SavedRecipes.jsx/SavedRecipes';
import Friends from '../../components/mainapp/Friends/Friends';
import SettingsPage from '../../components/mainapp/Settings/Settings';
import DiscoverSidebar from '../../components/layout/DiscoverSidebar/DiscoverSidebar';
import { House, Users, LayoutDashboard, Bookmark, Handshake, Settings } from "lucide-react";
import './MainApp.scss';


const sidebarData = [
  { name: "Feed", icon: House, path: "/feed", component: Feed },
  { name: "Communities", icon: Users, path: "/communities", component: Communities },
  { name: "Personal Dashboard", icon: LayoutDashboard, path: "/dashboard", component: PersonalDashboard },
  { name: "Saved Recipes", icon: Bookmark, path: "/saved", component: SavedRecipes },
  { name: "Friends", icon: Handshake, path: "/friends", component: Friends },
  { name: "Settings", icon: Settings, path: "/settings", component: SettingsPage },
];

const MainApp = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [currentPath, setCurrentPath] = useState(window.location.pathname);

  useEffect(() => {
    const handleLocationChange = () => {
      setCurrentPath(window.location.pathname);
    };
    
    window.addEventListener('popstate', handleLocationChange);
    return () => window.removeEventListener('popstate', handleLocationChange);
  }, []);

  const getCurrentComponent = () => {
    const currentItem = sidebarData.find(item => currentPath.startsWith(item.path));
    return currentItem ? currentItem.component : Feed; // Default to Feed if no match
  };

  const CurrentComponent = getCurrentComponent();

  return (
    <div className="main-app">
      <div className='sidebar-main'>
        <Sidebar sidebar={sidebarData} currentPath={currentPath} />
      </div>
      <div className="main-content-container">
        <main className="main-content">
          <CurrentComponent />
        </main>
        {CurrentComponent !== PersonalDashboard && (
          <aside className="discover-sidebar-main">
            <DiscoverSidebar />
          </aside>
        )}
      </div>
    </div>
  );
};

export default MainApp;

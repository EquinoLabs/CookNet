import React from 'react';
import SidebarOptions from './SidebarOptions';
import './Sidebar.scss';

const Sidebar = ({ sidebar, currentPath }) => {

  if (sidebar) {
    console.log("data", sidebar)
  }

  return (
    <div className="sidebar">
      <div className="logo">
        <h1 className="logo-text">CookNet</h1>
      </div>
      <nav className="navigation">
        {sidebar.map((sidebarOptions, index) => (
          <SidebarOptions key={index} {...sidebarOptions} currentPath={currentPath} />
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;
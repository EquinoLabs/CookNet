import React from 'react';
import './DiscoverSidebar.scss';

const DiscoverSidebar = () => {
  return (
    <div className="discover-sidebar">
      <h2>Discover</h2>
      <div className="suggested-communities">
        <h3>Suggested Communities</h3>
        <ul>
          <li>Community 1</li>
          <li>Community 2</li>
          <li>Community 3</li>
        </ul>
      </div>
      
      <div className="suggested-recipes">
        <h3>Suggested Recipes</h3>
        <ul>
          <li>Recipe A</li>
          <li>Recipe B</li>
          <li>Recipe C</li>
        </ul>
      </div>
    </div>
  );
};

export default DiscoverSidebar;

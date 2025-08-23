import React from 'react';

const PersonalDashboard = () => {
  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Personal Dashboard</h1>
        <p>Your cooking journey at a glance</p>
      </header>
      <div className="content">
        <div className="dashboard-stats">
          <div className="stat-card">
            <h3>42</h3>
            <p>Recipes Shared</p>
          </div>
          <div className="stat-card">
            <h3>127</h3>
            <p>Recipes Saved</p>
          </div>
          <div className="stat-card">
            <h3>89</h3>
            <p>Friends</p>
          </div>
        </div>
        <div className="recent-activity">
          <h3>Recent Activity</h3>
          <ul>
            <li>You saved "Beef Stir Fry" recipe</li>
            <li>You shared "Lemon Cake" recipe</li>
            <li>Sarah liked your "Pasta Carbonara" recipe</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default PersonalDashboard;

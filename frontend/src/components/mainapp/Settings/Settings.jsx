import React from 'react';

const Settings = () => {
  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Settings</h1>
        <p>Manage your account and preferences</p>
      </header>
      <div className="content">
        <div className="settings-section">
          <h3>Account Settings</h3>
          <div className="setting-item">
            <label>Display Name</label>
            <input type="text" placeholder="Your name" />
          </div>
          <div className="setting-item">
            <label>Email</label>
            <input type="email" placeholder="your.email@example.com" />
          </div>
          <div className="setting-item">
            <label>Bio</label>
            <textarea placeholder="Tell us about your cooking style..."></textarea>
          </div>
        </div>

        <div className="settings-section">
          <h3>Privacy Settings</h3>
          <div className="setting-item">
            <label>
              <input type="checkbox" defaultChecked />
              Make my recipes public
            </label>
          </div>
          <div className="setting-item">
            <label>
              <input type="checkbox" defaultChecked />
              Allow friend requests
            </label>
          </div>
        </div>

        <div className="settings-section">
          <h3>Notification Settings</h3>
          <div className="setting-item">
            <label>
              <input type="checkbox" defaultChecked />
              Email notifications
            </label>
          </div>
          <div className="setting-item">
            <label>
              <input type="checkbox" />
              Recipe recommendations
            </label>
          </div>
        </div>

        <button className="save-settings-btn">Save Changes</button>
      </div>
    </div>
  );
};

export default Settings;

import React from 'react';

const Friends = () => {
  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Friends</h1>
        <p>Connect with your cooking community</p>
      </header>
      <div className="content">
        <div className="friends-section">
          <h3>Friend Requests</h3>
          <div className="friend-request">
            <p><strong>Alex Johnson</strong> wants to be your friend</p>
            <div>
              <button className="accept-btn">Accept</button>
              <button className="decline-btn">Decline</button>
            </div>
          </div>
        </div>
        
        <div className="friends-section">
          <h3>Your Friends (89)</h3>
          <div className="friends-list">
            <div className="friend-card">
              <h4>Sarah Wilson</h4>
              <p>Shared 15 recipes • Active 2h ago</p>
            </div>
            <div className="friend-card">
              <h4>Mike Chen</h4>
              <p>Shared 8 recipes • Active 1d ago</p>
            </div>
            <div className="friend-card">
              <h4>Emma Davis</h4>
              <p>Shared 23 recipes • Active 3h ago</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Friends;

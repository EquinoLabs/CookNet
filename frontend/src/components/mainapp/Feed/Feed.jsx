import React from 'react';

const Feed = () => {
  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Feed</h1>
        <p>Discover the latest recipes from your network</p>
      </header>
      <div className="content">
        <div className="feed-post">
          <h3>Chocolate Chip Cookies</h3>
          <p>Shared by Chef Maria • 2 hours ago</p>
          <p>The perfect recipe for soft and chewy chocolate chip cookies...</p>
        </div>
        <div className="feed-post">
          <h3>Homemade Pizza Dough</h3>
          <p>Shared by Tony's Kitchen • 5 hours ago</p>
          <p>Master the art of pizza making with this simple dough recipe...</p>
        </div>
      </div>
    </div>
  );
};

export default Feed;

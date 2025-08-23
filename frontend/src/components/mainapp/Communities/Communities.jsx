import React from 'react';

const Communities = () => {
  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Communities</h1>
        <p>Connect with fellow food enthusiasts</p>
      </header>
      <div className="content">
        <div className="community-card">
          <h3>Baking Masters</h3>
          <p>1,234 members</p>
          <p>Share your best baking tips and recipes</p>
          <button>Join Community</button>
        </div>
        <div className="community-card">
          <h3>Vegan Recipes</h3>
          <p>856 members</p>
          <p>Plant-based cooking inspiration</p>
          <button>Join Community</button>
        </div>
        <div className="community-card">
          <h3>Quick Meals</h3>
          <p>2,101 members</p>
          <p>Fast and delicious meal ideas</p>
          <button>Join Community</button>
        </div>
      </div>
    </div>
  );
};

export default Communities;

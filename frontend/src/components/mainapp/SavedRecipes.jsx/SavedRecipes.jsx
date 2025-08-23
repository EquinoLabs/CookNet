import React from 'react';

const SavedRecipes = () => {
  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Saved Recipes</h1>
        <p>Your collection of favorite recipes</p>
      </header>
      <div className="content">
        <div className="recipe-grid">
          <div className="recipe-card">
            <h3>Chicken Tikka Masala</h3>
            <p>Indian • 45 mins</p>
            <p>Saved 3 days ago</p>
          </div>
          <div className="recipe-card">
            <h3>Chocolate Brownies</h3>
            <p>Dessert • 30 mins</p>
            <p>Saved 1 week ago</p>
          </div>
          <div className="recipe-card">
            <h3>Caesar Salad</h3>
            <p>Salad • 15 mins</p>
            <p>Saved 2 weeks ago</p>
          </div>
          <div className="recipe-card">
            <h3>Beef Tacos</h3>
            <p>Mexican • 25 mins</p>
            <p>Saved 1 month ago</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SavedRecipes;

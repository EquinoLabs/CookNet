import RecipeCard from "../RecipeCard/RecipeCard";
import './TrendingRecipes.scss'


export default function TrendingRecipes({ recipes }) {
  return (
    <section className="trending-recipes">
      <h2 className="title">Trending Recipes</h2>
      <div className="inner-container">
        {recipes.map((recipe, index) => (
          <RecipeCard key={index} {...recipe} />
        ))}
      </div>
    </section>
  );
}

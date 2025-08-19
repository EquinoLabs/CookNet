import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import { getRecipeById } from "../../api/actions";

export default function RecipePage() {
  const { state } = useLocation();
  const { id } = useParams();

  // If no state (refresh), fetch from backend using id
  const [recipe, setRecipe] = useState(state || null);

  const getRecipe = async () => {
    try {
      const data = await getRecipeById(id);
      setRecipe(data);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    if (!recipe) {
      getRecipe();
    }
  }, [id, recipe]);

  if (!recipe) return <p>Loading...</p>;

  return (
    <div className="max-w-3xl mx-auto p-4 space-y-6">
      {/* Name */}
      <h1 className="text-3xl font-bold">{recipe.name}</h1>

      {/* Description */}
      {recipe.description && (
        <p className="text-gray-700">{recipe.description}</p>
      )}

      {/* Minutes to make */}
      <p className="text-sm text-gray-500">
        ⏱ {recipe.minutes} minutes
      </p>

      {/* Number of ingredients */}
      <p className="text-sm text-gray-500">
        🥗 {recipe.n_ingredients} ingredients
      </p>

      {/* Ingredients */}
      <div>
        <h2 className="mt-4 font-semibold text-lg">Ingredients</h2>
        <ul className="list-disc list-inside">
          {Array.isArray(recipe.ingredients)
            ? recipe.ingredients.map((ing, i) => (
                <li key={i}>{ing}</li>
              ))
            : JSON.parse(recipe.ingredients || "[]").map((ing, i) => (
                <li key={i}>{ing}</li>
              ))}
        </ul>
      </div>

      {/* Number of steps */}
      <p className="text-sm text-gray-500">
        📜 {recipe.n_steps} steps
      </p>

      {/* Steps */}
      <div>
        <h2 className="mt-4 font-semibold text-lg">Instructions</h2>
        <ol className="list-decimal list-inside space-y-1">
          {Array.isArray(recipe.steps)
            ? recipe.steps.map((step, i) => <li key={i}>{step}</li>)
            : JSON.parse(recipe.steps || "[]").map((step, i) => (
                <li key={i}>{step}</li>
              ))}
        </ol>
      </div>

      {/* Nutrition */}
      <div>
        <h2 className="mt-4 font-semibold text-lg">Nutrition</h2>
        <ul className="list-disc list-inside">
          {Array.isArray(recipe.nutrition)
            ? recipe.nutrition.map((n, i) => (
                <li key={i}>Value {i + 1}: {n}</li>
              ))
            : JSON.parse(recipe.nutrition || "[]").map((n, i) => (
                <li key={i}>Value {i + 1}: {n}</li>
              ))}
        </ul>
      </div>

      {/* Tags */}
      <div>
        <h2 className="mt-4 font-semibold text-lg">Tags</h2>
        <div className="flex flex-wrap gap-2">
          {(Array.isArray(recipe.tags)
            ? recipe.tags
            : JSON.parse(recipe.tags || "[]")
          ).map((tag, i) => (
            <span
              key={i}
              className="bg-gray-200 text-gray-800 px-2 py-1 rounded text-sm"
            >
              {tag}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

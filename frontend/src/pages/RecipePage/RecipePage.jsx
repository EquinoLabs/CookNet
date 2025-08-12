import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";

export default function RecipePage() {
  const { state } = useLocation();
  const { id } = useParams();

  // If no state (refresh), fetch from backend using id
  const [recipe, setRecipe] = useState(state || {
    title: "Loading...",
    image: "",
    ingredients: [],
    instructions: "",
  });

  useEffect(() => {
    if (!recipe) {
      // fetch from backend
      fetch(`/api/recipe/${id}`)
        .then(res => res.json())
        .then(data => setRecipe(data));
    }
  }, [id, recipe]);

  if (!recipe) return <p>Loading...</p>;

  return (
    <div className="max-w-3xl mx-auto p-4">
      <img
        src={recipe.image}
        alt={recipe.title}
        className="w-full h-64 object-cover rounded"
      />
      <h1 className="text-2xl font-bold mt-4">{recipe.title}</h1>
      <h2 className="mt-4 font-semibold">Ingredients</h2>
      <ul className="list-disc list-inside">
        {recipe.ingredients?.map((ing, i) => (
          <li key={i}>{ing}</li>
        ))}
      </ul>
      <h2 className="mt-4 font-semibold">Instructions</h2>
      <p>{recipe.instructions}</p>
    </div>
  );
}

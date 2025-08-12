import { useState } from "react";
import SearchBar from "../../components/SearchBar/SearchBar";
import RecipeCard from "../../components/RecipeCard/RecipeCard";
import { useNavigate } from "react-router-dom";
import { navigateToRecipe } from "../../store/actions/navigateAction";
import { getUserSearch } from "../../api/actions";

export default function HomePage() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);   // show spinner later
  const [error, setError] = useState(null);        // handle errors

  const navigate = useNavigate();

  const handleSearch = async (query) => {
    if (!query.trim()) return; // ignore empty searches

    try {
      setLoading(true);
      setError(null);

      // Call your API function
      const data = await getUserSearch(query);

      // Assuming `data` is already the list of recipes
      setRecipes(data);
    } catch (err) {
      setError("Failed to fetch recipes. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const openRecipe = (recipe) => {
    navigateToRecipe(navigate, recipe.id);
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <SearchBar onSearch={handleSearch} />

      {loading && <p className="mt-4 text-gray-500">Loading...</p>}
      {error && <p className="mt-4 text-red-500">{error}</p>}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
        {recipes.map((r) => (
          <RecipeCard key={r.id} recipe={r} onClick={() => openRecipe(r)} />
        ))}
      </div>
    </div>
  );
}

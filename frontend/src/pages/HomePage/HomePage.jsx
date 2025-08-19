import { useState } from "react";
// import SearchBar from "../../components/SearchBar/SearchBar";
// import RecipeCard from "../../components/RecipeCard/RecipeCard";
import { useNavigate } from "react-router-dom";
import { navigateToRecipe } from "../../store/actions/navigateAction";
import { getUserSearch } from "../../api/actions";

import Navbar from "../../components/layout/Navbar/Navbar";
import Footer from "../../components/layout/Footer/Footer";
import HeroBanner from "../../components/homepage/HeroBanner/HeroBanner";
import TrendingRecipes from "../../components/homepage/TrendingRecipes/TrendingRecipes";
import CommunitiesSection from "../../components/homepage/CommunitiesSection/CommunitiesSection";
import FeaturedCreators from "../../components/homepage/FeaturedCreators/FeaturedCreators";
import AIRecommendationTeaser from "../../components/homepage/AIRecommendationTeaser/AIRecommendationTeaser";
import JoinNowSection from "../../components/homepage/JoinNowSection/JoinNowSection";


// Temporary dummy data
const recipesData = [
  {
    title: "Spaghetti Carbonara",
    image: "/images/Recipes/spaghetti-carbonara.jpg",
    tags: ["Italian", "Pasta"],
    time: 20,
    votes: 132
  },
  {
    title: "Vegan Buddha Bowl",
    image: "/images/Recipes/vegan-buddha-bowl.jpg",
    tags: ["Vegan", "Healthy"],
    time: 25,
    votes: 95
  },
  {
    title: "Chicken Teriyaki",
    image: "/images/Recipes/chicken-teriyaki.jpg",
    tags: ["Japanese", "Chicken"],
    time: 30,
    votes: 210
  },
  {
    title: "Avocado Toast",
    image: "/images/Recipes/avocado-toast.jpg",
    tags: ["Breakfast", "Healthy"],
    time: 10,
    votes: 78
  },
  {
    title: "Grilled Salmon",
    image: "/images/Recipes/grilled-salmon.jpg",
    tags: ["Seafood", "Healthy"],
    time: 35,
    votes: 185
  },
  {
    title: "Chocolate Lava Cake",
    image: "/images/Recipes/chocolate-lava-cake.jpg",
    tags: ["Dessert", "Chocolate"],
    time: 40,
    votes: 245
  }
];

import { House, ChefHat, Heart, Salad, Cookie, TrendingUp } from "lucide-react";

const communitiesData = [
  { name: "Solo Living", icon: House },
  { name: "Moms", icon: ChefHat },
  { name: "Gym Freaks", icon: Heart },
  { name: "Vegetarian", icon: Salad },
  { name: "Dessert Lovers", icon: Cookie },
  { name: "Street Food", icon: TrendingUp }
];

const creatorsData = [
  { name: "Chef Lakshya", avatar: "/images/Creators/lakshya.jpg", signature: "Panner Makhani" },
  { name: "Cooking With Aashi", avatar: "/images/Creators/aashi.jpg", signature: "Creamy Mushroom" }
];

const challengeData = {
  title: "5-Ingredient Challenge",
  description: "Create a delicious meal with only 5 ingredients!",
  image: "https://source.unsplash.com/400x300/?cooking"
};


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
      // const data = await getUserSearch(query);
      const data = getUserSearch(query);

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
    <>
      <Navbar />
      <HeroBanner onSearch={handleSearch} />
      <TrendingRecipes recipes={recipesData} />
      <CommunitiesSection communities={communitiesData} />
      <FeaturedCreators creators={creatorsData} />
      <AIRecommendationTeaser />
      <JoinNowSection />
      <Footer />
    </>
  );
}

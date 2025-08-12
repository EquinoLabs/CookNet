import HomePage from "../pages/HomePage/HomePage";
import RecipePage from "../pages/RecipePage/RecipePage"
import NotFound from "../pages/NotFound/NotFound";


const routerConfig = [
  { path: "/", element: <HomePage /> },
  { path: "/recipe/:id", element: <RecipePage /> },
  { path: "*", element: <NotFound /> },
];

export default routerConfig;

import HomePage from "../pages/HomePage/HomePage";
import RecipePage from "../pages/RecipePage/RecipePage";
import NotFound from "../pages/NotFound/NotFound";
import Register from "../pages/Authentication/Register";
import Login from "../pages/Authentication/Login";
import ProtectedRoute from "../components/ProtectedRoute";
import MainApp from "../pages/MainApp/MainApp";
import RootRedirect from "../components/RootRedirect";

const routerConfig = [
  { 
    path: "/", 
    element: <RootRedirect />  // Handles logged-in vs not-logged-in logic
  },
  {
    path: "/home", 
    element: (
      <ProtectedRoute>
        <MainApp />
      </ProtectedRoute>
    )
  },
  { 
    path: "/recipe/:id", 
    element: (
      <ProtectedRoute>
        <RecipePage />
      </ProtectedRoute>
    )
  },
  { path: "/register", element: <Register /> },
  { path: "/login", element: <Login /> },
  { path: "*", element: <NotFound /> },
];

export default routerConfig;

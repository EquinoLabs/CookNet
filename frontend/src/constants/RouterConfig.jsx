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
    path: "/feed", 
    element: (
      <ProtectedRoute>
        <MainApp />
      </ProtectedRoute>
    )
  },
  {
    path: "/communities", 
    element: (
      <ProtectedRoute>
        <MainApp />
      </ProtectedRoute>
    )
  },
  {
    path: "/dashboard", 
    element: (
      <ProtectedRoute>
        <MainApp />
      </ProtectedRoute>
    )
  },
  {
    path: "/saved", 
    element: (
      <ProtectedRoute>
        <MainApp />
      </ProtectedRoute>
    )
  },
  {
    path: "/friends", 
    element: (
      <ProtectedRoute>
        <MainApp />
      </ProtectedRoute>
    )
  },
  {
    path: "/settings", 
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

import { routes } from "../../constants/routes";

export const navigateToHome = (navigate) => {
    navigate(routes.ROOT);
};

export const navigateToSignUp = (navigate) => {
    navigate(routes.REGISTER)
};

export const navigateToLogin = (navigate) => {
    navigate(routes.LOGIN)
};

export const navigateToRecipe = (navigate, id) => {
  // Replace :id in the route with the actual id
  const path = routes.RECIPE.replace(":id", id);
  navigate(path);
};

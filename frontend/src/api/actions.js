// actions.js - your app specific API functions

import { callApi } from "./helper";
import dummyData from "../constants/dummy_recipe_data.json";

export function getAppStatus() {
  return callApi('get:/recipe');
}

export function getUserSearch(query) {
  // return callApi(`get:/search?query=${query}`);
  
  // Returning dummy data instead
  return dummyData;
}

export function getRecipeById(id) {
  // return callApi(`get:/recipe/${id}`);

  // Dummy data
  const recipe = dummyData.find(item => item.id === id);
  return recipe || null;
}

export function loginUser(email, password) {
  return callApi('post:/users/login', { email, password });
}

export function registerUser(username, email, password) {
  console.log(username, email, password);
  return callApi('post:/users/register', { username, email, password });
}

export function postLike(postId) {
  return callApi(`post:/posts/${postId}/like`, { postId });
}

export function getFeedPosts(cursor = null, limit = 10) {
  const params = new URLSearchParams();
  if (cursor) params.append('cursor', cursor);
  params.append('limit', limit);
  return callApi(`get:/posts/feed?${params.toString()}`);
}

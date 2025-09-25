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

export function googleAuthToken() {
  return callApi('get:/users/google-auth-url');
}

export function verifyEmail(token) {
  console.log("reuest came with token", token);
  return callApi(`get:/users/verify-email?token=${token}`);
}

export async function getMediaURL(mediaId) {
  let data = await callApi(`get:/stored-media/${mediaId}`);
  console.log("data", data.url)
  return data?.url;
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

export function createPost(formData) {
  return callApi('post:/posts', formData, true); // The third argument 'true' indicates multipart/form-data
}


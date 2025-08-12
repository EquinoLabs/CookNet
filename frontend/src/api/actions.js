// actions.js - your app specific API functions

import { callApi } from "./helper";


export function getAppStatus() {
  return callApi('get:/recipe');
}

export function getUserSearch(query) {
  return callApi(`get:/search?query=${query}`);
}

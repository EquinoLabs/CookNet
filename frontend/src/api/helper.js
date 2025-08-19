// axios wrapper

import axios from 'axios';

const api = axios.create({
  baseURL: '/api', // or your backend base URL
  // You can add headers here, e.g. Authorization token, content-type, etc.
});

export async function callApi(endpointWithMethod, data = null) {
  const [method, endpoint] = endpointWithMethod.split(':');
  
  const config = {};
  let response;

  try {
    if (method.toLowerCase() === 'get' || method.toLowerCase() === 'delete') {
      // For GET or DELETE, data is treated as query params
      config.params = data;
      console.log("url:", endpoint)
      response = await api.request({ method, url: endpoint, ...config });
    } else {
      // For POST, PUT, PATCH, data is the request body
      response = await api.request({ method, url: endpoint, data, ...config });
    }
    return response.data;
  } catch (error) {
    // You can customize error handling here
    console.error('API error:', error);
    throw error;
  }
}

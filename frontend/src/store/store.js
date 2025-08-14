import { createStore, applyMiddleware } from 'redux';
import { thunk } from 'redux-thunk';  // Corrected import for thunk
import { rootReducer } from './reducers'; // Your root reducer

// Create store with redux-thunk middleware
export const store = createStore(
  rootReducer,
  applyMiddleware(thunk)  // Use redux-thunk as middleware
);

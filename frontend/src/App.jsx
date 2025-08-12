import { RouterProvider, createBrowserRouter  } from 'react-router-dom';
import './App.css';
import routerConfig from './constants/RouterConfig';

export default function App() {
  // let route = [
  //   {
  //     path: "/",
  //     children: routerConfig.common_routes
  //   }
  // ];
  // let common_routes = routerConfig?.common_routes;

  // route = route.concat(common_routes);
  // const hashRouter = createHashRouter(route);

  const browserRouter = createBrowserRouter(routerConfig);

  return (
    <>
      <RouterProvider router={browserRouter} />
    </>
  );
}

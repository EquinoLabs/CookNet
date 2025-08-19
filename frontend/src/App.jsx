import { RouterProvider, createBrowserRouter  } from 'react-router-dom';
import './styles/global.scss'
import routerConfig from './constants/RouterConfig';

export default function App() {
  const browserRouter = createBrowserRouter(routerConfig);

  return (
    <>
      <RouterProvider router={browserRouter} />
    </>
  );
}

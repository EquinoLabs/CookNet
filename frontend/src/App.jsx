import { RouterProvider, createBrowserRouter  } from 'react-router-dom';
import './styles/global.scss'
import routerConfig from './constants/RouterConfig';
import { AuthProvider } from './components/AuthContext';

export default function App() {
  const browserRouter = createBrowserRouter(routerConfig);

  return (
    <AuthProvider>
      <RouterProvider router={browserRouter} />
    </AuthProvider>
  );
}

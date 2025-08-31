import { RouterProvider, createBrowserRouter  } from 'react-router-dom';
import './styles/global.scss'
import { GoogleOAuthProvider } from "@react-oauth/google"; 
import routerConfig from './constants/RouterConfig';
import { AuthProvider } from './components/AuthContext';
import { ToastProvider } from './components/common/ToastContext/ToastContext';

const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

export default function App() {
  const browserRouter = createBrowserRouter(routerConfig);

  return (
    <GoogleOAuthProvider clientId={clientId}>
      <AuthProvider>
        <ToastProvider>
          <RouterProvider router={browserRouter} />
        </ToastProvider>
      </AuthProvider>
    </GoogleOAuthProvider>
  );
}

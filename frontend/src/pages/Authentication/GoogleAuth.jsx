import { GoogleLogin } from "@react-oauth/google";
import { useAuth } from "../../components/AuthContext";
import './authentication.scss'

export default function GoogleAuth() {
  const { loginWithGoogle } = useAuth();

  const handleSuccess = async (credentialResponse) => {
    try {
      const token = credentialResponse.credential;

      // Use AuthContext to handle login
      const result = await loginWithGoogle(token);

      if (result.success) {
        console.log("Logged in with Google:", result.user);
        // Optional: navigate somewhere after login
      } else {
        console.error("Google login failed:", result.error);
      }
    } catch (err) {
      console.error("Unexpected error during Google login:", err);
    }
  };

  const handleError = () => {
    console.error("Google login failed");
  };

  return (
    <div>
      <GoogleLogin onSuccess={handleSuccess} onError={handleError} />
    </div>
  );
}

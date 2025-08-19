import React, { useState, useEffect } from "react";
import { useAuth } from "../../components/AuthContext";
import { useNavigate } from "react-router-dom";
import "./authentication.scss"; // import SCSS file

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/home');
    }
  }, [isAuthenticated, navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);
    
    try {
      const result = await login(email, password);
      if (result.success) {
        console.log("Login successful:", result.user);
        navigate('/'); // Redirect to homepage
      } else {
        setError(result.error);
      }
    } catch (error) {
      console.error("Login failed:", error);
      setError("An unexpected error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleLogin = () => {
    console.log("Login with Google clicked");
    // TODO: Implement Google login
  };

  return (
    <div className="login-wrapper">
      <a href="/" className="cooknet-link">CookNet</a>
      <div className="login-container">
        <h2 className="login-title">Welcome Back to CookNet</h2>
        <form className="login-form" onSubmit={handleLogin}>
          <label htmlFor="email-input" className="login-label">Email</label>
          <input
            type="email"
            id="email-input"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="login-input"
          />
          <label htmlFor="password-input" className="login-label">Password</label>
          <input
            type="password"
            id="password-input"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="login-input"
          />
          <button type="submit" className="login-button">
            Login
          </button>
          
          <div className="divider-container">
            <div className="divider-line"></div>
            <span className="divider-text">OR</span>
            <div className="divider-line"></div>
          </div>
          
          <button className="google-button" onClick={handleGoogleLogin}>
            Login with Google
          </button>
        </form>
        <p className="login-footer">
          Don't have an account? <a href="/register" className="register-link">Register</a>
        </p>
      </div>
    </div>
  );
};

export default Login;

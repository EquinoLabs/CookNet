import React, { useState, useEffect } from "react";
import { useAuth } from "../../components/AuthContext";
import { useNavigate } from "react-router-dom";
import { emitToast } from "../../components/common/ToastContext/ToastEmiiter";
import GoogleAuth from "./GoogleAuth";
import constants from "../../constants";
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
      navigate('/feed');
    }
  }, [isAuthenticated, navigate]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);
    
    try {
      const result = await login(email, password);
      if (result.success) {
        emitToast(constants.LoginPage.Success, "", "success");
        navigate('/'); // Redirect to homepage
      } else {
        let ErrorMsg = result.error
        if (Array.isArray(result.error) && result.error.length > 0) {
          ErrorMsg = result.error[0].msg;
        }
        emitToast(constants.LoginPage.Error.title, ErrorMsg, "error");
        setError(ErrorMsg);
      }
    } catch (error) {
      emitToast(constants.LoginPage.Error.title, constants.LoginPage.Error.err_500, "error");
      setError(constants.LoginPage.Error.err_500);
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
          <button 
            type="submit" 
            className={`login-button ${isLoading ? "loading" : ""}`} 
            disabled={isLoading}
          >
            {isLoading ? <span className="spinner"></span> : "Login"}
          </button>
          
          <div className="divider-container">
            <div className="divider-line"></div>
            <span className="divider-text">OR</span>
            <div className="divider-line"></div>
          </div>

          <div className="google-auth-wrapper">
            <GoogleAuth />
          </div>
        </form>
        <p className="login-footer">
          Don't have an account? <a href="/register" className="register-link">Register</a>
        </p>
      </div>
    </div>
  );
};

export default Login;

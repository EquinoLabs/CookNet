import React, { useState, useEffect } from "react";
import { useAuth } from "../../components/AuthContext";
import { useNavigate } from "react-router-dom";
import { getMediaURL } from "../../api/actions";
import { emitToast } from "../../components/common/ToastContext/ToastEmiiter";
import GoogleAuth from "./GoogleAuth";
import constants from "../../constants";
import "./authentication.scss";

const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  
  const { register, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const [bgUrl, setBgUrl] = useState(null);

  useEffect(() => {
      // fetch only if no url is set yet
      if (!bgUrl) {
          getMediaURL(constants.RegisterPage.imageId)
              .then((url) => setBgUrl(url))
              .catch((err) => {
                  console.error("Failed to load banner image:", err);
              });
          console.log("URL", bgUrl)
      }
  }, [bgUrl]);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setIsLoading(true);
    
    try {
      const result = await register(username, email, password);
      if (result.success) {
        emitToast(constants.RegisterPage.Success, "", "success");
        setSuccess(constants.RegisterPage.Success);
        // Clear form
        setUsername("");
        setEmail("");
        setPassword("");
        // Redirect to login after a delay
        setTimeout(() => {
          navigate('/email-verification-sent');
        }, 500);
      } else {
        let ErrorMsg = result.error
        if (Array.isArray(result.error) && result.error.length > 0) {
          ErrorMsg = result.error[0].msg;
        }
        emitToast(constants.RegisterPage.Error.title, ErrorMsg, "error");
        setError(ErrorMsg);
      }
    } catch (error) {
      emitToast(constants.RegisterPage.Error.title, constants.RegisterPage.Error.err_500, "error");
      setError(constants.RegisterPage.Error.err_500);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleSignup = () => {
    // TODO: Add Google signup logic
    console.log("Signup with Google clicked");
  };

  return (
    <div className="register-wrapper">
      <a href="/" className="cooknet-link">CookNet</a>
      <div className="register-banner">
        <img src={bgUrl} alt="CookNet Banner" className="banner-image" />
      </div>
      <div className="register-container">
        <h2 className="register-title">Join CookNet Today</h2>
        <span className="register-subtitle">Start your culinary journey!</span>
        <form className="register-form" onSubmit={handleRegister}>
          <label htmlFor="username-input" className="register-label">Username</label>
          <input
            type="text"
            id="username-input"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="register-input"
          />
          
          <label htmlFor="email-input" className="register-label">Email</label>
          <input
            type="email"
            id="email-input"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="register-input"
          />
          
          <label htmlFor="password-input" className="register-label">Password</label>
          <input
            type="password"
            id="password-input"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="register-input"
          />
          <button 
            type="submit" 
            className={`register-button ${isLoading ? "loading" : ""}`} 
            disabled={isLoading}
          >
            {isLoading ? <span className="spinner"></span> : "Register Account"}
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
        
        <p className="register-footer">
          Already have an account? <a href="/login" className="login-link">Login</a>
        </p>
      </div>
    </div>
  );
};

export default Register;

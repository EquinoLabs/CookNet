import React, { useState, useEffect } from "react";
import { useAuth } from "../../components/AuthContext";
import { useNavigate } from "react-router-dom";
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
        console.log("Registration successful:", result.message);
        setSuccess("Registration successful! Please login.");
        // Clear form
        setUsername("");
        setEmail("");
        setPassword("");
        // Redirect to login after a delay
        setTimeout(() => {
          navigate('/login');
        }, 2000);
      } else {
        setError(result.error);
      }
    } catch (error) {
      console.error("Registration failed:", error);
      setError("An unexpected error occurred");
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
        <img src="http://localhost:8000/media/images/HomePage/Herobanner2.jpg" alt="CookNet Banner" className="banner-image" />
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
          
          <button type="submit" className="register-button">
            Register Account
          </button>
          
          <div className="divider-container">
            <div className="divider-line"></div>
            <span className="divider-text">OR</span>
            <div className="divider-line"></div>
          </div>
          
          <button className="google-button" onClick={handleGoogleSignup}>
            Sign up with Gmail
          </button>
        </form>
        
        <p className="register-footer">
          Already have an account? <a href="/login" className="login-link">Login</a>
        </p>
      </div>
    </div>
  );
};

export default Register;

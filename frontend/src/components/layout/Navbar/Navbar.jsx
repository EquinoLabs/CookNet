import './Navbar.scss';
import { useNavigate } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate('/login');
  };

  const handleSignUpClick = () => {
    navigate('/register');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        
        {/* Logo */}
        <div className="navbar-logo">
          <h1 className="logo-text">CookNet</h1>
        </div>

        {/* Navigation Links - Centered */}
        <div className="navbar-nav">
          <a href="/" className="nav-link">Home</a>
          <a href="#" className="nav-link">Recipe</a>
          <a href="#" className="nav-link">Community</a>
          <a href="#" className="nav-link">Blog</a>
          <a href="#" className="nav-link">Contact</a>
        </div>

        {/* Auth Buttons */}
        <div className="navbar-auth">
          <button className="auth-btn login-btn" onClick={handleLoginClick}>Login</button>
          <button className="auth-btn signup-btn" onClick={handleSignUpClick}>Sign Up</button>
        </div>
      </div>
    </nav>
  );
}
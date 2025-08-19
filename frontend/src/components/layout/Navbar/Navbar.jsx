import './Navbar.scss';

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        
        {/* Logo */}
        <div className="navbar-logo">
          <h1 className="logo-text">CookNet</h1>
        </div>

        {/* Navigation Links - Centered */}
        <div className="navbar-nav">
          <a href="#" className="nav-link">Home</a>
          <a href="#" className="nav-link">Recipe</a>
          <a href="#" className="nav-link">Community</a>
          <a href="#" className="nav-link">Blog</a>
          <a href="#" className="nav-link">Contact</a>
        </div>

        {/* Auth Buttons */}
        <div className="navbar-auth">
          <button className="auth-btn login-btn">Login</button>
          <button className="auth-btn signup-btn">Sign Up</button>
        </div>
      </div>
    </nav>
  );
}
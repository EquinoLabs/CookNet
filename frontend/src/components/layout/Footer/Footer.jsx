
import { Facebook, Instagram, Twitter, Youtube } from "lucide-react";
import './Footer.scss';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        
        {/* Brand Section (Left) */}
        <div className="footer-brand">
          <h2 className="brand-name">CookNet</h2>
          <p className="brand-description">
            A community for cooking geeks to share, learn, and create recipes together.
          </p>
        </div>

        {/* Center Links */}
        <div className="footer-links">
          
          {/* Company */}
          <div className="link-section">
            <h3 className="section-title">Company</h3>
            <ul className="link-list">
              <li><a href="#" className="footer-link">About Us</a></li>
              <li><a href="#" className="footer-link">Careers</a></li>
              <li><a href="#" className="footer-link">Blog</a></li>
              <li><a href="#" className="footer-link">Press</a></li>
            </ul>
          </div>

          {/* Resources */}
          <div className="link-section">
            <h3 className="section-title">Resources</h3>
            <ul className="link-list">
              <li><a href="#" className="footer-link">Recipes</a></li>
              <li><a href="#" className="footer-link">Community</a></li>
              <li><a href="#" className="footer-link">Help Center</a></li>
              <li><a href="#" className="footer-link">Contact</a></li>
            </ul>
          </div>

          {/* Legal */}
          <div className="link-section">
            <h3 className="section-title">Legal</h3>
            <ul className="link-list">
              <li><a href="#" className="footer-link">Privacy Policy</a></li>
              <li><a href="#" className="footer-link">Terms of Service</a></li>
              <li><a href="#" className="footer-link">Cookie Policy</a></li>
              <li><a href="#" className="footer-link">Disclaimer</a></li>
            </ul>
          </div>

          {/* Download */}
          <div className="link-section">
            <h3 className="section-title">Download</h3>
            <div className="download-buttons">
              <button className="download-btn">iOS App</button>
              <button className="download-btn">Android App</button>
            </div>
          </div>
        </div>

        {/* Social Media Section (Right) */}
        <div className="footer-social">
          <h3 className="section-title">Follow Us</h3>
          <div className="social-icons">
            <a href="#" className="social-link">
              <Facebook className="social-icon" />
            </a>
            <a href="#" className="social-link">
              <Instagram className="social-icon" />
            </a>
            <a href="#" className="social-link">
              <Twitter className="social-icon" />
            </a>
            <a href="#" className="social-link">
              <Youtube className="social-icon" />
            </a>
          </div>
        </div>

      </div>

      {/* Copyright */}
      <div className="footer-bottom">
        <p className="copyright">
          © {new Date().getFullYear()} CookNet. All rights reserved.
        </p>
      </div>
    </footer>
  );
}

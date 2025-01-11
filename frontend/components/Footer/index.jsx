import React from "react";
import { Link } from "react-router-dom";
import "./footer.css";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-logo">
        <i className="fas fa-paw fa-2x"></i>
        <Link to="/">UaimVet</Link>
      </div>
    </footer>
  );
};

export default Footer;

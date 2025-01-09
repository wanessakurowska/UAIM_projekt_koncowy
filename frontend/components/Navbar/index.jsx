import React from "react";
import { Link } from "react-router-dom";
import "./navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul className="navbar-list">
        <li>
          <Link to="/services">Katalog usług</Link>
        </li>
        <li>
          <Link to="/veterinarians">Lekarze</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;

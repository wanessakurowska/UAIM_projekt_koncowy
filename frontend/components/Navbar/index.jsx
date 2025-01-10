import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./navbar.css";

const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));

  useEffect(() => {
    const updateLoginStatus = () => {
      setIsLoggedIn(!!localStorage.getItem("token"));
    };

    window.addEventListener("login", updateLoginStatus);
    window.addEventListener("logout", updateLoginStatus);

    return () => {
      window.removeEventListener("login", updateLoginStatus);
      window.removeEventListener("logout", updateLoginStatus);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    const event = new Event("logout");
    window.dispatchEvent(event);
    window.location.href = "/login";
  };

  return (
    <nav className="navbar">
      <ul className="navbar-list">
        <li>
          <Link to="/services">Katalog usług</Link>
        </li>
        <li>
          <Link to="/veterinarians">Lekarze</Link>
        </li>
        <li>
          {isLoggedIn ? (
            <button onClick={handleLogout}>Wyloguj</button>
          ) : (
            <Link to="/login">Zaloguj</Link>
          )}
        </li>
        {!isLoggedIn && (
          <li>
            <Link to="/register">Zarejestruj się</Link>
          </li>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;

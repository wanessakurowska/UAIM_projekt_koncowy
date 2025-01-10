import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./navbar.css";

const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));
  const navigate = useNavigate();

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

  const handleProtectedLink = () => {
    if (!isLoggedIn) {
      navigate("/login"); // Przenieś na stronę logowania, jeśli użytkownik nie jest zalogowany
    } else {
      navigate("/appointment-calendar"); // Przenieś na stronę rezerwacji, jeśli użytkownik jest zalogowany
    }
  };

  return (
    <nav className="navbar">
      <ul className="navbar-list left-links">
        <li>
          <Link to="/services">Katalog usług</Link>
        </li>
        <li>
          <Link to="/veterinarians">Lekarze</Link>
        </li>
        <li>
          <button onClick={handleProtectedLink} className="link-button">
            Rezerwacja wizyty
          </button>
        </li>
        {isLoggedIn && (
          <li>
            <Link to="/add-pet">Dodaj Zwierzaka</Link>
          </li>
        )}
      </ul>
      <ul className="navbar-list right-links">
        {isLoggedIn ? (
          <li>
            <span className="logout-link" onClick={handleLogout}>
              Wyloguj
            </span>
          </li>
        ) : (
          <>
            <li>
              <Link to="/login">Zaloguj</Link>
            </li>
            <li>
              <Link to="/register">Zarejestruj</Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;

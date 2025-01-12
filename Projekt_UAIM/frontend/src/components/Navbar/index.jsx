import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./navbar.css";

const Navbar = () => {
  // Przechowywanie informacji o zalogowaniu
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));
  const navigate = useNavigate();

  useEffect(() => {
    // Aktualizacja stanu zalogowania na podstawie tokenu
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

  const handleProtectedRoute = (e, route) => {
    // Przekierowanie na stronę logowania, jesli klient nie jest zalogowany
    if (!isLoggedIn) {
      e.preventDefault();
      navigate("/login");
    } else {
      navigate(route);
    }
  };

  return (
    <nav className="navbar">
      {/* Sekcja linków wyśrodkowanych */}
      <ul className="navbar-list">
        <li>
          <Link to="/">
            <i className="fas fa-home"></i>
          </Link>
        </li>
        <li>
          <Link to="/services">USŁUGI</Link>
        </li>
        <li>
          <Link to="/veterinarians">NASZ ZESPÓŁ</Link>
        </li>
        <li>
          <Link
            to="/appointment-calendar"
            onClick={(e) => handleProtectedRoute(e, "/appointment-calendar")}
          >
            REZERWACJA WIZYTY
          </Link>
        </li>
        {isLoggedIn && (
          <>
            <li>
              <Link to="/add-pet">DODAJ ZWIERZAKA</Link>
            </li>
            <li>
              <Link to="/my-pets">MOJE ZWIERZAKI</Link>
            </li>
            <li>
              <Link to="/appointments">WIZYTY</Link>
            </li>
          </>
        )}
      </ul>

      {/* Sekcja linków autoryzacji po prawej */}
      <ul className="navbar-auth">
        {isLoggedIn ? (
          <li>
            <span className="logout-link" onClick={handleLogout}>
              WYLOGUJ
            </span>
          </li>
        ) : (
          <>
            <li>
              <Link to="/login">ZALOGUJ</Link>
            </li>
            <li>
              <Link to="/register">ZAREJESTRUJ</Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;

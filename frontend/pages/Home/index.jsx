import React from "react";
import { Link } from "react-router-dom";
import "./home.css";

const Home = () => {
  return (
    <div className="home-container">
      <div className="hero-section">
        <h1>UaimVet</h1>
        <h2>Klinika Weterynaryjna</h2>
        <p>ul. Nowowiejska 15/19, 00-665 Warszawa</p>
        <Link to="/appointment-calendar" className="appointment-button">
          Umów wizytę
        </Link>
      </div>
    </div>
  );
};

export default Home;

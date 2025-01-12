import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../../api";
import "./login.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Obsługa procesu logowania
  const handleLogin = async () => {
    try {
      const response = await apiClient.post("/api/login", {
        adres_email: email,
        haslo: password,
      });
      // Zapisanie tokenu w LocalStorage
      localStorage.setItem("token", response.data.token);

      const event = new Event("login");
      window.dispatchEvent(event);

      navigate("/appointment-calendar");
    } catch (err) {
      setError("Nieprawidłowy email lub hasło.");
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1>Logowanie</h1>
        {error && <p className="error-message">{error}</p>}
        <div className="form-group">
          <label>Adres Email:</label>
          <input
            type="email"
            placeholder="Wpisz email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Hasło:</label>
          <input
            type="password"
            placeholder="Wpisz hasło"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button className="login-button" onClick={handleLogin}>
          Zaloguj się
        </button>
      </div>
    </div>
  );
};

export default Login;

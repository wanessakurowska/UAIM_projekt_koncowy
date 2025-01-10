import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../../api";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await apiClient.post("/api/login", {
        adres_email: email,
        haslo: password,
      });

      localStorage.setItem("token", response.data.token);

      const event = new Event("login");
      window.dispatchEvent(event);

      navigate("/services");
    } catch (err) {
      setError("Nieprawidłowy email lub hasło.");
    }
  };  

  return (
    <div>
      <h1>Logowanie</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Hasło"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Zaloguj się</button>
    </div>
  );
};

export default Login;

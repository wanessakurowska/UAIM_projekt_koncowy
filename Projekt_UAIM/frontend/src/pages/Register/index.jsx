import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../../api";
import "./register.css";

const Register = () => {
  const [formData, setFormData] = useState({
    imie: "",
    nazwisko: "",
    adres_email: "",
    haslo: "",
    nr_telefonu: "",
    id_adresu: "",
  });
  const [addresses, setAddresses] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAddresses = async () => {
      try {
        const response = await apiClient.get("/api/addresses");
        setAddresses(response.data);
      } catch (err) {
        console.error("Błąd podczas pobierania adresów:", err);
        setError("Nie udało się załadować listy adresów.");
      }
    };

    fetchAddresses();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async () => {
    try {
      await apiClient.post("/api/register", formData);

      setSuccess(true);
      setTimeout(() => {
        navigate("/login");
      }, 3000);
    } catch (err) {
      setError(err.response?.data?.error || "Wystąpił błąd podczas rejestracji.");
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <h1>Rejestracja</h1>
        {success && <p className="success-message">Rejestracja zakończona sukcesem. Przekierowanie...</p>}
        {error && <p className="error-message">{error}</p>}
        <div className="form-group">
          <label>Imię</label>
          <input
            type="text"
            name="imie"
            value={formData.imie}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label>Nazwisko</label>
          <input
            type="text"
            name="nazwisko"
            value={formData.nazwisko}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label>Adres Email</label>
          <input
            type="email"
            name="adres_email"
            value={formData.adres_email}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label>Hasło</label>
          <input
            type="password"
            name="haslo"
            value={formData.haslo}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label>Numer Telefonu</label>
          <input
            type="text"
            name="nr_telefonu"
            value={formData.nr_telefonu}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label>Adres</label>
          <select
            name="id_adresu"
            value={formData.id_adresu}
            onChange={handleChange}
          >
            <option value="">-- Wybierz adres --</option>
            {addresses.map((address) => (
              <option key={address.id_adresu} value={address.id_adresu}>
                {`${address.miasto}, ${address.ulica} ${address.nr_lokalu}, ${address.poczta.kod_pocztowy} ${address.poczta.poczta}`}
              </option>
            ))}
          </select>
        </div>
        <button className="register-button" onClick={handleRegister}>
          Zarejestruj się
        </button>
      </div>
    </div>
  );
};

export default Register;

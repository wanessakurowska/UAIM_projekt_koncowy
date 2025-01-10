import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../../api";
import "./addPet.css";

const AddPet = () => {
  const [formData, setFormData] = useState({
    imie: "",
    wiek: "",
    opis: "",
    plec: "",
    id_rasy: "",
  });
  const [rasy, setRasy] = useState([]); // Lista ras
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // Pobranie listy ras z backendu
    const fetchRasy = async () => {
      try {
        const response = await apiClient.get("/api/races"); // Endpoint do pobrania ras
        setRasy(response.data);
      } catch (err) {
        console.error("Błąd podczas pobierania ras:", err);
        setError("Nie udało się załadować listy ras.");
      }
    };

    fetchRasy();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiClient.post("/api/add-pet", formData);
      setSuccess(true);
      setTimeout(() => navigate("/"), 3000); // Przekierowanie po 3 sekundach
    } catch (err) {
      setError("Wystąpił błąd podczas dodawania zwierzaka.");
    }
  };

  return (
    <div className="add-pet-container">
      <h1>Dodaj Zwierzaka</h1>
      {success && (
        <p style={{ color: "green" }}>
          Zwierzaka dodano pomyślnie. Przekierowanie...
        </p>
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Imię:
          <input
            type="text"
            name="imie"
            value={formData.imie}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Wiek:
          <input
            type="number"
            name="wiek"
            value={formData.wiek}
            onChange={handleChange}
            required
          />
        </label>
        <label>
          Opis:
          <textarea
            name="opis"
            value={formData.opis}
            onChange={handleChange}
            required
          ></textarea>
        </label>
        <label>
          Płeć:
          <select
            name="plec"
            value={formData.plec}
            onChange={handleChange}
            required
          >
            <option value="">Wybierz</option>
            <option value="M">Męska</option>
            <option value="F">Żeńska</option>
          </select>
        </label>
        <label>
          Rasa:
          <select
            name="id_rasy"
            value={formData.id_rasy}
            onChange={handleChange}
            required
          >
            <option value="">Wybierz rasę</option>
            {rasy.map((rasa) => (
              <option key={rasa.id_rasy} value={rasa.id_rasy}>
                {rasa.nazwa}
              </option>
            ))}
          </select>
        </label>
        <button type="submit">Dodaj Zwierzaka</button>
      </form>
    </div>
  );
};

export default AddPet;

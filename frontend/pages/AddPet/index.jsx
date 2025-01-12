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
    id_gatunku: "",
  });
  const [gatunki, setGatunki] = useState([]); // Lista gatunków
  const [rasy, setRasy] = useState([]); // Lista ras
  const [filteredRasy, setFilteredRasy] = useState([]); // Filtrowane rasy
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [gatunkiResponse, rasyResponse] = await Promise.all([
          apiClient.get("/api/species"), // Pobieranie gatunków
          apiClient.get("/api/races"), // Pobieranie ras
        ]);
        setGatunki(gatunkiResponse.data);
        setRasy(rasyResponse.data);
      } catch (err) {
        console.error("Błąd podczas pobierania danych:", err);
        setError("Nie udało się załadować listy gatunków i ras.");
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    // Filtruj rasy na podstawie wybranego gatunku
    setFilteredRasy(
      rasy.filter((rasa) => rasa.id_gatunku === parseInt(formData.id_gatunku))
    );
  }, [formData.id_gatunku, rasy]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiClient.post("/api/add-pet", formData);
      setSuccess(true);
      setTimeout(() => navigate("/my-pets"), 3000); 
    } catch (err) {
      setError("Wystąpił błąd podczas dodawania zwierzaka.");
    }
  };

  return (
    <div className="add-pet-page">
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
              placeholder="Wpisz imię zwierzaka"
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
              placeholder="Wpisz wiek zwierzaka"
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Opis:
            <textarea
              name="opis"
              value={formData.opis}
              placeholder="Wpisz opis zwierzaka"
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
              <option value="">Wybierz płeć</option>
              <option value="M">Męska</option>
              <option value="F">Żeńska</option>
            </select>
          </label>
          <label>
            Gatunek:
            <select
              name="id_gatunku"
              value={formData.id_gatunku}
              onChange={handleChange}
              required
            >
              <option value="">Wybierz gatunek</option>
              {gatunki.map((gatunek) => (
                <option key={gatunek.id_gatunku} value={gatunek.id_gatunku}>
                  {gatunek.nazwa}
                </option>
              ))}
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
              {filteredRasy.map((rasa) => (
                <option key={rasa.id_rasy} value={rasa.id_rasy}>
                  {rasa.rasa}
                </option>
              ))}
            </select>
          </label>
          <button type="submit">Dodaj zwierzaka</button>
        </form>
      </div>
    </div>
  );
};

export default AddPet;

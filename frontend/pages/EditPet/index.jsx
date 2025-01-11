import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import apiClient from "../../api";
import "./editPet.css";

const EditPet = () => {
  const { id } = useParams();
  const [formData, setFormData] = useState({
    imie: "",
    wiek: "",
    opis: "",
    plec: "",
    id_gatunku: "",
    id_rasy: "",
  });
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPetDetails = async () => {
      try {
        const response = await apiClient.get(`/api/pet-details/${id}`);
        setFormData(response.data);
      } catch (err) {
        console.error("Error fetching pet details:", err);
        setError("Nie udało się załadować danych zwierzaka.");
      }
    };

    fetchPetDetails();
  }, [id]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiClient.put(`/api/pet-details/${id}/edit`, formData);
      setSuccess(true);
      setTimeout(() => navigate("/my-pets"), 2000);
    } catch (err) {
      console.error("Error updating pet details:", err);
      setError("Nie udało się zaktualizować danych zwierzaka.");
    }
  };

  return (
    <div className="edit-pet-container">
      <h1>Edytuj Zwierzaka</h1>
      {success && <p style={{ color: "green" }}>Zwierzak został zaktualizowany.</p>}
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
            <option value="M">Męska</option>
            <option value="F">Żeńska</option>
          </select>
        </label>
        <label>
          Gatunek:
          <input
            type="text"
            name="id_gatunku"
            value={formData.gatunek}
            readOnly
          />
        </label>
        <label>
          Rasa:
          <input
            type="text"
            name="id_rasy"
            value={formData.rasa}
            readOnly
          />
        </label>
        <button type="submit">Zapisz zmiany</button>
      </form>
    </div>
  );
};

export default EditPet;

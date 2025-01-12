import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import apiClient from "../../api";
import "./petDetails.css";

const PetDetails = () => {
  const { id } = useParams();
  const [pet, setPet] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPetDetails = async () => {
      try {
        const response = await apiClient.get(`/api/pet-details/${id}`);
        setPet(response.data);
      } catch (err) {
        console.error("Error fetching pet details:", err);
        setError("Nie udało się załadować szczegółów zwierzaka.");
      }
    };

    fetchPetDetails();
  }, [id]);

  const handleEdit = () => {
    navigate(`/edit-pet/${id}`);
  };

  if (error) {
    return <p className="error">{error}</p>;
  }

  if (!pet) {
    return <p>Ładowanie szczegółów zwierzaka...</p>;
  }

  return (
    <div className="pet-details-container">
      <h1>Szczegóły Zwierzaka</h1>
      <div className="pet-details">
        <p><strong>Imię:</strong> {pet.imie}</p>
        <p><strong>Wiek:</strong> {pet.wiek}</p>
        <p><strong>Opis:</strong> {pet.opis}</p>
        <p><strong>Płeć:</strong> {pet.plec === "M" ? "Męska" : "Żeńska"}</p>
        <p><strong>ID Rasy:</strong> {pet.id_rasy}</p>
        <button className="edit-button" onClick={handleEdit}>
          Edytuj Zwierzaka
        </button>
      </div>
    </div>
  );
};

export default PetDetails;

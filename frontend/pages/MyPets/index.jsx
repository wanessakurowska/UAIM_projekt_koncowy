import React, { useState, useEffect } from "react";
import apiClient from "../../api";
import "./myPets.css";

const MyPets = () => {
  const [pets, setPets] = useState([]);
  const [selectedPet, setSelectedPet] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchPets = async () => {
      try {
        const response = await apiClient.get("/api/my-pets");
        setPets(response.data);
      } catch (err) {
        console.error("Error fetching pets:", err);
        setError("Nie udało się załadować zwierząt.");
      }
    };
    fetchPets();
  }, []);

  const handleSelectPet = async (id) => {
    try {
      const response = await apiClient.get(`/api/pet-details/${id}`);
      setSelectedPet(response.data);
    } catch (err) {
      console.error("Error fetching pet details:", err);
      setError("Nie udało się załadować szczegółów zwierzaka.");
    }
  };

  return (
    <div className="my-pets-container">
      <h1>Moje Zwierzaki</h1>
      {error && <p className="error">{error}</p>}
      <table className="pets-table">
        <thead>
          <tr>
            <th>Imię</th>
            <th>Wiek</th>
            <th>Płeć</th>
            <th>Rasa</th>
            <th>Gatunek</th>
            <th>Akcje</th>
          </tr>
        </thead>
        <tbody>
          {pets.map((pet) => (
            <tr key={pet.id_pupila}>
              <td>{pet.imie}</td>
              <td>{pet.wiek}</td>
              <td>{pet.plec === "M" ? "Samiec" : "Samica"}</td>
              <td>{pet.rasa}</td>
              <td>{pet.gatunek}</td>
              <td>
                <button onClick={() => handleSelectPet(pet.id_pupila)}>
                  Pokaż szczegóły
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {selectedPet && (
        <div className="pet-details">
          <h2>Szczegóły zwierzaka</h2>
          <p>Imię: {selectedPet.imie}</p>
          <p>Wiek: {selectedPet.wiek}</p>
          <p>Opis: {selectedPet.opis}</p>
          <p>Płeć: {selectedPet.plec === "M" ? "Samiec" : "Samica"}</p>
          <p>Rasa: {selectedPet.rasa}</p>
          <p>Gatunek: {selectedPet.gatunek}</p>
          <button
            onClick={() =>
              (window.location.href = `/edit-pet/${selectedPet.id_pupila}`)
            }
          >
            Edytuj
          </button>
        </div>
      )}
    </div>
  );
};

export default MyPets;

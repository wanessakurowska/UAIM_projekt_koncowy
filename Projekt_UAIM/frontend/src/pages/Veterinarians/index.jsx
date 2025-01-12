import React, { useEffect, useState } from "react";
import apiClient from "../../api";
import "./veterinarians.css";

const Veterinarians = () => {
  const [veterinarians, setVeterinarians] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchVeterinarians = async () => {
      try {
        const response = await apiClient.get("/veterinarian-list"); // Endpoint backendu
        setVeterinarians(response.data);
      } catch (err) {
        console.error("Błąd podczas pobierania lekarzy:", err);
        setError("Nie udało się załadować listy lekarzy.");
      }
    };

    fetchVeterinarians();
  }, []);

  if (error) {
    return <p className="error">{error}</p>;
  }

  return (
    <div className="veterinarians-page">
      <div className="veterinarians-container">
        <h1>Lista lekarzy</h1>
        <div className="veterinarians-table-container">
          {veterinarians.length === 0 ? (
            <p>Brak dostępnych lekarzy.</p>
          ) : (
            <table className="veterinarians-table">
              <thead>
                <tr>
                  <th>Imię</th>
                  <th>Nazwisko</th>
                  <th>Doświadczenie</th>
                  <th>Kwalifikacje</th>
                  <th>Ocena</th>
                </tr>
              </thead>
              <tbody>
                {veterinarians.map((vet) => (
                  <tr key={vet.id}>
                    <td>{vet.imię}</td>
                    <td>{vet.nazwisko}</td>
                    <td>{vet.doświadczenie}</td>
                    <td>{vet.kwalifikacje}</td>
                    <td className="rating-cell">
                      {vet.ocena}
                      <i className="fas fa-star"></i>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

export default Veterinarians;

import React, { useState, useEffect } from "react";
import apiClient from "../../api";
import "./completedAppointments.css";

const CompletedAppointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [pets, setPets] = useState([]);
  const [selectedPetId, setSelectedPetId] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Pobierz listę zwierzaków
        const petsResponse = await apiClient.get("/api/my-pets");
        setPets(petsResponse.data);

        // Pobierz wizyty (domyślnie dla wszystkich zwierzaków)
        fetchAppointments();
      } catch (err) {
        console.error("Błąd podczas pobierania danych:", err);
        setError("Nie udało się załadować danych.");
      }
    };

    fetchData();
  }, []);

  const fetchAppointments = async (petId = null) => {
    try {
      const params = petId ? { id_pupila: petId } : {};
      const response = await apiClient.get("/api/completed-appointments", {
        params,
      });
      setAppointments(response.data);
      setError("");
    } catch (err) {
      console.error("Błąd podczas pobierania wizyt:", err);
      setAppointments([]);
      setError("Brak zrealizowanych wizyt lub wystąpił błąd.");
    }
  };

  const handlePetClick = (petId) => {
    setSelectedPetId(petId);
    fetchAppointments(petId);
  };

  return (
    <div className="appointments-container">
      <h1>Zrealizowane wizyty</h1>

      <div className="appointments-content">
        {/* Lista zwierzaków */}
        <div className="pets-list">
          <h2>Twoje zwierzaki</h2>
          <ul>
            <li
              className={!selectedPetId ? "active" : ""}
              onClick={() => handlePetClick(null)}
            >
              Wszystkie zwierzaki
            </li>
            {pets.map((pet) => (
              <li
                key={pet.id_pupila}
                className={selectedPetId === pet.id_pupila ? "active" : ""}
                onClick={() => handlePetClick(pet.id_pupila)}
              >
                {pet.imie}
              </li>
            ))}
          </ul>
        </div>

        {/* Tabela wizyt */}
        <div className="appointments-table-container">
          {error ? (
            <p className="error">{error}</p>
          ) : (
            <table className="appointments-table">
              <thead>
                <tr>
                  <th>Data wizyty</th>
                  <th>Godzina</th>
                  <th>Lekarz</th>
                  <th>Usługa</th>
                  <th>Pupil</th>
                  <th>Powód wizyty</th>
                </tr>
              </thead>
              <tbody>
                {appointments.map((appointment) => (
                  <tr key={`${appointment.data_wizyty}-${appointment.godzina_wizyty}`}>
                    <td>{appointment.data_wizyty}</td>
                    <td>{appointment.godzina_wizyty}</td>
                    <td>{appointment.lekarz}</td>
                    <td>{appointment.usluga.nazwa} ({appointment.usluga.opis})</td>
                    <td>
                      {appointment.pupil.imie} ({appointment.pupil.rasa}, {appointment.pupil.wiek} lat)
                    </td>
                    <td>{appointment.powod_wizyty}</td>
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

export default CompletedAppointments;

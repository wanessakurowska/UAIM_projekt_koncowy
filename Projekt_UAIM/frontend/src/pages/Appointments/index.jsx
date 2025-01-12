import React, { useState, useEffect } from "react";
import apiClient from "../../api";
import "./appointments.css";

const Appointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [pets, setPets] = useState([]);
  const [selectedPetId, setSelectedPetId] = useState(null);
  const [selectedAppointmentId, setSelectedAppointmentId] = useState(null);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("upcoming");
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Pobranie listy zwierzaków
        const petsResponse = await apiClient.get("/api/my-pets");
        setPets(petsResponse.data);

        // Pobranie wizyt wizyty (dla wszystkich zwierzaków)
        fetchAppointments();
      } catch (err) {
        console.error("Błąd podczas pobierania danych:", err);
        setError("Nie udało się załadować danych.");
      }
    };

    fetchData();
  }, []);

  // Pobranie wizyt (opcjonalnie dla wybranego zwierzaka)
  const fetchAppointments = async (petId = null) => {
    try {
      const params = petId ? { id_pupila: petId } : {};
      const response = await apiClient.get("/appointment-list", { params });
      setAppointments(response.data);
      setError("");
    } catch (err) {
      console.error("Błąd podczas pobierania wizyt:", err);
      setAppointments([]);
      setError("Brak wizyt lub wystąpił błąd.");
    }
  };

  // Obsługa kliknięcia na zwierzaka
  const handlePetClick = (petId) => {
    setSelectedPetId(petId);
    fetchAppointments(petId);
  };

  // Filtrowanie wizyt na podstawie filtru - nadchodzące lub zrealizowane
  const filterAppointments = () => {
    const today = new Date().toISOString().split("T")[0];
    return appointments.filter((appointment) => {
      if (filter === "completed") {
        return appointment.data_wizyty < today;
      } else if (filter === "upcoming") {
        return appointment.data_wizyty >= today;
      }
      return true;
    });
  };

  // Pokazanie/ukrycie szczegółów wizyty
  const toggleDetails = (id) => {
    setSelectedAppointmentId((prevId) => (prevId === id ? null : id));
  };

  // Anulowanie wizyty
  const cancelAppointment = async (appointmentId) => {
    try {
      await apiClient.delete(`/api/cancel-appointment/${appointmentId}`);
      setSuccessMessage("Wizyta została pomyślnie odwołana.");
      // Odswieżenie listy wizyt po anulowaniu
      fetchAppointments(selectedPetId);
    } catch (err) {
      console.error("Błąd podczas odwoływania wizyty:", err);
      setError("Nie udało się odwołać wizyty.");
    }
  };

  return (
    <div className="appointments-page">
      <div className="appointments-container">
        <h1>Wizyty</h1>

        {successMessage && <p className="success">{successMessage}</p>}
        <div className="appointments-filters">
          <button
            className={`filter-button ${filter === "upcoming" ? "active" : ""}`}
            onClick={() => setFilter("upcoming")}
          >
            Nadchodzące wizyty
          </button>
          <button
            className={`filter-button ${filter === "completed" ? "active" : ""}`}
            onClick={() => setFilter("completed")}
          >
            Zrealizowane wizyty
          </button>
        </div>

        <div className="appointments-content">
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
                    <th>Pupil</th>
                    <th>Usługa</th>
                    <th>Powód wizyty</th>
                    <th>Akcje</th>
                  </tr>
                </thead>
                <tbody>
                  {filterAppointments().map((appointment) => (
                    <React.Fragment key={`${appointment.data_wizyty}-${appointment.godzina_wizyty}`}>
                      <tr>
                        <td>{appointment.data_wizyty}</td>
                        <td>{appointment.godzina_wizyty}</td>
                        <td>{appointment.lekarz}</td>
                        <td>{appointment.pupil.imie}</td>
                        <td>{appointment.usluga.nazwa}</td>
                        <td>{appointment.powod_wizyty}</td>
                        <td>
                          <button
                            className="details-button"
                            onClick={() => toggleDetails(`${appointment.data_wizyty}-${appointment.godzina_wizyty}`)}
                          >
                            {selectedAppointmentId === `${appointment.data_wizyty}-${appointment.godzina_wizyty}`
                              ? "Ukryj szczegóły"
                              : "Pokaż szczegóły"}
                          </button>
                        </td>
                      </tr>
                      {selectedAppointmentId === `${appointment.data_wizyty}-${appointment.godzina_wizyty}` && (
                        <tr className="details-row">
                          <td colSpan="7">
                            <div className="details-container">
                              <p><strong>Opis usługi:</strong> {appointment.usluga.opis}</p>
                              <p><strong>Koszt usługi:</strong> {appointment.usluga.cena ? `${appointment.usluga.cena} zł` : "Brak danych"}</p>
                              {filter === "upcoming" && (
                                <button
                                  className="details-button"
                                  onClick={() => cancelAppointment(appointment.id_wizyty)}
                                >
                                  Anuluj wizytę
                                </button>
                              )}
                            </div>
                          </td>
                        </tr>
                      )}
                    </React.Fragment>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Appointments;

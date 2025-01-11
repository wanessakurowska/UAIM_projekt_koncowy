import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import apiClient from "../../api";
import "./bookAppointment.css";

const BookAppointment = () => {
  const location = useLocation();
  const { date, time, veterinarianId } = location.state || {};

  const [veterinarians, setVeterinarians] = useState([]);
  const [pets, setPets] = useState([]);
  const [selectedPet, setSelectedPet] = useState("");
  const [selectedService, setSelectedService] = useState("");
  const [description, setDescription] = useState("");
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const vetResponse = await apiClient.get("/veterinarian-list");
        setVeterinarians(vetResponse.data);

        const petResponse = await apiClient.get("/api/my-pets");
        setPets(petResponse.data);
      } catch (err) {
        console.error("Błąd podczas pobierania danych:", err);
        setError("Nie udało się załadować danych.");
      }
    };

    fetchData();
  }, []);

  const handleSubmit = async () => {
    setError("");
    setSuccess("");

    if (!selectedPet || !veterinarianId || !selectedService || !date || !time) {
      setError("Wszystkie pola są wymagane.");
      return;
    }

    const slot = `${date}T${time}`;

    try {
      await apiClient.post("/api/book-appointment", {
        id_pupila: selectedPet,
        id_weterynarza: veterinarianId,
        data_wizyty: date,
        godzina_wizyty_od: slot,
        id_uslugi: selectedService,
        opis_dolegliwosci: description,
      });
      setSuccess("Wizyta została pomyślnie zarezerwowana!");
    } catch (err) {
      console.error("Błąd podczas rezerwacji:", err);
      setError("Nie udało się zarezerwować wizyty.");
    }
  };

  return (
    <div className="book-appointment-page">
      <div className="book-appointment-container">
        <h1>Rezerwacja wizyty</h1>
        {success && <p className="success">{success}</p>}
        {error && <p className="error">{error}</p>}
        <form>
          <label>
            Wybierz pupila:
            <select
              value={selectedPet}
              onChange={(e) => setSelectedPet(e.target.value)}
            >
              <option value="">-- Wybierz pupila --</option>
              {pets.map((pet) => (
                <option key={pet.id_pupila} value={pet.id_pupila}>
                  {pet.imie}
                </option>
              ))}
            </select>
          </label>
          <label>
            Weterynarz:
            <select value={veterinarianId} disabled>
              {veterinarians.map((vet) => (
                <option key={vet.id} value={vet.id}>
                  {vet.imię} {vet.nazwisko}
                </option>
              ))}
            </select>
          </label>
          <label>
            Data:
            <input type="date" value={date} readOnly />
          </label>
          <label>
            Godzina:
            <input type="time" value={time} readOnly />
          </label>
          <label>
            Wybierz usługę:
            <select
              value={selectedService}
              onChange={(e) => setSelectedService(e.target.value)}
            >
              <option value="">-- Wybierz usługę --</option>
              <option value="1">Badanie kontrolne</option>
              <option value="2">Szczepienie</option>
              <option value="3">Sterylizacja</option>
              <option value="4">Czipowanie</option>
            </select>
          </label>
          <label>
            Opis dolegliwości:
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Opisz dolegliwości pupila"
            />
          </label>
          <button type="button" onClick={handleSubmit}>
            Zarezerwuj wizytę
          </button>
        </form>
      </div>
    </div>
  );
};

export default BookAppointment;

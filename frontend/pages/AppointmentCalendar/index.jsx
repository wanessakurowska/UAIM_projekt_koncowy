import React, { useState, useEffect } from "react";
import apiClient from "../../api";
import "./calendar.css";

const AppointmentCalendar = () => {
  const [veterinarians, setVeterinarians] = useState([]);
  const [services, setServices] = useState([]);
  const [veterinarianId, setVeterinarianId] = useState("");
  const [serviceId, setServiceId] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedTime, setSelectedTime] = useState("");
  const [petId, setPetId] = useState("");
  const [opisDolegliwosci, setOpisDolegliwosci] = useState("");
  const [pets, setPets] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isAvailable, setIsAvailable] = useState(false);
  const hours = Array.from({ length: 13 }, (_, i) => (8 + i).toString().padStart(2, "0"));
  const minutes = Array.from({ length: 12 }, (_, i) => (i * 5).toString().padStart(2, "0"));

  useEffect(() => {
    const fetchData = async () => {
      try {
        const vetResponse = await apiClient.get("/veterinarian-list");
        setVeterinarians(vetResponse.data);

        const serviceResponse = await apiClient.get("/service-list");
        setServices(serviceResponse.data);

        const petResponse = await apiClient.get("/api/my-pets");
        setPets(petResponse.data);
      } catch (err) {
        console.error("Błąd podczas pobierania danych:", err);
        setError("Nie udało się załadować danych.");
      }
    };

    fetchData();
  }, []);

  const checkAvailability = async () => {
    setSuccess("");
    setError("");

    if (!veterinarianId || !selectedDate || !selectedTime) {
      setError("Wybierz weterynarza, datę i godzinę, aby sprawdzić dostępność.");
      return;
    }

    const formattedTime = `${selectedDate}T${selectedTime}`;

    try {
      const response = await apiClient.get("/api/vet-availability", {
        params: {
          id_weterynarza: parseInt(veterinarianId),
          data_wizyty: selectedDate,
          godzina_wizyty_od: formattedTime,
        },
      });

      if (response.data.available) {
        setSuccess("Termin jest dostępny! Możesz go zarezerwować.");
        setIsAvailable(true);
      } else {
        setError("Termin jest zajęty.");
        setIsAvailable(false);
      }
    } catch (err) {
      console.error("Błąd podczas sprawdzania dostępności:", err);
      setError("Nie udało się sprawdzić dostępności terminu.");
      setIsAvailable(false);
    }
  };

  const bookAppointment = async () => {
    setSuccess("");
    setError("");

    if (!petId || !serviceId || !opisDolegliwosci.trim()) {
      setError("Wszystkie pola są wymagane.");
      return;
    }

    const formattedTime = `${selectedDate}T${selectedTime}`;

    try {
      await apiClient.post("/api/book-appointment", {
          id_pupila: parseInt(petId),
          id_weterynarza: parseInt(veterinarianId),
          data_wizyty: selectedDate,
          godzina_wizyty_od: formattedTime,
          id_uslugi: parseInt(serviceId),
          opis_dolegliwosci: opisDolegliwosci
        });

      setSuccess("Termin został pomyślnie zarezerwowany!");
      setIsAvailable(false);
      setOpisDolegliwosci("");
    } catch (err) {
      console.error("Błąd podczas rezerwacji terminu:", err);
      setError("Nie udało się zarezerwować terminu.");
    }
  };

  return (
    <div className="calendar-container">
      <h1>Rezerwacja wizyty</h1>
      {success && <p className="success">{success}</p>}
      {error && <p className="error">{error}</p>}
      <form>
        <label>
          Wybierz weterynarza:
          <select
            value={veterinarianId}
            onChange={(e) => setVeterinarianId(e.target.value)}
            required
          >
            <option value="">-- Wybierz weterynarza --</option>
            {veterinarians.map((vet) => (
              <option key={vet.id} value={vet.id}>
                {vet.imię} {vet.nazwisko}
              </option>
            ))}
          </select>
        </label>
        <label>
          Wybierz usługę:
          <select
            value={serviceId}
            onChange={(e) => setServiceId(e.target.value)}
            required
          >
            <option value="">-- Wybierz usługę --</option>
            {services.map((service) => (
              <option key={service.id} value={service.id}>
                {service.nazwa} - {service.cena} zł
              </option>
            ))}
          </select>
        </label>
        <label>
          Wybierz datę wizyty:
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            required
          />
        </label>
        <label>
          Wybierz godzinę wizyty:
          <div style={{ display: "flex", gap: "10px" }}>
            <select
              value={selectedTime.split(":")[0]}
              onChange={(e) =>
                setSelectedTime(`${e.target.value}:${selectedTime.split(":")[1]}`)
              }
            >
              <option value="">Godzina</option>
              {hours.map((hour) => (
                <option key={hour} value={hour}>
                  {hour}
                </option>
              ))}
            </select>
            <select
              value={selectedTime.split(":")[1]}
              onChange={(e) =>
                setSelectedTime(`${selectedTime.split(":")[0]}:${e.target.value}`)
              }
            >
              <option value="">Minuty</option>
              {minutes.map((minute) => (
                <option key={minute} value={minute}>
                  {minute}
                </option>
              ))}
            </select>
          </div>
        </label>
        <label>
          Wybierz pupila:
          <select value={petId} onChange={(e) => setPetId(e.target.value)} required>
            <option value="">-- Wybierz pupila --</option>
            {pets.map((pet) => (
              <option key={pet.id_pupila} value={pet.id_pupila}>
                {pet.imie} - {pet.rasa} ({pet.wiek} lat)
              </option>
            ))}
          </select>
        </label>
        <label>
          Opis dolegliwości:
          <textarea
            value={opisDolegliwosci}
            onChange={(e) => setOpisDolegliwosci(e.target.value)}
            placeholder="Opisz dolegliwości pupila"
            required
            onInput={(e) => {
              e.target.style.height = "auto"; // Resetuje wysokość
              e.target.style.height = `${e.target.scrollHeight}px`; // Ustawia wysokość na podstawie zawartości
            }}
          ></textarea>
        </label>
        <button type="button" onClick={checkAvailability}>
          Sprawdź dostępność
        </button>
        <button type="button" onClick={bookAppointment} disabled={!isAvailable}>
          Zarezerwuj termin
        </button>
      </form>
    </div>
  );
};

export default AppointmentCalendar;

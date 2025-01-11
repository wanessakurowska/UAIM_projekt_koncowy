import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../../api";
import "./calendar.css";

const AppointmentCalendar = () => {
  const [veterinarians, setVeterinarians] = useState([]);
  const [availableSlots, setAvailableSlots] = useState([]);
  const [currentDates, setCurrentDates] = useState([]); // Daty aktualnie widoczne na stronie
  const [selectedVeterinarian, setSelectedVeterinarian] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const daysToShow = 7; // Liczba dni wyświetlanych w jednym widoku

  useEffect(() => {
    const fetchVeterinarians = async () => {
      try {
        const response = await apiClient.get("/veterinarian-list");
        setVeterinarians(response.data);
      } catch (err) {
        console.error("Błąd podczas pobierania listy weterynarzy:", err);
        setError("Nie udało się załadować listy weterynarzy.");
      }
    };

    fetchVeterinarians();

    // Ustaw daty początkowe (dziś i kolejne 6 dni)
    const startDate = new Date();
    const initialDates = Array.from({ length: daysToShow }, (_, i) =>
      new Date(startDate.getTime() + i * 24 * 60 * 60 * 1000)
    );
    setCurrentDates(initialDates);
  }, []);

  // Użyj useCallback, aby funkcja była stabilna między renderami
  const fetchAvailableSlots = useCallback(async () => {
      setError("");
      setAvailableSlots([]);

      if (!selectedVeterinarian) {
        setError("Wybierz weterynarza.");
        return;
      }

      try {
        const response = await apiClient.get("/api/available-slots", {
          params: {
            date_from: currentDates[0].toISOString().split("T")[0],
            date_to: currentDates[currentDates.length - 1].toISOString().split("T")[0],
            id_weterynarza: selectedVeterinarian,
          },
        });

        setAvailableSlots(
          response.data.map((slot) => ({
            slot: `${slot.date}T${slot.time}`,
            available: slot.available,
          }))
        );
      } catch (err) {
        console.error("Błąd podczas pobierania wolnych terminów:", err);
        setError("Nie udało się pobrać wolnych terminów.");
      }
    }, [selectedVeterinarian, currentDates]); // Dodaj selectedVeterinarian jako zależność

  useEffect(() => {
    if (selectedVeterinarian) {
      fetchAvailableSlots();
    }
  }, [fetchAvailableSlots, selectedVeterinarian]); // Dodaj selectedVeterinarian tutaj


  const handleSlotClick = (slot) => {
    const [date, time] = slot.split("T");
    navigate("/book-appointment", {
      state: {
        date,
        time,
        veterinarianId: selectedVeterinarian,
      },
    });
  };

  // Przesuń zakres dat w przód
  const nextDates = () => {
    const newDates = currentDates.map(
      (date) => new Date(date.getTime() + daysToShow * 24 * 60 * 60 * 1000)
    );
    setCurrentDates(newDates);
  };

  // Przesuń zakres dat w tył
  const prevDates = () => {
    const newDates = currentDates.map(
      (date) => new Date(date.getTime() - daysToShow * 24 * 60 * 60 * 1000)
    );
    setCurrentDates(newDates);
  };

  return (
    <div className="calendar-container">
      <h1>Kalendarz wizyt</h1>
      {error && <p className="error">{error}</p>}
      <div className="form-inline">
        <select
          value={selectedVeterinarian}
          onChange={(e) => setSelectedVeterinarian(e.target.value)}
        >
          <option value="">-- Wybierz weterynarza --</option>
          {veterinarians.map((vet) => (
            <option key={vet.id} value={vet.id}>
              {vet.imię} {vet.nazwisko}
            </option>
          ))}
        </select>
      </div>
      <div className="calendar-navigation">
        <button onClick={prevDates} className="navigation-button">
          ◀
        </button>
        <button onClick={nextDates} className="navigation-button">
          ▶
        </button>
      </div>
      <div className="calendar">
        {currentDates.map((date) => (
          <div key={date.toISOString()} className="day-column">
            <h3>
              {date.toLocaleDateString("pl-PL", {
                weekday: "short",
                day: "numeric",
                month: "short",
              })}
            </h3>
            {availableSlots
              .filter((slot) => slot.slot.startsWith(date.toISOString().split("T")[0]))
              .map((slot) => (
                <div
                  key={slot.slot}
                  className={`time-slot ${slot.available ? "available" : "unavailable"}`}
                  onClick={() => slot.available && handleSlotClick(slot.slot)}
                >
                  {slot.slot.split("T")[1]}
                </div>
              ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AppointmentCalendar;

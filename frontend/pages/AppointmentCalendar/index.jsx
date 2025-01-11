import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../../api";
import "./calendar.css";

const AppointmentCalendar = () => {
  const [veterinarians, setVeterinarians] = useState([]);
  const [availableSlots, setAvailableSlots] = useState([]);
  const [dates, setDates] = useState([]);
  const [selectedDateRange, setSelectedDateRange] = useState({ from: "", to: "" });
  const [selectedVeterinarian, setSelectedVeterinarian] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

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
  }, []);

  const fetchAvailableSlots = async () => {
    setError("");
    setAvailableSlots([]);
    setDates([]);

    if (!selectedVeterinarian || !selectedDateRange.from || !selectedDateRange.to) {
      setError("Wybierz weterynarza i zakres dat.");
      return;
    }

    try {
      const response = await apiClient.get("/api/available-slots", {
        params: {
          date_from: selectedDateRange.from,
          date_to: selectedDateRange.to,
          id_weterynarza: selectedVeterinarian,
        },
      });

      const uniqueDates = [...new Set(response.data.map((slot) => slot.date))];
      setDates(uniqueDates);
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
  };

  const handleSlotClick = (slot) => {
    navigate("/book-appointment", { state: { slot, veterinarianId: selectedVeterinarian } });
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
        <input
          type="date"
          value={selectedDateRange.from}
          onChange={(e) =>
            setSelectedDateRange({ ...selectedDateRange, from: e.target.value })
          }
        />
        <input
          type="date"
          value={selectedDateRange.to}
          onChange={(e) =>
            setSelectedDateRange({ ...selectedDateRange, to: e.target.value })
          }
        />
        <button type="button" onClick={fetchAvailableSlots}>
          Pokaż wolne terminy
        </button>
      </div>
      <div className="calendar">
        {dates.map((date) => (
          <div key={date} className="day-column">
            <h3>
              {new Date(date).toLocaleDateString("pl-PL", {
                weekday: "short",
                day: "numeric",
                month: "short",
              })}
            </h3>
            {availableSlots
              .filter((slot) => slot.slot.startsWith(date))
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

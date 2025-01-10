import React, { useEffect, useState } from "react";
import apiClient from "../../api";
import "./services.css";

const Services = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchServices = async () => {
      try {
        const response = await apiClient.get("/service-list");
        setServices(response.data);
      } catch (err) {
        console.error("Błąd podczas pobierania usług:", err);
        setError("Nie udało się załadować usług.");
      } finally {
        setLoading(false);
      }
    };

    fetchServices();
  }, []);

  if (loading) {
    return <p>Ładowanie usług...</p>;
  }

  if (error) {
    return <p className="error">{error}</p>;
  }

  return (
    <div className="services-container">
      <h1>Katalog usług</h1>
      {services.length === 0 ? (
        <p>Brak dostępnych usług.</p>
      ) : (
        <table className="services-table">
          <thead>
            <tr>
              <th>Nazwa</th>
              <th>Opis</th>
              <th>Cena</th>
              <th>Dostępność</th>
            </tr>
          </thead>
          <tbody>
            {services.map((service) => (
              <tr key={service.id}>
                <td>{service.nazwa}</td>
                <td>{service.opis || "Brak opisu"}</td>
                <td>{service.cena ? `${service.cena} zł` : "Cena nieokreślona"}</td>
                <td>{service.dostepnosc || "Nieznana"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Services;

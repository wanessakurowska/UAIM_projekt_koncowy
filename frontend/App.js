import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Services from "./pages/Services";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Veterinarians from "./pages/Veterinarians";
import AppointmentCalendar from "./pages/AppointmentCalendar";
import CompletedAppointments from "./pages/CompletedAppointments";
import Register from "./pages/Register";
import AddPet from "./pages/AddPet";
import EditPet from "./pages/EditPet";
import MyPets from "./pages/MyPets";
import BookAppointment from "./pages/BookAppointment";

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <Navbar />
      <div style={{ minHeight: "calc(100vh - 100px)" }}>
        {/* Główna zawartość strony */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/services" element={<Services />} />
          <Route path="/veterinarians" element={<Veterinarians />} />
          <Route
            path="/appointment-calendar"
            element={
              <PrivateRoute>
                <AppointmentCalendar />
              </PrivateRoute>
            }
          />
          <Route
            path="/book-appointment"
            element={
              <PrivateRoute>
                <BookAppointment />
              </PrivateRoute>
            }
          />
          <Route path="/completed-appointments" element={<CompletedAppointments />} />
          <Route
            path="/my-pets"
            element={
              <PrivateRoute>
                <MyPets />
              </PrivateRoute>
            }
          />
          <Route
            path="/edit-pet/:id"
            element={
              <PrivateRoute>
                <EditPet />
              </PrivateRoute>
            }
          />
          <Route
            path="/add-pet"
            element={
              <PrivateRoute>
                <AddPet />
              </PrivateRoute>
            }
            />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
      <Footer />
    </Router>
  );
}

export default App;

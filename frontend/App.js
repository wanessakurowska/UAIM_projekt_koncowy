import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Services from "./pages/Services";
import Veterinarians from "./pages/Veterinarians";
import Register from "./pages/Register";
import Login from "./pages/Login";
import AppointmentCalendar from "./pages/AppointmentCalendar";
import CompletedAppointments from "./pages/CompletedAppointments";
import AddPet from "./pages/AddPet";
import EditPet from "./pages/EditPet";
import MyPets from "./pages/MyPets";

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/services" element={<Services />} />
        <Route path="/veterinarians" element={<Veterinarians />} />
        <Route path="/appointment-calendar" element={<AppointmentCalendar />} />
        <Route path="/completed-appointments" element={<CompletedAppointments/>} />
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
    </Router>
  );
}

export default App;

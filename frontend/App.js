import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Services from "./pages/Services";
import Login from "./pages/Login";
import Veterinarians from "./pages/Veterinarians";
import Register from "./pages/Register";
import AddPet from "./pages/AddPet";

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
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/add-pet"
          element={
            <PrivateRoute>
              <AddPet />
            </PrivateRoute>
          }
        />

      </Routes>
    </Router>
  );
}

export default App;

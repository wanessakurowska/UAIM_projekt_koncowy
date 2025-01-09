import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Services from "./pages/Services";
import Veterinarians from "./pages/Veterinarians";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/services" element={<Services />} />
        <Route path="/veterinarians" element={<Veterinarians />} />
      </Routes>
    </Router>
  );
}

export default App;

import { useState, useEffect, } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import SensorList from "./SensorList";
import "./App.css";
import SensorForm from "./SensorForm";
import SensorDetailsPage from "./SensorDetailsPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import Navbar from "./components/Navbar";
import { AuthProvider, useAuth } from "./context/AuthContext";

// The logic from your old App.jsx is now the HomePage
const HomePage = () => {
  const [sensors, setSensors] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [currentSensor, setCurrentSensor] = useState({})
  const { isAuthenticated, authFetch } = useAuth();

  useEffect(() => {
    fetchSensors()
  }, []);

  const fetchSensors = async () => {
    const response = await fetch("http://127.0.0.1:5000/sensors");
    const data = await response.json(); 
    setSensors(data.sensors);
  };

  const closeModal = () => {
    setIsModalOpen(false)
    setCurrentSensor({})
  }

  const openCreateModal = () => {
    if (isAuthenticated && !isModalOpen) setIsModalOpen(true)
  }

  const openEditModal = (sensor) => {
    if (isModalOpen) return
    setCurrentSensor(sensor)
    setIsModalOpen(true)
  }

  const onUpdate = () => {
    closeModal()
    fetchSensors()
  }

  return (
    <>
      <SensorList sensors={sensors} updateSensor={openEditModal} updateCallback={onUpdate} />
      {isAuthenticated && <button onClick={openCreateModal}>Create New Sensor</button>}
      {isModalOpen && <div className="modal">
        <div className="modal-content">
          <span className="close" onClick={closeModal}>&times;</span>
          <SensorForm existingSensor={currentSensor} updateCallback={onUpdate} />
        </div>
      </div>
      }
    </>
  );
}

function App() {
  // This is the main component that orchestrates the routing.
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <main className="container">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/details_sensor/:sensorId" element={<SensorDetailsPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
          </Routes>
        </main>
      </Router>
    </AuthProvider>
  );
}

export default App;
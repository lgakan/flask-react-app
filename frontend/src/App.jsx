import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ServerList from "./ServerList";
import "./App.css";
import ServerForm from "./ServerForm";
import ServerDetailsPage from "./ServerDetailsPage";

// The logic from your old App.jsx is now the HomePage
const HomePage = () => {
  const [servers, setServers] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [currentServer, setCurrentServer] = useState({})

  useEffect(() => {
    fetchServers()
  }, []);

  const fetchServers = async () => {
    const response = await fetch("http://127.0.0.1:5000/servers");
    const data = await response.json();
    setServers(data.servers);
  };

  const closeModal = () => {
    setIsModalOpen(false)
    setCurrentServer({})
  }

  const openCreateModal = () => {
    if (!isModalOpen) setIsModalOpen(true)
  }

  const openEditModal = (server) => {
    if (isModalOpen) return
    setCurrentServer(server)
    setIsModalOpen(true)
  }

  const onUpdate = () => {
    closeModal()
    fetchServers()
  }

  return (
    <>
      <ServerList servers={servers} updateServer={openEditModal} updateCallback={onUpdate} />
      <button onClick={openCreateModal}>Create New Server</button>
      {isModalOpen && <div className="modal">
        <div className="modal-content">
          <span className="close" onClick={closeModal}>&times;</span>
          <ServerForm existingServer={currentServer} updateCallback={onUpdate} />
        </div>
      </div>
      }
    </>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/details_server/:serverId" element={<ServerDetailsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
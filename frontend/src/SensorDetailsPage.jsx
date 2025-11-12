import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import SensorGraph from './SensorGraph';
import DataPointForm from './DataPointForm';
import './SensorDetailsPage.css'; // Import component-specific styles
import { useAuth } from './context/AuthContext';

const SensorDetailsPage = () => {
    const [sensorDetails, setSensorDetails] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentDataPoint, setCurrentDataPoint] = useState({});
    const { sensorId } = useParams(); // Get the sensorId from the URL
    const { isAuthenticated, authFetch } = useAuth();

    // Use useCallback to prevent re-creating the function on every render
    const fetchDetails = React.useCallback(async () => {
        try {
            // Reset states for re-fetching
            setLoading(true);
            setError(null);
            const response = await fetch(`http://127.0.0.1:5000/details_sensor/${sensorId}`);
            if (!response.ok) {
                throw new Error('Sensor not found');
            }
            const data = await response.json();
            setSensorDetails(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        } 
    }, [sensorId]);

    useEffect(() => {
        fetchDetails();
    }, [fetchDetails]);

    const closeModal = () => {
        setIsModalOpen(false);
        setCurrentDataPoint({});
    };

    const openCreateModal = () => {
        if (isAuthenticated) {
            setCurrentDataPoint({}); // Ensure form is for creation
            setIsModalOpen(true);
        }
    };

    const openEditModal = (dataPoint) => {
        setCurrentDataPoint(dataPoint);
        setIsModalOpen(true);
    };

    const onDataUpdate = () => {
        closeModal();
        fetchDetails(); // Re-fetch all data to update the page
    };

    const deleteDataPoint = async (dataId) => {
        if (window.confirm("Are you sure you want to delete this data point?")) {
            const url = `http://127.0.0.1:5000/sensor_data/${dataId}`;
            const response = await authFetch(url, { method: "DELETE" });
            if (response.status === 200) {
                onDataUpdate();
            } else {
                const data = await response.json();
                alert(data.message);
            }
        }
    };

    const handlePrint = () => {
        window.print();
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    // Don't render the component until the data has been fetched.
    if (!sensorDetails) return null;

    return (
        <div>
            <div className="no-print page-controls">
                <Link to="/">
                    <button className="button-secondary">&larr; Back to Sensor List</button>
                </Link>
                <button onClick={handlePrint}>Print</button>
            </div>
            <div className="page-header">
                <h2>{sensorDetails.name} ({sensorDetails.ipAddress})</h2>
                <p>Owner: {sensorDetails.ownerName}</p>
            </div>
            <div className="sensor-graph-container">
                <SensorGraph dataPoints={sensorDetails.dataPoints || []} onPointClick={openEditModal} />
            </div>

            {isAuthenticated && (
                <button onClick={openCreateModal} className="no-print button-primary">Add New Data Point</button>
            )}

            {isModalOpen && ( // The modal itself should not be printed
                <div className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={closeModal}>&times;</span>
                        <DataPointForm
                            existingData={currentDataPoint}
                            sensorId={sensorId}
                            updateCallback={onDataUpdate}
                        />
                    </div>
                </div>
            )}

        </div>
    );
};

export default SensorDetailsPage;
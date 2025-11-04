import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import ServerGraph from './ServerGraph';
import DataPointForm from './DataPointForm';

const ServerDetailsPage = () => {
    const [serverDetails, setServerDetails] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentDataPoint, setCurrentDataPoint] = useState({});
    const { serverId } = useParams(); // Get the serverId from the URL

    // Use useCallback to prevent re-creating the function on every render
    const fetchDetails = React.useCallback(async () => {
        try {
            // Reset states for re-fetching
            setLoading(true);
            setError(null);
            const response = await fetch(`http://127.0.0.1:5000/details_server/${serverId}`);
            if (!response.ok) {
                throw new Error('Server not found');
            }
            const data = await response.json();
            setServerDetails(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [serverId]);

    useEffect(() => {
        fetchDetails();
    }, [fetchDetails]);

    const closeModal = () => {
        setIsModalOpen(false);
        setCurrentDataPoint({});
    };

    const openCreateModal = () => {
        setCurrentDataPoint({}); // Ensure form is for creation
        setIsModalOpen(true);
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
            const url = `http://127.0.0.1:5000/server_data/${dataId}`;
            const options = { method: "DELETE" };
            const response = await fetch(url, options);
            if (response.status === 200) {
                onDataUpdate();
            } else {
                const data = await response.json();
                alert(data.message);
            }
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    // Don't render the component until the data has been fetched.
    if (!serverDetails) return null;

    return (
        <div>
            <Link to="/">Back to Server List</Link>
            <h2>Usage Details for {serverDetails.name} ({serverDetails.ipAddress})</h2>
            <ServerGraph dataPoints={serverDetails.dataPoints || []} onPointClick={openEditModal} />

            <button onClick={openCreateModal}>Add New Data Point</button>

            {isModalOpen && (
                <div className="modal">
                    <div className="modal-content">
                        <span className="close" onClick={closeModal}>&times;</span>
                        <DataPointForm
                            existingData={currentDataPoint}
                            serverId={serverId}
                            updateCallback={onDataUpdate}
                        />
                    </div>
                </div>
            )}

        </div>
    );
};

export default ServerDetailsPage;
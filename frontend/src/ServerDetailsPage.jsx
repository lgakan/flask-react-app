import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import ServerGraph from './ServerGraph';

const ServerDetailsPage = () => {
    const [serverDetails, setServerDetails] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { serverId } = useParams(); // Get the serverId from the URL

    useEffect(() => {
        const fetchDetails = async () => {
            try {
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
        };

        fetchDetails();
    }, [serverId]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    // Don't render the component until the data has been fetched.
    if (!serverDetails) return null;

    return (
        <div>
            <Link to="/">Back to Server List</Link>
            <h2>Usage Details for {serverDetails.firstName}</h2>
            <ServerGraph graphData={serverDetails.graphData} />
        </div>
    );
};

export default ServerDetailsPage;
import React, { useState } from 'react';

const DataPointForm = ({ existingData = {}, serverId, updateCallback }) => {
    const [cpuUsage, setCpuUsage] = useState(existingData.cpuUsage || "");
    const [memoryUsage, setMemoryUsage] = useState(existingData.memoryUsage || "");

    const isUpdating = Object.keys(existingData).length > 0;

    const onSubmit = async (e) => {
        e.preventDefault();

        const data = {
            cpuUsage: parseFloat(cpuUsage),
            memoryUsage: parseFloat(memoryUsage),
            serverId: serverId,
        };

        const url = "http://127.0.0.1:5000/" + (isUpdating ? `server_data/${existingData.id}` : "server_data");
        const options = {
            method: isUpdating ? "PATCH" : "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        };

        const response = await fetch(url, options);
        if (response.status !== 201 && response.status !== 200) {
            const responseData = await response.json();
            alert(responseData.message);
        } else {
            updateCallback(); // Refresh the data on the details page
        }
    };

    return (
        <form onSubmit={onSubmit}>
            <div>
                <label htmlFor="cpuUsage">CPU Usage (%):</label>
                <input
                    type="number"
                    id="cpuUsage"
                    value={cpuUsage}
                    onChange={(e) => setCpuUsage(e.target.value)}
                    step="0.1"
                />
            </div>
            <div>
                <label htmlFor="memoryUsage">Memory Usage (%):</label>
                <input
                    type="number"
                    id="memoryUsage"
                    value={memoryUsage}
                    onChange={(e) => setMemoryUsage(e.target.value)}
                    step="0.1"
                />
            </div>
            <p>Timestamp: {isUpdating ? new Date(existingData.timestamp).toLocaleString() : "Now"}</p>
            <button type="submit">{isUpdating ? "Update Data Point" : "Create Data Point"}</button>
        </form>
    );
};

export default DataPointForm;
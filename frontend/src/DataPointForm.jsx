import React, { useState } from 'react';

// Helper to format a Date object into a string suitable for datetime-local input (YYYY-MM-DDTHH:mm)
const formatDateTimeForInput = (date) => {
    if (!date) return '';
    const d = new Date(date);
    // Adjust for the local timezone offset to display the correct local time in the input
    const timezoneOffset = d.getTimezoneOffset() * 60000; // in milliseconds
    const localDate = new Date(d.getTime() - timezoneOffset);
    return localDate.toISOString().slice(0, 16);
};

const DataPointForm = ({ existingData = {}, serverId, updateCallback }) => {
    const [cpuUsage, setCpuUsage] = useState(existingData.cpuUsage || "");
    const [memoryUsage, setMemoryUsage] = useState(existingData.memoryUsage || "");
    const [timestamp, setTimestamp] = useState(formatDateTimeForInput(existingData.timestamp || new Date()));
    
    const isUpdating = Object.keys(existingData).length > 0;

    const onSubmit = async (e) => {
        e.preventDefault();

        const cpu = parseFloat(cpuUsage);
        const memory = parseFloat(memoryUsage);

        if (isNaN(cpu) || cpu < 0 || cpu > 100) {
            alert("CPU Usage must be a number between 0 and 100.");
            return;
        }
        if (isNaN(memory) || memory < 0 || memory > 100) {
            alert("Memory Usage must be a number between 0 and 100.");
            return;
        }

        const data = {
            cpuUsage: cpu,
            memoryUsage: memory,
            serverId: serverId,
            timestamp: new Date(timestamp).toISOString(), // Send timestamp in standard ISO format
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
                    min="0"
                    max="100"
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
                    min="0"
                    max="100"
                />
            </div>
            <div>
                <label htmlFor="timestamp">Timestamp:</label>
                <input
                    type="datetime-local"
                    id="timestamp"
                    value={timestamp}
                    onChange={(e) => setTimestamp(e.target.value)}
                />
            </div>
            <button type="submit">{isUpdating ? "Update Data Point" : "Create Data Point"}</button>
        </form>
    );
};

export default DataPointForm;
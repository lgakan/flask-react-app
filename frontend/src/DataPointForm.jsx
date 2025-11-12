import React, { useState } from 'react';
import { useAuth } from './context/AuthContext';
import "./Form.css"; // Import shared form styles

// Helper to format a Date object into a string suitable for datetime-local input (YYYY-MM-DDTHH:mm)
const formatDateTimeForInput = (date) => {
    if (!date) return '';
    const d = new Date(date);
    // Adjust for the local timezone offset to display the correct local time in the input
    const timezoneOffset = d.getTimezoneOffset() * 60000; // in milliseconds
    const localDate = new Date(d.getTime() - timezoneOffset);
    return localDate.toISOString().slice(0, 16);
};

const DataPointForm = ({ existingData = {}, sensorId, updateCallback }) => {
    const [temperature, setTemperature] = useState(existingData.temperature || "");
    const [humidity, setHumidity] = useState(existingData.humidity || "");
    const [pressure, setPressure] = useState(existingData.pressure || "");
    const [lightLevel, setLightLevel] = useState(existingData.lightLevel || "");
    const [timestamp, setTimestamp] = useState(formatDateTimeForInput(existingData.timestamp || new Date()));
    
    const isUpdating = Object.keys(existingData).length > 0;
    const { authFetch } = useAuth();

    const onSubmit = async (e) => {
        e.preventDefault();
        
        const data = {
            temperature: parseFloat(temperature),
            humidity: parseFloat(humidity),
            pressure: pressure ? parseFloat(pressure) : null,
            lightLevel: lightLevel ? parseFloat(lightLevel) : null,
            sensorId: sensorId,
            timestamp: new Date(timestamp).toISOString(), // Send timestamp in standard ISO format
        };

        // Basic validation
        if (isNaN(data.temperature) || isNaN(data.humidity)) {
            alert("Temperature and Humidity must be valid numbers.");
            return;
        }

        const url = "http://127.0.0.1:5000/" + (isUpdating ? `sensor_data/${existingData.id}` : "sensor_data");
        const options = {
            method: isUpdating ? "PATCH" : "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        };
        const response = await authFetch(url, options);
        if (response.status !== 201 && response.status !== 200) {
            const responseData = await response.json();
            alert(responseData.message);
        } else {
            updateCallback(); // Refresh the data on the details page
        }
    };

    return (
        <form onSubmit={onSubmit} className="form-container">
            <h3>{isUpdating ? "Update Data Point" : "Add New Data Point"}</h3>
            <div className="form-group">
                <label htmlFor="temperature">Temperature (°C):</label>
                <input
                    type="number"
                    id="temperature"
                    value={temperature}
                    onChange={(e) => setTemperature(e.target.value)}
                    required
                    step="0.1"
                />
            </div>
            <div className="form-group">
                <label htmlFor="humidity">Humidity (%):</label>
                <input
                    type="number"
                    id="humidity"
                    value={humidity}
                    onChange={(e) => setHumidity(e.target.value)}
                    required
                    step="0.1"
                />
            </div>
            <div className="form-group">
                <label htmlFor="pressure">Pressure (hPa):</label>
                <input
                    type="number"
                    id="pressure"
                    value={pressure}
                    onChange={(e) => setPressure(e.target.value)}
                    placeholder="Optional"
                    step="0.1"
                />
            </div>
            <div className="form-group">
                <label htmlFor="lightLevel">Light Level (lux):</label>
                <input
                    type="number"
                    id="lightLevel"
                    value={lightLevel}
                    onChange={(e) => setLightLevel(e.target.value)}
                    placeholder="Optional"
                    step="1"
                />
            </div>
            <div className="form-group">
                <label htmlFor="timestamp">Timestamp:</label>
                <input
                    type="datetime-local"
                    id="timestamp"
                    value={timestamp}
                    onChange={(e) => setTimestamp(e.target.value)}
                    required
                />
            </div>
            <button type="submit" className="button-primary">
                {isUpdating ? "Update Data Point" : "Create Data Point"}
            </button>
        </form>
    );
};

export default DataPointForm;
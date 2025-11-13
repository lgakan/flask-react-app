import React from "react"
import { Link } from "react-router-dom"
import {useAuth} from "./context/AuthContext";

const SensorList = ({ sensors, updateSensor, updateCallback }) => {
    const { isAuthenticated, authFetch } = useAuth()
    const onDelete = async (id) => {
        try {
            const options = {
                method: "DELETE"
            }
            const response = await authFetch(`https://flask-react-app-backend.onrender.com/delete_sensor/${id}`, options)
            if (response.status === 200) {
                updateCallback()
            } else {
                console.error("Error deleting sensor:", response)
                console.error("Failed to delete")
            }
        } catch (error) {
            alert(error)
        }
    }

    return <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <div>
            <h2>Sensors</h2>
            {/* This wrapper div makes the table scroll horizontally on small screens */}
            <div style={{ width: '100%', overflowX: 'auto' }}>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>IP Address</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sensors.map((sensor) => (
                            <tr key={sensor.id}>
                                <td>{sensor.name}</td>
                                <td>{sensor.ipAddress}</td>
                                <td style={{ whiteSpace: 'nowrap' }}>
                                    <div style={{ display: 'flex', gap: '5px', alignItems: 'center' }}>
                                        <Link to={`/details_sensor/${sensor.id}`}>
                                            <button>Details</button>
                                        </Link>
                                        {isAuthenticated && <>
                                            <button onClick={() => updateSensor(sensor)}>Update</button>
                                            <button onClick={() => onDelete(sensor.id)}>Delete</button>
                                        </>}
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
}

export default SensorList
import React from "react"
import { Link } from "react-router-dom"
// import {useAuth} from "./context/AuthContext";

const SensorList = ({ sensors, updateSensor, updateCallback }) => {
    // const { isAuthenticated, authFetch } = useAuth()
    const onDelete = async (id) => {
        try {
            const options = {
                method: "DELETE"
            }
            const response = await fetch(`http://127.0.0.1:5000/delete_sensor/${id}`, options)
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

    return <div>
        <h2>Sensors</h2>
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
                        <td>
                            <Link to={`/details_sensor/${sensor.id}`}>
                                <button>Details</button>
                            </Link>
                            <button onClick={() => updateSensor(sensor)}>Update</button>
                            <button onClick={() => onDelete(sensor.id)}>Delete</button>
                            {/*{isAuthenticated && <>*/}
                            {/*    <button onClick={() => updateSensor(sensor)}>Update</button>*/}
                            {/*    <button onClick={() => onDelete(sensor.id)}>Delete</button>*/}
                            {/*</>}*/}
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}

export default SensorList
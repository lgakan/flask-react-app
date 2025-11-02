import React from "react"

const ServerList = ({ servers, updateServer, updateCallback }) => {
    const onDelete = async (id) => {
        try {
            const options = {
                method: "DELETE"
            }
            const response = await fetch(`http://127.0.0.1:5000/delete_server/${id}`, options)
            if (response.status === 200) {
                updateCallback()
            } else {
                console.error("Failed to delete")
            }
        } catch (error) {
            alert(error)
        }
    }

    return <div>
        <h2>Servers</h2>
        <table>
            <thead>
                <tr>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Email</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {servers.map((server) => (
                    <tr key={server.id}>
                        <td>{server.firstName}</td>
                        <td>{server.lastName}</td>
                        <td>{server.email}</td>
                        <td>
                            <button onClick={() => updateServer(server)}>Update</button>
                            <button onClick={() => onDelete(server.id)}>Delete</button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}

export default ServerList
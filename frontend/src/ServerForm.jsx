import { useState } from "react";

const ServerForm = ({ existingServer = {}, updateCallback }) => {
    const [name, setName] = useState(existingServer.name || "");
    const [ipAddress, setIpAddress] = useState(existingServer.ipAddress || "");

    const isUpdating = Object.keys(existingServer).length > 0;

    const onSubmit = async (e) => {
        e.preventDefault()

        const data = {
            name,
            ipAddress
        }
        const url = "http://127.0.0.1:5000/" + (isUpdating ? `update_server/${existingServer.id}` : "create_server")
        const options = {
            method: isUpdating ? "PATCH" : "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
        const response = await fetch(url, options)
        if (response.status !== 201 && response.status !== 200) {
            const data = await response.json()
            alert(data.message)
        } else {
            updateCallback()
        }
    }

    return (
        <form onSubmit={onSubmit}>
            <div>
                <label htmlFor="name">Server Name:</label>
                <input
                    type="text"
                    id="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="ipAddress">IP Address:</label>
                <input
                    type="text"
                    id="ipAddress"
                    value={ipAddress}
                    onChange={(e) => setIpAddress(e.target.value)}
                />
            </div>
            <button type="submit">{isUpdating ? "Update" : "Create"}</button>
        </form>
    );
};

export default ServerForm;
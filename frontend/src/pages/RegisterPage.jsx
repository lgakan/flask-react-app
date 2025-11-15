import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../AuthForm.css';

const RegisterPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        try {
            const response = await fetch('https://flask-react-app-backend.onrender.com/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password, firstName, lastName, email }),
            });

            const data = await response.json();

            if (response.ok) {
                setSuccess(data.message || 'Registration successful! Please log in.');
                setTimeout(() => navigate('/login'), 2000);
            } else {
                setError(data.message || 'Registration failed');
            }
        } catch (err) {
            setError('Network error or server unreachable.');
            console.error('Registration error:', err);
        }
    };

    return (
        <div className="auth-container">
            <form className="auth-form" onSubmit={handleSubmit}>
                <h2>Register</h2>
                {error && <p style={{ color: 'var(--error-color)', textAlign: 'center' }}>{error}</p>}
                {success && <p style={{ color: 'var(--success-color)', textAlign: 'center' }}>{success}</p>}
                <div className="form-group">
                    <label htmlFor="firstName">First Name:</label>
                    <input type="text" id="firstName" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
                </div>
                <div className="form-group">
                    <label htmlFor="lastName">Last Name:</label>
                    <input type="text" id="lastName" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
                </div>
                <div className="form-group">
                    <label htmlFor="email">Email:</label>
                    <input type="email" id="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                </div>
                <div className="form-group">
                    <label htmlFor="username">Username:</label>
                    <input type="text" id="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <button type="submit" className="button-primary">Register</button>
            </form>
        </div>
    );
};

export default RegisterPage;
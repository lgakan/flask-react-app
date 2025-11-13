import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import '../AuthForm.css';
import '../print.css';

const ProfilePage = () => {
    const { authFetch, user, logout } = useAuth();
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handlePasswordChange = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (newPassword !== confirmPassword) {
            setError("New passwords do not match.");
            return;
        }

        try {
            const response = await authFetch('https://flask-react-app-backend.onrender.com/change_password', {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ currentPassword, newPassword }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Failed to change password.');
            }

            setSuccess('Password changed successfully! You will be logged out shortly.');
            setTimeout(() => {
                logout();
            }, 3000);

        } catch (err) {
            setError(err.message);
        }
    };

    if (!user) return <div>Loading profile...</div>;

    return (
        <div className="auth-container">
            <div className="auth-form">
                <h2>User Profile</h2>
                {user && (
                    <div className="profile-details">
                        <p><strong>Name:</strong> {user.firstName} {user.lastName}</p>
                        <p><strong>Email:</strong> {user.email}</p>
                    </div>
                )}
            </div>

            <form className="auth-form no-print" onSubmit={handlePasswordChange} style={{marginTop: '2rem'}}>
                <h2>Change Password</h2>
                {error && <p style={{ color: 'var(--error-color)', textAlign: 'center' }}>{error}</p>}
                {success && <p style={{ color: 'var(--success-color)', textAlign: 'center' }}>{success}</p>}
                <div className="form-group">
                    <label htmlFor="currentPassword">Current Password:</label>
                    <input
                        type="password"
                        id="currentPassword"
                        value={currentPassword}
                        onChange={(e) => setCurrentPassword(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="newPassword">New Password:</label>
                    <input
                        type="password"
                        id="newPassword"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="confirmPassword">Confirm New Password:</label>
                    <input
                        type="password"
                        id="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="button-primary">Change Password</button>
            </form>
        </div>
    );
};

export default ProfilePage;
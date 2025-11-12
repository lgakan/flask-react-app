import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
    const { isAuthenticated, logout, user } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <nav className="navbar">
            <Link to="/" className="nav-brand">Sensor Dashboard</Link>
            <div className="nav-links">
                {isAuthenticated ? (
                    <>
                        <span>Welcome, {user.firstName}!</span>
                        <button onClick={handleLogout} className="nav-button">Logout</button>
                    </>
                ) : (
                    <Link to="/login" className="nav-button">Login</Link>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
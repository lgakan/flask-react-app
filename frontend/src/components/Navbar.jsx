import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../App.css'; // Import App-wide styles for header/nav

const Navbar = () => {
    const { isAuthenticated, logout, user } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login'); // Redirect to login page after logout
    };

    return (
        <header className="app-header no-print">
            <nav className="app-nav">
                <Link to="/" className="app-nav-title">Sensor Dashboard</Link>
                <div className="app-nav-links">
                    {isAuthenticated ? (
                        <>
                            <span>Hello, {user?.firstName || user?.username}!</span>
                            <button onClick={handleLogout}>Logout</button>
                        </>
                    ) : (
                        <Link to="/login" className="button-primary">Login</Link>
                    )}
                </div>
            </nav>
        </header>
    );
};

export default Navbar;
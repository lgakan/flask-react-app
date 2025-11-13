import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';

const AuthContext = createContext(null);

export const useAuth = () => useContext(AuthContext);
 
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export const AuthProvider = ({ children }) => {
    const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken'));
    const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken'));
    const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')));
    const [isRefreshing, setIsRefreshing] = useState(false);

    useEffect(() => {
        if (accessToken) {
            localStorage.setItem('accessToken', accessToken);
        } else {
            localStorage.removeItem('accessToken');
        }
        if (refreshToken) {
            localStorage.setItem('refreshToken', refreshToken);
        } else {
            localStorage.removeItem('refreshToken');
        }
        if (user) {
            localStorage.setItem('user', JSON.stringify(user));
        } else {
            localStorage.removeItem('user');
        }
    }, [accessToken, refreshToken, user]);

    const login = (newAccessToken, newRefreshToken, userData) => {
        setAccessToken(newAccessToken);
        setRefreshToken(newRefreshToken);
        setUser(userData);
    };

    const logout = useCallback(() => {
        setAccessToken(null);
        setRefreshToken(null);
        setUser(null);
        window.location.href = '/login';
    }, []);

    const authFetch = useCallback(async (url, options = {}) => {
        // A function to perform the actual fetch with a given token
        const performFetch = async (token) => {
            const headers = { ...options.headers };

            if (options.body) {
                headers['Content-Type'] = 'application/json';
            }
            console.log(token)
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            return fetch(url, { ...options, headers });
        };

        let response = await performFetch(accessToken);

        if (response.status === 401 && !isRefreshing) {
            setIsRefreshing(true);
            try {
                // Attempt to refresh the token
                const refreshResponse = await fetch(`/refresh`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${refreshToken}`
                    }
                });

                if (!refreshResponse.ok) {
                    // If refresh fails, logout the user
                    throw new Error('Failed to refresh token');
                }

                const { accessToken: newAccessToken } = await refreshResponse.json();
                setAccessToken(newAccessToken);

                // Retry the original request with the new token
                response = await performFetch(newAccessToken);

            } catch (error) {
                console.error("Session refresh failed:", error);
                logout(); // Logout on refresh failure
                // Return the original failed response to avoid breaking the calling component
                return response;
            } finally {
                setIsRefreshing(false);
            }
        }

        return response;
    }, [accessToken, refreshToken, isRefreshing, logout]);

    const value = {
        accessToken,
        user,
        login,
        logout,
        authFetch,
        isAuthenticated: !!accessToken
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
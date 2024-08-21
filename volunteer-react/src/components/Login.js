import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [token, setToken] = useState('');
    const [error, setError] = useState(''); // For error messages
    const [success, setSuccess] = useState(''); // For success messages

    const handleLogin = async (e) => {
        e.preventDefault();
        
        // Payload to be sent
        const payload = {
            email,
            password,
        };

        console.log('Payload being sent:', payload);

        try {
            // Make the API call
            const response = await axios.post('http://127.0.0.1:8000/api-django/users/login/', payload);


            // Response received
            console.log('Response received:', response);

            const accessToken = response.data.access;
            setToken(accessToken);
            localStorage.setItem('token', accessToken);
            setSuccess('Login successful!'); // Set success message
            setError(''); // Clear any previous error messages
        } catch (error) {
            console.error('Login failed:', error);
            setError('Login failed: ' + (error.response?.data?.detail || 'Unknown error')); // Set error message
            setSuccess(''); // Clear any previous success messages
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Login</button>
            </form>
            {token && <p>Token: {token}</p>}
            {success && <p style={{ color: 'green' }}>{success}</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
};

export default Login;

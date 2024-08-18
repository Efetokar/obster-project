import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import '../components/Login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:5000/login', {
        email,
        password
      }, { withCredentials: true }); // Include credentials
      if (response.data.success) {
        navigate('/home');  // Redirect to homepage
      } else {
        alert(response.data.message);
      }
    } catch (error) {
      console.error("There was an error logging in!", error);
      alert('Login failed. Please try again.');
    }
  };

  return (
    <div className="login-container">
      <div className="login-left">
        <div>
          <h1 className="title">OBSTER</h1>
          <p className="subtitle">Personalized Diet & Exercise Application</p>
        </div>
      </div>
      <div className="login-right">
        <h2>WELCOME</h2>
        <div className="signup-link">
          <p>Don't have an account? <Link to="/signup">Sign up here</Link></p>
        </div>
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button onClick={handleLogin}>Login</button>
      </div>
    </div>
  );
}

export default Login;

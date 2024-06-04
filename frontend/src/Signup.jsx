import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

function Signup() {
  const history = useNavigate();

  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); // State for error messages

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/signup', {
        username,
        email,
        password,
      });

      console.log(response);

      history('/login');
    } catch (error) {
  
      if (error.response && error.response.status === 500) {
        setError('An error occurred. Please try again later.');
      }
      else if(error.response && error.response.status===400){
        setError('Email Already Registered');
      }
      // Handle other error cases if needed
    }
  }

  return (
    <div className='auth-form'>
      <form>
        <div className='form-inner'>
          <h2>Sign Up</h2>
          <div className='form-group error'>
            {error && <p className="error-message">{error}</p>}
          </div>
          <div className='form-group'>
            <label htmlFor='username'>Username: </label>
            <input type="text" name="username" id="username" onChange={(e) => setUsername(e.target.value)} value={username} />
          </div>
          <div className='form-group'>
            <label htmlFor='email'>Email: </label>
            <input type="text" name="email" id="email" onChange={(e) => setEmail(e.target.value)} value={email} />
          </div>
          <div className='form-group'>
            <label htmlFor='password'>Password: </label>
            <input type="password" name="password" id="password" onChange={(e) => setPassword(e.target.value)} value={password} />
          </div>
          <button onClick={handleSignup}>Sign Up</button>
          <div className='Signuplink'><Link to='/login' style={{ textDecoration: 'none', color: 'white' }}>Already Have an Account?</Link></div>
        </div>
      </form>
    </div>
  );
}

export default Signup;

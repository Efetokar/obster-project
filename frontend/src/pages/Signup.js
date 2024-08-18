import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import '../components/Signup.css'; // Ensure you create this CSS file for styling
import Slider from '@mui/material/Slider'; // For the slider component
import Modal from '@mui/material/Modal'; // Import Modal component

function Signup() {
  const [name, setName] = useState('');
  const [surname, setSurname] = useState('');
  const [email, setEmail] = useState('');
  const [birthdate, setBirthdate] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [gender, setGender] = useState('');
  const [height, setHeight] = useState('');
  const [weight, setWeight] = useState('');
  const [waist, setWaist] = useState('');
  const [activityLevel, setActivityLevel] = useState('');
  const [sleepDuration, setSleepDuration] = useState(7); // Default to 7 hours
  const [smoke, setSmoke] = useState(false);
  const [dietPref, setDietPref] = useState('');
  const [waterIntake, setWaterIntake] = useState('');
  const [diabetes, setDiabetes] = useState(false);
  const [hypertension, setHypertension] = useState(false);

  const [errors, setErrors] = useState({});
  const [showModal, setShowModal] = useState(false); // Modal visibility state
  const navigate = useNavigate();

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  };

  const validatePassword = (password) => {
    const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return re.test(password);
  };

  const handleSignup = () => {
    const newErrors = {};

    if (!name) newErrors.name = 'Name is required';
    if (!surname) newErrors.surname = 'Surname is required';
    if (!email || !validateEmail(email)) newErrors.email = 'Valid email is required';
    if (!birthdate) newErrors.birthdate = 'Birthdate is required';
    if (!gender) newErrors.gender = 'Gender is required';
    if (!height || height <= 0) newErrors.height = 'Valid height is required';
    if (!weight || weight <= 0) newErrors.weight = 'Valid weight is required';
    if (!waist || waist <= 0) newErrors.waist = 'Valid waist circumference is required';
    if (!dietPref) newErrors.dietPref = 'Diet preference is required';
    if (!waterIntake || waterIntake <= 0) newErrors.waterIntake = 'Valid water intake is required';
    if (!password || !validatePassword(password)) newErrors.password = 'Password must contain at least 8 characters, including uppercase, lowercase, number, and special character';
    if (password !== confirmPassword) newErrors.confirmPassword = 'Passwords do not match';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    axios.post('http://localhost:5000/signup', {
      name,
      surname,
      email,
      birthdate,
      password,
      gender,
      height: `${height} cm`,
      weight: `${weight} kg`,
      waist: `${waist} cm`,
      activityLevel,
      sleepDuration,
      smoke,
      dietPref,
      waterIntake,
      diabetes,
      hypertension
    }).then(response => {
      if (response.data.message === 'User created successfully. Please verify your email.') {
        setShowModal(true); // Show modal on success
      } else {
        alert(response.data.message);
      }
    }).catch(error => {
      console.error("There was an error signing up!", error);
    });
  };

  const handleCloseModal = () => {
    setShowModal(false);
    navigate('/verify-email', { state: { email } }); // Redirect to the next step
  };

  return (
    <div className="signup-wrapper">
      <div className="signup-container">
        <h2>OBSTER</h2>
        <p>Personalized Diet & Exercise Application</p>
        <div className="login-link">
          <p>Already have an account? <Link to="/login">Login here</Link></p>
        </div>
        <div className="input-container">
          <input type="text" id="name" value={name} onChange={(e) => setName(e.target.value)} required />
          <label htmlFor="name">Name</label>
          {errors.name && <div className="error-tooltip">⚠️ {errors.name}</div>}
        </div>
        <div className="input-container">
          <input type="text" id="surname" value={surname} onChange={(e) => setSurname(e.target.value)} required />
          <label htmlFor="surname">Surname</label>
          {errors.surname && <div className="error-tooltip">⚠️ {errors.surname}</div>}
        </div>
        <div className="input-container">
          <input type="email" id="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <label htmlFor="email">Email</label>
          {errors.email && <div className="error-tooltip">⚠️ {errors.email}</div>}
        </div>
        <div className="input-container">
          <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <label htmlFor="password">Password</label>
          {errors.password && <div className="error-tooltip">⚠️ {errors.password}</div>}
        </div>
        
        <div className="input-container">
          <input type="password" id="confirmPassword" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
          <label htmlFor="confirmPassword">Confirm Password</label>
          {errors.confirmPassword && <div className="error-tooltip">⚠️ {errors.confirmPassword}</div>}
        </div>
        <div className="input-container">
          <input type="date" id="birthdate" value={birthdate} onChange={(e) => setBirthdate(e.target.value)} required />
          <label htmlFor="birthdate">Birthdate</label>
          {errors.birthdate && <div className="error-tooltip">⚠️ {errors.birthdate}</div>}
        </div>
        <div className="input-container">
          <select id="gender" value={gender} onChange={(e) => setGender(e.target.value)} required>
            <option value="" disabled>Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
          <label htmlFor="gender">Gender</label>
          {errors.gender && <div className="error-tooltip">⚠️ {errors.gender}</div>}
        </div>
        <div className="input-pair">
          <div className="input-container">
            <input 
              type="number" 
              id="height" 
              value={height} 
              onChange={(e) => setHeight(e.target.value)} 
              required 
            />
            <label htmlFor="height">Height (cm)</label>
            {errors.height && <div className="error-tooltip">⚠️ {errors.height}</div>}
          </div>
        </div>
        <div className="input-pair">
          <div className="input-container">
            <input 
              type="number" 
              id="weight" 
              value={weight} 
              onChange={(e) => setWeight(e.target.value)} 
              required 
            />
            <label htmlFor="weight">Weight (kg)</label>
            {errors.weight && <div className="error-tooltip">⚠️ {errors.weight}</div>}
          </div>
        </div>
        <div className="input-pair">
          <div className="input-container">
            <input 
              type="number" 
              id="waist" 
              value={waist} 
              onChange={(e) => setWaist(e.target.value)} 
              required 
            />
            <label htmlFor="waist">Waist Circumference (cm)</label>
            {errors.waist && <div className="error-tooltip">⚠️ {errors.waist}</div>}
          </div>
        </div>
        
        <div className="sleep-label-container">
          <label>Sleep Duration (hours)</label>
        </div>

        <div className="input-container">
          <Slider
            value={sleepDuration}
            min={4}
            max={12}
            step={1}
            onChange={(e, value) => setSleepDuration(value)}
            valueLabelDisplay="auto"
          />
        </div>

        <div className="binary-options-container">
          <label>Do you smoke?</label>
          <div className="binary-options">
            <button 
              type="button" 
              className={`binary-button ${smoke === true ? 'selected' : ''}`} 
              onClick={() => setSmoke(true)}
            >
              Yes
            </button>
            <button 
              type="button" 
              className={`binary-button ${smoke === false ? 'selected' : ''}`} 
              onClick={() => setSmoke(false)}
            >
              No
            </button>
          </div>
        </div>

        <div className="input-container">
          <select id="dietPref" value={dietPref} onChange={(e) => setDietPref(e.target.value)} required>
            <option value="" disabled>Diet Preference</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="vegan">Vegan</option>
            <option value="gluten-free">Gluten-Free</option>
            <option value="standard">Standard</option>
          </select>
          <label htmlFor="dietPref">Diet Preference</label>
          {errors.dietPref && <div className="error-tooltip">⚠️ {errors.dietPref}</div>}
        </div>

        <div className="input-container">
          <input 
            type="number" 
            id="waterIntake" 
            value={waterIntake} 
            onChange={(e) => setWaterIntake(e.target.value)} 
          />
          <label htmlFor="waterIntake">Daily Water Intake (liters)</label>
          {errors.waterIntake && <div className="error-tooltip">⚠️ {errors.waterIntake}</div>}
        </div>

        <div className="binary-options-container">
          <label>Do you have diabetes?</label>
          <div className="binary-options">
            <button 
              type="button" 
              className={`binary-button ${diabetes === true ? 'selected' : ''}`} 
              onClick={() => setDiabetes(true)}
            >
              Yes
            </button>
            <button 
              type="button" 
              className={`binary-button ${diabetes === false ? 'selected' : ''}`} 
              onClick={() => setDiabetes(false)}
            >
              No
            </button>
          </div>
        </div>

        <div className="binary-options-container">
          <label>Do you have hypertension?</label>
          <div className="binary-options">
            <button 
              type="button" 
              className={`binary-button ${hypertension === true ? 'selected' : ''}`} 
              onClick={() => setHypertension(true)}
            >
              Yes
            </button>
            <button 
              type="button" 
              className={`binary-button ${hypertension === false ? 'selected' : ''}`} 
              onClick={() => setHypertension(false)}
            >
              No
            </button>
          </div>
        </div>

        <div className="activity-level-container">
          <label>Physical Activity Level</label>
          <div className="activity-level-buttons">
            <button
              type="button"
              className={`activity-button ${activityLevel === '1' ? 'selected' : ''}`}
              onClick={() => setActivityLevel('1')}
            >
              1 (Sedentary)
            </button>
            <button
              type="button"
              className={`activity-button ${activityLevel === '2' ? 'selected' : ''}`}
              onClick={() => setActivityLevel('2')}
            >
              2 (Light Activity)
            </button>
            <button
              type="button"
              className={`activity-button ${activityLevel === '3' ? 'selected' : ''}`}
              onClick={() => setActivityLevel('3')}
            >
              3 (Moderate Activity)
            </button>
            <button
              type="button"
              className={`activity-button ${activityLevel === '4' ? 'selected' : ''}`}
              onClick={() => setActivityLevel('4')}
            >
              4 (High Activity)
            </button>
          </div>
        </div>
        <div className="button-container">
          <button onClick={handleSignup}>Register</button>
        </div>
      </div>

      {/* Modal for success message */}
      <Modal
        open={showModal}
        onClose={handleCloseModal}
        aria-labelledby="modal-title"
        aria-describedby="modal-description"
      >
        <div className="modal-overlay">
          <div className="modal-content">
            <h2 id="modal-title">Signup Successful!</h2>
            <p id="modal-description">User created successfully. Please verify your email.</p>
            <button onClick={handleCloseModal}>Next</button>
          </div>
        </div>
      </Modal>

    </div>
  );
}

export default Signup;

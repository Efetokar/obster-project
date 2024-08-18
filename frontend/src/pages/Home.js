import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../components/Home.css';
import settingsLogo from '../assets/OBSTER-settings-logo.png';
import logoutLogo from '../assets/OBSTER-logout-logo.png';
import EditPopup from './EditPopup';  // Import the EditPopup component

function Home() {
  const [obesityPrediction, setObesityPrediction] = useState(null);
  const [breakfastSuggestion, setBreakfastSuggestion] = useState(null);
  const [lunchSuggestion, setLunchSuggestion] = useState(null);
  const [dinnerSuggestion, setDinnerSuggestion] = useState(null);
  const [snackSuggestion, setSnackSuggestion] = useState(null);
  const [exerciseSuggestion, setExerciseSuggestion] = useState(null);
  const [user, setUser] = useState(null);
  const [showLogoutPopup, setShowLogoutPopup] = useState(false);
  const [showEditPopup, setShowEditPopup] = useState(false);
  const [showSettingsPopup, setShowSettingsPopup] = useState(false); // State for showing the Settings Popup
  const [showAboutPopup, setShowAboutPopup] = useState(false); // State for showing the About Popup
  const [showChangePasswordPopup, setShowChangePasswordPopup] = useState(false); // State for showing the Change Password Popup
  const [showPasswordChangeMessagePopup, setShowPasswordChangeMessagePopup] = useState(false); // State for showing the Password Change Message Popup
  const [passwordChangeMessage, setPasswordChangeMessage] = useState(''); // Content of the Password Change Message

  // Fetch user info and other suggestions
  const fetchUserInfo = async () => {
    try {
      const response = await axios.get('http://localhost:5000/user-info', { withCredentials: true });
      setUser(response.data);
    } catch (error) {
      console.error("An error occurred while fetching user info!", error);
    }
  };

  const fetchPrediction = async () => {
    try {
      const response = await axios.post('http://localhost:5000/predict-obesity', {}, { withCredentials: true });
      setObesityPrediction(response.data.obesity_prediction);
    } catch (error) {
      console.error("An error occurred during the prediction!", error);
    }
  };

  const fetchBreakfastSuggestion = async () => {
    try {
      const response = await axios.post('http://localhost:5000/predict-breakfast', {}, { withCredentials: true });
      setBreakfastSuggestion(response.data);
    } catch (error) {
      console.error("An error occurred while fetching the breakfast suggestion!", error);
    }
  };

  const fetchLunchSuggestion = async () => {
    try {
      const response = await axios.post('http://localhost:5000/predict-lunch', {}, { withCredentials: true });
      setLunchSuggestion(response.data);
    } catch (error) {
      console.error("An error occurred while fetching the lunch suggestion!", error);
    }
  };

  const fetchDinnerSuggestion = async () => {
    try {
      const response = await axios.post('http://localhost:5000/predict-dinner', {}, { withCredentials: true });
      setDinnerSuggestion(response.data);
    } catch (error) {
      console.error("An error occurred while fetching the dinner suggestion!", error);
    }
  };

  const fetchSnackSuggestion = async () => {
    try {
      const response = await axios.post('http://localhost:5000/predict-snack', {}, { withCredentials: true });
      setSnackSuggestion(response.data);
    } catch (error) {
      console.error("An error occurred while fetching the snack suggestion!", error);
    }
  };

  const fetchExerciseSuggestion = async () => {
    try {
      const response = await axios.post('http://localhost:5000/predict-exercise', {}, { withCredentials: true });
      setExerciseSuggestion(response.data.exercise_suggestion);
    } catch (error) {
      console.error("An error occurred while fetching the exercise suggestion!", error);
    }
  };

  useEffect(() => {
    fetchUserInfo();
    fetchPrediction();
    fetchBreakfastSuggestion();
    fetchLunchSuggestion();
    fetchDinnerSuggestion();
    fetchSnackSuggestion();
    fetchExerciseSuggestion();
  }, []);

  const handleSave = async (updatedUserInfo) => {
    try {
        const response = await axios.put('http://localhost:5000/update-user-info', updatedUserInfo, { withCredentials: true });
        setUser(response.data);  // Update user info with the response data
        window.location.reload();
    } catch (error) {
        console.error("An error occurred while updating user info!", error);
    }
};

  const handleLogout = async () => {
    try {
      const response = await axios.post('http://localhost:5000/logout', {}, { withCredentials: true });
      if (response.data.message === 'Logout successful.') {
        window.location.href = '/login';
      }
    } catch (error) {
      console.error("An error occurred during logout!", error);
    }
  };

  const handleChangePassword = async (oldPassword, newPassword, verifyPassword) => {
    if (newPassword !== verifyPassword) {
      setPasswordChangeMessage('New passwords do not match.');
      setShowPasswordChangeMessagePopup(true);
      return;
    }
    try {
      const response = await axios.post('http://localhost:5000/change-password', {
        old_password: oldPassword,
        new_password: newPassword
      }, { withCredentials: true });
      
      setPasswordChangeMessage(response.data.message);
      setShowChangePasswordPopup(false); // Close the change password popup
      setShowPasswordChangeMessagePopup(true); // Show the message popup
    } catch (error) {
      console.error("An error occurred while changing the password!", error);
      setPasswordChangeMessage('An error occurred while changing the password. Please try again.');
      setShowPasswordChangeMessagePopup(true);
    }
  };

  return (
    <div className="home-container">
      <div className="header">
        <h1 className="header-title">OBSTER</h1>
        <div className="header-right">
          <img src={settingsLogo} alt="Settings" className="header-logo settings-logo" onClick={() => setShowSettingsPopup(true)} />
          <img src={logoutLogo} alt="Logout" className="header-logo logout-logo" onClick={() => setShowLogoutPopup(true)} />
        </div>
      </div>

      <div className="main-content">
        <div className="left-panel">
          {user ? (
            <>
              <div className="welcome-message-container">
                <h2 className="welcome-message">Welcome back, {user.name}</h2>
                <button className="edit-info-button" onClick={() => setShowEditPopup(true)}>Update</button>
              </div>
              <div className="prediction-cards">
                <div className="prediction-card obesity-card" style={{ backgroundColor: '#FFC107' }}>
                  <p className='obesity-title'><strong>Obesity Suggestion</strong></p>
                  <p className='obesity-p'>{obesityPrediction !== null ? obesityPrediction : "Loading..."}</p>
                </div>
                <div className="prediction-card" style={{ backgroundColor: '#4CAF50' }}>
                  <p><strong>Exercise Suggestion</strong></p>
                  <p>{exerciseSuggestion !== null ? exerciseSuggestion : "Loading..."}</p>
                </div>
              </div>

              <div className="user-info-cards">
                <div className="info-card" style={{ backgroundColor: '#A140DD' }}>
                  <p className="measure"><strong>{user.weight}</strong></p>
                  <p className='measure-title'>kg</p>
                </div>
                <div className="info-card height-card" style={{ backgroundColor: '#E31D1D' }}>
                  <p className="corner-label">H</p>
                  <p className="measure"><strong>{user.height}</strong></p>
                  <p className='measure-title'>cm</p>
                </div>
                <div className="info-card waist-card" style={{ backgroundColor: '#E69332' }}>
                  <p className="corner-label">W</p>
                  <p className="measure"><strong>{user.waist}</strong></p>
                  <p className='measure-title'>cm</p>
                </div>
                <div className="info-card" style={{ backgroundColor: '#000000' }}>
                  <p className="measure"><strong>{user.age}</strong></p>
                  <p className='measure-title'>years</p>
                </div>
                <div className="info-card" style={{ backgroundColor: '#409BDD' }}>
                  <p className="measure"><strong>{user.activity_level}</strong></p>
                  <p className='activity-title'>Activity Level</p>
                </div>
              </div>

            </>
          ) : (
            <p>Loading user info...</p>
          )}
        </div>
        <div className="right-panel">
          <div className="meal-row">
            <div className="meal-card">
              <h2>Today's Breakfast</h2>
              {breakfastSuggestion ? (
                <div>
                  <p>{breakfastSuggestion.breakfast_suggestion}</p>
                  <p><strong>Calories:</strong> {Math.round(breakfastSuggestion.calories)} kcal</p>
                </div>
              ) : (
                <p>Loading breakfast suggestion...</p>
              )}
            </div>
            <div className="meal-card">
              <h2>Today's Lunch</h2>
              {lunchSuggestion ? (
                <div>
                  <p>{lunchSuggestion.lunch_suggestion}</p>
                  <p><strong>Calories:</strong> {Math.round(lunchSuggestion.calories)} kcal</p>
                </div>
              ) : (
                <p>Loading lunch suggestion...</p>
              )}
            </div>
          </div>
          <div className="meal-row">
            <div className="meal-card">
              <h2>Today's Dinner</h2>
              {dinnerSuggestion ? (
                <div>
                  <p>{dinnerSuggestion.dinner_suggestion}</p>
                  <p><strong>Calories:</strong> {Math.round(dinnerSuggestion.calories)} kcal</p>
                </div>
              ) : (
                <p>Loading dinner suggestion...</p>
              )}
            </div>
            <div className="meal-card">
              <h2>Today's Snack</h2>
              {snackSuggestion ? (
                <div>
                  <p>{snackSuggestion.snack_suggestion}</p>
                  <p><strong>Calories:</strong> {Math.round(snackSuggestion.calories)} kcal</p>
                </div>
              ) : (
                <p>Loading snack suggestion...</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {showLogoutPopup && (
        <div className="logout-popup-overlay">
          <div className="logout-popup">
            <h2>Are you sure you want to logout?</h2>
            <button onClick={handleLogout}>Yes</button>
            <button onClick={() => setShowLogoutPopup(false)}>No</button>
          </div>
        </div>
      )}

      {showEditPopup && user && (
        <div className="edit-popup-overlay">
          <EditPopup
            user={user}
            onClose={() => setShowEditPopup(false)}
            onSave={handleSave}
          />
        </div>
      )}

      {showSettingsPopup && (
        <div className="settings-popup-overlay">
          <div className="settings-popup">
            <button className="close-button" onClick={() => setShowSettingsPopup(false)}>X</button>
            <h2>Settings</h2>
            <div className="settings-buttons">
              <button onClick={() => { setShowChangePasswordPopup(true); setShowSettingsPopup(false); }}>Change Password</button>
              <button onClick={() => { setShowAboutPopup(true); setShowSettingsPopup(false); }}>About</button>
            </div>
          </div>
        </div>
      )}

      {showAboutPopup && (
        <div className="about-popup-overlay">
          <div className="about-popup">
            <button className="close-button" onClick={() => setShowAboutPopup(false)}>X</button>
            <h2>About OBSTER</h2>
            <p>OBSTER is a comprehensive personalized diet and exercise application designed to help users manage their health
              and well-being by providing tailored recommendations based on individual profiles. Leveraging advanced machine
              learning models, OBSTER offers customized daily meal plans and exercise routines that consider factors such
              as dietary preferences, BMI, physical activity level, and health conditions like diabetes or hypertension.
              The application includes predictive models for obesity risk assessment and health monitoring, allowing users
              to track their progress over time and make informed decisions. Built with a secure and user-friendly interface
              using Flask and React, OBSTER ensures a seamless experience with real-time updates, secure login, and data 
              confidentiality. This dynamic platform adapts to the user's evolving needs, integrating data-driven insights
              to support a healthier lifestyle.</p>
          </div>
        </div>
      )}

      {showChangePasswordPopup && (
        <div className="change-password-popup-overlay">
          <div className="change-password-popup">
            <button className="close-button" onClick={() => setShowChangePasswordPopup(false)}>X</button>
            <h2>Change Password</h2>
            <input type="password" placeholder="Old Password" id="oldPassword" />
            <input type="password" placeholder="New Password" id="newPassword" />
            <input type="password" placeholder="Verify New Password" id="verifyPassword" />
            <button onClick={() => handleChangePassword(
              document.getElementById('oldPassword').value,
              document.getElementById('newPassword').value,
              document.getElementById('verifyPassword').value
            )}>Change Password</button>
          </div>
        </div>
      )}

      {showPasswordChangeMessagePopup && (
        <div className="message-popup-overlay">
          <div className="message-popup">
            <button className="close-button" onClick={() => setShowPasswordChangeMessagePopup(false)}>X</button>
            <h2>Password Change</h2>
            <p>{passwordChangeMessage}</p>
          </div>
        </div>
      )}

    </div>
  );
}

export default Home;

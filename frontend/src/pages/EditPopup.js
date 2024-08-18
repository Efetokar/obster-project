import React, { useState, useEffect } from 'react';
import '../components/EditPopup.css';

function EditPopup({ user, onClose, onSave }) {
  const [formData, setFormData] = useState({
    weight: '',
    height: '',
    waist: '',
    waterIntake: '',
    dietPref: '',
    smoke: false,
    sleepDuration: '',
    activityLevel: '',
    diabetes: false,
    hypertension: false,
  });

  useEffect(() => {
    setFormData({
      weight: user.weight || '',
      height: user.height || '',
      waist: user.waist || '',
      waterIntake: user.water_intake || '',
      dietPref: user.dietary_preferences || '',
      smoke: user.smoking_status || false,
      sleepDuration: user.sleep_duration || '',
      activityLevel: user.activity_level || '',
      diabetes: user.diabetes || false,
      hypertension: user.hypertension || false,
    });
  }, [user]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleRadioChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value === 'true',
    });
  };

  const handleSubmit = () => {
    onSave(formData);
  };

  return (
    <div className="edit-popup-overlay">
      <div className="popup-content">
        <h2>Edit Information</h2>
        <div className="form-row">
          <div className="input-container">
            <input
              type="number"
              id="weight"
              name="weight"
              value={formData.weight}
              onChange={handleChange}
              required
            />
            <label htmlFor="weight">Weight (kg)</label>
          </div>
          <div className="input-container">
            <input
              type="number"
              id="height"
              name="height"
              value={formData.height}
              onChange={handleChange}
              required
            />
            <label htmlFor="height">Height (cm)</label>
          </div>
        </div>
        <div className="form-row">
          <div className="input-container">
            <input
              type="number"
              id="waist"
              name="waist"
              value={formData.waist}
              onChange={handleChange}
              required
            />
            <label htmlFor="waist">Waist Circumference (cm)</label>
          </div>
          <div className="input-container">
            <input
              type="number"
              id="waterIntake"
              name="waterIntake"
              value={formData.waterIntake}
              onChange={handleChange}
              required
            />
            <label htmlFor="waterIntake">Water Intake (liters)</label>
          </div>
        </div>
        <div className="form-row">
          <div className="input-container">
            <select
              id="dietPref"
              name="dietPref"
              value={formData.dietPref}
              onChange={handleChange}
              required
            >
              <option value="" disabled>Diet Preference</option>
              <option value="vegetarian">Vegetarian</option>
              <option value="vegan">Vegan</option>
              <option value="gluten-free">Gluten-Free</option>
              <option value="standard">Standard</option>
            </select>
            <label htmlFor="dietPref">Diet Preference</label>
          </div>
          <div className="input-container">
            <input
              type="number"
              id="sleepDuration"
              name="sleepDuration"
              value={formData.sleepDuration}
              onChange={handleChange}
              required
            />
            <label htmlFor="sleepDuration">Sleep Duration (hours)</label>
          </div>
        </div>
        <div className="form-row">
          <div className="input-container">
            <select
              id="activityLevel"
              name="activityLevel"
              value={formData.activityLevel}
              onChange={handleChange}
              required
            >
              <option value="" disabled>Activity Level</option>
              <option value="1">1 (Sedentary)</option>
              <option value="2">2 (Light Activity)</option>
              <option value="3">3 (Moderate Activity)</option>
              <option value="4">4 (High Activity)</option>
            </select>
            <label htmlFor="activityLevel">Activity Level</label>
          </div>
        </div>
        <div className="form-row">
          <div className="radio-group">
            <label>Smoke</label>
            <div className="radio-options">
              <label>
                <input
                  type="radio"
                  name="smoke"
                  value="true"
                  checked={formData.smoke === true}
                  onChange={handleRadioChange}
                />
                Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="smoke"
                  value="false"
                  checked={formData.smoke === false}
                  onChange={handleRadioChange}
                />
                No
              </label>
            </div>
          </div>
          <div className="radio-group">
            <label>Diabetes</label>
            <div className="radio-options">
              <label>
                <input
                  type="radio"
                  name="diabetes"
                  value="true"
                  checked={formData.diabetes === true}
                  onChange={handleRadioChange}
                />
                Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="diabetes"
                  value="false"
                  checked={formData.diabetes === false}
                  onChange={handleRadioChange}
                />
                No
              </label>
            </div>
          </div>
          <div className="radio-group">
            <label>Hypertension</label>
            <div className="radio-options">
              <label>
                <input
                  type="radio"
                  name="hypertension"
                  value="true"
                  checked={formData.hypertension === true}
                  onChange={handleRadioChange}
                />
                Yes
              </label>
              <label>
                <input
                  type="radio"
                  name="hypertension"
                  value="false"
                  checked={formData.hypertension === false}
                  onChange={handleRadioChange}
                />
                No
              </label>
            </div>
          </div>
        </div>
        <div className="popup-buttons">
          <button onClick={onClose}>Cancel</button>
          <button onClick={handleSubmit}>Save</button>
        </div>
      </div>
    </div>
  );
}

export default EditPopup;

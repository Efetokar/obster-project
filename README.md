
# OBSTER
## Obesity Prediction and Meal-Exercise Plan Application

This application is a web-based platform for predicting obesity levels based on user data and generating personalized meal plans. The backend is built using Flask, and the frontend is developed using React.

## Features

- **User Signup and Login**: Users can sign up, verify their email, and log in.
- **Obesity Prediction**: Predicts the user's obesity category based on their physical attributes and lifestyle factors.
- **Personalized Meal Plans**: Generates meal plans tailored to the user's dietary preferences and health conditions.
- **Email Verification**: Sends a verification code to the user's email during signup.
- **Session Management**: Keeps the user logged in during the session.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.7+
- Node.js and npm (for the frontend)
- Virtual environment tools (`venv`)

Here's the corrected section of the README with the instruction to run the application using `python run.py` instead of `flask run`:

---

## Getting Started

### Backend Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/obesity-prediction-app.git
   cd obesity-prediction-app/backend
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Generate model files:**

   Before running the Flask application, you need to generate the `.pkl` model files using the provided Jupyter notebooks. Here's how to do it:

   - **Breakfast Model**:
     - Open the `Breakfast.ipynb` notebook.
     - Run all cells to train the model.
     - Save the model as `breakfast_model.pkl`.

   - **Lunch Model**:
     - Open the `Lunch.ipynb` notebook.
     - Run all cells to train the model.
     - Save the model as `lunch_model.pkl`.

   - **Dinner Model**:
     - Open the `Dinner.ipynb` notebook.
     - Run all cells to train the model.
     - Save the model as `dinner_model.pkl`.

   - **Snack Model**:
     - Open the `Snack.ipynb` notebook.
     - Run all cells to train the model.
     - Save the model as `snack_model.pkl`.

   - **Exercise Model**:
     - Open the `Exercise.ipynb` notebook.
     - Run all cells to train the model.
     - Save the model as `exercise_model.pkl`.

   - **Obesity Prediction Model**:
     - Open the `Obesity-Model.ipynb` notebook.
     - Run all cells to train the model.
     - Save the model as `obesity_model.pkl`.

   Ensure these `.pkl` files are saved in the appropriate directory that the Flask application expects.

5. **Run the Flask application:**

   ```bash
   python run.py
   ```

   The backend should now be running on `http://127.0.0.1:5000`.

### Frontend Setup

1. **Navigate to the frontend directory:**

   ```bash
   cd ../frontend
   ```

2. **Install the required npm packages:**

   ```bash
   npm install
   ```

3. **Start the React development server:**

   ```bash
   npm start
   ```

   The frontend should now be running on `http://localhost:3000`.

---

## Usage

- **Signup**: Create a new user account.
- **Login**: Log in with your credentials.
- **Predict Obesity**: Submit your physical attributes and lifestyle factors to receive an obesity prediction.
- **Generate Meal Plan**: Based on your prediction, generate a personalized meal plan.
- **Generate Exercise Plan**: Receive a personalized exercise plan to support your health and fitness goals.
  
## Acknowledgments

- Flask for the backend framework.
- React for the frontend framework.
- Scikit-learn for the machine learning models.
- Bootstrap for the frontend styling.

---


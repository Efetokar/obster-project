import pickle
import pandas as pd
import os

# Construct the absolute path to the model file
model_path = os.path.join(os.path.dirname(__file__), 'obesity_model.pkl')

# Load the model
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

def predict_obesity(user_data):
    # Convert user data to DataFrame
    df = pd.DataFrame([user_data])
    
    # One-hot encode the Gender feature
    df = pd.get_dummies(df, columns=['Gender'], drop_first=False)
    
    # Ensure all expected features are present
    expected_features = ['Female', 'Male', 'Age', 'Height', 'Weight', 'BMI', 'PhysicalActivityLevel', 'Waist_Width']
    
    # Add missing columns if necessary
    for feature in expected_features:
        if feature not in df.columns:
            df[feature] = 0
    
    # Reorder columns to match the model's expected input
    df = df[expected_features]
    
    # Make prediction
    prediction = model.predict(df)
    return prediction[0]

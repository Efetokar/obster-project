import pickle
import pandas as pd
import os

# Construct the absolute path to the model file
model_path = os.path.join(os.path.dirname(__file__), 'dinner_model.pkl')

# Load the model
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

def predict_dinner(user_data):
    """
    Predicts dinner based on the user's data.

    :param user_data: Dictionary containing the user's information.
    :return: Predicted dinner.
    """
    # Convert user data to DataFrame
    df = pd.DataFrame([user_data])

    # Map obesity_prediction to one-hot encoded columns
    obesity_map = {
        'Normal weight': {'Normalweight': 1, 'Obese': 0, 'Overweight': 0, 'Underweight': 0},
        'Obese': {'Normalweight': 0, 'Obese': 1, 'Overweight': 0, 'Underweight': 0},
        'Overweight': {'Normalweight': 0, 'Obese': 0, 'Overweight': 1, 'Underweight': 0},
        'Underweight': {'Normalweight': 0, 'Obese': 0, 'Overweight': 0, 'Underweight': 1}
    }
    obesity_category = obesity_map.get(df['ObesityCategory'][0], {'Normalweight': 0, 'Obese': 0, 'Overweight': 0, 'Underweight': 0})
    
    # Create a DataFrame from the obesity_category dictionary
    obesity_df = pd.DataFrame([obesity_category])

    # One-hot encode Diet Type
    diet_type = pd.get_dummies([df['Diet Type'][0]], dtype=int)
    
    # Update the user data with the encoded features
    df = df.drop(columns=['ObesityCategory', 'Diet Type'], errors='ignore')
    df = pd.concat([df, obesity_df, diet_type], axis=1)

    # Remove duplicates in model_features
    model_features = [
        'Age', 'Height', 'Weight', 'BMI', 'PhysicalActivityLevel',
        'Assigned_Dinner_Calories', 'Waist', 'Diabetes', 'Hypertension',
        'Normalweight', 'Obese', 'Overweight', 'Underweight',
        'Gluten Free', 'Standard', 'Vegan', 'Vegetarian', 'gender'
    ]
    model_features = list(dict.fromkeys(model_features))  # Remove duplicates

    # Ensure DataFrame does not contain duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    # Reorder columns to match the model's expected input
    df = df.reindex(columns=model_features, fill_value=0)

    # Make prediction
    prediction = model.predict(df)
    
    return prediction[0]

from flask import request, jsonify, Blueprint, session, current_app
from . import db, mail
from .models import User, BreakfastPrediction, LunchPrediction, DinnerPrediction, SnackPrediction
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
import string
from flask_mail import Message
from .breakfast_model import predict_breakfast 
from .lunch_model import predict_lunch
from .dinner_model import predict_dinner 
from .snack_model import predict_snack  
from .exercise_model import predict_exercise 
from .obesity_model import predict_obesity
import logging
import re

bp = Blueprint('routes', __name__)

def init_app(app):
    app.register_blueprint(bp)

def generate_verification_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))
def calculate_bmi(height_cm, weight_kg):
    # Height from cm to meters
    height_m = height_cm / 100
    # BMI calculation
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)  # Rounded to 2 decimal places

def calculate_daily_calorie_needs(bmi, height_m, age, gender, activity_level, smoking_status, sleep_duration, water_intake):
    # Derive weight from BMI and height in meters
    weight = bmi * (height_m ** 2)
    print(f"Derived weight from BMI and height: {weight:.2f} kg")

    # Calculate BMR using the Mifflin-St Jeor Equation
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * (height_m * 100) - 5 * age + 5  # height in cm
    elif gender.lower() == 'female':
        bmr = 10 * weight + 6.25 * (height_m * 100) - 5 * age - 161  # height in cm
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    print(f"Calculated BMR: {bmr:.2f} calories/day")

    # Adjust calorie needs based on activity level
    activity_multiplier = {
        1: 1.2,    # Sedentary (little or no exercise)
        2: 1.375,  # Lightly active (light exercise/sports 1-3 days/week)
        3: 1.55,   # Moderately active (moderate exercise/sports 3-5 days/week)
        4: 1.725,  # Very active (hard exercise/sports 6-7 days a week)
        5: 1.9     # Super active (very hard exercise/sports & physical job or 2x training)
    }
    calories = bmr * activity_multiplier[activity_level]
    print(f"Calories after activity level adjustment: {calories:.2f} calories/day")

    # Adjust for smoking (reduce calorie needs if smoking)
    if smoking_status:
        calories *= 0.95
        print(f"Calories after smoking adjustment: {calories:.2f} calories/day")

    # Adjust for sleep duration (more sleep, better metabolism)
    if sleep_duration and sleep_duration >= 7:
        calories *= 1.05
        print(f"Calories after sleep adjustment: {calories:.2f} calories/day")

    # Adjust for water intake (better hydration, better metabolism)
    if water_intake and water_intake >= 2.0:
        calories *= 1.05
        print(f"Calories after water intake adjustment: {calories:.2f} calories/day")

    return round(calories)


@bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'message': 'No input data provided'}), 400

        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400

        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
        age = (datetime.utcnow().date() - birthdate).days // 365  # Calculate age in years
        verification_code = generate_verification_code()
        verification_expiry = datetime.utcnow() + timedelta(minutes=5)

        height_cm = float(data['height'].replace(" cm", ""))
        height_m = height_cm / 100  # Convert height to meters
        weight_kg = float(data['weight'].replace(" kg", ""))
        bmi = calculate_bmi(height_cm, weight_kg)

        new_user = User(
            name=data['name'],
            surname=data['surname'],
            email=data['email'],
            birthdate=birthdate,
            password=hashed_password,
            gender=data['gender'],
            height=height_cm,
            weight=weight_kg,
            waist=float(data['waist'].replace(" cm", "")),
            activity_level=int(data['activityLevel']),
            sleep_duration=float(data['sleepDuration']),
            water_intake=float(data['waterIntake']),
            smoking_status=data['smoke'],
            diabetes=data.get('diabetes', False),
            hypertension=data.get('hypertension', False),
            dietary_preferences=data['dietPref'],
            bmi=bmi,  # Calculated BMI
            daily_calorie_needs=calculate_daily_calorie_needs(
                bmi=bmi,
                height_m=height_m,
                age=age,
                gender=data['gender'],
                activity_level=int(data['activityLevel']),
                smoking_status=data['smoke'], 
                sleep_duration=float(data['sleepDuration']),
                water_intake=float(data['waterIntake']) if data['waterIntake'] else 0,
            ),
            verification_code=verification_code,  # Store the generated verification code
            verification_expiry=verification_expiry  # Store the expiry time of the verification code
        )
        db.session.add(new_user)
        db.session.commit()

        msg = Message("Email Verification", recipients=[data['email']])
        msg.body = f"Your verification code is {verification_code}."
        mail.send(msg)

        return jsonify({'message': 'User created successfully. Please verify your email.', 'email': data['email']}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error during signup: {str(e)}")
        return jsonify({'message': 'An error occurred during signup', 'error': str(e)}), 500

@bp.route('/verify-email', methods=['POST'])
def verify_email():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'code' not in data:
            return jsonify({'message': 'Invalid input.'}), 400

        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return jsonify({'message': 'User not found.'}), 404

        if user.verification_expiry < datetime.utcnow():
            return jsonify({'message': 'Verification code has expired.'}), 400

        if user.verification_code == data['code']:
            user.is_verified = True
            user.verification_code = None
            user.verification_expiry = None
            db.session.commit()
            return jsonify({'message': 'Email verified successfully.'}), 200
        else:
            return jsonify({'message': 'Invalid verification code.'}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error during email verification: {str(e)}")
        return jsonify({'message': 'An error occurred during email verification', 'error': str(e)}), 500

@bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user:
            return jsonify({'message': 'User not found.'}), 404

        verification_code = generate_verification_code()
        verification_expiry = datetime.utcnow() + timedelta(minutes=5)
        user.verification_code = verification_code
        user.verification_expiry = verification_expiry
        db.session.commit()

        msg = Message("Email Verification", recipients=[data['email']])
        msg.body = f"Your new verification code is {verification_code}."
        mail.send(msg)

        return jsonify({'message': 'Verification code resent successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error during resending verification code: {str(e)}")
        return jsonify({'message': 'An error occurred during resending verification code', 'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Invalid input.'}), 400

        user = User.query.filter_by(email=data['email']).first()

        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid email or password.'}), 401

        if not user.is_verified:
            return jsonify({'message': 'Email not verified.'}), 403

        # Save user ID in session for later use
        session['user_id'] = user.id

        # Debug information
        logging.info(f"User ID {user.id} set in session.")
        logging.info(f"Session contents: {list(session.items())}")

        return jsonify({'message': 'Login successful.', 'success': True}), 200
    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        return jsonify({'message': 'An error occurred during login', 'error': str(e)}), 500

@bp.route('/predict-obesity', methods=['POST'])
def predict_obesity_route():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Unauthorized access'}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Directly use the float value from user.height
        height_in_cm = user.height
        weight_in_kg = user.weight

        # Convert height from cm to meters for BMI calculation
        height_in_meters = height_in_cm / 100
        bmi = weight_in_kg / (height_in_meters ** 2)

        user_data = {
            'Gender': user.gender.capitalize(),
            'Age': (datetime.now().date() - user.birthdate).days // 365,
            'Height': height_in_cm,
            'Weight': weight_in_kg,
            'BMI': bmi,
            'PhysicalActivityLevel': user.activity_level,
            'Waist_Width': user.waist  # Assuming waist is also in cm and stored as a float
        }

        # Make the prediction
        prediction = predict_obesity(user_data)

        # Update the user's obesity prediction in the database
        user.obesity_prediction = prediction
        db.session.commit()

        return jsonify({'obesity_prediction': prediction}), 200

    except Exception as e:
        logging.error("An error occurred during prediction", exc_info=True)
        return jsonify({'message': 'An error occurred during prediction', 'error': str(e)}), 500

from datetime import datetime

@bp.route('/user-info', methods=['GET'])
def user_info():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Unauthorized access'}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Calculate age based on the birthdate
        today = datetime.utcnow().date()
        birthdate = user.birthdate
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        user_info = {
            'name': user.name,
            'surname': user.surname,
            'email': user.email,
            'birthdate': user.birthdate.strftime('%Y-%m-%d'),
            'age': age,  # Include the calculated age
            'gender': user.gender,
            'height': user.height,
            'weight': user.weight,
            'waist': user.waist,
            'activity_level': user.activity_level,
            'smoking_status': user.smoking_status,
            'diabetes': user.diabetes,
            'hypertension': user.hypertension,
            'sleep_duration': user.sleep_duration,
            'water_intake': user.water_intake,
            'dietary_preferences':user.dietary_preferences

        }

        print(f"User info for user_id {user_id}: {user_info}")

        return jsonify(user_info), 200
    except Exception as e:
        logging.error("An error occurred while fetching user info", exc_info=True)
        return jsonify({'message': 'An error occurred while fetching user info', 'error': str(e)}), 500

@bp.route('/logout', methods=['POST'])
def logout():
    try:
        # Clear the user session
        session.clear()
        return jsonify({'message': 'Logout successful.'}), 200
    except Exception as e:
        logging.error(f"Error during logout: {str(e)}")
        return jsonify({'message': 'An error occurred during logout', 'error': str(e)}), 500

import sys

@bp.route('/predict-breakfast', methods=['POST'])
def predict_breakfast_route():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Unauthorized access'}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        today_date = datetime.now().date()
        existing_prediction = BreakfastPrediction.query.filter_by(user_id=user.id, date=today_date).first()

        if existing_prediction:
            return jsonify({
                'breakfast_suggestion': existing_prediction.suggestion,
                'calories': existing_prediction.calories
            }), 200

        # Prepare user data for prediction
        height_in_meters = user.height / 100
        bmi = user.weight / (height_in_meters ** 2)

        diet_mapping = {
            'standard': 'Standard',
            'vegetarian': 'Vegetarian',
            'vegan': 'Vegan',
            'gluten-free': 'Gluten Free'
        }

        user_diet_pref = user.dietary_preferences.strip().lower()
        dietary_pref = diet_mapping.get(user_diet_pref, 'Standard')

        # Print the mapping results
        print(f"User diet preference: {user_diet_pref}")
        print(f"Mapped dietary preference: {dietary_pref}")
        sys.stdout.flush()

        user_data = {
            'Age': (datetime.now().date() - user.birthdate).days // 365,
            'Height': user.height,
            'Weight': user.weight,
            'BMI': bmi,
            'PhysicalActivityLevel': user.activity_level,
            'Assigned_Breakfast_Calories': user.daily_calorie_needs * 0.25,
            'Waist': user.waist,
            'Diabetes': 1 if user.diabetes else 0,
            'Hypertension': 1 if user.hypertension else 0,
            'ObesityCategory': user.obesity_prediction,
            'gender': 1 if user.gender.lower() == 'male' else 0,
            'Diet Type': dietary_pref
        }

        predicted_breakfast = predict_breakfast(user_data)
        calorie_value = user_data['Assigned_Breakfast_Calories']

        new_prediction = BreakfastPrediction(
            user_id=user.id,
            date=today_date,
            suggestion=predicted_breakfast,
            calories=calorie_value
        )
        db.session.add(new_prediction)
        db.session.commit()

        return jsonify({
            'breakfast_suggestion': predicted_breakfast,
            'calories': calorie_value
        }), 200

    except Exception as e:
        logging.error("An error occurred during breakfast prediction", exc_info=True)
        return jsonify({'message': 'An error occurred during prediction', 'error': str(e)}), 500

@bp.route('/predict-lunch', methods=['POST'])
def predict_lunch_route():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Unauthorized access'}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        today_date = datetime.now().date()
        existing_prediction = LunchPrediction.query.filter_by(user_id=user.id, date=today_date).first()

        if existing_prediction:
            return jsonify({
                'lunch_suggestion': existing_prediction.suggestion,
                'calories': existing_prediction.calories
            }), 200

        # Prepare user data for prediction
        height_in_meters = user.height / 100
        bmi = user.weight / (height_in_meters ** 2)

        diet_mapping = {
            'standard': 'Standard',
            'vegetarian': 'Vegetarian',
            'vegan': 'Vegan',
            'gluten-free': 'Gluten Free'
        }

        user_diet_pref = user.dietary_preferences.strip().lower()
        dietary_pref = diet_mapping.get(user_diet_pref, 'Standard')

        # Print or log the mapping results
        print(f"User diet preference: {user_diet_pref}")
        print(f"Mapped dietary preference: {dietary_pref}")

        user_data = {
            'Age': (datetime.now().date() - user.birthdate).days // 365,
            'Height': user.height,
            'Weight': user.weight,
            'BMI': bmi,
            'PhysicalActivityLevel': user.activity_level,
            'Assigned_Lunch_Calories': user.daily_calorie_needs * 0.35,
            'Waist': user.waist,
            'Diabetes': 1 if user.diabetes else 0,
            'Hypertension': 1 if user.hypertension else 0,
            'ObesityCategory': user.obesity_prediction,
            'gender': 1 if user.gender.lower() == 'male' else 0,
            'Diet Type': dietary_pref
        }

        predicted_lunch = predict_lunch(user_data)
        calorie_value = user_data['Assigned_Lunch_Calories']

        new_prediction = LunchPrediction(
            user_id=user.id,
            date=today_date,
            suggestion=predicted_lunch,
            calories=calorie_value
        )
        db.session.add(new_prediction)
        db.session.commit()

        return jsonify({
            'lunch_suggestion': predicted_lunch,
            'calories': calorie_value
        }), 200

    except Exception as e:
        logging.error("An error occurred during lunch prediction", exc_info=True)
        return jsonify({'message': 'An error occurred during prediction', 'error': str(e)}), 500

@bp.route('/predict-dinner', methods=['POST'])
def predict_dinner_route():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Unauthorized access'}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        today_date = datetime.now().date()
        existing_prediction = DinnerPrediction.query.filter_by(user_id=user.id, date=today_date).first()

        if existing_prediction:
            return jsonify({
                'dinner_suggestion': existing_prediction.suggestion,
                'calories': existing_prediction.calories
            }), 200

        # Prepare user data for prediction
        height_in_meters = user.height / 100
        bmi = user.weight / (height_in_meters ** 2)

        diet_mapping = {
            'standard': 'Standard',
            'vegetarian': 'Vegetarian',
            'vegan': 'Vegan',
            'gluten-free': 'Gluten Free'
        }

        user_diet_pref = user.dietary_preferences.strip().lower()
        dietary_pref = diet_mapping.get(user_diet_pref, 'Standard')

        # Print or log the mapping results
        print(f"User diet preference: {user_diet_pref}")
        print(f"Mapped dietary preference: {dietary_pref}")

        user_data = {
            'Age': (datetime.now().date() - user.birthdate).days // 365,
            'Height': user.height,
            'Weight': user.weight,
            'BMI': bmi,
            'PhysicalActivityLevel': user.activity_level,
            'Assigned_Dinner_Calories': user.daily_calorie_needs * 0.3,
            'Waist': user.waist,
            'Diabetes': 1 if user.diabetes else 0,
            'Hypertension': 1 if user.hypertension else 0,
            'ObesityCategory': user.obesity_prediction,
            'gender': 1 if user.gender.lower() == 'male' else 0,
            'Diet Type': dietary_pref
        }

        predicted_dinner = predict_dinner(user_data)
        calorie_value = user_data['Assigned_Dinner_Calories']

        new_prediction = DinnerPrediction(
            user_id=user.id,
            date=today_date,
            suggestion=predicted_dinner,
            calories=calorie_value
        )
        db.session.add(new_prediction)
        db.session.commit()

        return jsonify({
            'dinner_suggestion': predicted_dinner,
            'calories': calorie_value
        }), 200

    except Exception as e:
        logging.error("An error occurred during dinner prediction", exc_info=True)
        return jsonify({'message': 'An error occurred during prediction', 'error': str(e)}), 500

@bp.route('/predict-snack', methods=['POST'])
def predict_snack_route():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Unauthorized access'}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        today_date = datetime.now().date()
        existing_prediction = SnackPrediction.query.filter_by(user_id=user.id, date=today_date).first()

        if existing_prediction:
            return jsonify({
                'snack_suggestion': existing_prediction.suggestion,
                'calories': existing_prediction.calories
            }), 200

        # Prepare user data for prediction
        height_in_meters = user.height / 100
        bmi = user.weight / (height_in_meters ** 2)

        diet_mapping = {
            'standard': 'Standard',
            'vegetarian': 'Vegetarian',
            'vegan': 'Vegan',
            'gluten-free': 'Gluten Free'
        }

        user_diet_pref = user.dietary_preferences.strip().lower()
        dietary_pref = diet_mapping.get(user_diet_pref, 'Standard')

        # Print or log the mapping results
        print(f"User diet preference: {user_diet_pref}")
        print(f"Mapped dietary preference: {dietary_pref}")

        user_data = {
            'Age': (datetime.now().date() - user.birthdate).days // 365,
            'Height': user.height,
            'Weight': user.weight,
            'BMI': bmi,
            'PhysicalActivityLevel': user.activity_level,
            'Assigned_Snack_Calories': user.daily_calorie_needs * 0.1,
            'Waist': user.waist,
            'Diabetes': 1 if user.diabetes else 0,
            'Hypertension': 1 if user.hypertension else 0,
            'ObesityCategory': user.obesity_prediction,
            'gender': 1 if user.gender.lower() == 'male' else 0,
            'Diet Type': dietary_pref
        }

        predicted_snack = predict_snack(user_data)
        calorie_value = user_data['Assigned_Snack_Calories']

        new_prediction = SnackPrediction(
            user_id=user.id,
            date=today_date,
            suggestion=predicted_snack,
            calories=calorie_value
        )
        db.session.add(new_prediction)
        db.session.commit()

        return jsonify({
            'snack_suggestion': predicted_snack,
            'calories': calorie_value
        }), 200

    except Exception as e:
        logging.error("An error occurred during snack prediction", exc_info=True)
        return jsonify({'message': 'An error occurred during prediction', 'error': str(e)}), 500


@bp.route('/predict-exercise', methods=['POST'])
def predict_exercise_route():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Unauthorized access'}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Prepare user data for prediction
        height_in_meters = user.height / 100
        bmi = user.weight / (height_in_meters ** 2)

        # Map dietary preferences to corresponding string
        diet_mapping = {
            'Standard': 'Standard',
            'Vegetarian': 'Vegetarian',
            'Vegan': 'Vegan',
            'Gluten Free': 'Gluten Free'
        }
        dietary_pref = diet_mapping.get(user.dietary_preferences, 'Standard')

        user_data = {
            'Age': (datetime.now().date() - user.birthdate).days // 365,
            'Height': user.height,
            'Weight': user.weight,
            'BMI': bmi,
            'PhysicalActivityLevel': user.activity_level,
            'Assigned_Exercise_Calories': user.daily_calorie_needs * 0.15,
            'Waist': user.waist,
            'Diabetes': 1 if user.diabetes else 0,
            'Hypertension': 1 if user.hypertension else 0,
            'ObesityCategory': user.obesity_prediction,  # Assuming this field exists
            'gender': 1 if user.gender.lower() == 'male' else 0,
            'Diet Type': dietary_pref  # Include dietary preferences
        }

        # Predict exercise
        predicted_exercise = predict_exercise(user_data)
        calorie_value = user_data['Assigned_Exercise_Calories']

        return jsonify({
            'exercise_suggestion': predicted_exercise,
            'calories': calorie_value
        }), 200

    except Exception as e:
        logging.error("An error occurred during exercise prediction", exc_info=True)
        return jsonify({'message': 'An error occurred during prediction', 'error': str(e)}), 500

@bp.route('/update-user-info', methods=['PUT'])
def update_user_info():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Unauthorized access'}), 403

        data = request.get_json()
        user = User.query.get(user_id)

        # Update user information
        user.weight = float(data['weight'])
        user.height = float(data['height'])
        user.waist = float(data['waist'])
        user.water_intake = float(data['waterIntake']) if data['waterIntake'] else 0.0
        user.dietary_preferences = data['dietPref']
        user.smoking_status = data['smoke']
        user.sleep_duration = float(data['sleepDuration'])
        user.activity_level = int(data['activityLevel'])
        user.diabetes = data['diabetes']
        user.hypertension = data['hypertension']

        # Recalculate BMI
        height_in_meters = user.height / 100
        user.bmi = user.weight / (height_in_meters ** 2)

        # Calculate age based on the birthdate
        today = datetime.utcnow().date()
        birthdate = user.birthdate
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        # Recalculate daily calorie needs using BMI
        user.daily_calorie_needs = calculate_daily_calorie_needs(
            bmi=user.bmi,
            height_m=height_in_meters,
            age=age,
            gender=user.gender,
            activity_level=user.activity_level,
            smoking_status=user.smoking_status, 
            sleep_duration=user.sleep_duration,
            water_intake=user.water_intake
        )

        # Commit updated user info to the database
        db.session.commit()

        # Clear existing predictions for the same date
        today_date = datetime.now().date()

        # Delete existing predictions for today
        BreakfastPrediction.query.filter_by(user_id=user.id, date=today_date).delete()
        LunchPrediction.query.filter_by(user_id=user.id, date=today_date).delete()
        DinnerPrediction.query.filter_by(user_id=user.id, date=today_date).delete()
        SnackPrediction.query.filter_by(user_id=user.id, date=today_date).delete()

        # Commit the deletions to the database
        db.session.commit()

        # Call prediction routes directly to create new predictions in the database
        predict_breakfast_route()
        predict_lunch_route()
        predict_dinner_route()
        predict_snack_route()

        # Updated user info to return
        user_info = {
            'weight': user.weight,
            'height': user.height,
            'waist': user.waist,
            'waterIntake': user.water_intake,
            'dietPref': user.dietary_preferences,
            'smoke': user.smoking_status,
            'sleepDuration': user.sleep_duration,
            'activityLevel': user.activity_level,
            'diabetes': user.diabetes,
            'hypertension': user.hypertension,
            'bmi': user.bmi,
            'daily_calorie_needs': user.daily_calorie_needs,
            'age': age,  # Include the calculated age
        }

        return jsonify(user_info), 200
    except Exception as e:
        db.session.rollback()
        logging.error("An error occurred while updating user info", exc_info=True)
        return jsonify({'message': 'An error occurred while updating user info', 'error': str(e)}), 500

def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)


@bp.route('/change-password', methods=['POST'])
def change_password():
    try:
        data = request.get_json()
        if not data or 'old_password' not in data or 'new_password' not in data:
            return jsonify({'message': 'Invalid input.'}), 400

        user = get_current_user()  # Assuming a function to get the current logged-in user

        if not check_password_hash(user.password, data['old_password']):
            return jsonify({'message': 'Old password is incorrect.'}), 400

        user.password = generate_password_hash(data['new_password'], method='pbkdf2:sha256')
        db.session.commit()
        return jsonify({'message': 'Password changed successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error during password change: {str(e)}")
        return jsonify({'message': 'An error occurred during password change', 'error': str(e)}), 500

from datetime import date
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Float, nullable=False)  # Height in cm
    weight = db.Column(db.Float, nullable=False)  # Weight in kg
    bmi = db.Column(db.Float, nullable=False)  # Calculated BMI
    waist = db.Column(db.Float, nullable=False)  # Waist circumference in cm
    activity_level = db.Column(db.Integer, nullable=False)  # 1 to 4
    sleep_duration = db.Column(db.Float, nullable=True)  # Sleep duration in hours
    smoking_status = db.Column(db.Boolean, nullable=True)  # True if smoking, else False
    diabetes = db.Column(db.Boolean, nullable=True)  # True if user has diabetes
    hypertension = db.Column(db.Boolean, nullable=True)  # True if user has hypertension
    water_intake = db.Column(db.Float, nullable=True) 
    dietary_preferences = db.Column(db.String(50), nullable=True)  # Diet preference
    daily_calorie_needs = db.Column(db.Float, nullable=False)  # Calculated daily calorie needs
    obesity_prediction = db.Column(db.String(50), nullable=True)  # Store the obesity prediction
    verification_code = db.Column(db.String(6), nullable=True)
    verification_expiry = db.Column(db.DateTime, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)


#Breakfast Prediction Model
class BreakfastPrediction(db.Model):
    __tablename__ = 'breakfast_predictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    suggestion = db.Column(db.String(255), nullable=False)
    calories = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref=db.backref('breakfast_predictions', lazy=True))

    def __repr__(self):
        return f'<BreakfastPrediction {self.suggestion} for {self.date}>'

# Lunch Prediction Model
class LunchPrediction(db.Model):
    __tablename__ = 'lunch_predictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    suggestion = db.Column(db.String(255), nullable=False)
    calories = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref=db.backref('lunch_predictions', lazy=True))

    def __repr__(self):
        return f'<LunchPrediction {self.suggestion} for {self.date}>'

# Dinner Prediction Model
class DinnerPrediction(db.Model):
    __tablename__ = 'dinner_predictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    suggestion = db.Column(db.String(255), nullable=False)
    calories = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref=db.backref('dinner_predictions', lazy=True))

    def __repr__(self):
        return f'<DinnerPrediction {self.suggestion} for {self.date}>'

# Snack Prediction Model
class SnackPrediction(db.Model):
    __tablename__ = 'snack_predictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    suggestion = db.Column(db.String(255), nullable=False)
    calories = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref=db.backref('snack_predictions', lazy=True))

    def __repr__(self):
        return f'<SnackPrediction {self.suggestion} for {self.date}>'

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
 
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(200))

    profile_completed = db.Column(db.Boolean, default=False)

    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    profession = db.Column(db.String(50))
    income_type = db.Column(db.String(50))
    monthly_income = db.Column(db.Float)

    # ✅ ADD THIS HERE
    monthly_budget = db.Column(db.Float, default=0)
    
    budget_cycle_start = db.Column(db.Integer, default=1)
    budget_start_date = db.Column(db.Date)
    budget_fixed = db.Column(db.Boolean, default=False)
    budget_edit_limit = db.Column(db.Integer, default=0)
    preferred_categories = db.Column(db.Text)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100))
    note = db.Column(db.String(200))
    date = db.Column(db.Date, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    type = db.Column(db.String(20), nullable=False)
# app/models.py

from flask import current_app
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    monthly_budget = db.Column(db.Float, nullable=False, default=1e9)
    phone_num = db.Column(db.Integer, nullable=False, default=1)
    def __repr__(self):
        return f'<User {self.username}>'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_password(self, new_password):
        try:
            self.password = new_password
            db.session.commit()
            return True
        except Exception as e:
            current_app.logger.error(f"Error updating user password: {str(e)}")
            db.session.rollback()
            return False

    def update_monthly_budget(self, new_budget):
        try:
            self.monthly_budget = new_budget
            db.session.commit()
            return True
        except Exception as e:
            current_app.logger.error(f"Error updating user monthly budget: {str(e)}")
            db.session.rollback()
            return False

    def update_phone_number(self, new_phone_num):
        try:
            self.phone_num = new_phone_num
            db.session.commit()
            return True
        except Exception as e:
            current_app.logger.error(f"Error updating user phone number: {str(e)}")
            db.session.rollback()
            return False
from datetime import datetime
from app import db

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    call_duration = db.Column(db.Integer, nullable=False, default=0)
    messages = db.Column(db.Integer, nullable=False, default=0)
    data_usage = db.Column(db.Float, nullable=False, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

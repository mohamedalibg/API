# app/expenses/resources.py

import marshal
from flask import current_app, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import extract, func
from werkzeug import Client
from app import db
from app.models import Expense, User
from datetime import datetime,timedelta 

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Expense, User

class ExpenseLogging(Resource):
    @jwt_required()
    def post(self,current_user,data):
        try:
            # Get the logged-in user's identity
            '''current_user = get_jwt_identity()'''

            # Parse the JSON data from the request
            data = request.get_json()

            # Create a new Expense instance
            new_expense = Expense(
                user_id=current_user,
                call_duration=data.get('call_duration', 0),
                messages=data.get('messages', 0),
                data_usage=data.get('data_usage', 0)
            )

            # Add the new expense to the database
            db.session.add(new_expense)
            db.session.commit()

            # Return the formatted response using marshal
            response = {'message': 'Expense logged successfully '}, 201

            # Send SMS to inform the client of the remaining budget
            userid = User.query.filter_by(username=current_user).first().id
            # Assuming you have a method send_sms_notification in your class
            self.send_sms_notification(userid)

            return response

        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an error
            error_message = {'message': str(e)}
            print(f"Error: {error_message}")
            return error_message, 500

    def send_sms_notification(self,userid):
        
        try:
            # Fetch the user's data from the database
            user = User.query.get(userid)  # Assuming user_id is the primary key (ID) of the User model
            if user and user.phone_num is not None:
            # Set up Twilio credentials (replace with your actual Twilio credentials)
                account_sid = 'ACa8b1ab0a00ee9d51dfa81b05163a78a6'
                auth_token = 'a6944acac3cd37ead99d583ac1648a4d'
                twilio_phone_number = '+14404828423'

            # Create a Twilio client
                client = Client(account_sid, auth_token)

            # Calculate remaining budget based on the user's specific budget from the database
                total_expenses = (
                    db.session.query(
                        (func.sum(Expense.call_duration).label('total_call_duration')*300) +
                        (func.sum(Expense.messages).label('total_messages')*50) +
                        (func.sum(Expense.data_usage).label('total_data_usage')*1)
                 )
                .filter(Expense.user_id == user.username)
                .scalar() or 0
                )

                remaining_budget = user.monthly_budget - total_expenses

            # Compose the SMS message
                message_body = f"Dear {user.username}, your remaining budget is {remaining_budget:.2f}."

            # Send the SMS
                message = client.messages.create(
                    to=f"{str(user.phone_num)}",  # Convert to string if needed
                    from_=twilio_phone_number,
                    body=message_body
                )

                current_app.logger.info(f"SMS sent: {message.sid}")
                return {'message': f"SMS sent successfully to {user.username}."}

            else:
                current_app.logger.warning("User not found or no phone number available for SMS notification.")
                return {'message': 'User not found or no phone number available for SMS notification.'}

        except Exception as e:
            current_app.logger.error(f"Error sending SMS notification: {str(e),str(userid),user.username}")
            return {'message': f"Error sending SMS: {str(e)}"}, 500



class ExpenseRetrieval(Resource):
    @jwt_required()
    def get(self):
        try:
            # Get the logged-in user's identity
            current_user = get_jwt_identity()

            # Retrieve total expenses for the user
            total_expenses = Expense.query.filter_by(user_id=current_user).with_entities((func.sum(Expense.call_duration).label('total_call_duration')*300)+(func.sum(Expense.messages).label('total_messages')*50)+(func.sum(Expense.data_usage).label('total_data_usage')*1)).scalar()

            # Retrieve breakdown of expenses by category
            breakdown = Expense.query.filter_by(user_id=current_user).with_entities(
                func.sum(Expense.call_duration).label('total_call_duration'),
                func.sum(Expense.messages).label('total_messages'),
                func.sum(Expense.data_usage).label('total_data_usage')
            ).first()

            # Retrieve historical expense data
            historical_data = Expense.query.filter_by(user_id=current_user).all()

            # Format the response
            return{
                'total_expenses': total_expenses,
                'breakdown': {
                    'total_call_duration': breakdown.total_call_duration,
                    'total_messages': breakdown.total_messages,
                    'total_data_usage': breakdown.total_data_usage
                },
                'historical_data': [{
                    'id': expense.id,
                    'call_duration': expense.call_duration,
                    'messages': expense.messages,
                    'data_usage': expense.data_usage,
                    'timestamp': str(expense.timestamp)
                } for expense in historical_data]
            },200

            

        except Exception as e:
            return {'message': str(e)}, 500
        
       
class ExpenseAnalytics(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()

            # Monthly usage trends
            monthly_trends = self.get_monthly_trends(current_user)

            # Expense patterns over time
            expense_patterns = self.get_expense_patterns(current_user)

            # Usage vs. budget analysis (example)

            usage_vs_budget = self.get_usage_vs_budget(current_user)

            return {
                'monthly_trends': monthly_trends,
                'expense_patterns': expense_patterns,
                'usage_vs_budget': usage_vs_budget
            }

        except Exception as e:
            return {'message': str(e)}, 500

    def get_monthly_trends(self, user_id):
        # Example: Get monthly usage trends for the last 6 months
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30 * 6)  # 6 months

        monthly_trends = (
            db.session.query(
                extract('year', Expense.timestamp).label('year'),
                extract('month', Expense.timestamp).label('month'),
                func.sum(Expense.call_duration).label('total_call_duration'),
                func.sum(Expense.messages).label('total_messages'),
                func.sum(Expense.data_usage).label('total_data_usage')
            )
            .filter(Expense.user_id == user_id)
            .filter(Expense.timestamp >= start_date, Expense.timestamp <= end_date)
            .group_by('year', 'month')
            .all()
        )

        return [{'month': f'{row.year:04d}-{row.month:02d}', 'data': {
            'total_call_duration': row.total_call_duration,
            'total_messages': row.total_messages,
            'total_data_usage': row.total_data_usage
        }} for row in monthly_trends]

    def get_expense_patterns(self, user_id):
        # Example: Get expense patterns over the last 6 months
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30 * 6)  # 6 months

        expense_patterns = (
            db.session.query(
                extract('year', Expense.timestamp).label('year'),
                extract('month', Expense.timestamp).label('month'),
                ((func.sum(Expense.call_duration).label('total_call_duration')*300)+(func.sum(Expense.messages).label('total_messages')*50)+(func.sum(Expense.data_usage).label('total_data_usage')*1)).label('total_amount')
            )
            .filter(Expense.user_id == user_id)
            .filter(Expense.timestamp >= start_date, Expense.timestamp <= end_date)
            .group_by('year','month')
            .all()
        )

        return [{'month': datetime(year=row.year, month=row.month, day=1).strftime('%Y-%m'), 'total_amount': row.total_amount} for row in expense_patterns]

    def get_usage_vs_budget(self, user_id):
        # Example: Calculate usage vs. budget analysis
        # You can customize this based on your budgeting logic
        total_expenses = db.session.query((func.sum(Expense.call_duration).label('total_call_duration')*300)+(func.sum(Expense.messages).label('total_messages')*50)+(func.sum(Expense.data_usage).label('total_data_usage')*1)).filter(Expense.user_id == user_id).scalar() or 0
        userid = User.query.filter_by(username=user_id).first().id
        user=User.query.get(userid)
        
        return {'total_expenses': total_expenses, 'monthly_budget': user.monthly_budget, 'remaining_budget': user.monthly_budget - total_expenses}
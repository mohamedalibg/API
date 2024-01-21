# app/users/routes.py

from flask_restful import Api, Resource
from app import api  # Import the 'api' instance from the main app

from app.users.resources import UserMonthlyBudgetModification, UserPasswordModification, UserPhoneNumberModification, UserRegistration, UserAuthentication

api.add_resource(UserRegistration, '/register')
api.add_resource(UserAuthentication, '/login')
api.add_resource(UserPasswordModification, '/user/password')
api.add_resource(UserMonthlyBudgetModification, '/user/monthly_budget')
api.add_resource(UserPhoneNumberModification, '/user/phone_number')


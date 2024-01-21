from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from flask import jsonify, request
from app.models import User

registration_parser = reqparse.RequestParser()
registration_parser.add_argument('username', type=str, help='Username is required', required=True)
registration_parser.add_argument('password', type=str, help='Password is required', required=True)
registration_parser.add_argument('phone_num', type=int, help='Phone Num is required', required=True)
registration_parser.add_argument('monthly_budget', type=float, help='Monthly budget (optional)', required=False)

authentication_parser = reqparse.RequestParser()
authentication_parser.add_argument('username', type=str, help='Username is required', required=True)
authentication_parser.add_argument('password', type=str, help='Password is required', required=True)

modification_parser = reqparse.RequestParser()
modification_parser.add_argument('new_value', type=str, help='New value is required', required=True)

import traceback

import traceback

import traceback

class UserRegistration(Resource):
    def post(self):
        try:
            args = registration_parser.parse_args()
            print(args)  # Print the parsed arguments for debugging

            username = args['username']
            password = args['password']

            # Convert 'monthly-budget' to float
            monthly_budget_str = args.get('monthly_budget', '1e9')
            monthly_budget = float(monthly_budget_str)

            # Convert 'phone-number' to int
            phone_num_str = args.get('phone_num', '0')
            phone_num = int(phone_num_str)

            if User.query.filter_by(username=username).first():
                return {'message': 'User already exists'}, 400

            user = User(username=username, password=password, monthly_budget=monthly_budget, phone_num=phone_num)
            user.save_to_db()

            return {'message': 'User registered successfully'}, 201
        except ValueError as ve:
            print(f"Validation error: {ve}")  # Print the validation error for debugging
            return {'message': str(ve)}, 400
        except Exception as e:
            traceback.print_exc()  # Print the full traceback for debugging
            return {'message': 'Internal server error'}, 500




class UserAuthentication(Resource):
    def post(self):
        args = authentication_parser.parse_args()
        username = args['username']
        password = args['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # Generate a JWT token
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

class UserPasswordModification(Resource):
    @jwt_required()
    def put(self):
        args = modification_parser.parse_args()
        current_user = get_jwt_identity()
        new_password = args['new_value']

        user = User.query.filter_by(username=current_user).first()
        if user:
            user.password = new_password
            user.save_to_db()
            return {'message': 'Password updated successfully'}, 200
        else:
            return {'message': 'User not found'}, 404

class UserMonthlyBudgetModification(Resource):
    @jwt_required()
    def put(self):
        args = modification_parser.parse_args()
        current_user = get_jwt_identity()
        new_monthly_budget = args['new_value']

        user = User.query.filter_by(username=current_user).first()
        if user:
            user.monthly_budget = new_monthly_budget
            user.save_to_db()
            return {'message': 'Monthly budget updated successfully'}, 200
        else:
            return {'message': 'User not found'}, 404

class UserPhoneNumberModification(Resource):
    @jwt_required()
    def put(self):
        args = modification_parser.parse_args()
        current_user = get_jwt_identity()
        new_phone_number = args['new_value']

        user = User.query.filter_by(username=current_user).first()
        if user:
            user.phone_num = new_phone_number
            user.save_to_db()
            return {'message': 'Phone number updated successfully'}, 200
        else:
            return {'message': 'User not found'}, 404

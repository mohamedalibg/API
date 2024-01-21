from flask import render_template, send_from_directory, request, jsonify
from flask_jwt_extended import  JWTManager, get_current_user, get_jwt_identity, jwt_required, verify_jwt_in_request
from flask_restful import Api
import jwt
from app import app
from app.expenses.resources import ExpenseLogging
from app.models import User

api = Api(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/user')
def user():
    return render_template('user.html')
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    try:
        identity = jwt_data["sub"]
        user = User.query.filter_by(username=identity).first()
        if user:
            return user
        else:
            raise Exception(f"User with ID {identity} not found.")
    except Exception as e:
        print("Error loading user:", str(e))
        return None
@app.route('/expenses', methods=['GET', 'POST'])
@jwt_required(optional=True)
def expenses():
    print("Authorization Header:", request.headers.get("Authorization"))

    if request.method == 'POST' and not get_jwt_identity():
        # If it's a POST request and the user is not authenticated, return an error
        return jsonify({'message': 'Authentication required'}), 401

    if request.method == 'POST':
        try:
            # Get the logged-in user's identity
            current_user = get_jwt_identity()

            print("Current User:", current_user)  # Add this line for debugging

            # Parse the JSON data from the request
            data = request.get_json()

            # Instantiate the ExpenseLogging resource
            expense_logging_resource = ExpenseLogging()

            # Call the post method from the ExpenseLogging resource
            response = expense_logging_resource.post(current_user=current_user, data=data)

            return jsonify(response), 201

        except Exception as e:
            print("Error:", str(e))  # Add this line for debugging
            return jsonify({'message': str(e)}), 500

    return render_template('expenses.html')

@app.route('/retrieve_expenses')
def retrieve_expenses():
    return render_template('retrieve_expenses.html')


# Add a route to serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_here'
jwt = JWTManager(app)

# Use the absolute path for the templates folder
templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app.template_folder = templates_path

app.config.from_pyfile('../config.py', silent=True)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes
from app.users import routes as user_routes
from app.expenses.resources import ExpenseAnalytics, ExpenseLogging, ExpenseRetrieval

# Add resources to the api with explicit endpoint names
api.add_resource(user_routes.UserRegistration, '/register', endpoint='user_registration')
api.add_resource(user_routes.UserAuthentication, '/login', endpoint='user_authentication')
api.add_resource(ExpenseLogging, '/expenses', endpoint='expense_logging')
api.add_resource(ExpenseRetrieval, '/expenses_retreive')
api.add_resource(ExpenseAnalytics, '/expenses_analytics')
# app/expenses/routes.py
from flask import render_template
from flask_restful import Api,Resource
from app import api
import app 
from app.expenses.resources import ExpenseAnalytics, ExpenseLogging
from app.expenses.resources import ExpenseRetrieval
api.add_resource(ExpenseLogging, '/expenses')  # Use '/expenses' as the endpoint
api.add_resource(ExpenseRetrieval, '/expenses_retreive')  # Use '/expenses' as the endpoint
api.add_resource(ExpenseAnalytics, '/expenses_analytics')


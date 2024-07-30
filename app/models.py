from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    groups = db.relationship('Group', secondary='user_groups', backref='members')

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expenses = db.relationship('Expense', backref='group', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    split_method = db.Column(db.String(50), nullable=False)
    splits = db.relationship('ExpenseSplit', backref='expense', lazy=True)

class ExpenseSplit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float)

class UserGroups(db.Model):
    __tablename__ = 'user_groups'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)

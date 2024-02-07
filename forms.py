# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, NumberRange, Length, Email


class SignupForm(FlaskForm):
    username = StringField('UserName:', validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField('Email:', validators=[DataRequired(), Email(), Length(min=10, max=30)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=5, max=100)])

class LoginForm(FlaskForm):
    username = StringField('UserName:', validators=[DataRequired(), Length(min=3, max=20)])
    # email = EmailField('Email:', validators=[DataRequired(), Email(), Length(min=10, max=30)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=5, max=100)])


class ExpenseForm(FlaskForm):
    product = StringField('Product:', validators=[DataRequired()])
    amount = IntegerField('Amount:', validators=[DataRequired(), NumberRange(min=0)])
    why = StringField('Why:', validators=[DataRequired()])
    submit = SubmitField('Add Expenses')

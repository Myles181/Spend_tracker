from flask import flash, render_template, request
from flask import jsonify, abort
from forms import ExpenseForm, SignupForm, LoginForm
from sqlalchemy.exc import SQLAlchemyError
from models import User, Expenses
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import login_user
from config import app, db, login_manager, bcrypt
import re
  
def validate_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/signup')
def signup_view():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        form = SignupForm(request.form)

        print(request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            print(username, email, password)
            # Check if email is valid
            if not validate_email(email):
                return jsonify({"message": "Email not valid", "status_code": 400})

            # Hash the password before storing it in the database
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            new_user = User(username=username, email=email, password=hashed_password)

            try:
                with app.app_context():
                    db.session.add(new_user)
                    db.session.commit()

                flash('Account created successfully! You can now log in.', 'success')
                return jsonify({"message": "Success", "status_code": 200})

            except Exception as e:
                print(f"Error: {e}")
                return jsonify({"message": "Error creating account. Please try again.", "status_code": 500})
        else:
            print("Form errors:", form.errors)

    return jsonify({"message": f"Invalid request {request.method}. Please provide valid signup data.", "status_code": 400})

@app.route('/login')
def login_view():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Replace this with your actual authentication logic
        user = User.query.filter_by(username=username).first()
        print(user)

        if user and bcrypt.check_password_hash(user.password, password):
            
            # Log in the user using Flask-Login
            login_user(user) 

            # Create and return a JWT token
            access_token = create_access_token(identity=user._id)
            return jsonify(access_token=access_token)

        else:
            return jsonify({"message": "Login failed. Please check your username and password.", "status_code": 401})

    return jsonify({"message": "Invalid request. Please provide valid credentials.", "status_code": 400})

@app.route('/expenses')
@jwt_required()
def add_expense():
    return render_template('expensea.html')

@app.route('/add_expenses', methods=['POST', 'GET'])
@jwt_required()
def add_expenses():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        form = ExpenseForm()

        if form.validate_on_submit():
            product = request.form.get('product')
            amount = request.form.get('amount')
            why = request.form.get('why')

            try:
                with app.app_context():
                    exp = Expenses(product=product, amount=amount, why=why)
                    db.session.add(exp)
                    db.session.commit()
                return jsonify({"message": "Succes",
                                "status_code": 200,
                                "user": current_user})
            except SQLAlchemyError as e:
                print(f"Error: {e}")
                abort(500, description="Database error")

    return jsonify({"message": "Failure",
                    "status_code": 400})


@app.route('/expenses/<int:user_id>')
def list_all(user_id):
    user = User.query.filter_by(_id=user_id).first()

    if not user:
        abort(404, description=f"User '{user_id}' not found")

    expenses = Expenses.query.filter_by(user_id=user.id).all()

    expenses_list = [
        {'product': exp.product, 'amount': exp.amount, 'why': exp.why}
        for exp in expenses
    ]

    return jsonify({'expenses': expenses_list, 'status_code': 200})
@app.route('/edit_expense/<int:expense_id>', methods=['PUT'])
@jwt_required()
def edit_expense(expense_id):
    current_user = get_jwt_identity()

    # Assuming you have a relationship between User and Expenses
    user = User.query.filter_by(username=current_user).first()

    if not user:
        abort(404, description=f"User '{current_user}' not found")

    expense = Expenses.query.get(expense_id)

    if not expense:
        abort(404, description=f"Expense with ID '{expense_id}' not found")

    if expense.user_id != user.id:
        abort(403, description="You do not have permission to edit this expense")

    if request.method == 'PUT':
        form_data = request.json  # Assuming JSON data is sent in the request body

        # Update the expense fields based on the form data
        expense.product = form_data.get('product', expense.product)
        expense.amount = form_data.get('amount', expense.amount)
        expense.why = form_data.get('why', expense.why)

        try:
            with app.app_context():
                db.session.commit()

            return jsonify({"message": "Expense updated successfully", "status_code": 200})

        except SQLAlchemyError as e:
            print(f"Error: {e}")
            abort(500, description="Database error")

    return jsonify({"message": "Invalid request method. Please use PUT.", "status_code": 400})

@app.route('/delete_expenses/<id>', methods=['POST', 'GET'])
def delete(id):
    return jsonify({'message': 'Success',
                    'status code': 200})

@app.route('/delete_all_expenses/<user_id>', methods=['POST', 'GET'])
def delete_all(user_id):
    return jsonify({'message': 'Success',
                    'status code': 200})


if __name__ == "__main__":
    app.run(debug=True)
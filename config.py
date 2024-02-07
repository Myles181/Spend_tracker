
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager

app = Flask(__name__)
load_dotenv()
bcrypt = Bcrypt(app)

username = os.getenv("MYSQL_USERNAME")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
database_name = os.getenv("MYSQL_DATABASE")
secret_key = os.getenv("MY_SECRET_KEY")

app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{username}:{password}@{host}:{port}/{database_name}"
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)
csrf = CSRFProtect()
csrf.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)  # Remove app=app argument

# with app.app_context():
#     db.create_all()

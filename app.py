from flask import Flask, render_template, request, redirect, jsonify, session, url_for, flash
import os
from db_access import get_user_by_email, create_user, get_user_by_email_and_username, clear_all_data

app = Flask(__name__)
app.secret_key = os.urandom(24)

from flask_restx import Api, Resource, fields, Namespace

api = Api(app, doc='/api/docs')

login_ns = Namespace('login', description='Login operations')

login_model = login_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@login_ns.route('/')
class Login(Resource):
    @login_ns.expect(login_model)
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')

        user = get_user_by_email(email)
        if user:
            if user['password'] == password:
                return {'message': 'Login successful'}, 200
            else:
                return {'message': 'Invalid password'}, 401
        else:
            create_user('', '', email, password)
            return {'message': 'Account created and logged in'}, 201

users_ns = Namespace('users', description='User operations')

@users_ns.route('/')
class Users(Resource):
    def get(self):
        # This can be improved to use db_access.py if needed
        return {'message': 'User list endpoint'}

api.add_namespace(login_ns, path='/api/auth/login')
api.add_namespace(users_ns, path='/api/auth/users')

# New namespace for username-password check
auth_ns = Namespace('auth', description='Authentication operations')

auth_model = auth_ns.model('Auth', {
    'username': fields.String(required=True, description='User username'),
    'password': fields.String(required=True, description='User password')
})

@auth_ns.route('/check_user')
class CheckUser(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = get_user_by_username_and_password(username, password)
        if user:
            return {'exists': True, 'user': user}, 200
        else:
            return {'exists': False}, 404

api.add_namespace(auth_ns, path='/api/auth')

# New namespace for admin operations
admin_ns = Namespace('admin', description='Admin operations')

@admin_ns.route('/clear_data')
class ClearData(Resource):
    def post(self):
        clear_all_data()
        return {'message': 'All data cleared successfully'}, 200

api.add_namespace(admin_ns, path='/api/admin')


@app.route('/')
def home():
    if 'user_email' in session:
        return redirect(url_for('welcome'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))

        existing_user = get_user_by_email(email)
        if existing_user:
            flash('User already exists', 'error')
            return redirect(url_for('signup'))

        create_user(username, '', email, password)
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        user = get_user_by_email_and_username(email, username)
        if user:
            if user['password'] == password:
                session['user_email'] = user['email']
                session['user_name'] = user['first_name']
                return redirect(url_for('welcome'))
            else:
                flash('Invalid password', 'error')
                return redirect(url_for('login'))
        else:
            flash('User not found. Please create an account.', 'error')
            return redirect(url_for('signup'))
    else:
        return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    return render_template('logged_in.html', user_email=session.get('user_email'), user_name=session.get('user_name'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)  

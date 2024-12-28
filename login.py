from flask import Flask, request, render_template, redirect, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import smtplib
import os
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages and session management

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="user_management"
)
cursor = db.cursor()

# Home Route - Redirect to Login by default
@app.route('/')
def home():
    return redirect(url_for('login_form'))

@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('login_form'))

    user_email = session['email']
    cursor.execute("SELECT username, email FROM users WHERE email = %s", (user_email,))
    user = cursor.fetchone()

    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))  # Redirect to home page after logout

# Login Page Route
@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

# Login Processing Route
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user:
        # If user exists, check if the password is correct
        if check_password_hash(user[3], password):
            session['email'] = email  # Store email in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard
        else:
            flash('Incorrect password!', 'danger')  # Flash message for incorrect password
            return redirect(url_for('login_form'))
    else:
        # If user is not registered
        flash('Email not found! Please register first.', 'danger')
        return redirect(url_for('register_form'))

# Dashboard Route - After successful login
@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login_form'))

    user_email = session['email']
    return render_template('mini.html', user_email=user_email)  # Pass the user email to the template

# Register Page Route
@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

# Register Processing Route
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = generate_password_hash(request.form.get('password'))

    # Check if email already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        flash('Email already registered!', 'danger')
        return redirect(url_for('register_form'))

    # Insert new user into the database
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    db.commit()
    flash('User registered successfully! Please log in.', 'success')
    return redirect(url_for('login_form'))

# Forgot Password Page Route
@app.route('/forgot-password', methods=['GET'])
def forgot_password_form():
    return render_template('forgot_password.html')

# Forgot Password Processing Route (Send reset email)
@app.route('/forgot-password', methods=['POST'])
def forgot_password_post():
    email = request.form.get('email')
    logging.debug(f'Received forgot-password request for email: {email}')

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    logging.debug(f'User lookup result: {user}')

    if user:
        reset_token = str(uuid.uuid4())
        logging.debug(f'Generated reset token: {reset_token}')
        
        cursor.execute("UPDATE users SET reset_token = %s WHERE email = %s", (reset_token, email))
        db.commit()
        logging.debug('Database updated with reset token')

        # Send email with reset token (using SMTP)
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS"))
            message = f"Click the link to reset your password: http://localhost:5000/reset-password?token={reset_token}"
            server.sendmail(os.environ.get("EMAIL_USER"), email, message)
            server.quit()
            flash('Reset link sent to your email!', 'success')
            logging.debug('Email sent successfully')
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            flash(f"Error sending email: {str(e)}", 'danger')
            return redirect(url_for('forgot_password_form'))

    else:
        flash('Email not found!', 'danger')
        logging.debug('Email not found in database')
        return redirect(url_for('forgot_password_form'))

    return redirect(url_for('login_form'))

# Password Reset Form Route
@app.route('/reset-password', methods=['GET'])
def reset_password_form():
    token = request.args.get('token')
    logging.debug(f'Received reset-password request with token: {token}')
    if not token:
        flash('Invalid or missing token!', 'danger')
        return redirect(url_for('login_form'))

    return render_template('reset_password.html', token=token)

# Password Reset Processing Route
@app.route('/reset-password', methods=['POST'])
def reset_password():
    token = request.form.get('token')
    new_password = request.form.get('password')

    # Find the user with the reset token
    cursor.execute("SELECT * FROM users WHERE reset_token = %s", (token,))
    user = cursor.fetchone()

    if user:
        new_password_hash = generate_password_hash(new_password)
        cursor.execute("UPDATE users SET password = %s, reset_token = NULL WHERE reset_token = %s", (new_password_hash, token))
        db.commit()
        flash('Password reset successfully! Please log in.', 'success')
        return redirect(url_for('login_form'))
    else:
        flash('Invalid or expired token!', 'danger')
        return redirect(url_for('reset_password_form', token=token))
    

@app.route('/contact')
def contact():
    return render_template('contact.html')




# User profile data
user_profile = {
    'first_name': 'John',
    'middle_name': 'A.',
    'last_name': 'Doe',
    'email': 'johndoe@example.com',
    'phone': '123-456-7890',
    'occupation': 'Software Developer',
    'country': 'USA',
    'state': 'California',
    'date_of_birth': '1990-01-01',
    'gender': 'Male'
}

@app.route('/profile1')
def profile1():
    return render_template('profile.html', profile=user_profile)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        # Capture form data and update profile
        user_profile['first_name'] = request.form.get('first_name')
        user_profile['middle_name'] = request.form.get('middle_name')
        user_profile['last_name'] = request.form.get('last_name')
        user_profile['email'] = request.form.get('email')
        user_profile['phone'] = request.form.get('phone')
        user_profile['occupation'] = request.form.get('occupation')
        user_profile['country'] = request.form.get('country')
        user_profile['state'] = request.form.get('state')
        user_profile['date_of_birth'] = request.form.get('date_of_birth')
        user_profile['gender'] = request.form.get('gender')
        
        flash('Profile updated successfully!')
        return redirect(url_for('profile1'))
    
    return render_template('edit_profile.html', profile=user_profile)



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

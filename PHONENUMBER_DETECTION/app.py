import pickle  # For loading the trained model
from flask import Flask, request, render_template_string
import numpy as np
import re

app = Flask(__name__)

# Load the trained model (update the path as per your environment)
MODEL_PATH = "D:\\MINI-PROJECT\\phonenumber\\decision_tree_spam_model_v2.pkl"
with open(MODEL_PATH, 'rb') as file:
    spam_model = pickle.load(file)

# HTML template with enhanced UI and responsive design

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Phone Number Spam Checker</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #fff;
            overflow: hidden;
            animation: backgroundAnimation 10s infinite alternate;
        }

        @keyframes backgroundAnimation {
            0% {
                background: linear-gradient(135deg, #667eea, #764ba2);
            }
            100% {
                background: linear-gradient(135deg, #ff7e5f, #feb47b);
            }
        }

        .container {
            background: rgba(255, 255, 255, 0.9);
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 100%;
            max-width: 400px;
            color: #333;
            animation: fadeIn 1s ease-in-out;
            position: relative;
            overflow: hidden;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .container::before, .container::after {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(135deg, transparent, rgba(255, 255, 255, 0.5));
            z-index: -1;
            animation: borderAnimation 5s infinite linear;
            border-radius: 10px;
        }

        .container::before {
            animation-delay: 0s;
        }

        .container::after {
            animation-delay: 2.5s;
        }

        @keyframes borderAnimation {
            0% {
                transform: rotate(0deg);
            }
            100% {
                transform: rotate(360deg);
            }
        }

        h1 {
            font-size: 24px;
            margin-bottom: 20px;
        }

        form {
            margin-top: 20px;
        }

        input[type="text"] {
            padding: 12px;
            width: calc(100% - 24px);
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
            transition: border-color 0.3s;
        }

        input[type="text"]:focus {
            border-color: #667eea;
        }

        button {
            padding: 12px 20px;
            background-color: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }
        .dashboard-button {
    padding: 12px 20px;
    background-color: #ff7e5f;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 20px;
    transition: background-color 0.3s ease, transform 0.3s ease;
}

.dashboard-button:hover {
    background-color: #e66a4e;
    transform: translateY(-2px);
}


        button:hover {
            background-color: #5564c1;
            transform: translateY(-2px);
        }

        .result {
            margin-top: 20px;
            font-size: 18px;
        }

        .spam {
            color: red;
            font-weight: bold;
        }

        .ham {
            color: green;
            font-weight: bold;
        }

        footer {
            margin-top: 30px;
            font-size: 14px;
            color: #ccc;
        }

        .footer-link {
            color: #667eea;
            text-decoration: none;
        }

        .footer-link:hover {
            text-decoration: underline;
        }

        .background-circles {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -1;
        }

        .background-circles li {
            position: absolute;
            display: block;
            list-style: none;
            width: 20px;
            height: 20px;
            background: rgba(255, 255, 255, 0.2);
            animation: animateCircles 25s linear infinite;
            bottom: -150px;
            border-radius: 50%;
        }

        .background-circles li:nth-child(1) {
            left: 25%;
            width: 80px;
            height: 80px;
            animation-delay: 0s;
        }

        .background-circles li:nth-child(2) {
            left: 10%;
            width: 20px;
            height: 20px;
            animation-delay: 2s;
            animation-duration: 12s;
        }

        .background-circles li:nth-child(3) {
            left: 70%;
            width: 20px;
            height: 20px;
            animation-delay: 4s;
        }

        .background-circles li:nth-child(4) {
            left: 40%;
            width: 60px;
            height: 60px;
            animation-delay: 0s;
            animation-duration: 18s;
        }

        .background-circles li:nth-child(5) {
            left: 65%;
            width: 20px;
            height: 20px;
            animation-delay: 0s;
        }

        .background-circles li:nth-child(6) {
            left: 75%;
            width: 110px;
            height: 110px;
            animation-delay: 3s;
        }

        .background-circles li:nth-child(7) {
            left: 35%;
            width: 150px;
            height: 150px;
            animation-delay: 7s;
        }

        .background-circles li:nth-child(8) {
            left: 50%;
            width: 25px;
            height: 25px;
            animation-delay: 15s;
            animation-duration: 45s;
        }

        .background-circles li:nth-child(9) {
            left: 20%;
            width: 15px;
            height: 15px;
            animation-delay: 2s;
            animation-duration: 35s;
        }

        .background-circles li:nth-child(10) {
            left: 85%;
            width: 150px;
            height: 150px;
            animation-delay: 0.5s;
            animation-duration: 11s;
        }

        @keyframes animateCircles {
            0% {
                transform: translateY(0) rotate(0deg);
                opacity: 1;
            }
             100% {
                transform: translateY(-1000px) rotate(720deg);
                opacity: 0;
            }
        }
    </style>
</head>
<body>
    <div class="background-circles">
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
    </div>
    <div class="container">
        <h1><i class="fas fa-phone-alt"></i> Phone Number Spam Checker</h1>
        <form action="/" method="post">
            <label for="phone_number">Enter phone number:</label>
            <input type="text" id="phone_number" name="phone_number" placeholder="e.g., 1234567890" required>
            <button type="submit"><i class="fas fa-search"></i> Check</button>
        </form>
        {% if result %}
            <div class="result">
                <p>The phone number <strong>{{ phone_number }}</strong> is <span class="{{ result }}">{{ result }}</span>.</p>
            </div>
        {% endif %}
        <button onclick="window.location.href='http://127.0.0.1:5000/dashboard'" class="dashboard-button">
        <i class="fas fa-home"></i> Go to Dashboard
        </button>
    </div>
</body>
</html>
"""

# Modify this function to match the 20 features expected by the model
def preprocess_phone_number(phone_number):
    phone_number_str = str(phone_number)
    
    # Ensure phone number is at least 10 digits long (zero-padding if needed)
    max_length = 10
    digits = [int(char) for char in phone_number_str if char.isdigit()]
    if len(digits) < max_length:
        digits = [0] * (max_length - len(digits)) + digits  # Zero-padding

    # Extract 20 features from the phone number
    length = len(phone_number_str)
    starts_with = int(phone_number_str[:3]) if len(phone_number_str) >= 3 else 0
    repeating_digits = len(set(phone_number_str))
    digit_counts = [phone_number_str.count(str(i)) for i in range(10)]
    digit_sum = sum(int(digit) for digit in phone_number_str)
    digit_avg = digit_sum / len(phone_number_str) if len(phone_number_str) > 0 else 0
    area_code = int(phone_number_str[:3]) if len(phone_number_str) >= 3 else 0
    has_certain_prefix = int(phone_number_str.startswith('123'))
    even_digits = sum(1 for digit in phone_number_str if int(digit) % 2 == 0)
    odd_digits = sum(1 for digit in phone_number_str if int(digit) % 2 != 0)
    unique_digits = len(set(phone_number_str))
    
    sum_even_digits = sum(int(digit) for digit in phone_number_str if int(digit) % 2 == 0)
    sum_odd_digits = sum(int(digit) for digit in phone_number_str if int(digit) % 2 != 0)
    max_digit = max(int(digit) for digit in phone_number_str)
    min_digit = min(int(digit) for digit in phone_number_str)
    count_digit_0 = phone_number_str.count('0')
    count_digit_1 = phone_number_str.count('1')
    count_digit_9 = phone_number_str.count('9')
    has_repeated_digits = int(len(set(phone_number_str)) < len(phone_number_str))

    # Return the 20 features in the required format
    return np.array([length, starts_with, repeating_digits] + digit_counts + [digit_sum, digit_avg, area_code, has_certain_prefix, even_digits, odd_digits, unique_digits, 
            sum_even_digits, sum_odd_digits, max_digit, min_digit, count_digit_0, count_digit_1, count_digit_9, has_repeated_digits])

def is_spam_number_ml(phone_number):
    feature_vector = preprocess_phone_number(phone_number)
    prediction = spam_model.predict([feature_vector])[0]
    return prediction == 1  # Assuming '1' represents spam, '0' represents ham

def check_phone_number(phone_number):
    """
    Determine if the phone number is spam or ham.
    """
    return "spam" if is_spam_number_ml(phone_number) else "ham"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    phone_number = ''
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        result = check_phone_number(phone_number)
    
    # Render the HTML template with results
    return render_template_string(HTML_TEMPLATE, phone_number=phone_number, result=result)

if __name__ == '__main__':
    app.run(port=5002, debug=True)

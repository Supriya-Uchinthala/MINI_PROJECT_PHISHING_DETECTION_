from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

# List of known spam numbers
known_spam_numbers = [
    "1234567890",
    "0987654321",
    "1112223333",
    # Add more known spam numbers here
]

def is_spam_number(phone_number):
    """
    Check if the phone number is spam based on known spam numbers and common spam patterns.
    """
    # Check if the number is in the known spam numbers list
    if phone_number in known_spam_numbers:
        return True

    # Check for common spam patterns (e.g., repetitive digits, unusual prefixes)
    spam_patterns = [
        r"(\d)\1{4,}",   # Repetitive digits (e.g., 11111, 22222)
        r"^(900|800)\d{7}$"  # Premium rate numbers (common spam pattern)
    ]

    for pattern in spam_patterns:
        if re.match(pattern, phone_number):
            return True

    # If no match is found, it's not considered spam
    return False

# Uncomment if you have a third-party API to use for checking spam numbers
# import requests
# def check_spam_with_api(phone_number):
#     """
#     Check if the phone number is spam using a third-party API.
#     """
#     api_key = "YOUR_API_KEY"
#     url = f"https://api.thirdpartyservice.com/check?number={phone_number}&api_key={api_key}"
#     
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#         return data.get("is_spam", False)
#     except requests.RequestException as e:
#         print(f"Failed to check spam status with API: {e}")
#         return False

def check_phone_number(phone_number):
    """
    Check if the phone number is spam or ham.
    """
    if is_spam_number(phone_number):
        return "spam"
    
    # Uncomment the following lines if using third-party API for enhanced checking
    # if check_spam_with_api(phone_number):
    #     return "spam"
    
    return "ham"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    phone_number = ''
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        result = check_phone_number(phone_number)
    
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Phone Number Spam Checker</title>
        </head>
        <body>
            <h1>Phone Number Spam Checker</h1>
            <form method="post">
                <label for="phone_number">Enter phone number:</label>
                <input type="text" id="phone_number" name="phone_number" required>
                <button type="submit">Check</button>
            </form>
            {% if result %}
                <p>The phone number {{ phone_number }} is {{ result }}.</p>
            {% endif %}
        </body>
        </html>
    ''', phone_number=phone_number, result=result)

if __name__ == '__main__':
    app.run(debug=True)

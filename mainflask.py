import subprocess
import time
from flask import Flask, render_template,redirect, send_from_directory,  request,  url_for, flash


app = Flask(__name__)

processes = {}

def start_flask_app(port, app_path, app_module):
    global processes
    if port not in processes:
        try:
            processes[port] = subprocess.Popen(
                ['flask', 'run', '--port={}'.format(port)],
                cwd=app_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(5)  # Increase sleep time if needed to ensure the app starts
        except Exception as e:
            print(f"Error starting Flask app on port {port}: {e}")

def stop_flask_app(port):
    global processes
    if port in processes:
        processes[port].terminate()
        processes[port].wait()
        del processes[port]

@app.route('/')
def home():
    return render_template('mini.html')
    
@app.route('/site1')
def site1():
    start_flask_app(5000, 'D:\\MINI-PROJECT\\Phishing-URL-Detection-master', 'app')
    return redirect("http://localhost:5001")

@app.route('/site2')
def site2():
    start_flask_app(5001, 'D:\\MINI-PROJECT\\phonenumber', 'app')
    return redirect("http://localhost:5002")

@app.route('/site3')
def site3():
    start_flask_app(5002, 'D:\\MINI-PROJECT\\QR-CODE', 'app')
    return redirect("http://localhost:5003")

@app.route('/site4')
def site4():
    start_flask_app(5003, 'D:\\MINI-PROJECT\\spam-email-classifier', 'app')
    return redirect("http://localhost:5004")



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




@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(port=5005)

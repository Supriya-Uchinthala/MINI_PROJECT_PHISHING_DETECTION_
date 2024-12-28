import pickle
from flask import Flask, render_template, request
import time

# Load the model and CountVectorizer from the model.pkl file
with open('D:/MINI-PROJECT/spam-email-classifier/model1.pkl','rb') as f:
    model, cv = pickle.load(f)

app = Flask(__name__)

result = ''

@app.route('/')
def index():
    return render_template('index.html', result=result)

@app.route('/predict', methods=['POST'])
def predict_spam():
    msg = request.form.get('message')

    # Transform the message using the loaded CountVectorizer
    msg_input = cv.transform([msg])

    # Make prediction using the loaded model
    result = model.predict(msg_input)

    if result[0] == 1:
        result = 'ham'
    else:
        result = 'spam'

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
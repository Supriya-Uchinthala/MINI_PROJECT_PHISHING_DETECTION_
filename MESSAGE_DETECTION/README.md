# Spam Detector

This project is a flask based web app that detects spam messages using Naive Bayes classifier algorithm of machine learning. The application is built with Python 3 and Flask. It uses `CountVectorizer` with `MultinomialNB` from `naive_bayes` to achieve the best performance. The vectorizer and model are serialized using `pickle` for easy access in the Flask web app.

## Table of Contents
- [Project Description](#project-description)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Example](#example)
- [Additional Notes](#additional-notes)

## Project Description <a name='project-description'></a>

The Spam Detector classifies messages as spam or not spam using a machine learning model. The model is trained with the `MultinomialNB` algorithm and `CountVectorizer` to convert text data into numerical format. The Flask web application serves as an interface for users to input messages and get predictions.

## Installation and Setup <a name='installation-and-setup'></a>

Follow these steps to set up and run the project:

1. **Create a virtual environment**:

   ```bash
   python -m venv myenv
   ```
2. **Activate the virtual environment**:

    ##### On Windows:

    ```bash
    .\myenv\Scripts\activate
    ```

    ##### On macOS and Linux:

    ```bash
    source myenv/bin/activate
    ```
    After activation, your terminal prompt will change to indicate that you are now working inside the virtual environment.

3. **Install the required packages**:

    ```bash
    pip install -r Requirements.txt
    ```

4. **Run the Flask application**:

    ```bash
    flask run
    ```

## Usage  <a name='usage'></a>
1. Open your web browser and go to
   ```bash
   http://127.0.0.1:5000
   ```
2. You will see an input field where you can enter a message.
3. Submit the message to get the prediction of whether it is spam or not spam.

## Example  <a name='example'></a>
Here is a brief example of how the application works:

1. Enter a message such as
   ```bash
   Congratulations! You've won a $1000 gift card. Click here to claim your prize here in this below link https://bitelottery4567.com/3frfty-ofgdf.
   ```
3. Click the "Predict" button.
4. The application will process the message and display the result, indicating whether the message is spam.
   
## Additional Notes  <a name='additional-notes'></a>
1. Ensure that the CountVectorizer and MultinomialNB model are properly serialized and available for the Flask app to load.
2. The project structure should include the necessary files such as app.py, the serialized model file, and Requirements.txt.

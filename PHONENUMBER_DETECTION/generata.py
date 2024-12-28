import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle

# Load the dataset
df = pd.read_csv("D:\\MINI-PROJECT\\phonenumber\\spam_ham_phone_numbers.csv")

# Feature extraction (now creating 11 features)
# Updated feature extraction to generate 20 features
def extract_features(phone_number):
    phone_number_str = str(phone_number)
    
    # 1. Length of phone number
    length = len(phone_number_str)
    
    # 2. Starting with first 3 digits
    starts_with = int(phone_number_str[:3]) if len(phone_number_str) >= 3 else 0
    
    # 3. Repeating digits
    repeating_digits = len(set(phone_number_str))
    
    # 4. Count of each digit (0-9)
    digit_counts = [phone_number_str.count(str(i)) for i in range(10)]
    
    # 5. Sum of digits
    digit_sum = sum(int(digit) for digit in phone_number_str)
    
    # 6. Average of digits
    digit_avg = digit_sum / len(phone_number_str) if len(phone_number_str) > 0 else 0
    
    # 7. Area code (e.g., first 3 digits as a simple example)
    area_code = int(phone_number_str[:3]) if len(phone_number_str) >= 3 else 0
    
    # 8. Has certain prefix (e.g., 123)
    has_certain_prefix = int(phone_number_str.startswith('123'))
    
    # 9. Count of even digits
    even_digits = sum(1 for digit in phone_number_str if int(digit) % 2 == 0)
    
    # 10. Count of odd digits
    odd_digits = sum(1 for digit in phone_number_str if int(digit) % 2 != 0)
    
    # 11. Number of unique digits
    unique_digits = len(set(phone_number_str))
    
    # 12-20. Additional features
    # Adding more complex statistical features or digit-specific information
    sum_even_digits = sum(int(digit) for digit in phone_number_str if int(digit) % 2 == 0)
    sum_odd_digits = sum(int(digit) for digit in phone_number_str if int(digit) % 2 != 0)
    max_digit = max(int(digit) for digit in phone_number_str)
    min_digit = min(int(digit) for digit in phone_number_str)
    count_digit_0 = phone_number_str.count('0')
    count_digit_1 = phone_number_str.count('1')
    count_digit_9 = phone_number_str.count('9')
    has_repeated_digits = int(len(set(phone_number_str)) < len(phone_number_str))
    
    return [length, starts_with, repeating_digits] + digit_counts + [digit_sum, digit_avg, area_code, has_certain_prefix, even_digits, odd_digits, unique_digits, 
            sum_even_digits, sum_odd_digits, max_digit, min_digit, count_digit_0, count_digit_1, count_digit_9, has_repeated_digits]


# Apply feature extraction
df["Features"] = df["Phone Number"].astype(str).apply(extract_features)

# Extracting the feature matrix (X) and labels (y)
X = np.array(df["Features"].tolist())
y = (df["Label"] == "Spam").astype(int)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train the DecisionTreeClassifier model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Save the trained model to a file
with open("decision_tree_spam_model_v2.pkl", "wb") as file:
    pickle.dump(model, file)
print("Model saved successfully.")

# Load the model back from the file
with open("decision_tree_spam_model_v2.pkl", "rb") as file:
    loaded_model = pickle.load(file)
print("Model loaded successfully.")

# Evaluate the model
y_pred = loaded_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

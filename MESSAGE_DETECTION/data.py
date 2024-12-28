import random
import pandas as pd

# Function to generate random phone numbers
def generate_phone_number(is_spam):
    if is_spam:
        # Generate spam patterns
        spam_patterns = [
            lambda: f"{random.randint(100, 999)}{random.randint(1000, 9999)}{random.randint(10, 99)}",  # Random
            lambda: "1234567890",  # Repeated sequence
            lambda: f"800{random.randint(1000000, 9999999)}",  # Telemarketer prefix
        ]
        return random.choice(spam_patterns)()
    else:
        # Generate valid personal phone numbers
        return f"{random.randint(600, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"

# Generate dataset
data = []
for _ in range(1000):
    if random.random() > 0.5:
        data.append([generate_phone_number(True), "Spam"])
    else:
        data.append([generate_phone_number(False), "Ham"])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Phone Number", "Label"])

# Save to CSV
df.to_csv("spam_ham_phone_numbers.csv", index=False)
print("Dataset saved as 'spam_ham_phone_numbers.csv'")

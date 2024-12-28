import os
import qrcode
import random
import pandas as pd

# Create directories to store QR codes
if not os.path.exists('qrcodes/spam'):
    os.makedirs('qrcodes/spam')
if not os.path.exists('qrcodes/ham'):
    os.makedirs('qrcodes/ham')

# Expanded list of URLs for spam and ham categories
spam_urls = [
    'http://example.com/phishing1', 'http://malicious-link.com', 'http://spam-site.com',
    'http://phishing-example.net', 'http://fakebank-login.com', 'http://fraud-alert.com',
    'http://phishing123.xyz', 'http://fake-news-site.com', 'http://malware-link.com', 
    'http://scam-link.org', 'http://suspicious-link.biz', 'http://badsite.com'
]

ham_urls = [
    'http://example.com/legit1', 'http://mywebsite.com', 'http://safe-site.com', 
    'http://goodexample.com', 'http://apple.com', 'http://google.com', 'http://bbc.com',
    'http://wikipedia.org', 'http://youtube.com', 'http://python.org', 'http://github.com',
    'http://stackoverflow.com'
]

# Function to generate QR codes
def generate_qr_code(url, filename, label):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    return {'image': filename, 'label': label}

# List to store dataset information
dataset = []

# Increase the number of generated QR codes
total_samples = 10000  # Set to 10,000 or more for a larger dataset
for i in range(total_samples):
    spam_url = random.choice(spam_urls)
    ham_url = random.choice(ham_urls)
    
    # Generate spam QR code
    spam_filename = f'qrcodes/spam/spam_{i}.png'
    dataset.append(generate_qr_code(spam_url, spam_filename, 'spam'))
    
    # Generate ham QR code
    ham_filename = f'qrcodes/ham/ham_{i}.png'
    dataset.append(generate_qr_code(ham_url, ham_filename, 'ham'))

# Convert the dataset to a pandas DataFrame and save as CSV
df = pd.DataFrame(dataset)
df.to_csv('qrcodes_large_dataset.csv', index=False)

print(f"Large QR codes dataset with {total_samples} samples created successfully!")

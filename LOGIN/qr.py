import qrcode

# Generate a QR code
data = "https://www.wikipedia.org/"
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(data)
qr.make(fit=True)

# Create an image of the QR code
img = qr.make_image(fill='black', back_color='white')
img.save('spam_qr_code.png')

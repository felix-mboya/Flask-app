from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
application = app 


EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            try:
                msg = MIMEText(f"Name: {name}\nEmail: {email}\n\n{message}")
                msg['Subject'] = 'New Contact Form Submission'
                msg['From'] = EMAIL_USERNAME
                msg['To'] = EMAIL_RECEIVER

                with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                    server.starttls()
                    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
                    server.send_message(msg)

                flash('Message sent successfully!', 'success')
            except Exception as e:
                flash(f'Error sending message: {str(e)}', 'danger')
        else:
            flash('All fields are required.', 'warning')

        return redirect('/contact')

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)



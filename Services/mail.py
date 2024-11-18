from flask import render_template, url_for, current_app
from flask_mail import Message
from Misc.my_logger import my_logger


def send_verification_email(mail, user):
    'Send a verification email to the user.'
    # mail settings
    current_app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your email provider's SMTP server
    current_app.config['MAIL_PORT'] = 587
    current_app.config['MAIL_USE_TLS'] = True
    current_app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Your email address
    current_app.config['MAIL_PASSWORD'] = 'your-email-password'  # Your email password (or app password for Gmail)
    current_app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@gmail.com'  # Default sender email

    current_app.config['PREFERRED_URL_SCHEME'] = 'http://'
    current_app.config['SERVER_NAME'] = '127.0.0.1:5004'
    current_app.config['APPLICATION_ROOT'] = '/'
    
    with current_app.app_context():
        verification_url = url_for('verify_email', token=user.token, _external=True)

    # Create the email message
    msg = Message(
        'Email Verification',
        recipients=[user.email],
        body=f'Please verify your email address by clicking the following link: {verification_url}',
        html=render_template('verify_email.html', user_first_name=user.first_name, verification_url=verification_url)
    )

    # Send the email
    # mail.send(msg)
    my_logger.debug(msg.html)

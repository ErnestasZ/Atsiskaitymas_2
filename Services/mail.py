from flask import render_template, url_for, current_app
from flask_mail import Message
from Misc.my_logger import my_logger


def send_verification_email(mail, user):
    'Send a verification email to the user.'
    current_app.config['PREFERRED_URL_SCHEME'] = 'http://'
    current_app.config['SERVER_NAME'] = '127.0.0.1:5004'
    current_app.config['APPLICATION_ROOT'] = '/'
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

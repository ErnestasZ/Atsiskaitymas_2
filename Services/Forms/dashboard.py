from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, DateField, DateTimeField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange, Length, Optional, InputRequired, AnyOf
from datetime import datetime
from Misc.constants import ORDER_STATUSES
import re

# from flask_wtf.csrf import generate_csrf

# csrf_token = generate_csrf()


class SelectDateRangeForm(FlaskForm):
    start_date = DateField('Start Date', validators=[
                           DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[
                         DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Submit')

    def validate_end_date(self, end_date):
        if self.start_date.data and end_date.data:
            if end_date.data < self.start_date.data:
                raise ValidationError('End date must be after start date.')


class StatusForm(FlaskForm):
    status = SelectField(
        'Change status',
        choices=[('', 'Select status')] + [(status, status.capitalize())
                                           for status in ORDER_STATUSES],
        validators=[InputRequired(), AnyOf(
            ORDER_STATUSES, message='Invalid status selection')]
    )


class ReviewForm(FlaskForm):
    rating = IntegerField('Rate (0-5)', validators=[
        Optional(),  # Allow nullable
        NumberRange(min=0, max=5, message="Rating must be between 0 and 5")
    ])

    content = TextAreaField('Content', validators=[
                            Optional()])  # Allow nullable

    def validate_content(self, content):
        if content.data:
            # Removes any HTML tags (example of sanitization)
            content.data = re.sub(r'<.*?>', '', content.data)
            # Remove unwanted special chars
            content.data = re.sub(
                r'[^a-zA-Z0-9\s,.?!;:()-]', '', content.data)

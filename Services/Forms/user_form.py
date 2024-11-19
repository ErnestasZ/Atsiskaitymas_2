from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, DateField, DateTimeField, TextAreaField, SelectField, EmailField, FloatField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError, NumberRange, Length, Optional, InputRequired, AnyOf
# from Models.user import User
from Misc.constants import password_regex


# def email_unique(form, field):
#     existing_user = User.query.filter_by(email=field.data).first()
#     if existing_user:
#         raise ValidationError('Email is already taken')
def letters_only(form, field):
    if not field.data.isalpha():
        raise ValidationError('This field can contain only letters.')
    
class BalanceForm(FlaskForm):
    balance = FloatField('Balance',
                         validators=[DataRequired(message='Enter numeric float separate "." decimals'),
                                     NumberRange(min=0, max=5000, message='Amount must be a positive number form 0 to 5000')],
                         render_kw={"placeholder": "Add amount"})


class UserForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(
        min=3, max=20, message='Min 3 char'), letters_only],
        render_kw={"placeholder": "Enter your first name"})
    last_name = StringField('Last name', validators=[DataRequired(), Length(
        min=3, max=20), letters_only],
        render_kw={"placeholder": "Enter your last name"})
    password = PasswordField('Password', validators=[
        Length(min=8, max=20, message='Min 8 characters required'),
        EqualTo('confirm_password', message='Passwords must match'),
        Optional(),
        
        Regexp(r'{password_regex}'),
               message='Password must contain at least one special character')
    ])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[ 
                                         Optional(),
                                         EqualTo(
                                             'password', message='Passwords must match')
                                     ])

    # def validate_confirm_password(self, field):
    #     print('patekau i validation')
    #     """Custom validation logic for confirm_password."""
    #     # If password is set, confirm_password is required and must match
    #     if self.password.data and not field.data:
    #         raise ValidationError(
    #             'Confirm password is required when password is set.')

    #     # If both password and confirm_password are set, they must match
    #     if self.password.data and field.data != self.password.data:
    #         raise ValidationError('Confirm password must match the password.')

    # email = EmailField('Email', validators=[DataRequired(),
    #                                         Email(
    #                                             message='Please enter a valid email address'),
    #                                         email_unique])


# class PasswordForm(FlaskForm):
#     password = PasswordField('Password', validators=[
#         Optional(),
#         Length(min=8, message='Min 8 characters required'),
#         Regexp(
#             r'^(?=.*[A-Z])', message='Password must contain at least one uppercase letter'),
#         Regexp(r'^(?=.*[!@#$%^&*(),.?":{}|<>])',
#                message='Password must contain at least one special character')
#     ])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[
#                                          Optional(),
#                                          EqualTo(
#                                              'password', message='Passwords must match')
#                                      ])

#     def validate_confirm_password(self, field):
#         if self.password.data and not field.data:
#             raise ValidationError(
#                 'Confirm password is required when password is set.')

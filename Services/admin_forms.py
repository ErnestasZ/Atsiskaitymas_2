from Models import Loyalty
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_admin.contrib.sqla import ModelView
from wtforms import ValidationError, HiddenField
from Controllers import get_user
import re


def password_validator(form, password):

    import re
    
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must contain at least one special character.")

class UserView(ModelView):
    
    # column_list = ('first_name', 'last_name', 'country')  # Specify columns to display
    form_columns = (
        'first_name', 
        'last_name', 
        'email',
        'password',
        'is_admin',
        'token',
        'verified_at',
        'is_deleted',
        'loyalty'
        )  # Specify form fields
    # column_searchable_list = ('first_name', 'last_name')  # Enable search
    # column_filters = ('country',)  # Enable filtering by country


    form_overrides = {
        'loyalty': QuerySelectField,
        # 'verified_at': BooleanField
    }
    form_args = {
        'loyalty': {
            'query_factory': lambda: Loyalty.query.all(),
            'allow_blank': False,
            'get_label': 'name'
        }
    }

    def edit_form(self, obj=None):
        form = super().edit_form(obj)         
        form.password.render_kw = {'required': False}
        form.password.data = ""
        form.password.validators = []
        return form

    form_labels = {
        'first_name' : 'First name', 
        'last_name' : 'Last name', 
        'email' : 'Email',
        'password' : 'password',
        'is_admin' : 'Admin',
        'token' : 'Verification token',
        'verified_at' : 'Verified',
        'is_deleted' : 'Deleted',
        'loyalty' : 'Loyalty status'
    }
    
    def on_model_change(self, form, model, is_created):
        # Only set the password if a new one is entered
        if is_created:
            password_validator(form, form.password.data)
        else:
            if form.password.data:
                password_validator(form, form.password.data)
            else:
                model.password = 'asdasdasd'
                print(f"{model.password} <---------------------------")

class LoyaltyView(ModelView):
    # column_list = ('first_name', 'last_name', 'country')  # Specify columns to display
    form_columns = (
        'name', 
        'discount', 
        ) 
    # column_searchable_list = ('first_name', 'last_name')  # Enable search
    # column_filters = ('country',)  # Enable filtering by country
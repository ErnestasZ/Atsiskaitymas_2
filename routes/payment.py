from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import current_user
import Controllers.main_myaccount as myac
# import Controllers.dashboard as dash
# import Services.Forms.dashboard as forms
# from Misc.my_logger import my_logger
import json
import os
import stripe
import Services.Forms.user_form as us_forms

# from Services.forms import testas
payment = Blueprint('stripe_payment', __name__, url_prefix='/stripe-payment')

stripe.api_key = 'sk_test_51QMlQGAGst8Frj15bEPfIeV9Qf0kpbgxOj2fCicQSQm6PMXmbcRiYyo2rkpBFAM655BE11nshTdZ2AbUX16xWG0Q00hdlVocG3'


def calculate_order_amount(items):
    print(items)
    amount = items[0]['amount']
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return amount


def register_payment_routes(app, db):

    @payment.route('/create-payment-intent', methods=['POST'])
    def create_payment():
        try:
            data = json.loads(request.data)
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=calculate_order_amount(data['items']),
                currency='eur',
                # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            print(intent['id'])
            myac.add_balance_stripe(current_user.id, calculate_order_amount(
                data['items']), intent['id'])
            flash('Balance updated successfully.', 'main success')
            return jsonify({
                'clientSecret': intent['client_secret'],
                # [DEV]: For demo purposes only, you should avoid exposing the PaymentIntent ID in the client-side code.
                'dpmCheckerLink': 'https://dashboard.stripe.com/settings/payment_methods/review?transaction_id={}'.format(intent['id']),
            })
        except Exception as e:
            return jsonify(error=str(e)), 403

    @payment.route('/', methods=['GET', 'POST'])
    def checkout():

        balance = request.args.get('balance')
        if not balance or float(balance) < 1:
            return redirect(url_for('main.my_balance'))
        # form = us_forms.BalanceForm()
        # if form.validate_on_submit():
        #     # if request.method == 'POST':
        #     # Get the 'balance' value from the form
        #     # Use .get() to fetch the field value
        #     # balance = request.form.get('balance')
        #     print(f"Received balance: {form.balance.data}")

        return render_template('payment/checkout.html', balance=balance)

    @payment.route('/complete')
    def complete():
        return render_template('payment/complete.html')

    # register blueprint
    app.register_blueprint(payment)

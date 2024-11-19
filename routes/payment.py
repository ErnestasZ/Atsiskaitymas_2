from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
# import Controllers.dashboard as dash
# import Services.Forms.dashboard as forms
# from Misc.my_logger import my_logger
import json
import os
import stripe

# from Services.forms import testas
payment = Blueprint('stripe_payment', __name__, url_prefix='/stripe-payment')


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


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
            return jsonify({
                'clientSecret': intent['client_secret'],
                # [DEV]: For demo purposes only, you should avoid exposing the PaymentIntent ID in the client-side code.
                'dpmCheckerLink': 'https://dashboard.stripe.com/settings/payment_methods/review?transaction_id={}'.format(intent['id']),
            })
        except Exception as e:
            return jsonify(error=str(e)), 403

    @payment.route('/')
    def checkout():
        return render_template('payment/checkout.html')

    # register blueprint
    app.register_blueprint(payment)

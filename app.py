from flask import Flask, render_template, abort, request, url_for, Response
from dotenv import load_dotenv
import os
import json

from modern_treasury import ModernTreasury

# Load local .env file and assign org ID and key for auth
load_dotenv(verbose=True)

modern_treasury = ModernTreasury(
    # defaults to os.environ.get("MODERN_TREASURY_API_KEY")
    api_key=os.environ.get("MT_API_KEY"),
    organization_id=os.environ.get("MT_ORG_ID"),
)

app = Flask(__name__)
app.config.from_file("config.json", load=json.load)

@app.context_processor
def custom_values():
    return dict(
        company_name = app.config.get("COMPANY_NAME"),
        company_name_short = app.config.get("COMPANY_NAME_SHORT"),
        company_logo = app.config.get("COMPANY_LOGO"),
        username = app.config.get("USERNAME")
    )

@app.route('/')
@app.route('/index')
def index():

    return render_template('login.html')

@app.route('/login', methods= ['GET'])
def bain_login():
    
    return render_template('login.html', title="Login Page")


@app.route('/dashboard', methods= ['GET'])
def render_dashboard():

    return render_template('dashboard.html')


@app.route('/payments', methods= ['GET'])
def list_payments():

    #expected_payments = modern_treasury.expected_payments.list(type='wire', counterparty_id='036118f0-0e41-42e7-9f38-d14031ef1970', created_at_lower_bound= '2023-02-27')
    expected_payments = modern_treasury.expected_payments.list()
    payment_count = str(len(list(enumerate(expected_payments))))
    
    return render_template('payments.html', payment_count=payment_count, payments=expected_payments)

@app.route('/distributions')
def list_distributions():

    #payment_orders = modern_treasury.payment_orders.list(counterparty_id = '036118f0-0e41-42e7-9f38-d14031ef1970', effective_date_end='2023-03-01')
    payment_orders = modern_treasury.payment_orders.list()
    payment_count = str(len(list(enumerate(payment_orders))))
    
    return render_template ('distributions.html', payment_count=payment_count, payments=payment_orders)


# NON-ROUTE METHODS BELOW


# def create_payment_order(payload, org_id, api_key):
#     url = 'https://app.moderntreasury.com/api/payment_orders'
#     try:
#         resp = requests.post(url=url, auth=(org_id, api_key), json=payload)
#         return resp
#     except Exception as e:
#         print(e)
#         return "Call failed."


# def async_create_po(payload, org_id, api_key):
#     url = "https://app.moderntreasury.com/api/payment_orders/create_async"
#     try:
#         response = requests.post(url=url, auth=(org_id, api_key), json=payload)
#         return response
#     except Exception as e:
#         print(e)
#         return "Call failed."


# def create_po(payload, org_id, api_key):
#     url = "https://app.moderntreasury.com/api/payment_orders"
#     try:
#         response = requests.post(url=url, auth=(org_id, api_key), json=payload)
#         return response
#     except Exception as e:
#         print(e)
#         return "Call failed."


# def create_ep_from_form(payload, org_id, api_key):
#     url = 'https://app.moderntreasury.com/api/expected_payments'
#     try:
#         resp = requests.post(url=url, auth=(org_id, api_key), json=payload)
#         return resp
#     except Exception as e:
#         print(e)
#         return "Call failed."


# def create_va(payload, org_id, api_key):
#     url = "https://app.moderntreasury.com/api/virtual_accounts"
#     try:
#         resp = requests.post(url=url, auth=(org_id, api_key), json=payload)
#         return resp
#     except Exception as e:
#         print(e)
#         return "Call failed."


# def list_expected_payments(org_id, api_key, params=None):
#     url = 'https://app.moderntreasury.com/api/expected_payments'
#     try:
#         resp = requests.get(url, auth=(org_id, api_key), params=params)
#         return resp
#     except Exception as e:
#         print(e)
#         return "Call failed."


# def list_payment_orders(org_id, api_key, params=None):
#     url = 'https://app.moderntreasury.com/api/payment_orders'
#     try:
#         resp = requests.get(url, auth=(org_id, api_key), params=params)
#         return resp
#     except Exception as e:
#         print(e)
#         return "Call failed."


def dollars_to_cents(dollars):
    cents = float(dollars) * 100

    return int(cents)


if __name__ == "__main__":
    app.run()
from flask import Flask, render_template, abort, request, url_for, Response
from dotenv import load_dotenv
import os
import json

from modern_treasury import ModernTreasury

# Load local .env file and assign org ID and key for auth
load_dotenv(verbose=True)

modern_treasury = ModernTreasury(
    # defaults to os.environ.get("MODERN_TREASURY_API_KEY")
    api_key=os.environ.get("MY_API_KEY"),
    organization_id=os.environ.get("MY_ORG_ID"),
)

app = Flask(__name__)
app.config.from_file("config.json", load=json.load)

@app.context_processor
def custom_values():
    return dict(
        company_name = app.config.get("COMPANY_NAME"),
        company_name_short = app.config.get("COMPANY_NAME_SHORT"),
        company_logo = app.config.get("COMPANY_LOGO"),
        login_logo = app.config.get("LOGIN_LOGO"),
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

    expected_payments = modern_treasury.expected_payments.list(type='wire', created_at_lower_bound= '2023-05-09')
    # expected_payments = modern_treasury.expected_payments.list()
    payment_count = str(len(list(enumerate(expected_payments))))
    
    return render_template('payments.html', payment_count=payment_count, payments=expected_payments)

@app.route('/distributions')
def list_distributions():

    payment_orders = modern_treasury.payment_orders.list(type='wire', status='needs_approval', effective_date_start= '2023-04-12')
    # payment_orders = modern_treasury.payment_orders.list()
    payment_count = str(len(list(enumerate(payment_orders))))
    
    return render_template ('distributions.html', payment_count=payment_count, payments=payment_orders)


# NON-ROUTE METHODS BELOW

def dollars_to_cents(dollars):
    cents = float(dollars) * 100

    return int(cents)


if __name__ == "__main__":
    app.run()
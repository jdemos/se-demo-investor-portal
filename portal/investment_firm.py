from flask import Flask, render_template, abort, request, url_for, Response, session, redirect, Blueprint, current_app
from modern_treasury import ModernTreasury
from datetime import date, timedelta
import os
import json

bp = Blueprint('investment_firm', __name__) # url_prefix='/auth' prepends path to all URLs w/blueprint

modern_treasury = ModernTreasury(
    # defaults to os.environ.get("MODERN_TREASURY_API_KEY")
    api_key=os.environ.get("KKMT_API_KEY"),
    organization_id=os.environ.get("KKMT_ORG_ID"),
)

LOWER_DATE_FILTER = date.today() - timedelta(14)

@bp.route('/dashboard', methods= ['GET'])
def render_dashboard():

    return render_template('dashboard.html')


@bp.route('/payments', methods= ['GET'])
def list_payments():

    expected_payments = modern_treasury.expected_payments.list(type='wire', created_at_lower_bound= LOWER_DATE_FILTER)
    # expected_payments = modern_treasury.expected_payments.list()
    payment_count = str(len(list(enumerate(expected_payments))))
    
    return render_template('payments.html', payment_count=payment_count, payments=expected_payments)

@bp.route('/distributions')
def list_distributions():

    payment_orders = modern_treasury.payment_orders.list(type='wire', effective_date_start=LOWER_DATE_FILTER)
    # payment_orders = modern_treasury.payment_orders.list()
    payment_count = str(len(list(enumerate(payment_orders))))
    
    return render_template ('distributions.html', payment_count=payment_count, payments=payment_orders)
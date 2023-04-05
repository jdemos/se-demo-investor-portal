from flask import Flask, render_template, abort, request, url_for, Response, session, redirect, Blueprint
from modern_treasury import AsyncModernTreasury
import os
import json


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import investment_firm

    app.register_blueprint(investment_firm.bp)

    app.config.from_file('config.json', load=json.load)

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
        
        return redirect('/login')

    @app.route('/login', methods= ['GET'])
    def bain_login():
        
        return render_template('login.html', title="Login Page")

    return app
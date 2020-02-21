#src/app.py

from flask import Flask, render_template, redirect, url_for

from .config import app_config
from .models import db, bcrypt
from .views.UserView import user_api as user_blueprint
from .views.SalesView import sales_api as sale_blueprint
from .views.OrdersView import order_api as order_blueprint
from flask_cors import CORS
from flask_bootstrap import Bootstrap

def create_app(env_name):

    # app initiliazation
    app = Flask(__name__)
    #app.config.from_object(app_config[env_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://User01:777@localhost/food_delivery'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # initializing bcrypt
    bcrypt.init_app(app)  # add this linese

    db.init_app(app)  # add this line
    Bootstrap(app)


    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users') # add this line
    app.register_blueprint(sale_blueprint, url_prefix='/api/v1/sales')
    app.register_blueprint(order_blueprint, url_prefix='/api/v1/orders')

    @app.route('/', methods=['GET'])
    def index():

        return render_template('index.html')

    @app.route('/sales', methods=['GET'])
    def sales():
        return render_template('sales.html')
    @app.route('/users', methods=['GET'])
    def login():
      return render_template('login.html')

    @app.route('/orders', methods=['GET'])
    def orders():
        return render_template('Orders.html')


    return app

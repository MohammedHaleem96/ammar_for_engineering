from flask import Flask, render_template, request,Blueprint
from app.models.products import Product, Inverter, Battery, Panel,ProductType

from app import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def index():

    return render_template('user/index.html')

@user_bp.route('/about')
def about():
    return render_template('user/about.html')

@user_bp.route('/services')
def services():
    return render_template('user/services.html')

@user_bp.route('/completed-projects')
def completed_projects():
    return render_template('user/completed_projects.html')

@user_bp.route('/products')
def products():
    product_types = ProductType.query.options(db.joinedload(ProductType.products)).all()

    return render_template('user/products.html',product_types=product_types)





@user_bp.route('/batteries')
def batteries():
    return render_template('batteries.html')

@user_bp.route('/solar_panels')
def solar_panels():
    return render_template('solar_panels.html')

@user_bp.route('/lamps')
def lamps():
    return render_template('lamps.html')

@user_bp.route('/electric_equipment')
def electric_equipment():
    return render_template('electric_equipment.html')

@user_bp.route('/additional')
def additional():
    return render_template('additional.html')
@user_bp.route('/inverters')
def inverters():
    # Placeholder for inverter prices; these should be fetched from the server or database.
    inverter_prices = {
        "1_kw": 1000,  # Replace with dynamic value from server
        "3_kw": 3000,  # Replace with dynamic value from server
        "5.2_kw": 5200  # Replace with dynamic value from server
    }
    return render_template('inverters.html', inverter_prices=inverter_prices)

@user_bp.route('/x_inverters')
def x_inverters():
    return render_template('x_inverters.html')


from flask import Flask, render_template, request,Blueprint
from app.models.products import Product, Inverter, Battery, Panel,ProductType
from app.models.AccomplishedProject import AccomplishedProject


from app import db

user_bp = Blueprint('user', __name__)



# Example project data for Sudan
PROJECT_DATA = [
    {"location": "Khartoum", "lat": 15.5007, "lng": 32.5599, "projects": 50},
    {"location": "Port Sudan", "lat": 19.6158, "lng": 37.2153, "projects": 30},
    {"location": "Omdurman", "lat": 15.6445, "lng": 32.4777, "projects": 40},
    {"location": "El Obeid", "lat": 13.1833, "lng": 30.2167, "projects": 20},
    {"location": "Kassala", "lat": 15.4500, "lng": 36.4000, "projects": 25},
]



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
    projects = AccomplishedProject.query.all()

    return render_template('user/accomplished_projects.html',projects = projects)

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


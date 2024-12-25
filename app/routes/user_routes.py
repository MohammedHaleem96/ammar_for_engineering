from flask import Flask, render_template, request,Blueprint
from app.models.products import Product, Inverter, Battery, Panel,ProductType
from app.models.AccomplishedProject import AccomplishedProject
from app.models.ourSevices import Service
from math import ceil


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
    services = Service.query.all()
    return render_template('user/services.html', services=services ,title="خدماتنا")

@user_bp.route('/completed-projects')
def completed_projects():
    projects = AccomplishedProject.query.all()

    return render_template('user/projects.html',projects = projects)

@user_bp.route('/products')
def products():
    product_types = ProductType.query.options(db.joinedload(ProductType.products)).all()

    return render_template('user/products.html',product_types=product_types)





@user_bp.route('/estimate_system', methods=['GET', 'POST'])
def estimate_system():
    if request.method == 'POST':
        is_electricity_available    = request.form['is_electricity_available']=="yes"
        if is_electricity_available ==True:
            is_want_panels              = request.form['is_want_panels']=="yes" 
        else:
            is_want_panels = True

        electricity_available_hours = int(request.form.get('electricity_available_hours', default=0.0))
        total_hours_needed          = int(request.form.get('total_hours_needed',default=0.0))
        total_load                  = int(request.form.get('total_load',default=0.0))
        number_of_rooms                  = int(request.form.get('number_of_rooms',default=0.0))

        # Call the system prediction function
        result = get_systems(
            total_load,
            electricity_available_hours,
            total_hours_needed,
            is_want_panels,
            is_electricity_available,
            number_of_rooms
        )
        
        return  render_template('user/estimate_result.html',
                        systems=result)

    return render_template('user/estimate_form.html')





def get_systems(total_load, electricity_available_hours, total_hours_needed,
                 is_want_panels, is_electricity_available, number_of_rooms):

    # Constants
    charging_efficiency = 0.9
    battery_discharge_depth = 0.8
    installation_cost_percentage = 0.15
    total_capacity_available = 23
    inverter_capacity = total_load * 1.25  # Adding a safety margin

    inverters_systems = {}
    inverters_ids = get_inverters_above_n_wattage(inverter_capacity)
    batteries_ids = get_c_batteries(0)

    for  id in inverters_ids:
        product_inverter , inverter = get_product(id, 'inverter')
        system_voltage = int(inverter.system_voltage )
        number_of_batteries = int(system_voltage / 12)
        inverter_price = int(product_inverter.price)
        for bid in batteries_ids:
            product_battery , battery = get_product(bid, 'battery')
            battery_price = int(product_battery.price)
            battery_capacity = int(battery.capacity)
            batteries_price = int(battery_price * number_of_batteries)
            total_capacity_available = int(battery_capacity* system_voltage)
            load_75_watage = total_load * .75
            load_50_watage = total_load * .50
            load_25_watage = total_load * .25
            inverters_systems[f'sys_{id}'] = {"inverter_name":product_inverter.name,
                                          "inverter_cost":inverter_price,
                                          "number_of_battery":number_of_batteries,
                                           "cost_of_batteries":batteries_price ,
                                           "total_capacity": total_capacity_available,
                                           "is_with_panel":is_want_panels,
                                           "system_total_cost":inverter_price + batteries_price ,
                                           "load_100_time":convert_to_hours_and_minutes(total_capacity_available/total_load),
                                            "load_100_watage":total_load,
                                           "load_75_time":convert_to_hours_and_minutes(total_capacity_available/load_75_watage),
                                            "load_75_watage":load_75_watage,
                                            "load_50_time":convert_to_hours_and_minutes(total_capacity_available/load_50_watage),
                                             "load_50_watage":load_50_watage,
                                            "load_25_time":convert_to_hours_and_minutes(total_capacity_available/load_25_watage),
                                            "load_25_watage":load_25_watage,
                                            'is_electricity_available':is_electricity_available,
                                            "electricity_available_hours":electricity_available_hours,
                                            "total_hours_needed":total_hours_needed,
                                            "number_of_rooms":number_of_rooms,
                                          }
    return inverters_systems


    





def get_inverters_above_n_wattage(n):
    # Query the Inverter table where power_rating > n
    inverters = db.session.query(Product.id).join(Inverter).filter(Inverter.power_rating >= n).all()
    # Return the list of product IDs
    return [inverter.id for inverter in inverters]

def get_c_batteries(c):
    # Query the battery table where capacity c
    batteries = db.session.query(Product.id).join(Battery).filter(Battery.capacity >= c).all()
    # Return the list of product IDs
    return [battery.id for battery in batteries]


# Function to get the cost of an inverter
def get_product(product_id, product_type):
    # Fetch the product using the product_id
    product = Product.query.get(product_id)

    # Ensure the product exists and is of type 
    if product and product.type.name == product_type:
        # Access the inverter related to the product
        if product_type == 'inverter':
            inverter = product.product_inverter
            if inverter:
                # Return the price of the product (inverter cost)
                return product, inverter
            
        if product_type == 'battery':
            battery = product.product_battery
            if battery:
                # Return the price of the product (inverter cost)
                return product , battery
            
        if product_type == 'panel':
            panel = product.product_panel
            if panel:
                # Return the price of the product (inverter cost)
                return product, panel
            
        if product_type == 'wire':
            wire = product.product_wire
            if wire:
                # Return the price of the product (inverter cost)
                return product, wire
            
        if product_type == 'solar lamp':
            solarLamp = product.solar_lamp
            if solarLamp:
                # Return the price of the product (inverter cost)
                return product, solarLamp
                          
        else:
            return "product not found for this product."
    else:
        return "Product is not an products or does not exist."
    
    

@user_bp.route('test')
def test():
    ids = get_inverters_above_n_wattage(500)
    bids = get_c_batteries(200)

    for id in ids :
        inverter,k = get_product(id,'inverter')
    for id in bids :
        battery ,b= get_product(id,'battery')
        print(battery.model + " " + str(b.capacity))



    return f"inverter price: {inverter} \n batteries price "

def convert_to_hours_and_minutes(decimal_hours):
    """
    Convert a decimal number representing hours into hours and minutes.

    Args:
        decimal_hours (float): A number representing hours (e.g., 2.5 for 2 hours and 30 minutes).
    
    Returns:
        str: A formatted string showing hours and minutes (e.g., "2 hours, 30 minutes").
    """
    hours = int(decimal_hours)  # Extract the whole number part for hours
    minutes = round((decimal_hours - hours) * 60)  # Convert the fractional part to minutes
    return f"{hours} hours, {minutes} minutes"

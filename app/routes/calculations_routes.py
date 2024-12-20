from app.models.products import Product, Inverter, Battery, Panel,ProductType
from flask import Flask, render_template, request,Blueprint
from app import db

calc_bp = Blueprint('calc', __name__)

# Example pricing and system specifications
SYSTEMS = {
    "1kw": {"cost":   300+600+50, "battery_count": 1, "panel_capacity": 1000,"Charging_current": 80,},
    "3kw": {"cost":   500+600*2+50, "battery_count": 2, "panel_capacity": 3000,"Charging_current": 100,},
    "5.2kw": {"cost": 900+600*4+50, "battery_count": 4, "panel_capacity": 6000,"Charging_current": 120,},
}
def get_systems(total_load, electricity_available_hours, total_hours_needed, is_want_panels, is_electricity_available, number_of_rooms):
    # Query the database for product types, specifically for inverters and batteries
    # product_types = ProductType.query.options(db.joinedload(ProductType.products)).all()
    # inverters = Inverter.query.filter(Inverter.power_rating >= total_load).all()
    # batteries = Battery.query.filter(Battery.capacity == 200).all()

  
    # inverter = None
    # battery = None

    # # Loop through the product types and find inverter and battery products
    # for product_type in product_types:
    #     if product_type.name.lower() == 'inverter':
    #         inverter = product_type.products[0].inverter  # Get the first inverter associated with this product
    #     elif product_type.name.lower() == 'battery':
    #         battery = product_type.products[0].battery  # Get the first battery associated with this product

    # # If inverter or battery is not found in the database, return an error message
    # if not inverter or not battery:
    #     return 'Inverter or Battery not found in the database'
    inverters = Inverter.query.filter(Inverter.power_rating >= total_load).all()
    bateries = Battery.query.filter(Battery.capacity == 200).all()

    # Logic to calculate the system size based on total_load
    if total_load < 1000:
        inverter = inverters[0]
        battery = bateries[0]
        totla_cost = inverter.product.price + battery.product.price * inverter.system_voltage / 12
        print( battery.product.price)

    elif total_load >= 1000 and total_load < 3000:
        inverter = inverters[0]
        print(  inverter.product.price)
    elif total_load >= 3000 and total_load < 5200:
        inverter = inverters[0]
        print( inverter.product.price)
    # Returning the total cost of the system (sum of inverter and battery costs)
    return inverter.product.price


@calc_bp.route('/suitable-system')
def suitable_system():
    return render_template('user/suitable_system.html',
                           cost= SYSTEMS)


@calc_bp.route('/system_result', methods=['GET', 'POST'])
def estimate_system():
    if request.method == 'POST':
        # Get data from form
        is_electricity_available    = request.form['is_electricity_available']=="yes"
        if is_electricity_available ==True:
            is_want_panels              = request.form['is_want_panels']=="yes" 
        else:
            is_want_panels = True

        electricity_available_hours = int(request.form.get('electricity_available_hours', default=0.0))
        total_hours_needed          = int(request.form.get('total_hours_needed',default=0.0))
        total_load                  = int(request.form.get('total_load',default=0.0))
        number_of_rooms                  = int(request.form.get('number_of_rooms',default=0.0))


        # Calculate costs and requirements
        total_cost = get_systems(total_load, electricity_available_hours, total_hours_needed, is_want_panels, is_electricity_available,number_of_rooms)
        #inverter_cost, batteries_cost, installation_cost = get_inverter(total_load, total_hours_needed)

        # Calculate additional installation, accessories, and total costs here
        #total_cost = inverter_cost 

        return render_template('user/estimate_result.html', 
                               total_cost=total_cost,
                               is_electricity_available=is_electricity_available,
                               electricity_available_hours=electricity_available_hours,
                               is_want_panels=is_want_panels,
                               total_hours_needed=total_hours_needed,
                               total_load=total_load
                               )

    return render_template('estimate_form.html')



from flask import Flask, render_template, request,Blueprint

calc_bp = Blueprint('calc', __name__)

# Example pricing and system specifications
SYSTEMS = {
    "1kw": {"cost":   300+600+50, "battery_count": 1, "panel_capacity": 1000,"Charging_current": 80,},
    "3kw": {"cost":   500+600*2+50, "battery_count": 2, "panel_capacity": 3000,"Charging_current": 100,},
    "5.2kw": {"cost": 900+600*4+50, "battery_count": 4, "panel_capacity": 6000,"Charging_current": 120,},
}

def get_system(total_load, electricity_available_hours, total_hours_needed, is_want_panels, is_electricity_available):
    if total_load < 1000:
        system_size = SYSTEMS['1kw']
    elif total_load >= 1000 and total_load < 3000:
        system_size = SYSTEMS['3kw']
    elif total_load >= 3000 and total_load < 5200:
        system_size = SYSTEMS['5.2kw']
    elif total_load > 5200:
        return 'استشر مهندسينا'
    battary_charge_time = 200 / system_size['Charging_current'] 
    System_total_capacity =  system_size['battery_count']*12*200
    system_total_hours_available= (System_total_capacity / total_load)*0.9
    return system_size["cost"]

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
        total_hours_needed          = request.form.get('total_hours_needed',default=0.0)
        total_load                  = int(request.form.get('total_load',default=0.0))

        # Calculate costs and requirements
        total_cost = get_system(total_load, electricity_available_hours, total_hours_needed, is_want_panels, is_electricity_available)
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


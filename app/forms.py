from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    brand = StringField('Brand', validators=[Optional()])
    price = DecimalField('Price', places=2, validators=[Optional()])
    product_type_id = SelectField('Product Type', coerce=int, validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[Optional()])

class InverterForm(FlaskForm):
    power_rating = DecimalField('Power Rating (W)', places=2, validators=[Optional()])
    battery_count = DecimalField('Battery Count', places=2, validators=[Optional()])
    max_pv_voltage = DecimalField('Max PV Voltage (V)', places=2, validators=[Optional()])
    min_pv_voltage = DecimalField('Min PV Voltage (V)', places=2, validators=[Optional()])
    max_pv_current = DecimalField('Max PV Current (A)', places=2, validators=[Optional()])
    min_pv_current = DecimalField('Min PV Current (A)', places=2, validators=[Optional()])
    mppt_voltage_min = DecimalField('MPPT Voltage Min (V)', places=2, validators=[Optional()])
    mppt_voltage_max = DecimalField('MPPT Voltage Max (V)', places=2, validators=[Optional()])
    charging_current = DecimalField('Charging Current (A)', places=2, validators=[Optional()])
    max_pv_power = DecimalField('Max PV Power (W)', places=2, validators=[Optional()])

class BatteryForm(FlaskForm):
    capacity = DecimalField('Capacity (Ah/Wh)', places=2, validators=[Optional()])
    voltage = DecimalField('Voltage (V)', places=2, validators=[Optional()])
    battery_type = StringField('Battery Type', validators=[Optional()])
    cycle_number = DecimalField('Cycle Number', places=2, validators=[Optional()])

class PanelForm(FlaskForm):
    wattage = DecimalField('Wattage (W)', places=2, validators=[Optional()])
    efficiency = DecimalField('Efficiency (%)', places=2, validators=[Optional()])
    width = DecimalField('Width (cm)', places=2, validators=[Optional()])
    length = DecimalField('Length (cm)', places=2, validators=[Optional()])
    Voc = DecimalField('Open Circuit Voltage (V)', places=2, validators=[Optional()])
    Vmp = DecimalField('Maximum Power Voltage (V)', places=2, validators=[Optional()])
    Isc = DecimalField('Short-Circuit Current (A)', places=2, validators=[Optional()])
    Imp = DecimalField('Maximum Power Current (A)', places=2, validators=[Optional()])
    brand = StringField('Brand', validators=[Optional()])
    dimension = StringField('Dimensions (cm)', validators=[Optional()])

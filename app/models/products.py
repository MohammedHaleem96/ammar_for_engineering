from app import db



class ProductType(db.Model):
    __tablename__ = 'product_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    products = db.relationship('Product', backref='type', lazy=True)




# Base Product Model
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    brand = db.Column(db.Text, nullable=True)
    model = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    image_url = db.Column(db.Text, nullable=True) 
    
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'), nullable=False)
    product_type = db.relationship('ProductType', backref=db.backref('product_list', lazy=True))


    # Add cascade behavior to delete associated objects (e.g., Inverters, Batteries)
    product_inverter = db.relationship('Inverter', backref=db.backref('product_inverter'), cascade="all, delete-orphan", uselist=False)
    product_battery = db.relationship('Battery', backref=db.backref('product_batttery'), cascade="all, delete-orphan", uselist=False )
    product_panel = db.relationship('Panel', backref=db.backref('product_panel'), cascade="all, delete-orphan", uselist=False )


# Inverter Model (specific to inverters)
"""Features:
Cold start function.
Support USB, RS485 Monitoring Function (WiFi Monitoring USB Plug)
Pure sine wave inverter.
Built-in MPPT solar charge controller.
Overload and short circuit protection.
Compatible with mains voltage or generator power.
Selectable charging current based on applications.
Configurable AC/Solar input priority via LCD setting.
Smart battery charger design for optimized battery performance.
Built-in MPPT Solar and Battery Charger
Selectable input voltage range for home appliances and personal computers.
Supports parallel operation up to 3 units
Technical specifications:
Model: PV18-5048VHM
Rated Power: 5000VA/5000W.
Warranty: 24 months (view warranty)
Input 
Voltage: 230VAC.
Selectable Voltage Range: 170-280VAC(UPS)  90-280VAC (APL).
Frequency Range: 50Hz/60Hz(Auto sensing).
Output
AC Voltage Regulation: 220VAC-230VAC (Setting) 
Surge Power: 10000VA.
Efficiency(Peak): 90%-93%.
Transfer Time: 10 ms (For Personal Computers) 20 ms (For Home Appliances).
Waveform: Pure sine wave.
Battery and AC Charger 
Battery Voltage: 48VDC.
Floating Charge Voltage: 54.8VDC.
Overcharge Protection: 60VDC.
Solar Charger
Maximum PV Array Power: 4000W.
MPPT Range @ Operating Voltage: 60VDC – 130VDC.
Maximum PV Array Open Circuit Voltage: 145VDC.
Maximum Solar Charge Current: 80A.
Maximum AC Charge Current: 60A.
Maximum Charge Current: 140A.
Physical
Dimesion: 66cm x 41cm x 25cm.
Weight: 18kg.
Operating Environment
Humidity: 5% to 95% Relative Humidity(Non-condensing).
Operating Temperature: -0°C – 50°C.
Storage Temperature: -15°C – 60°C.
 
 """
class Inverter(db.Model):
    __tablename__ = 'inverters'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    power_rating = db.Column(db.Numeric(10, 2))  
    system_voltage = db.Column(db.Numeric(10, 2)) 

    max_pv_voltage = db.Column(db.Numeric(10, 2)) 
    min_pv_voltage = db.Column(db.Numeric(10, 2)) 

    max_pv_current= db.Column(db.Numeric(10, 2))
    min_pv_current = db.Column(db.Numeric(10, 2))

    mppt_voltage_min = db.Column(db.Numeric(10, 2))
    mppt_voltage_max = db.Column(db.Numeric(10, 2))


    ac_max_charging_current = db.Column(db.Numeric(10, 2))
    pv_max_charging_current = db.Column(db.Numeric(10, 2))
    max_charging_current = db.Column(db.Numeric(10, 2))


    max_pv_power     = db.Column(db.Numeric(10, 2))

    product = db.relationship('Product', backref='inverter', uselist=False)

# Battery Model (specific to batteries)
class Battery(db.Model):
    __tablename__ = 'batteries'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    capacity = db.Column(db.Numeric(10, 2))  # e.g., battery capacity in Ah or Wh
    voltage = db.Column(db.Numeric(10, 2))
    battery_type = db.Column(db.String(255))
    cycle_number = db.Column(db.Numeric(10, 2))

    product = db.relationship('Product', backref='battery', uselist=False)

# Panel Model (specific to panels)
class Panel(db.Model):
    __tablename__ = 'panels'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    wattage = db.Column(db.Numeric(10, 2))  # Panel wattage

    width = db.Column(db.Numeric(5, 2))  # width
    length = db.Column(db.Numeric(5, 2))  # length
    thickness =db.Column(db.Numeric(5, 2))  # length 

    Voc = db.Column(db.Numeric(5, 2))  # open circuit voltage
    Vmp = db.Column(db.Numeric(5, 2))  # 
    Isc = db.Column(db.Numeric(5, 2))  # 
    Imp = db.Column(db.Numeric(5, 2))  # len
    alpha = db.Column(db.Numeric(5, 2))  # temp coefiecient

    product = db.relationship('Product', backref='panel', uselist=False)

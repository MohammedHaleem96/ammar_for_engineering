from app import db


# Base Product Model
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    brand = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    image_url = db.Column(db.Text, nullable=True) 
    
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'), nullable=False)
    product_type = db.relationship('ProductType', backref=db.backref('product_list', lazy=True))

# Inverter Model (specific to inverters)
class Inverter(db.Model):
    __tablename__ = 'inverters'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    power_rating = db.Column(db.Numeric(10, 2))  # e.g., power rating in watts
    battery_count = db.Column(db.Numeric(10, 2)) 

    max_pv_voltage = db.Column(db.Numeric(10, 2)) 
    min_pv_voltage = db.Column(db.Numeric(10, 2)) 

    max_pv_current= db.Column(db.Numeric(10, 2))
    min_pv_current = db.Column(db.Numeric(10, 2))

    mppt_voltage_min = db.Column(db.Numeric(10, 2))
    mppt_voltage_max = db.Column(db.Numeric(10, 2))


    charging_current = db.Column(db.Numeric(10, 2))
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
    efficiency = db.Column(db.Numeric(5, 2))  # Efficiency percentage

    width = db.Column(db.Numeric(5, 2))  # width
    length = db.Column(db.Numeric(5, 2))  # length

    Voc = db.Column(db.Numeric(5, 2))  # open circuit voltage
    Vmp = db.Column(db.Numeric(5, 2))  # 
    Isc = db.Column(db.Numeric(5, 2))  # 
    Imp = db.Column(db.Numeric(5, 2))  # len

    brand = db.Column(db.String(255))  # brand
    dimension = db.Column(db.String(255))  # Panel dimensions

    product = db.relationship('Product', backref='panel', uselist=False)

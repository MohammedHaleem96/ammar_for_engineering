from app import db


# ProductType: Defines the types of products (e.g., inverter, battery, etc.)
class ProductType(db.Model):
    __tablename__ = 'product_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)  # Ensures each type name is unique
    description = db.Column(db.Text, nullable=True)  # Additional details about the product type

    # One-to-Many relationship with Product
    products = db.relationship('Product', backref='type', lazy=True)

    def __repr__(self):
        return f"<ProductType(id={self.id}, name='{self.name}')>"


# Base Product Model: Represents general products in the system
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # Name of the product
    description = db.Column(db.Text, nullable=True)  # Optional detailed description
    brand = db.Column(db.String(255), nullable=False)  # Brand information
    model = db.Column(db.String(255), nullable=False)  # Model information
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Price with precision up to 2 decimal places
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Auto-set timestamp
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # Updates on changes
    image_url = db.Column(db.Text, nullable=True)  # URL for product image

    # Foreign key linking to the ProductType table
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_types.id'), nullable=False)

    # Relationships with specific product types (e.g., inverters, batteries, etc.)
    product_inverter = db.relationship('Inverter', backref='product_inverter', cascade="all, delete-orphan", uselist=False)
    product_battery = db.relationship('Battery', backref='product_battery', cascade="all, delete-orphan", uselist=False)
    product_panel = db.relationship('Panel', backref='product_panel', cascade="all, delete-orphan", uselist=False)
    product_wire = db.relationship('Wire', backref='product_wire', cascade="all, delete-orphan", uselist=False)
    product_breaker = db.relationship('Breaker', backref='product_breaker', cascade="all, delete-orphan", uselist=False)
    product_solar_lamp = db.relationship('SolarLamp', backref='product_solar_lamp', cascade="all, delete-orphan", uselist=False)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', brand='{self.brand}', model='{self.model}')>"


# Inverter Model: Represents inverters with specific attributes
class Inverter(db.Model):
    __tablename__ = 'inverters'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)  # Product ID is the primary key
    inverter_type = db.Column(db.String(255), nullable=False)  # Type of inverter
    power_rating = db.Column(db.Numeric(10, 2), nullable=False)  # Power rating in Watts or kW
    system_voltage = db.Column(db.Numeric(10, 2), nullable=False)  # System voltage

    max_pv_voltage = db.Column(db.Numeric(10, 2), nullable=False)  # Maximum photovoltaic voltage
    min_pv_voltage = db.Column(db.Numeric(10, 2), nullable=False)  # Minimum photovoltaic voltage

    max_pv_current = db.Column(db.Numeric(10, 2), nullable=False)  # Maximum current from PV
    min_pv_current = db.Column(db.Numeric(10, 2), nullable=False)  # Minimum current from PV

    mppt_voltage_min = db.Column(db.Numeric(10, 2), nullable=False)  # Minimum MPPT voltage
    mppt_voltage_max = db.Column(db.Numeric(10, 2), nullable=False)  # Maximum MPPT voltage

    ac_max_charging_current = db.Column(db.Numeric(10, 2), nullable=False)  # Max AC charging current
    pv_max_charging_current = db.Column(db.Numeric(10, 2), nullable=False)  # Max PV charging current
    max_charging_current = db.Column(db.Numeric(10, 2), nullable=False)  # Overall maximum charging current

    max_pv_power = db.Column(db.Numeric(10, 2), nullable=False)  # Maximum PV power

    # Relationship back to the product
    product = db.relationship('Product', backref='inverter', uselist=False)


# Battery Model: Represents batteries with specific attributes
class Battery(db.Model):
    __tablename__ = 'batteries'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    capacity = db.Column(db.Numeric(10, 2), nullable=False)  # Capacity (e.g., in Ah or Wh)
    voltage = db.Column(db.Numeric(10, 2), nullable=False)  # Voltage
    battery_type = db.Column(db.String(255), nullable=False)  # Type of battery (e.g., Li-ion, Lead Acid)
    cycle_number = db.Column(db.Numeric(10, 2), nullable=False)  # Number of charge cycles

    product = db.relationship('Product', backref='battery', uselist=False)


# Panel Model: Represents solar panels with specific attributes
class Panel(db.Model):
    __tablename__ = 'panels'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    wattage = db.Column(db.Numeric(10, 2), nullable=False)  # Panel wattage
    width = db.Column(db.Numeric(5, 2), nullable=False)  # Width in meters or inches
    length = db.Column(db.Numeric(5, 2), nullable=False)  # Length
    thickness = db.Column(db.Numeric(5, 2), nullable=False)  # Thickness

    Voc = db.Column(db.Numeric(5, 2), nullable=False)  # Open circuit voltage
    Vmp = db.Column(db.Numeric(5, 2), nullable=False)  # Maximum power voltage
    Isc = db.Column(db.Numeric(5, 2), nullable=False)  # Short circuit current
    Imp = db.Column(db.Numeric(5, 2), nullable=False)  # Maximum power current
    alpha = db.Column(db.Numeric(5, 2), nullable=False)  # Temperature coefficient

    product = db.relationship('Product', backref='panel', uselist=False)


# Wire Model: Represents wires with specific attributes
class Wire(db.Model):
    __tablename__ = 'wires'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    size = db.Column(db.Numeric(10, 2), nullable=False)  # Size (e.g., in mm²)
    length = db.Column(db.Numeric(5, 2), nullable=False)  # Length of the wire
    wire_gauge = db.Column(db.Numeric(5, 2))  # Gauge (e.g., AWG)

    product = db.relationship('Product', backref='wire', uselist=False)


# Breaker Model: Represents breakers with specific attributes
class Breaker(db.Model):
    __tablename__ = 'breakers'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    rated_current = db.Column(db.Numeric(10, 2), nullable=False)  # Rated current in Amps
    rated_voltage = db.Column(db.Numeric(5, 2), nullable=False)  # Rated voltage
    poles = db.Column(db.Numeric(5, 2), nullable=False)  # Number of poles
    category = db.Column(db.String(255), nullable=False)  # AC or DC breaker

    product = db.relationship('Product', backref='breaker', uselist=False)


# SolarLamp Model: Represents solar lamps with specific attributes
class SolarLamp(db.Model):
    __tablename__ = 'solar_lamps'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    solar_panel_capacity = db.Column(db.Numeric(10, 2), nullable=False)  # Solar panel capacity (in Watts)
    operation_time = db.Column(db.Numeric(5, 2), nullable=False)  # Operation time (in hours)
    lamp_power = db.Column(db.Numeric(5, 2), nullable=False)  # Lamp power (in Watts)

    product = db.relationship('Product', backref='solar_lamp', uselist=False)

from flask import Flask, render_template, request, Blueprint, redirect, url_for, flash
#from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#from app.models.products import Product, Inverter, Battery, Panel
from app.models.product_types import ProductType
#from app.forms import ProductForm, InverterForm, BatteryForm, PanelForm
from app.models.admins import Admin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


from app import db

# Initialize Blueprint for admin
admin_bp = Blueprint('admin', __name__)



@admin_bp.route('/')
def index():
    return render_template('admin/login_form.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('admin.dashboard'))
        print("post detected")
        '''
        username = request.form.get('username')
        password = request.form.get('password')

        # Find the admin by username
        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password_hash, password):
            # Successful login
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))  # Redirect to dashboard after login 
        
        else:
            # Failed login
            redirect(url_for('admin.index'))
            flash('Login failed. Check your username and/or password.', 'error')
            '''
    else:
        print("no post")
        return "what is this "
    
    return render_template('admin/login_form.html')

@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('/products')
def products():
    return render_template('admin/product_management_form.html')

@admin_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_type = request.form['productType']
        if product_type == 'inverter':
            inverter_model = request.form.get('inverter_model')
            inverter_power = request.form.get('inverter_power')
            inverter_max_pv_voltage = request.form.get('inverter_max_pv_voltage')
            inverter_min_pv_voltage = request.form.get('inverter_min_pv_voltage')
            inverter_brand = request.form.get('inverter_brand')
            inverter_price = request.form.get('inverter_price')
            inverter_image= request.form.get('inverter_image')
        elif product_type == 'battery':
            battery_capacity = request.form.get('battery_capacity')
            battery_cost = request.form.get('battery_cost')
            battery_brand = request.form.get('battery_brand')


    else:
        print("oh no")
    return render_template('admin/product_management_form.html')


@admin_bp.route('/signout')
def signout():
    return render_template('admin/login_form.html')


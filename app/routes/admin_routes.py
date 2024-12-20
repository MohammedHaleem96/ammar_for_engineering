from flask import Flask, render_template, request, Blueprint, redirect, url_for, flash,jsonify, current_app
#from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from app.models.products import Product, Inverter, Battery, Panel,ProductType
#from app.forms import ProductForm, InverterForm, BatteryForm, PanelForm
from app.models.admins import Admin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


from app import db

# Initialize Blueprint for admin
admin_bp = Blueprint('admin', __name__)



UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_PANNER_EXTENSIONS= {'png', 'jpg', 'jpeg', 'gif','pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

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
    try:
        # Query all product types with their products
        product_types = ProductType.query.options(db.joinedload(ProductType.products)).all()
        # Pass the product types to the template
        return render_template('admin/products.html', product_types=product_types)

    except Exception as e:
        return {"error": str(e)}, 500
    
@admin_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_type_name = request.form['productType'].lower()

        if product_type_name == "chose_product":
            flash('You must select a product type.', 'error')
            return "you should chose a type" # Redirect to form
        product_type_name = request.form['productType'].lower()
        product_description = request.form.get('description')
        product_name= request.form.get('name')
        product_brand = request.form.get('brand')
        product_price = request.form.get('price')
        product_model = request.form.get('model')
        product_image= request.files.get("image")        
        # Create A producttype of not existed 
        product_type = ProductType.query.filter_by(name=product_type_name).first()
        print(product_type)
        if not product_type:
            print("herer")
            new_type = ProductType(name = product_type_name )
            db.session.add(new_type)
            db.session.commit()  # Flush to get product_type ID before committing
        product_type = ProductType.query.filter_by(name=product_type_name).first()

        image_url = None
        if product_image and allowed_file(product_image.filename):
            filename = f"{product_name.replace(' ', '_')}-{product_image.filename}"
            image_path = os.path.join(UPLOAD_FOLDER+f"/{product_type_name}", filename)
            if not os.path.exists(UPLOAD_FOLDER+f"/{product_type_name}"):
                os.makedirs(UPLOAD_FOLDER+f"/{product_type_name}")             
            product_image.save(image_path)
            image_url = f"uploads/{product_type_name}/{filename}"

        #if there are image and it is in the right existension 

        print(image_url)
        #add_product_to_database(product_type_name,product_name,product_brand,product_price,file_path,product_type)
        product = Product(
        name= product_name ,
        description=product_description,
        brand=product_brand,
        model = product_model,
        price=product_price,
        image_url= image_url,
        product_type_id= product_type.id
                         )
        
        db.session.add(product)
        db.session.flush()  # Flush to get product ID before committin

        if product_type_name == 'inverter':
            try:      
                inverter_battery_voltage = request.form.get('inverter_battery_voltage')
                inverter_power = request.form.get('inverter_power')

                inverter_max_pv_voltage = request.form.get('inverter_max_pv_voltage')
                inverter_min_pv_voltage = request.form.get('inverter_min_pv_voltage')

                inverter_max_pv_current = request.form.get('inverter_max_pv_current')
                inverter_min_pv_current = request.form.get('inverter_min_pv_current')

                inverter_mppt_voltage_min = request.form.get("inverter_mppt_voltage_min")
                inverter_mppt_voltage_max = request.form.get("inverter_mppt_voltage_max")

                pv_max_charging_current = request.form.get("inverter_max_pv_charging_current")  
                ac_max_charging_current = request.form.get("inverter_max_ac_charging_current")
                inverter_charging_current = request.form.get("inverter_max_charging_current")

                max_pv_power = request.form.get("inverter_max_pv_power")

                new_inverter = Inverter(  
                                    id = product.id, 
                                    power_rating   = inverter_power, 
                                    max_pv_power   = max_pv_power ,
                                    system_voltage = inverter_battery_voltage,

                                    max_pv_voltage = inverter_max_pv_voltage,
                                    min_pv_voltage = inverter_min_pv_voltage, 

                                    max_pv_current= inverter_max_pv_current,
                                    min_pv_current = inverter_min_pv_current,

                                    mppt_voltage_min = inverter_mppt_voltage_min,
                                    mppt_voltage_max = inverter_mppt_voltage_max,

                                    ac_max_charging_current=ac_max_charging_current,
                                    pv_max_charging_current=pv_max_charging_current,
                                    max_charging_current = inverter_charging_current

                                )
             
                db.session.add(new_inverter)
                # Commit the transaction
                db.session.commit()

                return redirect("products")

            except Exception as e:
                db.session.rollback()  # Rollback on error
                return jsonify({"error": str(e)}), 500
                
        elif product_type_name == 'battery':
            print("adding new battery")
            battery_capacity = request.form.get('battery_capacity')
            cycle_number = request.form.get('cycle_time')
            battery_type = request.form.get('battery_type')
            voltage = 12
            new_battery = Battery(
                id = product.id, 
                capacity = battery_capacity,
                voltage = voltage,
                battery_type = battery_type,
                cycle_number = cycle_number
            )
            db.session.add(new_battery)
            # Commit the transaction
            db.session.commit()
        elif product_type_name == 'panel':

            panel_wattage = request.form.get('panel_power')
            panel_alpha = request.form.get('panel_alpha')

            panel_width = request.form.get('panel_width')
            panel_length= request.form.get('panel_length')
            panel_thickness = request.form.get('panel_thickness')

            panel_voc = request.form.get('panel_voc')
            panel_vmp = request.form.get('panel_vmp')

            panel_isc = request.form.get('panel_isc')
            panel_imp = request.form.get('panel_imp')

            new_battery = Panel(
                id = product.id, 
                wattage = panel_wattage,
                alpha = panel_alpha,
                width = panel_width,
                length = panel_length,
                thickness=panel_thickness,
                Voc=panel_voc,
                Vmp=panel_vmp,
                Isc=panel_isc,
                Imp=panel_imp,
            )
            db.session.add(new_battery)
            # Commit the transaction
            db.session.commit()


    else:
        print("oh no")
    return render_template('admin/products.html')


@admin_bp.route('/signout')
def signout():
    return render_template('admin/login_form.html')



def get_upload_folder(subfolder):
    # Combine root path with the target folder structure
    upload_folder = os.path.join('uploads', subfolder)
    print(upload_folder)
    return upload_folder



# Route: Manage Products (Add/Update/Delete)
@admin_bp.route('/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'POST':
        # Add New Product
        name = request.form.get('name')
        description = request.form.get('description')
        brand = request.form.get('brand')
        model = request.form.get('brand')
        price = request.form.get('price')
        product_type_id = request.form.get('product_type_id')
        image = request.files.get('image')

        # Handle Image Upload
        image_url = None
        if image:
            filename = f"{name.replace(' ', '_')}-{image.filename}"
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
            image_url = f"uploads/{filename}"  # Save relative path for rendering in HTML
        # Save Product to Database
        new_product = Product(
            name=name,
            description=description,
            brand=brand,
            model = model,
            price=price,
            product_type_id=product_type_id,
            image_url=image_url
        )
        db.session.add(new_product)
        db.session.commit()

        flash('تم إضافة المنتج بنجاح', 'success')
        return redirect(url_for('admin.manage_products'))

    # GET: Render the Product Management Page
    product_types = ProductType.query.options(db.joinedload(ProductType.products)).all()
    return render_template('admin/products.html', product_types=product_types)


# Route: Update Product
@admin_bp.route('/update-product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)

    # Update Product Fields
    product.name = request.form.get('name')
    product.description = request.form.get('description')
    product.brand = request.form.get('brand')
    product.price = request.form.get('price')

    # Handle Image Update
    image = request.files.get('image')
    if image:
        filename = f"{product.name.replace(' ', '_')}-{image.filename}"
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)
        product.image_url = f"uploads/{filename}"  # Update image URL

    db.session.commit()
    flash('تم تحديث المنتج بنجاح', 'success')
    return redirect(url_for('admin.manage_products'))


# Route: Delete Product
@admin_bp.route('/delete-product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    # Remove the image file if it exists
    if product.image_url:
        image_path = os.path.join(UPLOAD_FOLDER, product.image_url.split('/')[-1])
        if os.path.exists(image_path):
            os.remove(image_path)
    db.session.delete(product)
    db.session.commit()
    flash('تم حذف المنتج بنجاح', 'success')
    return redirect(url_for('admin.manage_products'))




@admin_bp.route('/add_type', methods=['GET', 'POST'])
def add_type():
    # Create a new ProductType instance
    if request.method == 'POST':
        type_name =  request.form.get('type_name')
        description = request.form.get('description')
        
        new_product_type = ProductType(
            name= type_name,
            description=description,
        )
        db.session.add(new_product_type)
        db.session.commit()
        flash('Product type added successfully!', 'success')
        return redirect(url_for('admin.add_type'))  # Redirect to the same page or another route
    return render_template("admin/add_product_type.html")


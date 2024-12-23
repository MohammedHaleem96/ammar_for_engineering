from flask import Flask, render_template, request, Blueprint, redirect, url_for, flash,jsonify, current_app
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from datetime import datetime
from app.models.products import Product, Inverter, Battery, Panel,ProductType, Wire
from app.models.AccomplishedProject import AccomplishedProject
from app.models.ourSevices import OurService

#from app.forms import ProductForm, InverterForm, BatteryForm, PanelForm
from app.models.admins import Admin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError


from app import db


inverter_types = ['Hypred','ups','block']

# Initialize Blueprint for admin
admin_bp = Blueprint('admin', __name__)



UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_PANNER_EXTENSIONS= {'png', 'jpg', 'jpeg', 'gif','pdf'}




@admin_bp.route('/add_accomplished_project', methods=['GET', 'POST'])
@login_required
def add_accomplished_project():
    projects = AccomplishedProject.query.all()

    if request.method == 'POST':
        project_name = request.form.get('project_name')
        project_type = request.form.get('project_type')
        location = request.form.get('location')
        description = request.form.get('description')
        completion_date = request.form.get('completion_date')
        image_url = "request.form.get('image')"

        # Convert the string completion_date to a Python date object
        try:
            completion_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format. Please use 'YYYY-MM-DD'.", 'error')
            return redirect(url_for('admin.add_accomplished_project'))

        new_project = AccomplishedProject(
                        name=project_name,
                        type=project_type,
                        location=location,
                        description=description,
                        completion_date=completion_date,
                        image_url=image_url
                                 )
        db.session.add(new_project)
        db.session.commit()
        projects = AccomplishedProject.query.all()

        flash('Project added successfully!', 'success')
        return redirect(url_for('admin.manage_projects'))
    
    return render_template('admin/accomplished_projects.html', projects=projects)


@admin_bp.route('/manage_projects')
@login_required
def manage_projects():
    projects = AccomplishedProject.query.all()
    return render_template('admin/accomplished_projects.html', projects=projects)

@admin_bp.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    # Get the project by ID
    project = AccomplishedProject.query.get_or_404(project_id)

    if request.method == 'POST':
        # Update the project details from the form
        project.name = request.form['name']
        project.type = request.form['type']
        project.location = request.form['location']
        project.description = request.form['description']
        image_url='image_url'
        completion_date_str = request.form.get('completion_date')

        try:
            project.completion_date = datetime.strptime(completion_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format. Please use 'YYYY-MM-DD'.", 'error')
            return redirect(url_for('admin.edit_project', project_id=project.id))

        # Commit changes to the database
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.manage_projects'))  # Redirect to the projects management page

    return render_template('admin/edit_project.html', project=project)




@admin_bp.route('/delete_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def delete_project(project_id):
    project = AccomplishedProject.query.get_or_404(project_id)

    # Delete the project
    db.session.delete(project)
    db.session.commit()
    
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.manage_projects'))  # Redirect to the projects management page










# --- - - --
# Add Service Route
@admin_bp.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        new_service = OurService(name=name, description=description)
        db.session.add(new_service)
        db.session.commit()
        
        flash('Service added successfully!', 'success')
        return redirect(url_for('admin.manage_services'))
    
    return render_template('admin/add_service.html')

# Manage Services (List, Edit, Delete)
@admin_bp.route('/manage_services')
def manage_services():
    services = OurService.query.all()
    return render_template('admin/manage_services.html', services=services)

# Edit Service Route
@admin_bp.route('/edit_service/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    service = OurService.query.get_or_404(service_id)
    
    if request.method == 'POST':
        service.name = request.form.get('name')
        service.description = request.form.get('description')
        db.session.commit()
        
        flash('Service updated successfully!', 'success')
        return redirect(url_for('admin.manage_services'))
    
    return render_template('admin/edit_service.html', service=service)

# Delete Service Route
@admin_bp.route('/delete_service/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    service = OurService.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin.manage_services'))



#-----------

@admin_bp.route('/create_admin', methods=['GET', 'POST'])
#@login_required
def create_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if username already exists
        existing_admin = Admin.query.filter_by(username=username).first()
        
        if existing_admin:
            flash('Username already exists, please choose another one.', 'error')
            return redirect(url_for('admin.create_admin'))  # Redirect back to the form

        # Proceed to create a new admin if username is unique
        password_hash = generate_password_hash(password)

        try:
            new_admin = Admin(username=username, password_hash=password_hash)
            db.session.add(new_admin)
            db.session.commit()
            flash('Admin created successfully!', 'success')
            return redirect(url_for('admin.dashboard'))  # Redirect to dashboard after creation
        except IntegrityError:
            # This block may not be hit if we check for username existence first.
            db.session.rollback()  # Rollback in case of any error during commit
            flash('An error occurred while creating the admin. Please try again.', 'error')
            return redirect(url_for('admin.create_admin'))  # Redirect back to the form
    return render_template('admin/create_admin.html')  # Render create admin form





def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@admin_bp.route('/')
def index():
    return render_template('admin/login_form.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("post detected")
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
    else:
        return redirect(url_for('admin.index'))

    
    return render_template('admin/login_form.html')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/products')
@login_required
def products():

    try:
        # Query all product types with their products
        product_types = ProductType.query.options(db.joinedload(ProductType.products)).all()
        # Pass the product types to the template
        return render_template('admin/products.html', product_types=product_types , types = inverter_types)

    except Exception as e:
        return {"error": str(e)}, 500
    
@admin_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
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
                inverter_type = request.form.get('inverter_type')


                inverter_max_pv_voltage = request.form.get('inverter_max_pv_voltage')
                inverter_min_pv_voltage = request.form.get('inverter_min_pv_voltage')

                inverter_max_pv_current = request.form.get('inverter_max_pv_current')
                inverter_min_pv_current = request.form.get('inverter_min_pv_current')

                inverter_mppt_voltage_min = request.form.get("inverter_mppt_voltage_min")
                inverter_mppt_voltage_max = request.form.get("inverter_mppt_voltage_max")

                pv_max_charging_current = request.form.get("pv_max_charging_current")  
                ac_max_charging_current = request.form.get("inverter_max_ac_charging_current")
                inverter_charging_current = request.form.get("inverter_max_charging_current")

                max_pv_power = request.form.get("inverter_max_pv_power")

                new_inverter = Inverter(  
                                    id = product.id, 
                                    power_rating   = inverter_power, 
                                    max_pv_power   = max_pv_power ,
                                    inverter_type = inverter_type,
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
    return redirect('admin.products')


@admin_bp.route('/signout')
@login_required
def signout():
    logout_user()
    
    flash('تم تسجيل خروج بنجاح', 'success')
    return render_template('admin/login_form.html')


def get_upload_folder(subfolder):
    # Combine root path with the target folder structure
    upload_folder = os.path.join('uploads', subfolder)
    print(upload_folder)
    return upload_folder



# Route: Manage Products (Add/Update/Delete)
@admin_bp.route('/products', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
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


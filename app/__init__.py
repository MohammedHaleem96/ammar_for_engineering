from flask import Flask, render_template, redirect
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__,static_folder='static')
    
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    # Tell login manager where to redirect for login
    login_manager.login_view = 'admin.login'  # For example, redirect to login page if not logged in
    with app.app_context():
        from app.routes.user_routes import user_bp  # Import user routes blueprint
        from app.routes.admin_routes import admin_bp  # Import admin routes blueprint
            # Register Blueprints
        app.register_blueprint(user_bp, url_prefix='/user')
        app.register_blueprint(admin_bp, url_prefix='/admin')
        




        
    @app.template_filter('currency')
    def currency_filter(value):
        """Format a number as currency."""
        if value is None:
            return ''
        return f"{value:,.0f}"  # Adjust for your desired format

    @app.route('/')
    def index():
        return render_template('user/index.html')


    return app

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models.admins import Admin  # Import inside the function to avoid circular imports
    return Admin.query.get(int(user_id))  # Return the user by their ID

import os
from dotenv import load_dotenv

IS_ADMIN_TEST = False

# Load environment variables from the .env file
load_dotenv()
class Config:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    ALLOWED_IMAGE_EXTENSIONS = os.getenv('ALLOWED_IMAGE_EXTENSIONS')
    ALLOWED_PANNER_EXTENSIONS = os.getenv('ALLOWED_PANNER_EXTENSIONS')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    SQLALCHEMY_TRACK_MODIFICATIONS =  False
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    SECRET_KEY = os.urandom(24) 

    #FLASK_ENV = os.getenv('FLASK_ENV', 'production')  # Default to 'production' if not set


import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '102030'),
    'database': os.getenv('DB_NAME', 'instagram_clone'),
    'auth_plugin': 'mysql_native_password'
}

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

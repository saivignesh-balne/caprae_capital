import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    'linkedin': {
        'email': os.getenv('LINKEDIN_EMAIL'),
        'password': os.getenv('LINKEDIN_PASSWORD'),
        'login_url': 'https://www.linkedin.com/login'
    },
    'flask': {
        'secret_key': os.getenv('FLASK_SECRET_KEY', 'dev-key-123'),
        'debug': os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    },
    'selenium': {
        'headless': False,
        'timeout': 30
    }
}
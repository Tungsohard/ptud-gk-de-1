from flask import Blueprint

# Import các blueprints cụ thể 
from .admin import admin_bp
from .auth import auth_bp
from .main import main_bp
from .post import post_bp
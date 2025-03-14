from flask import render_template, abort
from flask_login import current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)  # Unauthorized
        if not current_user.is_admin:
            return render_template('errors/403.html'), 403
        return f(*args, **kwargs)
    return decorated_function
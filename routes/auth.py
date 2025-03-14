from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
from forms import LoginForm, RegistrationForm
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            if not hasattr(user, 'is_active') or user.is_active:
                # Lỗi: form.remember.data không tồn tại trong LoginForm
                login_user(user)  # Xóa remember=form.remember.data
                next_page = request.args.get('next')
                flash('Đăng nhập thành công!', 'success')
                return redirect(next_page or url_for('main.index'))
            else:
                flash('Tài khoản đã bị vô hiệu hóa. Vui lòng liên hệ quản trị viên.', 'danger')
        else:
            flash('Đăng nhập thất bại. Kiểm tra lại tên đăng nhập và mật khẩu.', 'danger')
            
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # Kiểm tra xem username đã tồn tại chưa
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Tên người dùng đã tồn tại. Vui lòng chọn tên khác.', 'danger')
            return render_template('auth/register.html', form=form)
            
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(
            username=form.username.data, 
            password=hashed_password,
            is_admin=False, 
            is_active=True,
            date_joined=datetime.utcnow()
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('main.index'))
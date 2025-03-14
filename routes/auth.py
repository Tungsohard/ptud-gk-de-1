from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if not user:
            flash('Tên đăng nhập không tồn tại.', 'danger')
            return render_template('auth/login.html', form=form)
            
        if not user.check_password(form.password.data):
            flash('Mật khẩu không chính xác.', 'danger')
            return render_template('auth/login.html', form=form)
            
        if not user.is_active:
            flash('Tài khoản của bạn đã bị vô hiệu hóa.', 'danger')
            return render_template('auth/login.html', form=form)
            
        login_user(user, remember=form.remember.data)
        
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('main.index'))
        
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
            date_joined=datetime.utcnow(),
            role='viewer'  # Mặc định là viewer
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
    flash('Bạn đã đăng xuất thành công.', 'info')
    return redirect(url_for('auth.login'))
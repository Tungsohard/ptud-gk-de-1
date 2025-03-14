# File: create_admin.py
from app import app
from models import db, User
from werkzeug.security import generate_password_hash

# Thông tin tài khoản admin bạn muốn tạo
admin_username = "admin"  
admin_password = "Admin@123"  # Nên thay đổi thành mật khẩu mạnh

with app.app_context():
    # Kiểm tra xem admin đã tồn tại chưa
    existing_admin = User.query.filter_by(username=admin_username).first()
    
    if existing_admin:
        print(f"Admin '{admin_username}' đã tồn tại")
    else:
        # Tạo tài khoản admin mới
        hashed_password = generate_password_hash(admin_password, method='sha256')
        new_admin = User(username=admin_username, password=hashed_password, is_admin=True)
        
        db.session.add(new_admin)
        db.session.commit()
        
        print(f"Đã tạo tài khoản admin '{admin_username}' thành công")
        print(f"Tên đăng nhập: {admin_username}")
        print(f"Mật khẩu: {admin_password}")
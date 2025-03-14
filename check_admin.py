# Tạo file check_admin.py trong thư mục chính
from app import app
from models import User

with app.app_context():
    username = input("Nhập tên người dùng cần kiểm tra: ")
    user = User.query.filter_by(username=username).first()
    
    if user:
        print(f"Username: {user.username}")
        print(f"Is Admin: {user.is_admin}")
        print(f"Is Active: {user.is_active}")
        
        if not user.is_admin:
            make_admin = input("Bạn có muốn cấp quyền admin cho tài khoản này? (y/n): ")
            if make_admin.lower() == 'y':
                user.is_admin = True
                from models import db
                db.session.commit()
                print(f"Đã cấp quyền admin cho {user.username}")
    else:
        print(f"Không tìm thấy tài khoản {username}")
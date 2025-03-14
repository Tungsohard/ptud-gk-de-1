# update_roles.py
from app import app
from models import db, User
from sqlalchemy import text
from datetime import datetime

with app.app_context():
    # 1. Kiểm tra xem cột role đã tồn tại chưa
    try:
        # Thử truy vấn để kiểm tra cột role
        User.query.filter_by(role='viewer').first()
        print("✅ Cột 'role' đã tồn tại trong database.")
    except Exception as e:
        print(f"❌ Lỗi khi truy vấn cột role: {str(e)}")
        print("➡️ Đang thực hiện tạo lại database...")
        
        # Tạo lại database
        db.drop_all()
        db.create_all()
        print("✅ Đã tạo lại database với cột 'role'.")
        
        # Tạo lại tài khoản admin
        from werkzeug.security import generate_password_hash
        admin = User(
            username='admin',
            password=generate_password_hash('Admin@123'),
            is_admin=True,
            is_active=True,
            date_joined=datetime.utcnow(),
            role='editor'  # Admin luôn có quyền cao nhất
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Đã tạo lại tài khoản admin với username: 'admin' và password: 'Admin@123'")
    
    # 2. Cập nhật các quyền mặc định cho người dùng chưa có role
    users_without_role = User.query.filter(User.role.is_(None)).all()
    if users_without_role:
        print(f"🔄 Đang cập nhật role cho {len(users_without_role)} người dùng...")
        for user in users_without_role:
            user.role = 'viewer'  # Mặc định là quyền xem
        db.session.commit()
        print("✅ Đã cập nhật role mặc định thành công.")
    
    # 3. Hiển thị thống kê người dùng theo role
    print("\n📊 Thống kê người dùng theo quyền:")
    print(f"- Viewer: {User.query.filter_by(role='viewer').count()} người dùng")
    print(f"- Collaborator: {User.query.filter_by(role='collaborator').count()} người dùng")
    print(f"- Editor: {User.query.filter_by(role='editor').count()} người dùng")
    print(f"- Admin: {User.query.filter_by(is_admin=True).count()} người dùng")
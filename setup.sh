#!/bin/bash
# Script cài đặt và chạy Blog Cá Nhân với Flask

# Màu sắc cho thông báo
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Cài đặt và Chạy Blog Cá Nhân =====${NC}"

# Kiểm tra Python đã được cài đặt chưa
if command -v python &>/dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
else
    echo -e "${RED}Không tìm thấy Python. Vui lòng cài đặt Python 3.7 hoặc cao hơn.${NC}"
    exit 1
fi

# Hiện thông tin phiên bản Python
echo -e "${GREEN}Đang sử dụng:${NC} $($PYTHON_CMD --version)"

# Kiểm tra và tạo thư mục cần thiết
echo -e "${YELLOW}Kiểm tra và tạo thư mục cần thiết...${NC}"
mkdir -p static/uploads
mkdir -p instance
echo -e "${GREEN}Đã tạo thư mục cần thiết.${NC}"

# Tạo file requirements.txt nếu chưa tồn tại
if [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}Tạo file requirements.txt...${NC}"
    cat > requirements.txt << EOF
Flask==2.0.1
Flask-WTF==1.0.0
Flask-Login==0.5.0
Flask-SQLAlchemy==2.5.1
SQLAlchemy==1.4.46
Werkzeug==2.0.2
Pillow==9.0.0
email_validator==1.1.3
WTForms==3.0.0
EOF
    echo -e "${GREEN}Đã tạo file requirements.txt với các phiên bản phù hợp.${NC}"
fi

# Tạo và kích hoạt môi trường ảo
echo -e "${YELLOW}Tạo môi trường ảo...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Môi trường ảo đã tồn tại.${NC}"
    read -p "Bạn có muốn xóa và tạo lại môi trường ảo không? (y/n): " recreate_venv
    if [ "$recreate_venv" == "y" ] || [ "$recreate_venv" == "Y" ]; then
        echo -e "${YELLOW}Xóa môi trường ảo cũ...${NC}"
        rm -rf venv
        $PYTHON_CMD -m venv venv
        echo -e "${GREEN}Đã tạo lại môi trường ảo.${NC}"
    fi
else
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}Đã tạo môi trường ảo.${NC}"
fi

# Kích hoạt môi trường ảo
echo -e "${YELLOW}Kích hoạt môi trường ảo...${NC}"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi
echo -e "${GREEN}Đã kích hoạt môi trường ảo.${NC}"

# Cài đặt các thư viện từ requirements.txt
echo -e "${YELLOW}Cài đặt các thư viện...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}Đã cài đặt thư viện.${NC}"

# Kiểm tra xem cơ sở dữ liệu đã tồn tại chưa
if [ -f "instance/site.db" ]; then
    echo -e "${YELLOW}Phát hiện cơ sở dữ liệu hiện có.${NC}"
    read -p "Bạn có muốn tạo lại cơ sở dữ liệu? (y/n): " recreate_db
    if [ "$recreate_db" == "y" ] || [ "$recreate_db" == "Y" ]; then
        echo -e "${YELLOW}Xóa cơ sở dữ liệu cũ...${NC}"
        rm instance/site.db
        echo -e "${GREEN}Đã xóa cơ sở dữ liệu.${NC}"
    fi
fi

# Kiểm tra file app.py để tránh lỗi SQLAlchemy
echo -e "${YELLOW}Kiểm tra và cập nhật file app.py nếu cần...${NC}"
if [ -f "app.py" ]; then
    # Kiểm tra xem đã có đoạn code xử lý lỗi SQLAlchemy chưa
    if ! grep -q "__all__" app.py; then
        # Tạo file tạm chứa đoạn code cần thêm vào đầu file
        cat > temp_fix.py << EOF
# Fix cho lỗi SQLAlchemy __all__
import sqlalchemy
if not hasattr(sqlalchemy, '__all__'):
    sqlalchemy.__all__ = []  # Tạo thuộc tính __all__ nếu không tồn tại

EOF
        # Thêm đoạn code fix vào đầu file app.py
        cat temp_fix.py app.py > app.py.new
        mv app.py.new app.py
        rm temp_fix.py
        echo -e "${GREEN}Đã cập nhật file app.py để xử lý lỗi SQLAlchemy.${NC}"
    else
        echo -e "${GREEN}File app.py đã có fix cho SQLAlchemy.${NC}"
    fi
else
    echo -e "${RED}Không tìm thấy file app.py. Vui lòng kiểm tra lại.${NC}"
    exit 1
fi

# Chạy ứng dụng để tạo cơ sở dữ liệu
echo -e "${YELLOW}Khởi tạo cơ sở dữ liệu...${NC}"
$PYTHON_CMD app.py &
APP_PID=$!
sleep 5
kill $APP_PID 2>/dev/null
wait $APP_PID 2>/dev/null
echo -e "${GREEN}Đã khởi tạo cơ sở dữ liệu.${NC}"

# Tạo tài khoản admin nếu chưa tồn tại
echo -e "${YELLOW}Kiểm tra và tạo tài khoản admin...${NC}"

# Kiểm tra xem file create_admin.py đã tồn tại chưa
if [ ! -f "create_admin.py" ]; then
    echo -e "${YELLOW}Tạo file create_admin.py...${NC}"
    cat > create_admin.py << EOF
from app import app
from models import db, User
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_new_admin(username, password):
    with app.app_context():
        # Kiểm tra xem admin đã tồn tại chưa
        existing_admin = User.query.filter_by(username=username).first()
        
        if existing_admin:
            print(f"Tài khoản '{username}' đã tồn tại")
            return False
        else:
            # Tạo tài khoản admin mới
            hashed_password = generate_password_hash(password, method='sha256')
            new_admin = User(
                username=username, 
                password=hashed_password, 
                is_admin=True,
                is_active=True,
                date_joined=datetime.utcnow()
            )
            
            db.session.add(new_admin)
            db.session.commit()
            
            print(f"Đã tạo tài khoản admin '{username}' thành công")
            return True

if __name__ == "__main__":
    create_new_admin("admin", "Admin@123")
EOF
    echo -e "${GREEN}Đã tạo file create_admin.py.${NC}"
fi

# Tạo tài khoản admin
$PYTHON_CMD create_admin.py
echo -e "${GREEN}Đã kiểm tra/tạo tài khoản admin.${NC}"

# Hiển thị thông tin
echo -e "\n${BLUE}===== Cài Đặt Hoàn Tất =====${NC}"
echo -e "${GREEN}Thông tin tài khoản admin mặc định:${NC}"
echo -e "  Username: admin"
echo -e "  Password: Admin@123"
echo -e "\n${GREEN}Để khởi động ứng dụng, chạy lệnh:${NC}"
echo -e "  $PYTHON_CMD app.py"
echo -e "\n${GREEN}Truy cập trang web tại:${NC}"
echo -e "  http://localhost:5000"

# Hỏi người dùng có muốn chạy ứng dụng không
read -p "Bạn có muốn khởi động ứng dụng ngay bây giờ không? (y/n): " start_app
if [ "$start_app" == "y" ] || [ "$start_app" == "Y" ]; then
    echo -e "${YELLOW}Đang khởi động ứng dụng...${NC}"
    echo -e "${GREEN}Ứng dụng đang chạy tại http://localhost:5000${NC}"
    echo -e "${YELLOW}Nhấn Ctrl+C để dừng ứng dụng.${NC}"
    $PYTHON_CMD app.py
else
    echo -e "${BLUE}Cài đặt hoàn tất. Chạy '$PYTHON_CMD app.py' khi bạn muốn khởi động ứng dụng.${NC}"
fi
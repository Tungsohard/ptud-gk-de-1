Blog Cá Nhân
Dự án này là một ứng dụng blog cá nhân được xây dựng trên nền tảng Flask, cho phép người dùng đăng ký, đăng nhập, tạo và quản lý bài viết. Hệ thống cũng có trang quản trị dành cho admin để quản lý người dùng và bài viết.

Tính năng chính
Quản lý người dùng: Đăng ký, đăng nhập, đăng xuất
Quản lý bài viết: Tạo, đọc, cập nhật, xóa bài viết
Upload hình ảnh: Hỗ trợ upload hình ảnh cho bài viết
Trang quản trị Admin:
Quản lý người dùng (xóa, vô hiệu hóa tài khoản)
Quản lý bài viết (xóa, ẩn/hiện bài viết)
Dashboard thống kê
Giao diện: Responsive, thân thiện với người dùng

Cấu trúc dự án

blog-ca-nhan/
├── app.py                # Điểm khởi đầu ứng dụng
├── config.py             # Cấu hình ứng dụng
├── create_admin.py       # Script tạo tài khoản admin
├── check_admin.py        # Script kiểm tra/cấp quyền admin
├── models.py             # Mô hình cơ sở dữ liệu
├── forms.py              # Định nghĩa các form
├── requirements.txt      # Thư viện phụ thuộc
├── routes/               # Các route của ứng dụng
│   ├── __init__.py
│   ├── admin.py          # Route quản trị
│   ├── auth.py           # Route xác thực
│   ├── main.py           # Route chính
│   ├── post.py           # Route quản lý bài viết
│   └── utils.py          # Tiện ích hỗ trợ
├── static/               # Tài nguyên tĩnh
│   ├── css/
│   │   └── style.css     # File CSS chính
│   ├── js/
│   │   └── main.js       # JavaScript phía client
│   └── uploads/          # Thư mục lưu hình ảnh upload
└── templates/            # Các template HTML
    ├── admin/            # Template cho trang admin
    │   ├── dashboard.html
    │   ├── posts.html
    │   └── users.html
    ├── auth/             # Template xác thực
    │   ├── login.html
    │   └── register.html
    ├── post/             # Template quản lý bài viết
    │   ├── create_post.html
    │   ├── post.html
    │   └── user_posts.html
    ├── errors/           # Template trang lỗi
    ├── base.html         # Template cơ sở
    └── index.html        # Trang chủ

## Cài đặt

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-auth-website
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create admin_user

   python create_admin.py

4. Run the application:
   ```
   python app.py
   ```

## Usage

- Navigate to the homepage to access the registration and login pages.
- Admin users can access the dashboard to manage user accounts.

## License

This project is licensed under the MIT License.
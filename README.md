# Blog Cá Nhân
# Tên: Nguyễn Văn Tùng-22647011

Ứng dụng blog cá nhân xây dựng trên Flask với hệ thống quản lý người dùng, bài viết, bình luận và phân quyền người dùng.

## Tính năng chính

- **Hệ thống tài khoản người dùng**
  - Đăng ký, đăng nhập, đăng xuất
  - Ghi nhớ đăng nhập
  - Phân quyền 4 cấp độ: Viewer, Collaborator, Editor và Admin

- **Quản lý bài viết**
  - Tạo, xem, chỉnh sửa và xóa bài viết
  - Upload hình ảnh cho bài viết
  - Phân loại quyền truy cập với từng thao tác

- **Hệ thống bình luận**
  - Bình luận bài viết
  - Quản lý bình luận (xóa, ẩn/hiện)

- **Trang quản trị admin**
  - Dashboard thống kê
  - Quản lý người dùng (xóa, vô hiệu hóa, phân quyền)
  - Quản lý bài viết (xóa, ẩn/hiện)
  - Quản lý bình luận (xóa, ẩn/hiện)

- **Giao diện**
  - Responsive design
  - Thân thiện với người dùng
  - Tương thích với nhiều thiết bị

## Công nghệ sử dụng

- **Back-end**: Python, Flask
- **Database**: SQLite, SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Front-end**: HTML, CSS, JavaScript, Font Awesome

## Cấu trúc dự án

flask-auth-website/
├── app.py                   # Điểm khởi đầu ứng dụng
├── config.py                # Cấu hình ứng dụng
├── create_admin.py          # Script tạo tài khoản admin
├── check_admin.py           # Script kiểm tra/cấp quyền admin
├── update_roles.py          # Script cập nhật hệ thống phân quyền
├── models.py                # Mô hình cơ sở dữ liệu
├── forms.py                 # Định nghĩa các form
├── requirements.txt         # Thư viện phụ thuộc
├── setup.bat                # Script cài đặt tự động (Windows)
├── setup.sh                 # Script cài đặt tự động (Linux/Mac)
├── routes/                  # Các route của ứng dụng
│   ├── __init__.py
│   ├── admin.py             # Route quản trị
│   ├── auth.py              # Route xác thực
│   ├── main.py              # Route chính
│   ├── post.py              # Route quản lý bài viết
│   └── utils.py             # Tiện ích hỗ trợ
├── static/                  # Tài nguyên tĩnh
│   ├── css/
│   │   └── style.css        # File CSS chính
│   ├── js/
│   │   └── main.js          # JavaScript phía client
│   └── uploads/             # Thư mục lưu hình ảnh bài viết
└── templates/               # Các template HTML
    ├── admin/               # Template cho trang admin
    │   ├── dashboard.html
    │   ├── posts.html
    │   ├── users.html
    │   └── comments.html
    ├── auth/                # Template xác thực
    │   ├── login.html
    │   └── register.html
    ├── post/                # Template quản lý bài viết
    │   ├── create_post.html
    │   ├── post.html
    │   └── user_posts.html
    ├── errors/              # Template trang lỗi
    │   └── 403.html
    ├── base.html            # Template cơ sở
    ├── index.html           # Trang chủ
    └── user_roles_help.html


## Hệ thống phân quyền
| Quyền           | Mô tả |
|----------------|------------------------------------------|
| **Viewer**     | Chỉ có quyền xem bài viết và bình luận |
| **Collaborator** | Có thể tạo và chỉnh sửa bài viết của mình |
| **Editor**     | Có thể tạo, chỉnh sửa và xóa bài viết của mình |
| **Admin**      | Có mọi quyền trên hệ thống - Là người trao quyền                          (Viewer/Collaborator/Editor) cho user  |


## Cài đặt và chạy

### Cài đặt tự động
Sử dụng script tự động để cài đặt và chạy ứng dụng:

#### Windows
Chạy lệnh sau trong terminal (Command Prompt):
```sh
setup.bat
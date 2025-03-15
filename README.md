# Hệ thống Blog Cá Nhân

## Tổng quan dự án
Ứng dụng Blog Cá Nhân được xây dựng với các chức năng sau:

- Hệ thống đăng ký, đăng nhập và quản lý người dùng
- Chức năng tạo, chỉnh sửa, xóa và hiển thị bài viết
- Hệ thống bình luận cho bài viết
- Phân quyền người dùng 4 cấp độ (Viewer, Collaborator, Editor, Admin)
- Giao diện quản trị cho người dùng Admin
- Giao diện người dùng thân thiện và responsive

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
## Kiến trúc ứng dụng
Dự án được tổ chức theo mô hình MVC (Model-View-Controller) với các thành phần chính:

- **Models**: Định nghĩa cấu trúc dữ liệu (User, Post, Comment)
- **Views**: Các template HTML trong thư mục `templates`
- **Controllers**: Các routes trong thư mục `routes`
- **Static assets**: CSS, JavaScript, và hình ảnh trong thư mục `static`

## Hệ thống phân quyền
Hệ thống phân quyền bao gồm 4 cấp độ:

| Quyền          | Mô tả |
|---------------|------------------------------------------|
| **Viewer**    | Chỉ có quyền xem và bình luận bài viết |
| **Collaborator** | Có thể tạo và chỉnh sửa bài viết của mình (không xóa) |
| **Editor**    | Có thể tạo, chỉnh sửa và xóa bài viết của mình |
| **Admin**     | Có toàn quyền quản lý hệ thống |

Các quyền được quản lý thông qua thuộc tính `role` trong model `User`, với các phương thức kiểm tra quyền như `is_viewer()`, `is_collaborator()`, `is_editor()`.

## Chức năng quan trọng đã triển khai
### 1. Hệ thống xác thực
- Đăng ký tài khoản với tên người dùng và mật khẩu
- Đăng nhập với chức năng "Ghi nhớ đăng nhập"
- Mã hóa mật khẩu với Werkzeug's security
- Đăng xuất và quản lý phiên

### 2. Quản lý bài viết
- Tạo bài viết mới với tiêu đề, nội dung và hình ảnh
- Xem chi tiết bài viết
- Chỉnh sửa bài viết hiện có
- Xóa bài viết với xác nhận
- Upload và lưu trữ hình ảnh

### 3. Hệ thống bình luận
- Thêm bình luận cho bài viết
- Xóa bình luận
- Ẩn/hiện bình luận (đối với Admin)
- Hiển thị số lượng bình luận

### 4. Dashboard Admin
- Thống kê tổng quan (số lượng người dùng, bài viết, bình luận)
- Quản lý người dùng (xem, vô hiệu hóa, xóa, phân quyền)
- Quản lý bài viết (xem, ẩn/hiện, xóa)
- Quản lý bình luận (xem, ẩn/hiện, xóa)

### 5. Giao diện người dùng
- Thiết kế responsive, hoạt động trên nhiều thiết bị
- Menu điều hướng tùy biến theo quyền người dùng
- Hiển thị thông báo flash cho các hành động
- Xác nhận trước khi xóa với JavaScript
- Dropdown menu cho các chức năng phụ

## Công nghệ sử dụng
### Back-end:
- Python với Flask framework
- SQLite làm cơ sở dữ liệu
- SQLAlchemy ORM để tương tác với database
- Flask-Login để quản lý phiên đăng nhập
- Flask-WTF để xử lý form và validate dữ liệu

### Front-end:
- HTML, CSS thuần
- JavaScript cho tương tác người dùng
- Font Awesome cho các icon
- Responsive design

## Công cụ hỗ trợ
Các script tiện ích:
- `setup.bat`: Script tự động cài đặt và cấu hình môi trường trên Windows
- `update_roles.py`: Cập nhật cơ sở dữ liệu với cột role mới và thiết lập quyền mặc định
- `create_admin.py`: Tạo tài khoản admin mặc định
- `check_admin.py`: Kiểm tra và cấp quyền admin cho người dùng

## Tính năng đặc biệt
- **Phân trang**: Hiển thị bài viết theo trang với SQLAlchemy pagination
- **Giải thích hệ thống phân quyền**: Trang riêng giải thích vai trò của mỗi loại người dùng
- **Thông báo flash**: Hiển thị thông báo phản hồi cho người dùng
- **Tự động ẩn thông báo**: JavaScript tự động ẩn thông báo sau 5 giây
- **Responsive design**: Giao diện thích ứng với nhiều thiết bị
- **Breadcrumbs**: Hiển thị đường dẫn điều hướng

## Tổ chức mã nguồn
Mã nguồn được tổ chức thành các thư mục và file có chức năng rõ ràng:

- `app.py`: Điểm khởi đầu ứng dụng
- `models.py`: Định nghĩa các model database
- `forms.py`: Định nghĩa các form
- `routes/`: Chứa các blueprint route theo chức năng
- `templates/`: Chứa các template HTML được tổ chức theo chức năng
- `static/`: Chứa tài nguyên tĩnh (CSS, JS, uploads)

## Các biện pháp bảo mật đã triển khai
- Mã hóa mật khẩu người dùng
- Kiểm tra quyền trước khi thực hiện hành động (decorators)
- Xác thực form với CSRF token
- Validate dữ liệu người dùng nhập vào
- Phân quyền rõ ràng và kiểm tra quyền
- Xác thực người dùng trước khi thực hiện các thao tác quan trọng

## Kết luận
Dự án Blog Cá Nhân là một ứng dụng web đầy đủ chức năng với nhiều tính năng nâng cao, được thiết kế theo nguyên tắc phần mềm hiện đại:

- Tách biệt các thành phần logic (MVC)
- Sử dụng blueprints để tổ chức code
- Tái sử dụng mã với templates
- Xử lý lỗi và thông báo người dùng
- Bảo mật dữ liệu và kiểm soát quyền truy cập

## Cài đặt và chạy

### Cài đặt tự động  
Sử dụng script tự động để cài đặt và chạy ứng dụng:

#### Windows  
Chạy lệnh sau trong terminal (Command Prompt):

```bash
cd ptud-gk-de-1
.\setup.bat
Hoặc click vào file setup.bat để chạy trực tiếp.

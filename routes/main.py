from flask import Blueprint, render_template
from models import Post, User
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Nếu là admin, hiển thị tất cả bài viết
    # Nếu không, chỉ hiển thị bài viết không bị ẩn từ người dùng đang hoạt động
    if current_user.is_authenticated and current_user.is_admin:
        posts = Post.query.order_by(Post.date_posted.desc()).all()
    else:
        posts = Post.query.filter_by(is_hidden=False).join(User).filter_by(is_active=True).order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@main_bp.route('/roles-help')
def roles_help():
    return render_template('user_roles_help.html')
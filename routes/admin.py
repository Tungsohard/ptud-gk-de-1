from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from models import db, User, Post, Comment
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

# Decorator để bảo vệ các route chỉ dành cho admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_posts = Post.query.count()
    total_comments = Comment.query.count()
    recent_users = User.query.order_by(User.id.desc()).limit(5).all()
    recent_posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
    recent_comments = Comment.query.order_by(Comment.date_posted.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          total_users=total_users,
                          total_posts=total_posts,
                          total_comments=total_comments,
                          recent_users=recent_users,
                          recent_posts=recent_posts,
                          recent_comments=recent_comments,
                          current_year=datetime.now().year)

@admin_bp.route('/admin/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/admin/posts')
@login_required
@admin_required
def posts():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('admin/posts.html', posts=posts)

@admin_bp.route('/admin/users/<int:user_id>/toggle_status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Không thể vô hiệu hóa tài khoản admin.', 'danger')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        status = "kích hoạt" if user.is_active else "vô hiệu hóa"
        flash(f'Đã {status} tài khoản người dùng thành công.', 'success')
        
    return redirect(url_for('admin.users'))

@admin_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Không thể xóa tài khoản admin.', 'danger')
    else:
        username = user.username
        db.session.delete(user)
        db.session.commit()
        flash(f'Đã xóa người dùng "{username}" thành công.', 'success')
        
    return redirect(url_for('admin.users'))

@admin_bp.route('/admin/posts/<int:post_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_post_status(post_id):
    post = Post.query.get_or_404(post_id)
    post.is_hidden = not post.is_hidden
    db.session.commit()
    status = "ẩn" if post.is_hidden else "hiển thị"
    flash(f'Đã {status} bài viết thành công.', 'success')
    return redirect(url_for('admin.posts'))

@admin_bp.route('/admin/posts/<int:post_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Đã xóa bài viết thành công.', 'success')
    return redirect(url_for('admin.posts'))

# Thêm route cho chức năng quản lý bình luận
@admin_bp.route('/admin/comments')
@login_required
@admin_required
def comments():
    comments = Comment.query.order_by(Comment.date_posted.desc()).all()
    return render_template('admin/comments.html', comments=comments)

@admin_bp.route('/admin/comments/<int:comment_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_comment_status(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.is_hidden = not comment.is_hidden
    db.session.commit()
    status = "ẩn" if comment.is_hidden else "hiển thị"
    flash(f'Đã {status} bình luận thành công.', 'success')
    return redirect(url_for('admin.comments'))

@admin_bp.route('/admin/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Đã xóa bình luận thành công.', 'success')
    return redirect(url_for('admin.comments'))

# Thêm route xử lý thay đổi role người dùng
@admin_bp.route('/admin/users/<int:user_id>/role/<string:role>', methods=['POST'])
@login_required
@admin_required
def change_user_role(user_id, role):
    user = User.query.get_or_404(user_id)
    
    if user.is_admin:
        flash('Không thể thay đổi quyền của tài khoản admin.', 'danger')
        return redirect(url_for('admin.users'))
        
    # Kiểm tra role hợp lệ
    valid_roles = ['viewer', 'collaborator', 'editor']
    if role not in valid_roles:
        flash('Quyền không hợp lệ.', 'danger')
        return redirect(url_for('admin.users'))
        
    user.role = role
    db.session.commit()
    flash(f'Đã thay đổi quyền của người dùng {user.username} thành {role}.', 'success')
    return redirect(url_for('admin.users'))
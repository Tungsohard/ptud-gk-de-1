from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from models import db, Post, User, Comment
from forms import PostForm, CommentForm
import os
import secrets
from werkzeug.utils import secure_filename
from datetime import datetime

post_bp = Blueprint('post', __name__)

def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/uploads', image_filename)
    
    # Tạo thư mục uploads nếu chưa tồn tại
    uploads_dir = os.path.join(current_app.root_path, 'static/uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    form_image.save(image_path)
    return 'uploads/' + image_filename

@post_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    # Chỉ collaborator và editor mới có quyền tạo bài viết
    if not current_user.is_collaborator():
        flash('Bạn không có quyền tạo bài viết mới.', 'danger')
        return redirect(url_for('main.index'))
        
    form = PostForm()
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            image_path = save_image(form.image.data)
            
        post = Post(
            title=form.title.data,
            content=form.content.data,
            image_path=image_path,
            user_id=current_user.id
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Bài viết đã được tạo!', 'success')
        return redirect(url_for('post.post', post_id=post.id))
        
    return render_template('post/create_post.html', form=form, legend='Đăng bài mới')

@post_bp.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    comments = Comment.query.filter_by(post_id=post_id, is_hidden=False).order_by(Comment.date_posted.desc()).all()
    return render_template('post/post.html', 
                         title=post.title, 
                         post=post, 
                         form=form, 
                         comments=comments)

@post_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            post_id=post.id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Bình luận của bạn đã được đăng!', 'success')
    
    return redirect(url_for('post.post', post_id=post.id))

@post_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post_id
    
    # Kiểm tra xem người dùng có quyền xóa không
    if comment.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    db.session.delete(comment)
    db.session.commit()
    flash('Bình luận đã được xóa!', 'success')
    return redirect(url_for('post.post', post_id=post_id))

@post_bp.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    pagination = Post.query.filter_by(user_id=user.id, is_hidden=False)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    posts = pagination.items  # Lấy danh sách các bài viết từ pagination
    return render_template('post/user_posts.html', posts=posts, user=user, pagination=pagination)

@post_bp.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Kiểm tra quyền: là tác giả VÀ có quyền collaborator trở lên HOẶC là admin
    if not ((post.user_id == current_user.id and current_user.is_collaborator()) or current_user.is_admin):
        abort(403)
        
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        
        if form.image.data:
            post.image_path = save_image(form.image.data)
            
        db.session.commit()
        flash('Bài viết đã được cập nhật!', 'success')
        return redirect(url_for('post.post', post_id=post.id))
        
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        
    return render_template('post/create_post.html', form=form, legend='Chỉnh sửa bài viết')

@post_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Kiểm tra quyền: là tác giả VÀ có quyền editor trở lên HOẶC là admin
    if not ((post.user_id == current_user.id and current_user.is_editor()) or current_user.is_admin):
        abort(403)
        
    db.session.delete(post)
    db.session.commit()
    flash('Bài viết đã được xóa!', 'success')
    return redirect(url_for('main.index'))
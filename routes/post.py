from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app, url_for
from flask_login import login_required, current_user
from models import db, Post, User
from forms import PostForm
import os
import secrets
from werkzeug.utils import secure_filename
from datetime import datetime
from models import Comment
from forms import CommentForm

post_bp = Blueprint('post', __name__)

def save_image(form_image):
    # Tạo tên ngẫu nhiên cho file hình ảnh
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + f_ext
    
    # Tạo đường dẫn đến thư mục static/uploads (đường dẫn chính xác)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(current_dir)  # Đi lên 1 cấp từ thư mục routes
    upload_dir = os.path.join(app_dir, 'static', 'uploads')
    
    # Đảm bảo thư mục tồn tại
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Lưu file hình ảnh
    image_path = os.path.join(upload_dir, image_filename)
    form_image.save(image_path)
    
    # Trả về đường dẫn tương đối cho URLs
    return 'uploads/' + image_filename

@post_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            image_path = save_image(form.image.data)
            
        post = Post(
            title=form.title.data,
            content=form.content.data,
            image_path=image_path,
            date_posted=datetime.utcnow(),
            user_id=current_user.id
        )
        
        db.session.add(post)
        db.session.commit()
        flash('Bài viết đã được tạo thành công!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('post/create_post.html', 
                          title='Bài Viết Mới', 
                          form=form, 
                          legend='Tạo Bài Viết Mới')


@post_bp.route('/user/<string:username>/posts')
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).all()
    return render_template('post/user_posts.html', posts=posts, user=user)

@post_bp.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
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
    return render_template('post/create_post.html', 
                          title='Cập Nhật Bài Viết', 
                          form=form, 
                          legend='Cập Nhật Bài Viết')

@post_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    
    # Xóa file ảnh nếu có
    if post.image_path:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_dir = os.path.dirname(current_dir)
        image_path = os.path.join(app_dir, 'static', post.image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(post)
    db.session.commit()
    flash('Bài viết đã được xóa!', 'success')
    return redirect(url_for('main.index'))

@post_bp.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        posts = Post.query.filter(Post.title.contains(query) | Post.content.contains(query)).all()
    else:
        posts = []
    
    return render_template('post/search_results.html', 
                          title='Kết Quả Tìm Kiếm', 
                          posts=posts, 
                          query=query)

@post_bp.route('/posts')
def all_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('post/all_posts.html', posts=posts)

# Cập nhật route xem chi tiết bài viết để có form bình luận
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

# Thêm route để xử lý đăng bình luận
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

# Thêm route để xóa bình luận
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

@post_bp.route('/debug-uploads')
def debug_uploads():
    """Route để kiểm tra thư mục uploads và hiển thị các hình ảnh đã tải lên"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(current_dir)
    upload_dir = os.path.join(app_dir, 'static', 'uploads')
    
    files = []
    if os.path.exists(upload_dir):
        files = os.listdir(upload_dir)
    
    # Lấy danh sách bài viết có hình ảnh
    posts_with_images = Post.query.filter(Post.image_path.isnot(None)).all()
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Debug Uploads</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .debug-info {{ background: #f5f5f5; padding: 15px; margin-bottom: 20px; border-radius: 5px; }}
            .file-list {{ display: flex; flex-wrap: wrap; gap: 20px; }}
            .file-item {{ border: 1px solid #ddd; padding: 10px; border-radius: 5px; width: 250px; }}
            .file-item img {{ max-width: 100%; max-height: 150px; display: block; margin: 10px 0; }}
            .post-list {{ margin-top: 30px; }}
            .post-item {{ border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }}
            .post-item img {{ max-width: 300px; max-height: 200px; margin-top: 10px; }}
            h2, h3 {{ color: #333; }}
        </style>
    </head>
    <body>
        <h1>Debug Thông tin Upload</h1>
        
        <div class="debug-info">
            <h2>Thông tin Thư mục</h2>
            <p><strong>Current directory:</strong> {current_dir}</p>
            <p><strong>App directory:</strong> {app_dir}</p>
            <p><strong>Upload directory:</strong> {upload_dir}</p>
            <p><strong>Directory exists:</strong> {os.path.exists(upload_dir)}</p>
            <p><strong>Total files in directory:</strong> {len(files)}</p>
        </div>
        
        <h2>Danh sách Files trong thư mục uploads</h2>
        <div class="file-list">
    """
    
    if files:
        for file in files:
            file_path = os.path.join(upload_dir, file)
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            image_url = url_for('static', filename=f'uploads/{file}')
            
            html += f"""
            <div class="file-item">
                <p><strong>Tên file:</strong> {file}</p>
                <p><strong>Kích thước:</strong> {file_size} bytes</p>
                <p><strong>URL:</strong> <a href="{image_url}" target="_blank">{image_url}</a></p>
                <img src="{image_url}" alt="{file}">
            </div>
            """
    else:
        html += "<p>Không có file nào trong thư mục uploads</p>"
    
    html += """
        </div>
        
        <div class="post-list">
            <h2>Bài viết có hình ảnh trong database</h2>
    """
    
    if posts_with_images:
        for post in posts_with_images:
            image_url = url_for('static', filename=post.image_path)
            
            html += f"""
            <div class="post-item">
                <h3>Post ID: {post.id} - {post.title}</h3>
                <p><strong>Đường dẫn lưu trong DB:</strong> {post.image_path}</p>
                <p><strong>URL đầy đủ:</strong> <a href="{image_url}" target="_blank">{image_url}</a></p>
                <p><strong>Test hiển thị:</strong></p>
                <img src="{image_url}" alt="{post.title}">
            </div>
            """
    else:
        html += "<p>Không có bài viết nào có hình ảnh trong database</p>"
    
    html += """
        </div>
        
        <div>
            <h2>Bước tiếp theo</h2>
            <ul>
                <li>Kiểm tra các đường dẫn URL hiển thị trên trang này</li>
                <li>Xem hình ảnh có hiển thị ở mục "Test hiển thị" không</li>
                <li>Đảm bảo đường dẫn lưu trong DB khớp với cấu trúc thư mục</li>
                <li>Kiểm tra quyền truy cập thư mục uploads</li>
            </ul>
            <p><a href="/">Trở về trang chủ</a></p>
        </div>
    </body>
    </html>
    """
    
    return html

@post_bp.route('/fix-image-paths')
@login_required
def fix_image_paths():
    """Route để sửa đường dẫn ảnh trong database nếu cần"""
    posts_with_images = Post.query.filter(Post.image_path.isnot(None)).all()
    fixed_count = 0
    
    for post in posts_with_images:
        # Kiểm tra nếu đường dẫn hiện tại chứa 'flask-auth-website/static/'
        if 'flask-auth-website/static/' in post.image_path:
            # Sửa lại đường dẫn
            post.image_path = post.image_path.split('flask-auth-website/static/')[1]
            fixed_count += 1
        
        # Hoặc nếu đường dẫn hiện tại chứa 'static/'
        elif post.image_path.startswith('static/'):
            # Sửa lại đường dẫn
            post.image_path = post.image_path[7:]  # Cắt bỏ 'static/'
            fixed_count += 1
    
    if fixed_count > 0:
        db.session.commit()
        return f"Đã sửa {fixed_count} đường dẫn hình ảnh trong database"
    else:
        return "Không có đường dẫn nào cần sửa"
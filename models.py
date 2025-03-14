from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user', lazy=True)
    # Thêm trường role để phân quyền người dùng
    role = db.Column(db.String(20), default='viewer')  # 'viewer', 'collaborator', 'editor'

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    # Thêm các phương thức kiểm tra quyền
    def is_viewer(self):
        return self.role == 'viewer' or self.role == 'collaborator' or self.role == 'editor' or self.is_admin
    
    def is_collaborator(self):
        return self.role == 'collaborator' or self.role == 'editor' or self.is_admin
    
    def is_editor(self):
        return self.role == 'editor' or self.is_admin
    
    def __repr__(self):
        return f"User('{self.username}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_hidden = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    is_hidden = db.Column(db.Boolean, default=False)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))
    
    def __repr__(self):
        return f"Comment('{self.content[:20]}...', '{self.date_posted}')"
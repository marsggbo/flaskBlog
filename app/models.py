#coding=utf-8

from app import db
from flask_login import UserMixin
from app import loginManager
from werkzeug.security import generate_password_hash,check_password_hash
import bleach,markdown

ROLE_USER = 0
ROLE_ADMIN = 1


@loginManager.user_loader
def load_user(user_id):
	try:
		return User.query.get(int(user_id))
	except Exception as e:
		print(str(e))

class User(UserMixin,db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), unique = True)
	email = db.Column(db.String(120), unique = True)
	# posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
	articles = db.relationship('Article', backref = 'author', lazy = 'dynamic')
	password_hash = db.Column(db.String(128), unique=False)

	@property
	def password(self):
		raise AttributeError('不能直接获取明文密码！')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User %r>' % (self.username)

# class Post(db.Model):
# 	__tablename__ = 'post'
# 	id = db.Column(db.Integer, primary_key = True)
# 	body = db.Column(db.String(140))
# 	timestamp = db.Column(db.DateTime)
# 	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
# 	def __repr__(self):
# 		return '<Post %r>' % (self.body)

class Article(db.Model):
	__tablename__ = 'article'
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(64))
	tags = db.Column(db.String(64))
	categories = db.Column(db.String(64))
	content = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<article %r>' % (self.title)

	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		# 需要转换的标签
		allowed_tags = [
			'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
			'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
			'h1', 'h2', 'h3', 'p', 'img'
		]
		# 需要提取的标签属性，否则会被忽略掉
		attrs = {
			'*': ['class'],
			'a': ['href', 'rel'],
			'img': ['src', 'alt']
		}
		target.content_html = bleach.linkify(
			bleach.clean(
				markdown(value, output_format='html'),
				tags=allowed_tags,
				attributes=attrs,
				strip=True
			)
		)

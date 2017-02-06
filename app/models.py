#coding=utf-8

from app import db
from flask_login import UserMixin
from app import loginManager
from werkzeug.security import generate_password_hash,check_password_hash


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
	def generate_fake_data(count=100):
		from sqlalchemy.exc import IntegrityError
		from random import seed,randint
		import forgery_py,datetime

		u = User.query.get(1)
		seed()
		articles = []
		for i in range(count):
			a = Article(title=forgery_py.lorem_ipsum.title(),
			            tags=forgery_py.lorem_ipsum.words(quantity=randint(1, 5)),
			            categories=forgery_py.lorem_ipsum.word(),
			            content=forgery_py.lorem_ipsum.sentences(randint(1, 20)),
			            timestamp=forgery_py.date.date(True),
			            author=u)
			articles.append(a)
		try:
			db.session.add_all(articles)
			db.session.commit()
		except Exception as e:
			print(str(e))


# class Tag(db.Model):
# 	__tablename__ = 'tag'
# 	id = db.Column(db.Integer, primary_key = True)
# 	tag = db.Column(db.String(64),unique=True)
#
# 	def __repr__(self):
# 		return '<tag %r>' % (self.tag)
#
# class Category(db.Model):
# 	__tablename__ = 'category'
# 	id = db.Column(db.Integer, primary_key = True)
# 	category = db.Column(db.String(64),unique=True)
#
# 	def __repr__(self):
# 		return '<category %r>' % (self.category)
#coding=utf-8

from flask import render_template,flash,redirect,url_for,session,g,request
from flask_login import login_user,logout_user,current_user,login_required
from app import app,db,loginManager
from .forms import LoginForm,ArticleForm
from .models import User,Article

from flask import Markup
import markdown

import datetime

@app.route('/')
@app.route('/index')
def index(): 
	form = LoginForm()
	isLogin = False
	if session.get('remember_me'):
		hasLogin = True
	return render_template('index.html',title = 'Home',isLogin=isLogin)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data is None or form.email.data == '':
			flash('Invalid login.Please try again!')
			return redirect(url_for('login'))
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and form.password.data == user.password_hash:
			session['remember_me'] = form.remember_me.data
			session['email'] = form.email.data
			login_user(user,form.remember_me.data)
			return redirect(request.args.get('next') or url_for('index',isLogin=True))
		flash('Invalid username or password.')
	return render_template('login.html', title='Sign In',form=form)

@app.route('/logout')
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('index'))

@app.route('/about')
def about():
	aboutPage = '../templates/index.html'
	return render_template('about.html',aboutPage=aboutPage)

@app.route('/aboutMe')
def aboutMe():
	return render_template('aboutMe.html')


@app.route('/edit',methods=['GET','POST'])
@login_required
def edit():
	form = ArticleForm()
	if form.validate_on_submit():
		# 文章内容以markdown的格式存储，需要显示页面时可通过markdown模块解析后显示。如
		# print(markdown.markdown(form.content.data))
		article = Article(title=form.title.data,
			tags=form.tags.data,
			category=form.category.data,
			content=form.content.data,
			timestamp=datetime.datetime.utcnow(),
			author=current_user._get_current_object())
		try:
			db.session.add(article)
			db.session.commit()
		except Exception as e:
			print(str(e))
		return redirect(url_for('index'))

	return render_template('edit.html',form=form)

@app.route('/tags')
def tags():
	code ='''
	print(123)
	def hello():
		print('hello world!')
	'''
	code = Markup(markdown.markdown(code))
	return render_template('tags.html',code=code)

@app.route('/categories')
def categories():
	code = '''
	# header
	## herder2
	- list1
	- list2
	**bold**
	'''
	return render_template('categories.html',code=code)

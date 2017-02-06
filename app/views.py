#coding=utf-8

from flask import render_template,flash,redirect,url_for,session,g,request,current_app
from flask_login import login_user,logout_user,current_user,login_required
from app import app,db,loginManager,bootstrap
from .forms import LoginForm,ArticleForm
from .models import User,Article

from flask import Markup
import markdown

import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	page_index = request.args.get('page',1,type=int)
	pagination = Article.query.order_by(Article.timestamp.desc()).paginate(
		page_index,per_page=current_app.config['FLASK_ARTICLE_PER_PAGE'],error_out=False
	)
	articles = pagination.items
	article_footer = '''
<br><br><br><hr style='color:rgb(204,204,204)'>
'''
	return render_template('index.html',
	                       title = 'Home',
	                       articles=articles,
	                       pagination=pagination,
	                       article_footer=article_footer)

@app.template_filter('md')
def markdown_to_html(md):
	return markdown.markdown(md, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])

@app.template_filter('abstract')
def abstract_article(article):
	if len(article) > 400:
		return article[:400]
	else:
		return article


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

	if request.method == 'POST':
		if form.title.data and (form.categories.raw_data) and len(form.tags.data) and form.content.data:
			# 文章内容以markdown的格式存储，需要显示页面时可通过markdown模块解析后显示。如
			# print(Makeup(markdown.markdown(form.content.data)))
			tags_data = str(form.tags.raw_data).replace("[",'').replace("]",'').replace("'",'')
			categories_data = str(form.categories.raw_data).replace("[",'').replace("]",'').replace("'",'')
			article = Article(title=form.title.data,
			                  tags=tags_data,
			                  categories=categories_data,
			                  content=form.content.data,
			                  timestamp=datetime.datetime.utcnow(),
			                  author=current_user._get_current_object())
			try:
				db.session.add(article)
				db.session.commit()
			except Exception as e:
				print(str(e))
			return redirect(url_for('index'))
		else:
			return redirect(url_for('edit',warning=True))

	return render_template('edit.html',form=form,warning=False)

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

@app.route('/archives')
def archives():
	return render_template('archives.html')

@app.route('/test')
def test():
	return render_template('test.html')
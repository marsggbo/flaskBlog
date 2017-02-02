#coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Required
from app.models import Article

from flask_pagedown.fields import PageDownField

class LoginForm(FlaskForm):
	"""docstring for LoginForm"""
	# username = StringField('Username',validators=[DataRequired()])
	email = StringField('Email',validators=[DataRequired()])
	password = StringField('Password',validators=[DataRequired()])
	remember_me = BooleanField('Remember me?',default=False)
	submit = SubmitField('Submit')

def getUserFactory():
	return Article.query

class ArticleForm(FlaskForm):
	title = StringField(u"标题", validators=[DataRequired()])
	# category = QuerySelectField(u"分类", query_factory=getUserFactory(), get_label='name')
	categories = StringField(u'分类',validators=[DataRequired()])
    # categories = SelectMultipleField(u'分类', coerce=int,validators=[DataRequired()])
	tags = StringField(u"标签", validators=[DataRequired()]) #这里本来准备绑定到`models.py`定义的`Tag`表的，但是`WTFORMS`貌似没有这种字段，只有用字符串来表示了
	content = TextAreaField(u"正文", validators=[DataRequired()])
	submit = SubmitField(u"发布")

	def __init__(self):
		super(ArticleForm,self).__init__()

#coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,TextAreaField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired,Required
from app import db
from app.models import Article


class LoginForm(FlaskForm):
	"""docstring for LoginForm"""
	# username = StringField('Username',validators=[DataRequired()])
	email = StringField('Email',validators=[DataRequired()])
	password = StringField('Password',validators=[DataRequired()])
	remember_me = BooleanField('Remember me?',default=False)
	submit = SubmitField('Submit')

def parseData(data):
	result = []
	for item in data:
		if ',' in item:
			for i in range(len(item.split(','))):
				result.append(item.split(',')[i])
		else:
			result.append(item)
	return list(set(result))

def doubleData(data):
	result = []
	for item in data:
		result.append([item,item])
	return result

class ArticleForm(FlaskForm):
	# 读取数据库中分类的数据，并同步至表单

	choices_categories = [item.categories for item in Article.query.all()]
	choices_tags = [item.tags for item in Article.query.all()]
	# 标签去重&多标签解析
	choices_categories = parseData(choices_categories)
	choices_tags = parseData(choices_tags)
	# 生成choices
	choices_tags = doubleData(choices_tags)
	choices_categories = doubleData(choices_categories)

	categories = SelectField(u'分类', choices=choices_categories, validators=[DataRequired()])
	tags = SelectMultipleField(u"标签", choices=choices_tags,validators=[DataRequired()])
	title = StringField(u"标题", validators=[DataRequired()])
	content = TextAreaField(u"正文", validators=[DataRequired()])
	submit = SubmitField(u"发布")

	def __init__(self):
		super(ArticleForm,self).__init__()



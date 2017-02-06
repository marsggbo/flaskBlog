#coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

import os
from config import basedir

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# 延迟创建app
loginManager = LoginManager()
loginManager.init_app(app)

loginManager.session_protection = "strong"
#可以设置None,'basic','strong'  以提供不同的安全等级,一般设置strong,如果发现异常会登出用户
 
loginManager.login_view = "login"
#这里填写你的登陆界面的路由

bootstrap = Bootstrap(app)
from app import views,models


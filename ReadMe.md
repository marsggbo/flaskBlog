---
title: MarsBlog
tags: python,flask,博客
grammar_cjkRuby: true
---

很久之前就想着自己做一个博客，能力有限一直拖着，当然现在能力也还是有限，所以实现的效果还有很多需要提高的地方。放在github上希望能一起学习，一起进步~~


# 更新日志


----------
## **2017.2.2**

### 1、博客架构
该博客使用**flask**框架搭建，博客架构为
- 首页 HOME
- 分类 Category
- 标签 Tag
- 关于 About
- 编辑文章 Edit
- 登录\登出 Login\Logout


### 2、开发环境
- python3.4
- Windows10(没钱买mac，没有讽刺Windows的意思啊~~)
- sublime text3
- Pycharm Pro(用了学校邮箱，免费的，吼吼)
- Chrome
- cmder (良心推荐，比Windows自带命令行好一万倍。)

![cmder][1]
- python包含的库
> flask
flask-login==0.2.11
flask-mail
flask-sqlalchemy
sqlalchemy-migrate
flask-wtf
markdown
flask-markdown

可使用pip命令安装
```
pip install -r requirements.txt
```

### 3、代码结构


### 4、运行代码
```hell
$ venv3\script\activate
$ (venv3)python run.py
```

### 5、已实现功能
- **1) 关于页面(About)**
使用bootstrap模板，自我感觉还不错。

![about][2]
参考：[Kelvin – Resume Theme][3]

- **2) 编辑页面(Edit)**
flask-markdown模块用了好久都不行，所以使用editormd插件，非常方便。存储数据库的时候文章内容存储的是markdown的格式，需要显示页面的时候只需导入markdown模块即可，用法如下：

```python
markdown_text = "# 一级标题"

import markdown
html_text = markdown.markdown(markdown_text)
```

![edit][4]

参考：[Flask实现Markdown在线编辑与解析][5]

- **3) 登录登出页面**
使用flask-login模块，确实好用，但是初次接触感觉有点麻烦，以后再慢慢深入学习吧。

![login][6]

参考：[用户登录][7]


  [1]: ./images/cmder.png "cmder.png"
  [2]: ./images/about.png "about.png"
  [3]: http://blacktie.co/2013/10/kelvin-resume-theme/
  [4]: ./images/edit.png "edit.png"
  [5]: https://www.cdxy.me/?p=719
  [6]: ./images/login.png "login.png"
  [7]: http://www.pythondoc.com/flask-mega-tutorial/userlogin.html
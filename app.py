#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, request, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)


# 模型类声明都要继承db.Model
class User(db.Model):
    """
    db.Column() 传入的参数决定了字段的类型
    Integer：整形  String（size）：字符串（最大长度）
    Text：长文本  DateTime：时间日期   Float 浮点数
    BooLean 布尔值
    还可以传入额外的选项对字段进行设置：
    primary_key设置当前字段是否为主键（布尔值）
    index（布尔值，是否设置索引）
    nullable（布尔值，设置是否运行为空值）
    unique（布尔值，设置是否可以为重复值）
    default（设置默认值）
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))
    director = db.Column(db.String(20))


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


# 定义模板上下文处理函数 该函数的返回值将会统一注入到每个模板的上下文环境，可以在模板中直接使用
@app.context_processor
def user_all():
    user = User.query.first()
    return dict(user=user)


@app.route("/")
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route("/hello")
def get_name():
    return "hello"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)

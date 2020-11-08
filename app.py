#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask, request, url_for, render_template, flash, redirect
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

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
# 写入SQLALCHEMY_DATABASE_URI配置变量来告诉数据库连接地址（数据库文件的绝对地址）
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 初始化扩展，传入程序实例APP
db = SQLAlchemy(app)


# 创建的两个模型类来表示两个表（user 和 movies）
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


# 注册为命令：在flask中输入命令执行该函数的内容
@app.cli.command()
def forge():
    """创建表"""
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
    # 创建一条记录
    user = User(name=name)
    # 提交的数据库会话(如git的工作区)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    # 提交的数据库，只需在最后执行一次
    db.session.commit()
    click.echo('Done.')


# 定义模板上下文处理函数 该函数的返回值将会统一注入到每个模板的上下文环境，可以在模板中直接使用
@app.context_processor
def user_all():
    user = User.query.first()
    return dict(user=user)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'GET':
        movies = Movie.query.all()
        return render_template('index.html', movies=movies)
    if request.method == 'POST':
        # 如果是post方式，则读取表单的数据，没读到则提示且返回主页
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.Chick Your Input')
            return redirect(url_for('index'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Creat succeed')
        return redirect(url_for('index'))
    # 不是POST和GET情况， 提高鲁棒性
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route("/movie/edit/<int:movie_id>", methods=['POST', 'GET'])
def edit(movie_id):
    """
    修改记录
    <int:movie_id> 部分表示 URL 变量，
    而 int 则是将变量转换成整型的 URL 变量转换器。
    在生成这个视图的 URL 时，我们也需要传入对应的变量，
    比如 url_for('edit', movie_id=2) 会生成 /movie/edit/2。
    """
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input')
            # 重定向响应，向新的URL发出请求
            return redirect(url_for('edit', movir_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POsT'])
def delete(movie_id):
    # get_or_404:如名 返回对应主键的记录，没有找到则直接返回404响应
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)

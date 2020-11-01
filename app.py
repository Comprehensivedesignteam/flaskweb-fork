#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
from flask import request, url_for
from flask import render_template

app = Flask('app')

name = 'BeiChuan Zhang'
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


@app.route("/")
def index():
    return render_template('index.html', name=name, movies=movies)


@app.route("/test")
def test_url_for():
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'


@app.route("/userprofile", methods=('POST', 'GET'))
def get_userprofile():

    if request.method=='GET':
        name = request.args.get('name', ' ')
        if name=='zbc':
            return dict(name='zbc from get', fans=10000)
        else:
            return dict(name='gsl', fans=10000000)
    elif request.method == 'POST':
        print(request.form)
        print(request.json)
        print(request.date)


if __name__ == "__main__":
    app.run(debug=True)

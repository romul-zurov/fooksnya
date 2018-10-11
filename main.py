#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from sanic.response import json as json_response
from sanic_session import Session
from sanic_jinja2 import SanicJinja2

from sanic import Sanic
app = Sanic()
Session(app)
jinja = SanicJinja2(app)
app.static('/static', './static')


@app.route('/')
@jinja.template('index.html')
async def test(request):
    return {'info': 'в разработке :)'}

@app.route('/vk-callback')
async def test(request):
    print(request.args)
    return json_response('')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8901)

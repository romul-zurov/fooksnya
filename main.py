#!/usr/bin/env python3.7
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8901)

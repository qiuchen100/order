# -*- coding: utf-8 -*-
from web.controllers.index import route_index


def register_blueprint(app):
    app.register_blueprint(route_index, url_prefix='/')

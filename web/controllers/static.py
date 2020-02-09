# -*- coding: utf-8 -*-

from flask import Blueprint, send_from_directory, current_app


route_static = Blueprint('static', __name__)


@route_static.route('/<path:filename>')
def index(filename):
    return send_from_directory(current_app.root_path + current_app.static_folder, filename)

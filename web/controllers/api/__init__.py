# -*- coding: utf-8 -*-
from flask import Blueprint


route_api = Blueprint('api', __name__)

from web.controllers.api.member import *


@route_api.route("/")
def index():
    return "Mina Api V1.0~"
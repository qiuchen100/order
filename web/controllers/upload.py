# -*- coding: utf-8 -*-
from flask import Blueprint


route_upload = Blueprint('upload_page', __name__)


@route_upload.route('/ueditor', methods=['GET', 'POST'])
def ueditor():
    pass
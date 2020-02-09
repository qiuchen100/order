# -*- coding: utf-8 -*-
from common.libs.urlManager import UrlManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import os
from www import register_blueprint


class Application(Flask):
    def __init__(self, import_name):
        super(Application, self).__init__(
            import_name, static_folder='web/static', template_folder='web/templates')
        self.config.from_pyfile('config/base_setting.py')
        if 'ops_config' in os.environ:
            self.config.from_pyfile(
                'config/{}_setting.py'.format(os.environ['ops_config']))
        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__)
manager = Manager(app)
register_blueprint(app)


'''
函数模板
'''
app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')

# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

import sys
reload(sys)
sys.setdefaultencoding('utf8')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

CSRF_ENABLED = True
SECRET_KEY = '201292066'
FRIENDS_LINKS = [
    { 'name': u'Python教程', 'url': 'http://www.runoob.com/python/python-tutorial.html' },
    { 'name': u'Flask', 'url': 'https://www.jianshu.com/p/836ea309c81f' },
    { 'name': u'Bootstrap', 'url': 'http://www.runoob.com/bootstrap/bootstrap-tutorial.html' },
    { 'name': u'Html+Css', 'url': 'http://www.runoob.com/css/css-tutorial.html' },
    { 'name': u'Git教程', 'url': 'http://www.runoob.com/git/git-basic-operations.html'}]

UPLOADED_AVATAR_DEST = os.path.join(basedir,"app/static/img/avatar")
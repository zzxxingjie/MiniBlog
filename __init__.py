# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_ckeditor import CKEditor

# -*- flask -*-
app = Flask(__name__)

# -*- config -*-
app.config.from_object('config')

# -*- sqlalchemy -*-
db = SQLAlchemy(app) 

# -*- bootstrap -*-
bootstrap=Bootstrap(app)

# -*- user:login -*-
lm = LoginManager()
lm.setup_app(app) 

# -*- user:avatar -*-
avatar = UploadSet('AVATAR',IMAGES)
configure_uploads(app,avatar)

# -*- blog:ckeditor -*-
ckeditor = CKEditor(app)

from app import views, models
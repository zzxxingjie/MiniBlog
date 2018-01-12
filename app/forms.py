# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app import avatar

# -*- user: loginForm -*-
class LoginForm(FlaskForm):
    email = StringField(u'邮箱', validators = [DataRequired(message = u'请填写邮箱'), Email(u'邮箱格式不正确')])
    password = PasswordField(u'密码', validators = [DataRequired(message = u'请填写密码')])

# -*- user: SignUpForm -*-
class SignUpForm(FlaskForm):
    nickname = StringField(u'昵称', validators = [DataRequired(message = u'请输入昵称'), Length(max = 20,message = u'不能超过20个字符')])
    email = StringField(u'邮箱', validators = [DataRequired(message = u'请填写邮箱'), Email(u'邮箱格式不正确')])
    password = PasswordField(u'密码', validators = [DataRequired(message = u'请填写密码'), Length(6, 20, u'密码长度6~20位')])

# -*- user: UploadForm -*-
class UploadForm(FlaskForm):
    avatar = FileField(validators=[FileAllowed(avatar, u'只能上传图片格式'), FileRequired(u'请选择图片')])

# -*- user: UpdateProfileForm -*-
class UpdateProfileForm(FlaskForm):
    about_me = TextAreaField(u'内容')

# -*- blog: PublishBlogForm -*-
class PublishBlogForm(FlaskForm):
    title = StringField(u'标题', validators = [DataRequired(message = u'标题不能为空')])
    body = TextAreaField(u'博客内容', validators = [DataRequired(message = u'内容不能为空')])
    tag = SelectField('tag', choices=[
        ('Python', 'Python'),
        ('Flask', 'Flask'),
        ('Bootstrap', 'Bootstrap'),
        ('Sql', 'Sql'),
        ('Css','Css')
    ])

# -*- comment: PublishCommentForm -*-
class PublishCommentForm(FlaskForm):
    body = TextAreaField(u'内容',validators = [DataRequired(message = u'请填写评论')] )
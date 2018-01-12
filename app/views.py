# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, flash, url_for, session, g
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, SignUpForm, UploadForm, PublishBlogForm, PublishCommentForm, UpdateProfileForm
from models import User, Blog, Comment
from app import app, db, lm, avatar
import datetime

per_page = 5

# -*- index -*-
@app.route('/')
@app.route('/<int:page>')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page = 1):
    pagination = Blog.query.order_by(Blog.create_at.desc()).paginate(page, per_page,error_out=False)
    blogs = pagination.items
    return render_template('index.html', blogs = blogs, pagination = pagination, links = app.config['FRIENDS_LINKS'])

# -*- user:any user? -*-
@app.before_request
def before_request():
    g.user = current_user

# -*- user:loader -*-
@lm.user_loader
def load_user(id):
    user = User.query.get(int(id))
    return user

# -*- user:login -*-
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data, password = form.password.data).first()
        if(user is not None):
            login_user(user)
            if(user.admin == 0):
                flash('用户登录成功！')
                return redirect(url_for('index'))
            flash('管理员登录成功！')
            return redirect(url_for('admin'))
        flash('登录失败！')
        return redirect('/login')
    return render_template('login.html',form = form)

# -*- user:logout -*-
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功！')
    return redirect(url_for('index'))

# -*- user:signup -*-
@app.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        name_check = User.query.filter_by(nickname = form.nickname.data).first()
        email_check = User.query.filter_by(email = form.email.data).first()
        if(name_check is not None or email_check is not None):
            flash('昵称或邮箱已被注册！')
            return redirect('/sign_up')
        user = User()
        user.nickname = form.nickname.data
        user.email = form.email.data
        user.password = form.password.data
        user.create_at = datetime.datetime.now()
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash('注册失败！')
            return redirect('/sign_up')
        login_user(user)
        flash('注册成功！')
        return redirect(url_for('index'))
    return render_template('sign_up.html',form = form)

# -*- user:profile -*-
@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.filter_by(id = user_id).first()
    if(user is None):
        flash('该用户尚未注册！')
        return redirect(url_for('index'))
    return render_template('profile.html', user = user)

# -*- user:upload avatar -*-
@app.route('/edit_avatar/<int:user_id>', methods = ['GET', 'POST'])
@login_required
def edit_avatar(user_id):
    form = UploadForm()
    if form.validate_on_submit():
        filename = avatar.save(form.avatar.data)
        file_url = avatar.url(filename)
        current_user.avatar = file_url
        db.session.add(current_user)
        db.session.commit()
        flash('头像上传成功！')
        return redirect(url_for('profile',user_id = current_user.id))
    return render_template('edit_avatar.html', form = form)

# -*- user:update user_information -*-
@app.route('/update_profile/<int:user_id>', methods = ['GET', 'POST'])
@login_required
def update_profile(user_id):
    form = UpdateProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id = user_id).first()
        user.about_me = form.about_me.data
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash('更改失败！')
            return redirect(url_for('update_profile', user_id = user_id))
        flash('更改成功！')
        return redirect(url_for('profile', user_id = user_id))
    return render_template('update_profile.html', form = form)



# -*- blog:publish -*-
@app.route('/publish/<int:user_id>', methods = ['GET', 'POST'])
@login_required
def publish(user_id):
    form = PublishBlogForm()
    blog = Blog()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.body = form.body.data
        blog.tag = form.tag.data
        blog.create_at = datetime.datetime.now()
        blog.user_id = user_id

        title_check = Blog.query.filter_by(title = blog.title).first()
        if(title_check is not None):
            flash('标题已被使用！')
            return redirect(url_for('publish', user_id = user_id))
        try:
            db.session.add(blog)
            db.session.commit()
        except:
            flash('发布失败，请重新发布！')
            return redirect(url_for('publish', user_id = user_id))
        flash('发布成功！')
        return redirect('/')
    return render_template('publish.html', form = form)

# -*- blog:myblogs -*-
@app.route('/myblogs')
@app.route('/myblogs/<int:page>')
@login_required
def myblogs(page = 1):
    user = current_user
    pagination = user.blogs.order_by(Blog.create_at.desc()).paginate(page, per_page, error_out=False)
    blogs = pagination.items
    return render_template('myblogs.html',blogs = blogs,pagination = pagination)

# -*- blog:delete -*-
@app.route('/delete_myblog/<int:blog_id>')
@login_required
def delete_myblog(blog_id):
    blog = Blog.query.filter_by(id = blog_id).first()
    comment = blog.comments
    try:
        db.session.delete(blog)
        db.session.commit()
    except:
        flash('删除失败！')
        return redirect('/myblogs')
    flash('博客删除成功！')
    return redirect('/myblogs')

# -*- blog:update -*-
@app.route('/update_blog/<int:blog_id>', methods = ['GET', 'POST'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.filter_by(id = blog_id).first()
    if request.method=='POST':
        blog.body = request.form.get('body')
        try:
            db.session.add(blog)
            db.session.commit()
        except:
            flash('博客更改失败！')
            return redirect(url_for('update_blog', blog_id = blog_id))
        flash('博客更改成功！')
        return redirect('/myblogs')
    return render_template('update_blog.html', blog = blog)

# -*- blog:blog and comments-*-
@app.route('/blog/<int:blog_id>', methods = ['GET', 'POST'])
def blog(blog_id):
    blog = Blog.query.filter_by(id = blog_id).first()
    if(blog is None):
        flash('查找错误，没有此博客！')
        return redirect('/index')
    blog.read_times = blog.read_times + 1
    db.session.add(blog)
    db.session.commit()

    form = PublishCommentForm()
    comment = Comment()
    if form.validate_on_submit():
        comment.body = form.body.data
        comment.create_at = datetime.datetime.now()
        comment.blog_id = blog_id
        comment.user_id = g.user.id
        try:
            db.session.add(comment)
            db.session.commit()
        except:
            flash('回复评论失败！')
            return redirect(url_for('blog', blog_id = blog_id))
        flash('评论成功！')
        return redirect(url_for('blog', blog_id = blog_id))
    return render_template('blog.html', blog = blog, form = form)


# -*- comment:my comments-*-
@app.route('/mycomments')
@app.route('/mycomments/<int:page>')
@login_required
def mycomments(page=1):
    user = current_user
    pagination = user.comments.order_by(Comment.create_at.desc()).paginate(page, per_page, error_out=False)
    comments = pagination.items
    return render_template('mycomments.html', comments =comments, pagination = pagination)

@app.route('/delete_mycomment/<int:comment_id>')
@login_required
def delete_mycomment(comment_id):
    comment = Comment.query.filter_by(id = comment_id).first()
    try:
        db.session.delete(comment)
        db.session.commit()
    except:
        flash('删除失败！')
        return redirect('/mycomments')
    flash('博客删除成功！')
    return redirect('/mycomments')

# -*- admin-*-
@app.route('/admin')
@login_required
def admin():
    if(g.user.admin == 0):
        flash('您不是管理员！')
        return redirect('/index')
    return render_template('admin.html')

# -*- admin:user_list-*-
@app.route('/user_list')
@app.route('/user_list/<int:page>')
@login_required
def user_list(page=1):
    user = User.query.filter_by(admin = 0)
    pagination = user.order_by(User.create_at.desc()).paginate(page, per_page, error_out=False)
    users = pagination.items
    return render_template('user_list.html', users = users, pagination = pagination)

# -*- admin:blog_list-*-
@app.route('/blog_list')
@app.route('/blog_list/<int:page>')
@login_required
def blog_list(page=1):
    pagination = Blog.query.order_by(Blog.create_at.desc()).paginate(page, per_page, error_out=False)
    blogs = pagination.items
    return render_template('blog_list.html', blogs = blogs, pagination = pagination)

# -*- admin:commnet_list-*-
@app.route('/comment_list')
@app.route('/comment_list/<int:page>')
@login_required
def comment_list(page=1):
    pagination = Comment.query.order_by(Comment.create_at.desc()).paginate(page, per_page, error_out=False)
    comments = pagination.items
    return render_template('comment_list.html', comments = comments, pagination = pagination)

# -*- admin:delete_user-*-
@app.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
    except:
        flash('删除用户失败！')
        return redirect('/user_list')
    flash('成功删除用户！')
    return redirect('/user_list')

# -*- admin:delete_blog-*-
@app.route('/delete_blog/<int:blog_id>')
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get(blog_id)
    try:
        db.session.delete(blog)
        db.session.commit()
    except:
        flash('删除博客失败！')
        return redirect('/blog_list')
    flash('成功删除博客！')
    return redirect('/blog_list')

# -*- admin:delete_comment-*-
@app.route('/delete_comment/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    try:
        db.session.delete(comment)
        db.session.commit()
    except:
        flash('删除评论失败！')
        return redirect('/comment_list')
    flash('成功删除评论！')
    return redirect('/comment_list')
from app import db

# -*- users -*-
class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(50), index = True, unique = True)
    email = db.Column(db.String(50), index = True, unique = True)
    password = db.Column(db.String(50))
    create_at = db.Column(db.DateTime)
    avatar = db.Column(db.String(500), default = '/static/img/avatar/1.jpg') 
    about_me = db.Column(db.String(500))
    admin = db.Column(db.Integer, default = 0)   
    blogs = db.relationship('Blog', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref = 'reviewer', lazy='dynamic')
    
    is_authenticated=True
    is_active=True
    is_anonymous=False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

# -*- blogs -*-
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), unique = True)
    body = db.Column(db.Text)
    create_at = db.Column(db.DateTime)
    like = db.Column(db.Integer, default = 0)
    read_times = db.Column(db.Integer, default = 0)
    tag = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref = 'post', lazy = 'dynamic')

    def __repr__(self):
        return '<Blog %r>' % (self.title)

# -*- comments -*-
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(50))
    create_at = db.Column(db.DateTime)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment %r>' % (self.body)
from app import db
from datetime import datetime
import re
from flask_security import UserMixin, RoleMixin


# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean())
    created = db.Column(db.DateTime, default=datetime.now())
    roles = db.relationship('Role' ,secondary=roles_users, backref=db.backref('users', lazy='dynamic')) 

    def __repr__(self):
        return '<User %r>' % self.email


# Setup Flask-Security


# Post models

def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    image = db.Column(db.String(140))
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()


    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)




class SwInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sw = db.Column(db.String(140))
    ip = db.Column(db.String(140), unique=True)
    location = db.Column(db.String(140))
    presence = db.Column(db.String(140))
    fixed_vlan = db.Column(db.String(140))
    model = db.Column(db.String(140))
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<SwInfo id: {}, sw: {}>'.format(self.id, self.sw)


class VlanInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vlanid = db.Column(db.Integer)
    vlanname = db.Column(db.String(100), unique=True)
    network = db.Column(db.String(50))
    group = db.Column(db.String(140))
    desc = db.Column(db.String(140))
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<SwInfo id: {}, vlanname: {}>'.format(self.id, self.vlanname)



import os
import datetime
from flask_login import UserMixin

from pyblog import app, bcrypt, db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(70), default="default.png")
    email = db.Column(db.String(50), nullable=False, unique=True)
    hash_password = db.Column(db.String(60), nullable=False)
    about_me = db.Column(db.String(150), nullable=False)

    posts = db.relationship("Post", back_populates="author")

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def password(self):
        return self.hash_password

    @password.setter
    def password(self, new_password):
        self.hash_password = bcrypt.generate_password_hash(new_password).decode("utf-8")

    def __repr__(self):
        return f"User({self.id}: {self.first_name} {self.last_name})" 

    def add(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.hash_password, password)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def num_public_posts(self):
        i = 0
        for _ in self.public_posts():
            i += 1
        return i

    def public_posts(self):
        return (post for post in self.posts if post.public == True)

    def update(self, **kwargs):
        for attr in kwargs.keys():
            # When updating the password, write the corresponding hash to the database instead.
            if attr == "password":
                setattr(self, "hash_password", bcrypt.generate_password_hash(kwargs["password"]))
                continue
            try:
                getattr(self, attr)
            except AttributeError:
                continue
            else:
                setattr(self, attr, kwargs[attr])
        db.session.commit()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subheading = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    level = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    public = db.Column(db.Boolean, nullable=False, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", back_populates="posts")

    @property
    def reading_time(self):
        avg_reading_speed = 250 # Average Reading Speed: 250 wpm
        return round(self.content.count(" ") / avg_reading_speed)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def hide(self):
        self.public = False
        db.session.commit()

    @classmethod
    def next_post(cls, current_post=None):
        """Given the current post, fetch the next public post, if any, written by the same author."""
        return db.session.execute(db.select(Post).filter(
            cls.id > current_post.id, 
            cls.user_id == current_post.user_id, 
            cls.public == True
            )).scalar()  

    @classmethod
    def public_posts(cls, author=None):
        if author:
            return db.session.execute(db.select(cls).filter(cls.public==True, cls.user_id==author.id)).scalars()
        return db.session.execute(db.select(cls).filter(cls.public==True)).scalars() 

    @classmethod
    def previous_post(cls, current_post=None): 
        """Given the current post, fetch the next public post, if any, written by the same author.""" 
        return db.session.execute(db.select(Post).order_by(cls.id.desc()).filter(
            cls.id < current_post.id, 
            cls.user_id == current_post.user_id, 
            cls.public == True
            )).scalar() 

    def show(self):
        self.public = True
        db.session.commit()

    def update(self, **kwargs):
        for attr in kwargs.keys():
            try:
                getattr(self, attr)
            except AttributeError:
                continue
            else:
                setattr(self, attr, kwargs[attr])
        db.session.commit() 

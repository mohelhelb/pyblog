import datetime
from flask_login import UserMixin
from sqlalchemy import func
import jwt

from pyblog import app, bcrypt, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


followers = db.Table(
        "followers", 
        db.Column("follower_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
        db.Column("followed_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)
        )

starred_posts = db.Table(
        "starred_posts",
        db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
        db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True)
        )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(70), default="default.png")
    email = db.Column(db.String(50), nullable=False, unique=True)
    hash_password = db.Column(db.String(60), nullable=False)
    about_me = db.Column(db.String(150), nullable=False)

    following = db.relationship(
            "User", 
            secondary=followers, 
            primaryjoin=(followers.c.follower_id == id), 
            secondaryjoin=(followers.c.followed_id == id),
            backref="followers"
            )
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

    def __lt__(self, other):
        return True if self.num_public_posts() < other.num_public_posts() else False

    def __repr__(self):
        return f"User({self.id}: {self.first_name} {self.last_name})" 

    def add(self):
        db.session.add(self)
        db.session.commit() 

    def bookmark(self, post):
        self.saved_posts.append(post)
        db.session.commit() 

    def check_password(self, password):
        return bcrypt.check_password_hash(self.hash_password, password)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def follow(self, other):
        self.following.append(other)
        db.session.commit()

    def generate_jwt(self, seconds=1800):
        return jwt.encode(
                payload={"user_id": self.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)},
                key=app.config["SECRET_KEY"],
                algorithm="HS256"
                )

    def hidden_posts(self):
        return (post for post in self.posts if not post.public)

    def num_hidden_posts(self):
        i = 0
        for _ in self.hidden_posts():
            i += 1
        return i

    def num_public_posts(self):
        i = 0
        for _ in self.public_posts():
            i += 1
        return i 

    @classmethod
    def num_users(cls):
        return db.session.scalar(func.count(cls.id)) 

    def public_posts(self):
        return (post for post in self.posts if post.public)

    def unfollow(self, other):
        self.following.remove(other)
        db.session.commit()

    def unbookmark(self, post):
        self.saved_posts.remove(post)
        db.session.commit()

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

    @classmethod
    def verify_jwt(cls, token):
        try:
            user_id = jwt.decode(token, key=app.config["SECRET_KEY"], algorithms=["HS256"])["user_id"]
        except Exception:
            return None
        return db.session.get(cls, user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subheading = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    level = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    public = db.Column(db.Boolean, nullable=False, default=True)
    views = db.Column(db.Integer, nullable=False, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", back_populates="posts") 
    saved_by = db.relationship(
            "User",
            secondary=starred_posts,
            primaryjoin=(starred_posts.c.post_id == id),
            secondaryjoin=(starred_posts.c.user_id == User.id),
            backref="saved_posts"
            )   

    @property
    def reading_time(self):
        avg_reading_speed = 250  # Average Reading Speed: 250 wpm
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

    def increase_view(self):
        self.views += 1
        db.session.commit()

    @classmethod
    def num_public_posts(cls, author=None):
        if author:
            return db.session.scalar(db.select(func.count(cls.id)).filter(cls.user_id == author.id, cls.public == 1))
        return db.session.scalar(db.select(func.count(cls.id)).filter(cls.public == 1))

    @classmethod
    def num_trending_posts(cls):
        i = 0
        for _ in cls.trending_posts():
            i += 1
        return i

    @classmethod
    def next_post(cls, current_post=None):
        """Given the current post, fetch the next public post, if any, written by the same author."""
        return db.session.execute(db.select(Post).filter(
            cls.id > current_post.id, 
            cls.user_id == current_post.user_id, 
            cls.public == 1
            )).scalar()  

    @classmethod
    def public_posts(cls, author=None):
        if author:
            return db.session.execute(db.select(cls).filter(cls.public == 1, cls.user_id == author.id)).scalars()
        return db.session.execute(db.select(cls).filter(cls.public == 1)).scalars() 

    @classmethod
    def previous_post(cls, current_post=None): 
        """Given the current post, fetch the previous public post, if any, written by the same author.""" 
        return db.session.execute(db.select(Post).order_by(cls.id.desc()).filter(
            cls.id < current_post.id, 
            cls.user_id == current_post.user_id, 
            cls.public == 1
            )).scalar() 

    def show(self):
        self.public = True
        db.session.commit()

    @classmethod
    def top_writers(cls):
        user_ids = db.session.execute(db.select(cls.user_id).filter(cls.public == 1).order_by(cls.views.desc()).limit(9)).unique().scalars()
        return [db.session.get(User, user_id) for user_id in user_ids]

    @classmethod
    def trending_posts(cls):
        return db.session.execute(db.select(cls).filter(cls.public == 1).order_by(cls.views.desc()).limit(3)).scalars()

    def update(self, **kwargs):
        for attr in kwargs.keys():
            try:
                getattr(self, attr)
            except AttributeError:
                continue
            else:
                setattr(self, attr, kwargs[attr])
        db.session.commit() 

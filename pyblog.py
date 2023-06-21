from flask import Flask, render_template
from mock_data import posts, users
from random import shuffle

app = Flask(__name__)



@app.route("/")
@app.route("/index")
def index():
    trending_posts = posts[-3:]
    return render_template("index.html", trending_posts=trending_posts, posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create/post")
def create_post():
    return render_template("create_post.html", action="Create", post=None)


@app.route("/edit/post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = posts[post_id]
    return render_template("create_post.html", action="Edit", post=post)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = posts[post_id]
    return render_template("post.html", post=post)

@app.route("/posts/<author>")
def posts_written_by(author):
    user = [user for user in users if user["full_name"] == author][0]
    posts_by_author = [post for post in posts if post["author"] == author]
    return render_template("posts_by_author.html", user=user, posts_by_author=posts_by_author)


@app.route("/reset-password")
def reset_before_email():
    return render_template("reset_before_email.html")

@app.route("/reset-password/token")
def reset_after_email():
    return render_template("reset_after_email.html")


@app.route("/profile/<int:user_id>")
def profile(user_id):
    user = [user for user in users if user["user_id"] == user_id][0]
    return render_template("profile.html", user=user)

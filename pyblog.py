from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


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
    return render_template("create_post.html")

@app.route("/post/<int:post_id>")
def post(post_id):
    return render_template("post.html")

@app.route("/posts/<author>")
def posts_written_by(author):
    return render_template("postsByAuthor.html")


@app.route("/resetPassword")
def reset_before_email():
    return render_template("resetBeforeEmail.html")

@app.route("/resetPassword/token")
def reset_after_email():
    return render_template("resetAfterEmail.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")

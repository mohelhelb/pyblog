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

@app.route("/post")
def post():
    return render_template("post.html")

@app.route("/resetPassword")
def resetBeforeEmail():
    return render_template("resetBeforeEmail.html")

@app.route("/resetPassword/token")
def resetAfterEmail():
    return render_template("resetAfterEmail.html")

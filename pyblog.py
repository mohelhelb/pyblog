from flask import Flask, render_template, request
from wtforms import Form, PasswordField, StringField, TextAreaField
from wtforms.validators import Email, InputRequired, Length

from forms import ChangePasswordForm, CreatePostForm, EmailTokenForm, ImageForm, ProfileForm, SigninForm, SignupForm
from config import DevelopmentConfig

from mock_data import posts, users
from random import shuffle

app = Flask(__name__) 

# Configuration
app.config.from_object(DevelopmentConfig) 

# Pending
shuffle(posts)

@app.route("/")
@app.route("/index")
def index():
    public_posts = [post for post in posts if post["status"] == "public"]  
    trending_posts = sorted(public_posts, key=lambda post: post["views"], reverse=True)[:3]
    return render_template("index.html", public_posts=public_posts, trending_posts=trending_posts) 


@app.route("/posts/<author>")
def posts_written_by(author):
    user = [user for user in users if user["full_name"] == author][0]
    public_posts_by_author = [post for post in posts if post["author"] == author and post["status"] == "public"]
    return render_template("posts_by_author.html", public_posts_by_author=public_posts_by_author, user=user) 


@app.route("/register", methods=["GET", "POST"])
def register():
    # WTForms library:
    # form = SignupForm(request.form)
    # if request.method == "POST" and form.validate():
    #   ...
    form = SignupForm()
    if form.validate_on_submit():
        return "Pending"
    return render_template("register.html", form=form) 


@app.route("/login", methods=["GET", "POST"])
def login():
    form = SigninForm()
    if form.validate_on_submit():
        return "Pending"
    return render_template("login.html", form=form) 


@app.route("/profile/<int:user_id>", methods=["GET", "POST"])
def profile(user_id): 
    image_form = ImageForm() 
    profile_form = ProfileForm()
    user = [user for user in users if user["user_id"] == user_id][0] 
    if request.method == "GET" or "submit_image" in request.form:  
        profile_form.first_name.data = user["first_name"]
        profile_form.last_name.data = user["last_name"]
        profile_form.email.data = user["email"]
        profile_form.about_me.data = user["about_me"] 
        if image_form.validate_on_submit():
            return "Pending I" 
    if "submit_profile" in request.form and profile_form.validate_on_submit():
        return "Pending II"
    return render_template("profile.html", profile_form=profile_form, image_form=image_form, user=user)  


@app.route("/reset-password", methods=["GET", "POST"])
def email_token():
    form = EmailTokenForm()
    if form.validate_on_submit():
        return "Pending"
    return render_template("email_token.html", form=form)  


@app.route("/reset-password/token", methods=["GET", "POST"])
def reset_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        return "Pending"
    return render_template("choose_password.html", form=form) 


@app.route("/change-password/<int:user_id>", methods=["GET", "POST"])
def change_password(user_id):
    form = ChangePasswordForm()
    if form.validate_on_submit():
        return "Pending"
    return render_template("choose_password.html", form=form)  

 
@app.route("/post/create", methods=["GET", "POST"])
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        return "Pending"
    return render_template("create_post.html", action="Create", form=form)  


@app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    form=CreatePostForm()
    post = posts[post_id]
    if form.validate_on_submit():
        return "Pending"
    if request.method == "GET":
        form.title.data = post["title"]
        form.subheading.data = post["subheading"]
        form.content.data = post["content"]
        form.level.data = post["level"]
    return render_template("create_post.html", action="Edit", form=form) 
###



@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/post/<int:post_id>")
def post(post_id):
    post = posts[post_id]
    return render_template("post.html", post=post)

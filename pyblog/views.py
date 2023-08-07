import datetime
import os
import random
from flask import abort, flash, redirect, render_template, request, url_for  

from pyblog import app, db
from pyblog.forms import ChangePasswordForm, CreatePostForm, EmailTokenForm, ImageForm, ProfileForm, SigninForm, SignupForm   
from pyblog.models import Post, User
from pyblog.pytools import Img

import pyblog.mock_data as mock_data # Pending 


@app.route("/")
@app.route("/index")
def index():
    public_posts = Post.public_posts()
    trending_posts = mock_data.trending_posts[:3] # Pending
    return render_template("index.html", public_posts=public_posts, trending_posts=trending_posts)  


@app.route("/about")
def about():
    return render_template("about.html") 


@app.route("/register", methods=["GET", "POST"])
def register():
    # WTForms library:
    # form = SignupForm(request.form)
    # if request.method == "POST" and form.validate():
    #   ...
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                email = form.email.data,
                password = form.password.data,
                about_me = form.about_me.data
                )
        user.add()
        flash("Your account has been created successfully", category="success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form) 


@app.route("/login", methods=["GET", "POST"])
def login():
    form = SigninForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()
        if user and user.check_password(form.password.data):
            flash(f"Hi, {user.first_name}! How is it going?", category="success")
            return redirect(url_for("profile", user_id=user.user_id))
        elif user: 
            flash("The password is incorrect. Please try again.", category="danger")
            return redirect(request.url) 
        flash("There is no account with that email", category="danger")
        return redirect(request.url)
    return render_template("login.html", form=form) 


@app.route("/profile/<int:user_id>", methods=["GET", "POST"])
def profile(user_id): 
    user = db.get_or_404(User, user_id) 
    image_form = ImageForm() 
    profile_form = ProfileForm()
    if "submit_image" in request.form:
        if image_form.validate():
            # Change the filename of the uploaded image.
            # If any, remove all the current images.
            # Save the uploaded image.
            img = Img(image_form.image.data)
            img.fn = f"img-{user.user_id}.{img.ext}"
            img.remove_current_imgs(user_id=user.user_id)
            img.save_uploaded_img(size=(100, 100))
            #
            user.update(image=img.fname)
            return redirect(request.url)
        profile_form.first_name.data = user.first_name
        profile_form.last_name.data = user.last_name
        profile_form.email.data = user.email
        profile_form.about_me.data = user.about_me
    elif "submit_profile" in request.form and profile_form.validate():
        user.update(
                first_name = profile_form.first_name.data,
                last_name = profile_form.last_name.data,
                email = profile_form.email.data,
                about_me = profile_form.about_me.data
                )
        return redirect(url_for("profile", user_id=user.user_id))
    if request.method == "GET":
        profile_form.first_name.data = user.first_name
        profile_form.last_name.data = user.last_name
        profile_form.email.data = user.email
        profile_form.about_me.data = user.about_me 
    return render_template("profile.html", image_form=image_form, profile_form=profile_form, user=user)


@app.route("/reset-password", methods=["GET", "POST"])
def email_token():
    form = EmailTokenForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()
        if user:
            return "Pending" 
        flash("There is no account with that email.", category="danger")
        return redirect(request.url) 
    return render_template("email_token.html", form=form)  


@app.route("/reset-password/token", methods=["GET", "POST"])
def reset_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        return "Pending"
    return render_template("choose_password.html", form=form) 


@app.route("/change-password/<int:user_id>", methods=["GET", "POST"])
def change_password(user_id):
    user = db.get_or_404(User, user_id)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.update(password=form.password.data)
        flash("Your password has been changed successfully", category="success")
        return redirect(url_for("profile", user_id=user.user_id))
    return render_template("choose_password.html", form=form)   


@app.route("/posts/<int:user_id>")
def posts_written_by(user_id):
    user = db.get_or_404(User, user_id)
    return render_template("posts_by_author.html", user=user) 
 

@app.route("/post/<int:post_id>")
def post(post_id):
    selected_post = db.get_or_404(Post, post_id)
    if not selected_post.public:
        abort(404)
    next_post = Post.next_post(current_post=selected_post)
    previous_post = Post.previous_post(current_post=selected_post)
    # Retrieve three or less random public posts written by the same author and distinct from the selected post
    posts = Post.public_posts(author=selected_post.author) 
    random_posts = [post for post in sorted(posts, key=lambda post: random.random()) if post.post_id != selected_post.post_id][:3]
    more_posts = (post for post in random_posts)
    #
    return render_template("post.html", more_posts=more_posts, selected_post=selected_post, next_post=next_post, previous_post=previous_post) 

 
@app.route("/post/create", methods=["GET", "POST"])
def create_post():
    user = db.get_or_404(User, 1) # Pending
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(
                title = form.title.data,
                subheading = form.subheading.data,
                content = form.content.data,
                level = form.level.data,
                author = user # Pending
                )
        post.add()
        flash("Your post has been created successfully!", category="success")
        return redirect(url_for("post", post_id=post.post_id)) 
    return render_template("create_post.html", action="Create", form=form)  


@app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    form=CreatePostForm()
    if form.validate_on_submit():
        post.update(
                title = form.title.data,
                subheading = form.subheading.data,
                content = form.content.data,
                level = form.level.data,
                date_posted = datetime.datetime.utcnow()
                ) 
        flash("Your post has been updated successfully!", category="success") 
        return redirect(url_for("post", post_id=post.post_id))
    if request.method == "GET":
        form.title.data = post.title
        form.subheading.data = post.subheading
        form.content.data = post.content
        form.level.data = post.level
    return render_template("create_post.html", action="Edit", form=form)          

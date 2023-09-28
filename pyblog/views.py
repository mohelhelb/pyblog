import datetime
import os
import random
from flask import abort, flash, redirect, render_template, request, url_for  
from flask_login import current_user, fresh_login_required, login_required, login_user, logout_user
from flask_mail import Message
from werkzeug.urls import url_parse

from pyblog import app, db, mail
from pyblog.forms import ChangePasswordForm, CreatePostForm, EmailTokenForm, FollowerForm, ImageForm, ProfileForm, SigninForm, SignupForm   
from pyblog.models import Post, User
from pyblog.pytools import Img


@app.route("/")
@app.route("/index")
def index():
    public_posts = Post.public_posts()
    trending_posts = Post.trending_posts()
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
    # If the current user is already authenticated and navigate to the login page, redirect them to their profile page.
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    #
    form = SigninForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc:
                next_page = url_for("profile")
            flash(f"Hi, {user.first_name}! How is it going?", category="success") 
            return redirect(next_page)
        elif user: 
            flash("The password is incorrect. Please try again.", category="danger")
            return redirect(request.url) 
        flash("There is no account with that email", category="danger")
        return redirect(request.url)
    return render_template("login.html", form=form) 


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    image_form = ImageForm() 
    profile_form = ProfileForm()
    if "submit_image" in request.form:
        if image_form.validate():
            # Change the filename of the uploaded image.
            # If any, remove all the current images.
            # Save the uploaded image.
            img = Img(image_form.image.data)
            img.fn = f"img-{current_user.id}.{img.ext}"
            img.remove_current_imgs(user=current_user)
            img.save_uploaded_img(size=(100, 100))
            #
            user.update(image=img.fname)
            return redirect(request.url)
        profile_form.first_name.data = current_user.first_name
        profile_form.last_name.data = current_user.last_name
        profile_form.email.data = current_user.email
        profile_form.about_me.data = current_user.about_me
    elif "submit_profile" in request.form and profile_form.validate():
        current_user.update(
                first_name = profile_form.first_name.data,
                last_name = profile_form.last_name.data,
                email = profile_form.email.data,
                about_me = profile_form.about_me.data
                )
        return redirect(request.url)
    if request.method == "GET":
        profile_form.first_name.data = current_user.first_name
        profile_form.last_name.data = current_user.last_name
        profile_form.email.data = current_user.email
        profile_form.about_me.data = current_user.about_me 
    return render_template("profile.html", image_form=image_form, profile_form=profile_form)  


@app.route("/change-password", methods=["GET", "POST"])
@fresh_login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.update(password=form.password.data)
        flash("Your password has been changed successfully", category="success")
        return redirect(url_for("profile", user_id=current_user.id))
    return render_template("choose_password.html", form=form) 


@app.route("/reset-password", methods=["GET", "POST"])
def email_token():
    if current_user.is_authenticated:
        flash("Please sign out first to be able to recover your account.", category="info")
        return redirect(url_for("profile"))
    form = EmailTokenForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()
        if user:
            msg = Message(
                    sender="mohelhelb@gmail.com",
                    recipients=[user.email],
                    subject="PyBlog: Verification Link",
                    body=f"""{url_for("reset_password", token=user.generate_jwt(), _external=True)}"""
                    )
            mail.send(msg)
            flash("Please check your email inbox and follow the verification link", category="success")
            return redirect(url_for("index")) 
        flash("There is no account with that email.", category="danger")
        return redirect(request.url) 
    return render_template("email_token.html", form=form)  


@app.route("/reset-password/<string:token>", methods=["GET", "POST"])
def reset_password(token): 
    if current_user.is_authenticated:
        flash("Please sign out first to be able to recover your account.", category="info")
        return redirect(url_for("profile")) 
    user = User.verify_jwt(token)
    if not user:
        flash("The verification link is invalid. Please try again", category="danger")
        return redirect(url_for("email_token"))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.update(password=form.password.data)
        flash("Your password has been changed successfully", category="success")
        return redirect(url_for("login"))
    return render_template("choose_password.html", form=form)  


@app.route("/posts/<int:user_id>")
def posts_written_by(user_id):
    user = db.get_or_404(User, user_id)
    return render_template("posts_by_author.html", user=user) 
 

@app.route("/post/<int:post_id>")
def post(post_id):
    form = FollowerForm()
    selected_post = db.get_or_404(Post, post_id)
    if not selected_post.public and selected_post.author != current_user:
        abort(403)
    next_post = Post.next_post(current_post=selected_post)
    previous_post = Post.previous_post(current_post=selected_post)
    # Retrieve three or less random public posts written by the same author and distinct from the selected post
    posts = Post.public_posts(author=selected_post.author) 
    random_posts = [post for post in sorted(posts, key=lambda post: random.random()) if post.id != selected_post.id][:3]
    more_posts = (post for post in random_posts)
    #
    # Increase the number of views by one
    if current_user != selected_post.author:
        selected_post.increase_view()
    #
    return render_template("post.html", form=form, more_posts=more_posts, selected_post=selected_post, next_post=next_post, previous_post=previous_post) 

 
@app.route("/post/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(
                title = form.title.data,
                subheading = form.subheading.data,
                content = form.content.data,
                level = form.level.data,
                author = current_user
                )
        post.add()
        flash("Your post has been created successfully!", category="success")
        return redirect(url_for("post", post_id=post.id)) 
    return render_template("create_post.html", action="Create", form=form)  


@app.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
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
        return redirect(url_for("post", post_id=post.id))
    if request.method == "GET":
        form.title.data = post.title
        form.subheading.data = post.subheading
        form.content.data = post.content
        form.level.data = post.level
    return render_template("create_post.html", action="Edit", form=form)          


@app.route("/post/<int:post_id>/delete")
@login_required
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    post.delete()
    return redirect(url_for("posts_written_by", user_id=current_user.id)) 


@app.route("/post/<int:post_id>/hide")
@login_required
def hide_post(post_id):
    post = db.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    post.hide()
    return redirect(url_for("post", post_id=post.id)) 


@app.route("/post/<int:post_id>/show")
@login_required
def show_post(post_id):
    post = db.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    post.show()
    return redirect(url_for("post", post_id=post.id))


@app.route("/follow/<int:post_id>", methods=["POST"])
def follow(post_id):
    if not current_user.is_authenticated:
        flash("Please sign in first to be able to follow users", category="info")
        return redirect(url_for("login"))
    form = FollowerForm()
    if form.validate_on_submit():
        user = db.session.get(Post, post_id).author
        if not user:
            flash("The user you are trying to follow was not found", category="danger")
        elif current_user == user:
            flash("Oops! You cannot follow yourself", category="danger")
        else:
            current_user.follow(user)
    return redirect(url_for("post", post_id=post_id))

@app.route("/unfollow/<int:post_id>", methods=["POST"])
def unfollow(post_id): 
    if not current_user.is_authenticated:
        flash("Please sign in first to be able to follow users", category="info")
        return redirect(url_for("login"))
    form = FollowerForm()
    if form.validate_on_submit():
        user = db.session.get(Post, post_id).author
        if not user:
            flash("The user you are trying to unfollow was not found", category="danger")
        elif current_user == user:
            flash("Oops! You cannot unfollow yourself", category="danger")
        else:
            current_user.unfollow(user)
    return redirect(url_for("post", post_id=post_id)) 


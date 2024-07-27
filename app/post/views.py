  
### IMPORTS  ###################################################################

import datetime
import random

from flask import (
        abort,
        flash,
        redirect,
        render_template,
        request,
        url_for
        )
from flask_login import current_user, login_required

from app import db
from app.forms import CreatePostForm, EmptyForm
from app.models import Post, User  
from app.post import bp_post


### VIEW FUNCTIONS #############################################################             

@bp_post.route("/posts/<int:user_id>")
def posts_written_by(user_id):
    user = db.get_or_404(User, user_id)
    form = EmptyForm()
    if form.validate_on_submit():
        return redirect(request.url)
    return render_template("post/posts_by_author.html", form=form, user=user)  


@bp_post.route("/post/<int:post_id>")
def post(post_id):
    follower_form = EmptyForm()
    delete_post_form = EmptyForm()
    bookmark_form = EmptyForm()
    selected_post = db.get_or_404(Post, post_id)
    if not selected_post.public and selected_post.author != current_user:
        abort(403)
    if follower_form.validate_on_submit():
        return redirect(request.url)
    if bookmark_form.validate_on_submit():
        return redirect(request.url)
    next_post = Post.next_post(current_post=selected_post)
    previous_post = Post.previous_post(current_post=selected_post)
    # Retrieve three or less random public posts written by the same author and distinct
    # from the selected post
    posts = Post.public_posts(author=selected_post.author) 
    more_posts = [post for post in sorted(posts, key=lambda post: random.random()) if post.id != selected_post.id]
    #
    # Increase the number of post views by one
    if current_user != selected_post.author:
        selected_post.increase_view()
    #
    if delete_post_form.validate_on_submit():
        return redirect(url_for("bp_post.delete_post", post_id=post_id))
    return render_template(
            "post/post.html", 
            bookmark_form=bookmark_form,
            delete_post_form=delete_post_form,
            follower_form=follower_form, 
            more_posts=more_posts, 
            selected_post=selected_post, 
            next_post=next_post, 
            previous_post=previous_post)  


@bp_post.route("/post/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(
                title=form.title.data,
                subheading=form.subheading.data,
                content=form.content.data,
                level=form.level.data,
                public=True if form.status.data == "Now" else False,
                author=current_user
                )
        post.add()
        if not post.public:
            flash("Your post was saved, but not published. Please check your profile", category="info")
            return redirect(url_for("bp_post.post", post_id=post.id))
        flash("Your post has been published successfully", category="success")
        return redirect(url_for("bp_post.post", post_id=post.id)) 
    return render_template("post/create_post.html", action="Create", form=form)  


@bp_post.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    form = CreatePostForm()
    if form.validate_on_submit():
        post.update(
                title=form.title.data,
                subheading=form.subheading.data,
                content=form.content.data,
                level=form.level.data,
                date_posted=datetime.datetime.utcnow()
                ) 
        flash("Your post has been updated", category="success") 
        return redirect(url_for("bp_post.post", post_id=post.id))
    if request.method == "GET":
        form.title.data = post.title
        form.subheading.data = post.subheading
        form.content.data = post.content
        form.level.data = post.level
    return render_template("post/create_post.html", action="Edit", form=form)    


@bp_post.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    delete_post_form = EmptyForm()
    post = db.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    if delete_post_form.validate_on_submit():
        post.delete()
        flash("Your post has been deleted", category="success")
        return redirect(url_for("bp_user.profile")) 
    flash("Oops! Something unexpected happened. Please try again later", category="danger")
    return redirect(url_for("bp_post.post", post_id=post_id))         


@bp_post.route("/post/<int:post_id>/hide")
@login_required
def hide_post(post_id):
    post = db.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    post.hide()
    flash("Your post has been hidden", category="info")
    return redirect(url_for("bp_post.post", post_id=post.id)) 


@bp_post.route("/post/<int:post_id>/show")
@login_required
def show_post(post_id):
    post = db.get_or_404(Post, post_id)
    if post.author != current_user:
        abort(403)
    post.show()
    flash("Your post has been published", category="success")
    return redirect(url_for("bp_post.post", post_id=post.id))          

 
### IMPORTS  ###################################################################

from flask import (
        abort,
        current_app,
        flash,
        redirect,
        render_template,
        request,
        url_for
        )
from flask_login import (
        current_user,
        fresh_login_required,
        login_required,
        logout_user
        )

from app import db
from app.forms import (                                                              
        ChangePasswordForm,
        EmailTokenForm,
        EmptyForm,
        ImageForm,
        LogoutForm,
        ProfileForm,
        ResetPasswordForm
        )                 
from app.helpers import Img, logout_required 
from app.models import Post, User
from app.user import bp_user


### VIEW FUNCTIONS #############################################################

@bp_user.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    image_form = ImageForm() 
    profile_form = ProfileForm()
    delete_account_form = EmptyForm()
    if "submit_image" in request.form:
        if image_form.validate():
            img = Img(
                    static_folder=current_app.static_folder,
                    uploaded_img=image_form.image.data,
                    user=current_user
                    )
            img.remove_current_img()
            img.save_uploaded_img()
            return redirect(request.url)
        profile_form.first_name.data = current_user.first_name
        profile_form.last_name.data = current_user.last_name
        profile_form.about_me.data = current_user.about_me
    elif "submit_profile" in request.form and profile_form.validate():
        current_user.update(
                first_name=profile_form.first_name.data,
                last_name=profile_form.last_name.data,
                about_me=profile_form.about_me.data
                )
        return redirect(request.url)
    if request.method == "GET":
        profile_form.first_name.data = current_user.first_name
        profile_form.last_name.data = current_user.last_name
        profile_form.about_me.data = current_user.about_me 
    return render_template(
            "user/profile.html",
            delete_account_form=delete_account_form,
            image_form=image_form,
            profile_form=profile_form
            )  


@bp_user.route("/change-password", methods=["GET", "POST"])
@fresh_login_required
def change_password():
    change_password_form = ChangePasswordForm()
    logout_form = LogoutForm()
    if "submit_change_password_form" in request.form and change_password_form.validate():
        if current_user.check_password(change_password_form.current_password.data):
            current_user.update(password=change_password_form.password.data)
            flash("Your password has been changed successfully", category="success")
            return redirect(url_for("bp_user.profile", user_id=current_user.id))
        flash("The current password is incorrect. Please try again", category="danger")
        return redirect(request.url)
    if "submit_logout_form" in request.form and logout_form.validate():
        logout_user()
        return redirect(url_for("bp_user.email_token"))
    return render_template(
            "user/change_password.html",
            change_password_form=change_password_form,
            logout_form=logout_form
            ) 


@bp_user.route("/reset-password", methods=["GET", "POST"])
@logout_required
def email_token():
    if current_user.is_authenticated:
        flash("Please sign out first to be able to reset your password", category="info")
        return redirect(url_for("bp_user.profile"))
    form = EmailTokenForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()
        if user:
            user.send_reset_password_link()
            flash("Please check your email inbox and follow the reset password link", category="success")
            return redirect(url_for("bp_main.index")) 
        flash("There is no account with that email.", category="danger")
        return redirect(request.url) 
    return render_template("user/email_token.html", form=form)  


@bp_user.route("/reset-password/<string:token>", methods=["GET", "POST"])
@logout_required
def reset_password(token): 
    if current_user.is_authenticated:
        flash("Please sign out first to be able to recover your account.", category="info")
        return redirect(url_for("bp_user.profile")) 
    user = User.verify_jwt(token)
    if not user:
        flash("The verification link is invalid. Please try again", category="danger")
        return redirect(url_for("bp_user.email_token"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.update(password=form.password.data)
        flash("Your password has been changed successfully", category="success")
        return redirect(url_for("bp_auth.login"))
    return render_template("user/reset_password.html", form=form)  


@bp_user.route("/delete-account/<int:user_id>", methods=["POST"])
@fresh_login_required
def delete_account(user_id):
    user = db.get_or_404(User, user_id)
    if user != current_user:
        abort(403)
    delete_account_form = EmptyForm()
    if delete_account_form.validate_on_submit():
        for post in user.posts:
            post.delete()
        user.delete()
        flash("Your account has been deleted successfully", category="success")
        return redirect(url_for("bp_main.index"))
    flash("Oops! Something unexpected happened. Please try again later", category="danger")
    return redirect(url_for("bp_user.profile"))
 

@bp_user.route("/follow/<int:user_id>", methods=["POST"])
def follow(user_id):
    user = db.get_or_404(User, user_id)
    if not current_user.is_authenticated:
        flash(f"Please sign in first to be able to follow {user.fullname}", category="info")
        return redirect(url_for("bp_auth.login"))
    form = EmptyForm()
    if form.validate_on_submit():
        if current_user == user:
            flash("Oops! You cannot follow yourself", category="danger")
        else:
            current_user.follow(user)
            flash(f"You are now following {user.fullname}", category="success")
    return redirect(url_for("bp_post.posts_written_by", user_id=user.id)) 


@bp_user.route("/unfollow/<int:user_id>", methods=["POST"])
def unfollow(user_id):
    user = db.get_or_404(User, user_id)
    if not current_user.is_authenticated:
        flash(f"Please sign in first to be able to unfollow {user.fullname}", category="info")
        return redirect(url_for("bp_auth.login"))
    form = EmptyForm()
    if form.validate_on_submit():
        if current_user == user: 
            flash("Oops! This cannot be done", category="danger")
        else:
            current_user.unfollow(user)
            flash(f"You are no longer following {user.fullname}", category="success")
    return redirect(url_for("bp_post.posts_written_by", user_id=user.id))    


@bp_user.route("/bookmark/<int:post_id>", methods=["POST"])
def bookmark(post_id):
    post = db.get_or_404(Post, post_id)
    if not current_user.is_authenticated:
        flash("Please sign in first to be able to add bookmarks", category="info")
        return redirect(url_for("bp_auth.login"))
    form = EmptyForm()
    if form.validate_on_submit():
        if current_user == post.author:
            flash("Oops! This cannot be done", category="danger")
        else:
            current_user.bookmark(post)
            flash("This post has been added to your bookmarks successfully", category="success")
    return redirect(url_for("bp_post.post", post_id=post_id))   


@bp_user.route("/unbookmark/<int:post_id>", methods=["POST"])
def unbookmark(post_id):
    post = db.get_or_404(Post, post_id)
    if not current_user.is_authenticated:
        flash("Please sign in first to be able to add this post to your bookmarks", category="info")
        return redirect(url_for("bp_auth.login"))
    form = EmptyForm()
    if form.validate_on_submit():
        if current_user == post.author:
            flash("Oops! This cannot be done", category="danger")
        else:
            current_user.unbookmark(post)
            flash("This post has been removed from your bookmarks successfully", category="success")
    return redirect(url_for("bp_post.post", post_id=post_id))                                                                                  

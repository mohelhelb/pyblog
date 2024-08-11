
### IMPORTS  ###################################################################

from flask import (
        flash,
        redirect,
        render_template,
        request,
        url_for
        )
from flask_login import (
        login_required,
        login_user,
        logout_user
        )
from werkzeug.urls import url_parse

from app.auth import bp_auth
from app.forms import SigninForm, SignupForm
from app.helpers import logout_required
from app.models import User          


### VIEW FUNCTIONS  ############################################################

@bp_auth.route("/register", methods=["GET", "POST"])
@logout_required
def register():
    # WTForms library:
    # form = SignupForm(request.form)
    # if request.method == "POST" and form.validate():
    #   ...
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
                about_me=form.about_me.data
                )
        user.add()
        flash("Your account has been created successfully", category="success")
        return redirect(url_for("bp_auth.login"))
    return render_template("auth/register.html", form=form) 


@bp_auth.route("/login", methods=["GET", "POST"])
@logout_required
def login():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.retrieve_user_with(email=form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc:
                next_page = url_for("bp_user.profile")
            flash(f"Hi, {user.first_name}!", category="success") 
            return redirect(next_page)
        elif user: 
            flash("The password is incorrect. Please try again", category="danger")
            return redirect(request.url) 
        flash("There is no account with that email", category="danger")
        return redirect(request.url)
    return render_template("auth/login.html", form=form)   


@bp_auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("bp_main.index"))  

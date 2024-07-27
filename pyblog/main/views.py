
### IMPORTS  ###################################################################

from flask import g, render_template

from pyblog.main import bp_main
from pyblog.models import Post, User  


### FUNCTIONS  #################################################################

@bp_main.before_app_request
def before_request():
    '''Set the jinja2 variables in the base template.'''
    g.total_users = User.num_users()
    g.total_public_posts = Post.num_public_posts()
    g.top_writers = Post.top_writers()  


### VIEW FUNCTIONS #############################################################

@bp_main.route("/") 
@bp_main.route("/index") 
@bp_main.route("/home")
def index():
    trending_posts = Post.trending_posts() if Post.num_trending_posts() else None 
    public_posts = Post.public_posts() if Post.num_public_posts() else None
    return render_template("main/index.html", public_posts=public_posts, trending_posts=trending_posts)  


@bp_main.route("/about")
def about():
    return render_template("main/about.html")               

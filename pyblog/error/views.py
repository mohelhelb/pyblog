 
### IMPORTS  ###################################################################

from flask import render_template

from pyblog.error import bp_error


### ERROR HANDLERS  ############################################################  

@bp_error.errorhandler(404)
def error_404(error):
    return render_template("error/error_404.html"), 404  


@bp_error.errorhandler(403)
def error_403(error):
    return render_template("error/error_403.html"), 403  


@bp_error.errorhandler(500)
def error_500(error):
    return render_template("error/error_500.html"), 500                

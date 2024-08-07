
### IMPORTS  ###################################################################  

import glob
import os

from flask import current_app, flash, redirect, url_for
from flask_login import current_user
from functools import wraps
from PIL import Image


### Functions  #################################################################

def logout_required(view):
    """
    Prevent authenticated users from visiting certain pages.

    If an authenticated user attempts to visit pages intended only for
    non-authenticated users (e.g. "login" page), they are redirected to their 
    profile page.

    Parameters:
    view: View function to be decorated.

    Returns:
    view(*args, **kwargs): View call if the user is not authenticated, profile view call otherwise.
    """
    @wraps(view)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            flash("Please log out first to visit that page", category="info")
            return redirect(url_for("bp_user.profile")), 302
        return view(*args, **kwargs)
    return wrapper

 
### Classes  ###################################################################

class Img:

    def __init__(self, uploaded_img=None):
        self.img = uploaded_img

    @property
    def fname(self):
        return self.img.filename

    @fname.setter
    def fname(self, new_fname):
        self.img.filename = new_fname
    
    def remove_current_img(self, user=None, static_folder=None):
        if user.image != "default.png":
            try:
                os.remove(os.path.join(static_folder, "images", user.image))
            except Exception:
                pass # Pending

    def save_uploaded_img(self, static_folder=None, size=(100, 100), user=None): 
        with Image.open(self.img) as img:
            img.thumbnail(size) 
            img_ext = img.format.lower()  
            img_fn = f"img-{user.id}.{img_ext}" 
            try:
                img.save(os.path.join(static_folder, "images", img_fn))
            except Exception:
                pass # Pending
            else:
                self.fname = img_fn

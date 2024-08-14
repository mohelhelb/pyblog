
### IMPORTS  ###################################################################  

import os

from flask import flash, redirect, url_for
from flask_login import current_user
from functools import wraps
from PIL import Image


### Functions  #################################################################

def logout_required(view):
    """
    Prevent authenticated users from visiting given pages.

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

    def __init__(self, static_folder=None, uploaded_img=None, user=None):
        self.static_folder = static_folder
        self.uploaded_img = uploaded_img
        self.user = user
    
    def remove_current_img(self):
        if self.user.image != "default.png":
            try:
                os.remove(os.path.join(self.static_folder, "images", self.user.image))
            except Exception:
                pass # Pending

    def save_uploaded_img(self, size=(100, 100)): 
        with Image.open(self.uploaded_img) as img:
            img.thumbnail(size) 
            img_ext = img.format.lower()  
            img_fn = f"img-{self.user.id}.{img_ext}" 
            try:
                img.save(os.path.join(self.static_folder, "images", img_fn))
            except Exception:
                img.close() # Pending
            else:
                self.user.update(image=img_fn)

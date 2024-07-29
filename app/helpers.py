
### IMPORTS  ###################################################################  

import glob
import os

from flask import flash, redirect, url_for
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

    root_img_dir = os.path.join("/home/mo/projects/pyblog/static", "images") # Pending: Circular import

    def __init__(self, img_file):
        self.img = img_file 

    @property
    def fn(self):
        return self.img.filename

    @fn.setter
    def fn(self, new_filename):
        self.img.filename = new_filename

    @property
    def ext(self):
        filename = self.img.filename
        return filename.rsplit(".", 1)[-1].lower()
    
    @classmethod
    def remove_current_imgs(cls, user=None):
        images = glob.glob(pathname=f"img-{user.id}.*", root_dir=cls.root_img_dir)
        if images:
            for image in images:
                os.remove(os.path.join(cls.root_img_dir, image))

    def save_uploaded_img(self, size=None):
        with Image.open(self.img) as img:
            img.thumbnail(size)
            img.save(os.path.join(self.root_img_dir, self.fn))
            

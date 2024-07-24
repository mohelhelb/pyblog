
### IMPORTS  ###################################################################  

import glob
import os
from PIL import Image

from pyblog import app

 
### Classes  ###################################################################

class Img:

    root_img_dir = os.path.join(app.static_folder, "images")

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
            

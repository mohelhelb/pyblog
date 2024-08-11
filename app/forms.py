
### IMPORTS  ###################################################################  

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from PIL import Image, UnidentifiedImageError
from wtforms import (
        EmailField,
        PasswordField,
        RadioField,
        StringField,
        SubmitField,
        TextAreaField
        )
from wtforms.validators import (
        Email,
        EqualTo,
        DataRequired,
        Length,
        ValidationError
        )

from app.models import User


### CUSTOM VALIDATOR  ##########################################################

class Account:

    def __init__(self, existent=True):
        self.existent = existent

    def __call__(self, form, field):
        user = User.retrieve_user_with(email=field.data)
        if self.existent and not user:
            raise ValidationError("There is no account with this email")
        if not self.existent and user:
            raise ValidationError("This email is already in use.") 


### FORMS: USER  ###############################################################
 
class SignupForm(FlaskForm):
    first_name = StringField(
            label="First Name",
            validators=[DataRequired(), Length(max=30)],
            id="firstName",
            description="e.g. John"
            )
    last_name = StringField(
            label="Last Name", 
            validators=[DataRequired(), Length(max=30)],
            id="lastName",
            description="e.g. Doe"
            )
    email = EmailField(
            label="Email",
            validators=[Account(existent=False), DataRequired(), Email()], 
            id="emailAddress",
            description="e.g. johndoe@demo.com"
            )
    password = PasswordField(
            label="Password",
            validators=[Length(min=4, max=20)],
            id="password",
            description="At least 4 characters"
            )
    confirm_password = PasswordField(
            label="Repeat Password",
            validators=[EqualTo("password")],
            id="confirmPassword",
            description="Repeat Password"
            )
    about_me = TextAreaField(
            label="About me", 
            validators=[DataRequired(), Length(max=150)],
            id="aboutMe",
            description="Enter a brief description of yourself"
            )
    submit = SubmitField(label="Sign up")   


class SigninForm(FlaskForm): 
    email = EmailField(
            label="Email",
            validators=[Account(existent=True), DataRequired(), Email()], 
            id="emailAddress",
            description="e.g. johndoe@demo.com"
            ) 
    password = PasswordField(
            label="Password",
            validators=[Length(min=4, max=20)],
            id="password",
            description="At least 4 characters"
            ) 
    submit = SubmitField(label="Sign in")  


class EmailTokenForm(FlaskForm): 
    email = EmailField(
            label="Email",
            validators=[Account(existent=True), DataRequired(), Email()], 
            id="emailAddress",
            description="e.g. johndoe@demo.com"
            )  
    submit = SubmitField(label="Reset Password")


class ProfileForm(FlaskForm):
    first_name = StringField(
            label="First Name",
            validators=[DataRequired(), Length(max=30)],
            id="firstName",
            description="e.g. John"
            )
    last_name = StringField(
            label="Last Name", 
            validators=[DataRequired(), Length(max=30)],
            id="lastName",
            description="e.g. Doe"
            )
    about_me = TextAreaField(
            label="About me", 
            validators=[DataRequired(), Length(max=150)],
            id="aboutMe",
            description="Enter a brief description of yourself"
            )     
    submit_profile = SubmitField(label="Edit")    


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
            label="Current Password",
            validators=[Length(min=4, max=20)],
            id="currentPassword",
            description="Enter current password"
            )
    password = PasswordField(
            label="New Password",
            validators=[Length(min=4, max=20)],
            id="password",
            description="At least 4 characters long"
            )
    confirm_password = PasswordField(
            label="Repeat Password",
            validators=[EqualTo("password")],
            id="confirmPassword",
            description="Repeat new password"
            ) 
    submit_change_password_form = SubmitField(label="Confirm")  


class LogoutForm(FlaskForm):
    submit_logout_form = SubmitField(label="Sign out")


class ResetPasswordForm(FlaskForm):
    password = ChangePasswordForm.password
    confirm_password = ChangePasswordForm.confirm_password
    submit = SubmitField(label="Reset Password")                 


class ImageForm(FlaskForm):
    image = FileField(
            label="Image",
            id="image"
            )
    submit_image = SubmitField()

    def validate_image(form, field):
        if field.data:
            try:
                image = Image.open(field.data)
            except UnidentifiedImageError:
                raise ValidationError("Invalid image.")
            else:
                try:
                    image.verify()
                except Exception:
                    image.close()
                    raise ValidationError("Corrupted image.")
                else:
                    if image.format not in ("JPEG", "PNG"):
                        image.close()
                        raise ValidationError("Invalid image extention.")

 
class EmptyForm(FlaskForm):
    submit = SubmitField()   


### FORMS: POST  ###############################################################

class CreatePostForm(FlaskForm):
    title = StringField(
            label="Title",
            validators=[DataRequired(), Length(max=100)],
            id="postTitle",
            description="Enter Post Title"
            )
    subheading = TextAreaField(
            label="Subheading",
            validators=[DataRequired(), Length(max=150)],
            id="postSubheading",
            description="Enter Post Subheading"
            )
    content = TextAreaField(
            label="Content",
            validators=[DataRequired()],
            id="content",
            description="Enter Post Content"
            )
    level = RadioField(
            label="Difficulty Level",
            id="level",
            choices=["Beginner", "Intermediate", "Advanced"]
            )
    status = RadioField(
            label="When do you want to publish your post?",
            id="status",
            choices=["Now", "Later"]
            )
    submit = SubmitField() 

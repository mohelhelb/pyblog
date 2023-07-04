from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import Form, EmailField, PasswordField, RadioField, StringField, SubmitField, TextAreaField
from wtforms.validators import Email, EqualTo, DataRequired, Length 
 
 
class UserBaseForm(FlaskForm):
    first_name = StringField(
            label="First Name",
            validators=[DataRequired(), Length(max=20)],
            id="firstName",
            description="e.g. John"
            )
    last_name = StringField(
            label="Last Name", 
            validators=[DataRequired(), Length(max=20)],
            id="lastName",
            description="e.g. Doe"
            )
    email = EmailField(
            label="Email",
            validators=[DataRequired(), Email()], 
            id="emailAddress",
            description="e.g. johndoe@demo.com"
            )
    password = PasswordField(
            label="Password",
            validators=[Length(min=4, max=20)],
            id="password",
            description="Must be at least 4 characters long"
            )
    confirm_password = PasswordField(
            label="Confirm Password",
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

class ImageForm(FlaskForm):
    image = FileField(
            label = "Image",
            validators = [FileAllowed(["jpg", "jpeg", "png"], "Invalid image file. Allowed extensions: jpg, jpeg, png.")],
            id = "image"
            )
    submit_image = SubmitField()

class CreatePostForm(FlaskForm):
    title = StringField(
            label = "Title",
            validators = [DataRequired(), Length(max=100)],
            id = "postTitle",
            description = "Enter Post Title"
            )
    subheading = TextAreaField(
            label = "Subheading",
            validators = [DataRequired(), Length(max=150)],
            id = "postSubheading",
            description = "Enter Post Subheading"
            )
    content = TextAreaField(
            label = "Content",
            validators = [DataRequired()],
            id = "content",
            description = "Enter Post Content"
            )
    level = RadioField(
            label = "Difficulty Level",
            id="level",
            choices = ["Beginner", "Intermediate", "Advanced"]
            )
    submit = SubmitField()


# Python Inheritance

class SignupForm(UserBaseForm):
    submit = SubmitField(label="Sign up") 

# Python Composition

class SigninForm(FlaskForm):
    email = UserBaseForm.email
    password = UserBaseForm.password
    submit = SubmitField(label="Sign in")


class EmailTokenForm(FlaskForm):
    email = UserBaseForm.email
    submit = SubmitField(label="Reset Password")


class ChangePasswordForm(FlaskForm):
    password = UserBaseForm.password
    confirm_password = UserBaseForm.confirm_password
    submit = SubmitField(label="Confirm") 


class ProfileForm(FlaskForm):
    first_name = UserBaseForm.first_name
    last_name = UserBaseForm.last_name
    email = UserBaseForm.email
    about_me = UserBaseForm.about_me
    submit_profile = SubmitField(label="Edit") 


    

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length

from app.models import User


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Request Password Reset")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


class TaskForm(FlaskForm):
    task = TextAreaField("Add new task...", validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField("Submit")


class EmptyForm(FlaskForm):
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    # WTForms knows to use methods called `validate_{field}` to apply
    # as validators to that field.
    def validate_username(self, username):
        """Make sure this username isn't taken."""
        user = User.query.filter_by(username=username.data).first()

        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        """Make sure this email isn't taken."""
        user = User.query.filter_by(email=email.data).first()

        if user is not None:
            raise ValidationError("Please use a different email.")


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs) -> None:
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """Make sure the new username isn't taken. 
        Allow user to keep existing username on submit."""
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()

            # If there is a duplicate...
            if user is not None:
                raise ValidationError("Please use a different username.")

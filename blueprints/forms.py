import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import UserModel


class RegisterForms(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="Wrong Email")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="Wrong Username")])
    password = wtforms.StringField(validators=[Length(min=6, max=25, message="Password Format Error")])
    passwordConfirm = wtforms.StringField(validators=[EqualTo("password")])

    def validate_email(form, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="This Email has been registered")


class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="Wrong Username")])
    password = wtforms.StringField(validators=[Length(min=6, max=25, message="Password Format Error")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="Title Format Error")])
    content = wtforms.StringField(validators=[Length(min=3, message="Content Format Error")])

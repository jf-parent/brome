# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired

from brome.core.model.user import User
from brome.webserver.webserver.extensions import db

class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = db.session.query(User).filter_by(username = self.username.data).first()
        if not self.user:
            self.username.errors.append('Unknown username')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        return True

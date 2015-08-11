# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from IPython import embed

from brome.webserver.extensions import db
from brome.core.model.configurator import default_config, ini_to_dict, save_brome_config
from brome.core.model.user import User

class RegisterForm(Form):
    username = TextField('Username',
                    validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('Email',
                    validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                                validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                [DataRequired(), EqualTo('password', message='Passwords must match')])
    token = PasswordField('Token')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.app = kwargs.get('app')
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False

        if self.app.config.get('CLOSED_REGISTRATION', False):
            if self.token.data != self.app.config.get('REGISTRATION_TOKEN'):
                self.token.errors.append("The registration security token doesn't match")
                return False

        user = db.session.query(User).filter_by(username = self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False

        user = db.session.query(User).filter_by(email = self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False

        return True

class ConfigForm(object):
    def __init__(self, app):
        self.app = app

        self.fields = self.get_fields()

    def get_fields(self):
        data = default_config
        config = ini_to_dict(self.app.brome.config_path)
        
        for section_key, section_item in config.iteritems():

            for option_key, option_item in section_item.iteritems():

                #User defined section
                if not data.has_key(section_key):
                    data[section_key] = {}
                    data[section_key][option_key] = {
                        'value': option_item,
                        'type': 'input',
                        'title': option_key
                    }

                else:
                    #User defined option
                    if not data[section_key].has_key(option_key):
                        data[section_key][option_key] = {
                            'value': option_item,
                            'type': 'input',
                            'title': option_key
                        }
                    else:
                        data[section_key][option_key]['value'] = option_item

        return data

    def save(self, data):
        for section_id, section in self.fields.iteritems():
            for field_id, field in section.iteritems():
                try:
                    value = data.getlist("%s_%s"%(section_id, field_id))[0]
                    if value == 'on':
                        field['value'] = True
                    else:
                        field['value'] = value
                except IndexError:
                    field['value'] = False

        return save_brome_config(self.app.brome.config_path, self.fields)

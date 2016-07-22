import urllib
import hashlib

import bcrypt
from mongoalchemy.document import Index
from mongoalchemy.fields import (
    EnumField,
    BoolField,
    StringField
)
from validate_email import validate_email

from brome.webserver.server.utils import SafeStringField
from brome.core import exceptions
from brome.model.basemodel import BaseModel

NAME_MIN_LEN = 2  # e.g.: Ed
NAME_MAX_LEN = 60  # e.g.: Hubert Blaine Wolfeschlegelsteinhausenbergerdorff, Sr. # noqa


class User(BaseModel):
    name = SafeStringField(required=True, min_length=NAME_MIN_LEN, max_length=NAME_MAX_LEN)  # noqa
    email = SafeStringField(required=True)
    role = EnumField(StringField(), 'admin', 'user', default="user")
    enable = BoolField(default=True)
    gravatar_url = StringField(default="")
    # settings =
    # social_id =
    # social_provider =

    # PASSWORD
    hashed_password = StringField(required=True)
    salt = StringField(required=True)

    # INDEX
    i_email = Index().ascending('email').unique()

    def __eq__(self, target):
        return target.get_uid() == self.get_uid()

    def __repr__(self):
        try:
            _repr = "User <uid: '{uid}'><name:'{name}'><email:'{email}'><role:'{role}'><enable:'{enable}'>"  # noqa
            return _repr.format(
                    name=self.name,
                    uid=self.get_uid(),
                    email=self.email,
                    enable=self.enable,
                    role=self.role
                )
        except AttributeError:
            return "User uninitialized"

##############################################################################
# FUNC
##############################################################################

    async def check_password(self, target_password):
        target_hashed_password, _ = await self.gen_hashed_password(
            target_password,
            self.salt
        )

        if target_hashed_password == self.hashed_password:
            return True
        else:
            return False

    async def gen_hashed_password(self, raw_password, salt_str=False):
        if not salt_str:
            salt = bcrypt.gensalt()
            salt_str = salt.decode('utf-8')
        else:
            salt = bytes(salt_str.encode('utf-8'))

        mixed_password = raw_password + salt_str
        hashed_password = bcrypt.hashpw(
            mixed_password.encode('utf-8'),
            salt
        ).decode('utf-8')
        return hashed_password, salt_str

    async def sanitize_data(self, context):
        author = context.get('author')
        data = context.get('data')

        if author:
            if author.role == 'admin':
                return data
            else:
                editable_fields = [
                    'name',
                    'email',
                    'old_password',
                    'new_password'
                ]
        else:
            editable_fields = ['name', 'email', 'password']

        return {k: data[k] for k in data if k in editable_fields}

    async def validate_and_save(self, context):
        data = context.get('data')
        db_session = context.get('db_session')
        save = context.get('save', True)

        is_new = await self.is_new()

        # NAME
        name = data.get('name')
        if name:
            if len(name) < NAME_MIN_LEN or len(name) > NAME_MAX_LEN:
                raise exceptions.InvalidNameException(name)

            self.name = name
        else:
            if is_new:
                raise exceptions.InvalidNameException('empty name')

        # ROLE
        role = data.get('role')
        if role:
            self.role = role

        # ENABLE
        enable = data.get('enable')
        if enable is not None:
            self.enable = enable

        # PASSWORD
        password = data.get('password')
        if password:
            await self.set_password(password)
        else:
            if is_new:
                raise exceptions.InvalidPasswordException('empty password')

        # NEW PASSWORD
        new_password = data.get('new_password')
        if new_password:
            old_password = data.get('old_password')
            if old_password:
                is_password_valid = await self.check_password(old_password)
                if is_password_valid:
                    await self.set_password(new_password)
                else:
                    raise exceptions.WrongEmailOrPasswordException()
            else:
                raise exceptions.InvalidRequestException(
                    'Missing old password'
                )

        # EMAIL
        email = data.get('email')
        if email:
            if is_new or self.email != email:
                is_email_valid = validate_email(email)
                if not is_email_valid:
                    raise exceptions.InvalidEmailException(email)

                email_uniqueness_query = db_session.query(User)\
                    .filter(User.email == email)
                if not is_new:
                    email_uniqueness_query = email_uniqueness_query\
                        .filter(User.mongo_id != self.get_uid())

                if email_uniqueness_query.count():
                    raise exceptions.EmailAlreadyExistsException(email)

                self.email = email
                self.email_confirmed = False

                # GRAVATAR
                gravatar_url = "{base_url}{md5_hash}?{params}".format(
                    base_url="https://www.gravatar.com/avatar/",
                    md5_hash=hashlib.md5(
                        email.lower().encode('utf')
                    ).hexdigest(),
                    params=urllib.parse.urlencode(
                        {'d': "identicon", 's': '40'}
                    )
                )
                self.gravatar_url = gravatar_url

        else:
            if is_new:
                raise exceptions.InvalidEmailException('empty email')

        if save:
            db_session.save(self, safe=True)

    async def set_password(self, password):
        if await self.is_password_valid(password):
            hashed_password, salt = await self.gen_hashed_password(password)
            self.hashed_password = hashed_password
            self.salt = salt
        else:
            raise exceptions.InvalidPasswordException(password)

    async def is_password_valid(self, password):
        if len(password) < 6:
            return False
        else:
            return True

    async def method_autorized(self, context):
        method = context.get('method')
        author = context.get('author')

        if method in ['create', 'delete']:
            if author.role == 'admin':
                return True
            else:
                return False
        elif method in ['update', 'read']:
            if author == self:
                return True
            elif author.role == 'admin':
                return True
            else:
                return False

    async def serialize(self, context):
        data = {}
        data['uid'] = self.get_uid()
        data['name'] = self.name
        data['email'] = self.email
        data['gravatar_url'] = self.gravatar_url
        return data

    def logout(self, session):
        del session['uid']

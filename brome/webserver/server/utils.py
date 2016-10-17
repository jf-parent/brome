
import os
import binascii

import jinja2
from mongoalchemy.fields import StringField


def generate_token(n):
    return binascii.hexlify(os.urandom(n)).decode('utf')


class SafeStringField(StringField):

    def __set__(self, instance, value):
        value = jinja2.utils.escape(value)
        self.set_value(instance, value)

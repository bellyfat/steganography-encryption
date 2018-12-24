from marshmallow import (
    fields,
    validate,
    post_load
)

from stegano.extensions import ma
from stegano.models import Messages


class MessageSchema(ma.Schema):
    id = ma.Int(dump_only=True)
    msg_payload = ma.String(required=True)
    msg_enc_key = ma.String(required=True)
    share_to = ma.String(
        required=True,
        validate=validate.Email(
            error='Not a valid email address')
    )
    img_file = ma.String(dump_only=True)
    sent_on = ma.DateTime(dump_only=True)

    # @post_load
    # def make_user(self, data):
    #     return Messages(**data)

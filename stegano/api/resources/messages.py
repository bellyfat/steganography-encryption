from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from stegano.models import Messages
from stegano.schemas import MessageSchema
from stegano.extensions import db
from stegano.helpers.paginator import paginate
from stegano.helpers.steg import SteganoImage
from stegano.helpers import loadconf, get_save_location
from Crypto.Cipher import AES

import os

conf = loadconf()

ALLOWED_EXTENSIONS = set(['png', 'bmp'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class MessageResource(Resource):

    method_decorators = [jwt_required]

    def get(self, mid):
        schema = MessageSchema()

        if not request.is_json:
            return make_response(
                jsonify(msg='Missing JSON in request'), 400)

        return schema.jsonify(msg)

    def put(self, mid):
        schema = MessageSchema(partial=True)

        if not request.is_json:
            return make_response(
                jsonify(msg='Missing JSON in request'), 400)

        msg, errors = schema.load(request.json)
        if errors:
            return errors, 422

        return schema.jsonify(msg)

    def delete(self, mid):

        return jsonify(msg='User deleted')


class MessagesResource(Resource):

    method_decorators = [jwt_required]

    def get(self):
        schema = MessageSchema(many=True)

        return paginate(msgs, schema)

    def post(self):
        # Validate file in req
        if 'file' not in request.files:
            return make_response(
                jsonify(msg='An image file is required'),
                400
            )
        file = request.files['file']
        if file.filename == '':
            return make_response(
                jsonify(msg='No file'),
                400
            )
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            imgpath = os.path.join(conf.TMP_UPLOAD_PATH, filename)
            file.save(imgpath)

            save_filename = f'enc_{filename}'
            save_path = get_save_location(save_filename)

        else:
            return make_response(
                jsonify(msg='File not allowed'), 400)

        schema = MessageSchema()
        payload, errors = schema.load(request.data)
        if errors:
            return errors, 422

        # Save user upload img to a tmp folder

        # Get an AES object corresponding to user input key
        aes = AES.new(
            payload.msg_enc_key,
            AES.MODE_CFB,
            conf.SECRET_KEY
        )
        cph_txt = aes.encrypt(payload.msg_payload)

        # Hide the cipher text into user uploaded image
        steg = SteganoImage(imgpath, msg=cph_txt)
        steg.encode(save_path)

        return schema.jsonify(msg)

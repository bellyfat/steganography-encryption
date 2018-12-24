from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_current_user
from werkzeug.utils import secure_filename

from stegano.models import Messages, Users
from stegano.schemas import MessageSchema
from stegano.extensions import db
from stegano.helpers.paginator import paginate
from stegano.helpers.steg import SteganoImage
from stegano.helpers import loadconf, get_save_location, get_aes_key
from Crypto.Cipher import AES
from Crypto.Util import Counter
from uuid import uuid4
import os

conf = loadconf()
ctr = Counter.new(128)
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
        filter_by = request.args.get('msg_type', 'inbox')
        if filter_by == 'sent':
            msgs = Messages.query.filter_by(sent_by=get_current_user())
        else:
            msgs = Messages.query.filter_by(sent_to=get_current_user())
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
            # Save user upload img to a tmp folder
            file.save(imgpath)
            uid = uuid4().hex
            save_filename = f'{uid}_{filename}'
            save_path = get_save_location(save_filename)
        else:
            return make_response(
                jsonify(msg='File not allowed'), 400)

        schema = MessageSchema()
        payload, errors = schema.load(request.form)
        if errors:
            return errors, 422

        # Get an AES object corresponding to user input key
        key = get_aes_key(payload['msg_enc_key'])
        aes = AES.new(
            key,
            AES.MODE_CTR,
            counter=ctr
        )
        cph_txt = aes.encrypt(payload['msg_payload'])

        # Hide the cipher text into user uploaded image
        steg = SteganoImage(imgpath, msg=str(cph_txt))
        steg.encode(save_path)

        # Record this as an entry in table
        model = Messages(
            share_to=payload['share_to'],
            img_file=save_filename,
            sent_by=get_current_user()
        )

        sent_to = Users.query.filter_by(email=payload['share_to']).first()
        if sent_to:
            model.sent_to = sent_to
        else:
            # If the recepient is not signed up, send a mail
            print('User not found')
            pass

        db.session.add(model)
        db.session.commit()
        return schema.jsonify(model)

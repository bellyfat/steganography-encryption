from flask import request, make_response, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_current_user
from werkzeug.utils import secure_filename

from stegano.models import Messages, Users
from stegano.schemas import MessageSchema
from stegano.extensions import db
from stegano.helpers.paginator import paginate
from stegano.helpers.steg import SteganoImage
from stegano.helpers.aes import encrypt, decrypt
from stegano.helpers.mailers import send_signup_mail
from stegano.helpers import loadconf, get_save_location, get_aes_key
from stegano.log import logger
from uuid import uuid4
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
        msg = Messages.query.get_or_404(mid)
        txt = ''
        decr_key = request.args.get('decr_key')
        if decr_key:
            # decode message for the user from corresponding image
            msg_img = get_save_location(msg.img_file)
            # Unhide the cipher text
            steg = SteganoImage(msg_img)
            cph_txt = steg.decode()
            decr_key = get_aes_key(decr_key)
            txt = decrypt(decr_key, cph_txt)
            try:
                txt = txt.decode()
            except UnicodeDecodeError as err:
                logger.error(err)
                txt = ''
            return jsonify(msg=txt)
        return schema.jsonify(msg)


class MessagesResource(Resource):

    method_decorators = [jwt_required]

    def get(self):
        schema = MessageSchema(many=True)
        filter_by = request.args.get('msg_type', 'inbox')
        if filter_by == 'sent':
            msgs = Messages.query.filter_by(
                sent_by=get_current_user()
            )
        else:
            # In other words, we can also add in user foreign key
            # details on signup as a background thread
            msgs = Messages.query.filter_by(
                share_to=get_current_user().email
            )
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
        cph_txt = encrypt(key, payload['msg_payload'])

        # Hide the cipher text into user uploaded image
        steg = SteganoImage(imgpath, msg=cph_txt.decode())
        try:
            steg.encode(save_path)
        except TypeError as err:
            return make_response(
                jsonify(msg=str(err)), 422
            )

        curruser = get_current_user()
        # Record this as an entry in table
        model = Messages(
            share_to=payload['share_to'],
            img_file=save_filename,
            sent_by=curruser
        )

        sent_to = Users.query.filter_by(email=payload['share_to']).first()
        if sent_to:
            model.sent_to = sent_to
        else:
            logger.debug('User not found, sending signup invite!')
            # If the recepient is not signed up, send a mail
            send_signup_mail(curruser.username, payload['share_to'])
        db.session.add(model)
        db.session.commit()
        return schema.jsonify(model)

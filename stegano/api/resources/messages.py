from flask import request, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from stegano.models import Messages
from stegano.schemas import MessageSchema
from stegano.extensions import db
from stegano.helpers.paginator import paginate


class MessageResource(Resource):

    method_decorators = [jwt_required]

    def get(self, mid):
        schema = MessageSchema()

        if not request.is_json:
            return make_response(
                jsonify(msg='Missing JSON in request'), 400)

        msg = Messages.objects.get_or_404(id=mid)
        return schema.jsonify(msg)

    def put(self, mid):
        schema = MessageSchema(partial=True)

        if not request.is_json:
            return make_response(
                jsonify(msg='Missing JSON in request'), 400)

        msg = Messages.objects.get_or_404(id=mid)

        msg, errors = schema.load(request.json)
        if errors:
            return errors, 422

        msg.save()
        return schema.jsonify(msg)

    def delete(self, mid):
        msg = Messages.objects.get_or_404(id=mid)

        return jsonify(msg='User deleted')


class MessagesResource(Resource):

    method_decorators = [jwt_required]

    def get(self):
        schema = MessageSchema(many=True)

        msgs = Messages.objects()

        return paginate(msgs, schema)

    def post(self):
        schema = MessageSchema()

        msg, errors = schema.load(request.json)
        if errors:
            return errors, 422

        msg.save()

        return schema.jsonify(msg)

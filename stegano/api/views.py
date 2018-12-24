from flask import Blueprint
from flask_restful import Api

from stegano.api.resources import (
    MessageResource,
    MessagesResource
)


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(MessageResource, '/messages/<mid>')
api.add_resource(MessagesResource, '/messages')

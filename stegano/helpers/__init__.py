from ..config import configuration
from .paginator import paginate
import os

def loadconf():
    '''
    Load the server configuration
    '''
    env = os.getenv('STEGANO_ENV', 'dev').lower()
    config = configuration[env]
    return config

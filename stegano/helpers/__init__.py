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


def get_save_location(filename):
    conf = loadconf()
    app_root = os.path.dirname(
        os.path.abspath(__file__))
    enc_save_path = os.path.join(
        app_root,
        conf.ENC_IMG_SAVE_PATH,
        filename
    )
    return enc_save_path

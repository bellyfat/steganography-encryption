from ..config import configuration
from .paginator import paginate
from Crypto.Hash import SHA256
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
    enc_save_path = os.path.join(
        conf.APP_ROOT,
        conf.ENC_IMG_SAVE_PATH,
        filename
    )
    return enc_save_path


def get_aes_key(txt):
    hasher = SHA256.new(str(txt).encode('utf-8'))
    return hasher.digest()

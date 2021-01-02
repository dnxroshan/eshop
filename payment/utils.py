import uuid
import hashlib
from eshop import settings

def generate_payment_id():
    return uuid.uuid4().hex[0:-2]

def get_hash_string(params):
    keys = ['key', 'txnid', 'amount', 'productinfo', 'firstname', 'email']
    values = [str(params[key]) for key in keys]
    hash_string = '|'.join(values)
    hash_string += '|||||||||||' + settings.PAYU_SALT
    return hash_string

def generate_hash(params):
    hash_string = get_hash_string(params)
    return hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()

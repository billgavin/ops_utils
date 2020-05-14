from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64

def RSAUtils(object):

    def __init__(self, pub_key):

    def generateKeys(self, key_length=1024):
        random_gen = Random.new().read
        ras = RSA.generate(key_length, random_gen)
        private_pem = rsa.exportKey()
        public_pem = rsa.publickey().exportKey()

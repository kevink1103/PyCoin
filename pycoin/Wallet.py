import binascii

import Crypto
import Crypto.Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

from pycoin import Transaction

# EE4017 Lab 4


class Wallet:
    # constructor (create an object from the Wallet class)
    # both keys are stored in terms of Crypto object
    def __init__(self):
        random = Crypto.Random.new().read
        # private key is the proof that you own this wallet
        # => derive a public key from the private key
        self._private_key = RSA.generate(1024, random)
        # public key is your wallet address
        # => randomly generate a public key from the private key
        self._public_key = self._private_key.publickey()

    # method to prove that the signature is coming from the actual owner in a transaction
    # implemented in the Wallet class instead of Transaction class to protect the private key from illegal access
    def sign_transaction(self, transaction: Transaction) -> str:
        signer = PKCS1_v1_5.new(self._private_key)
        payload = str(transaction.to_dict()).encode('utf-8')
        h = SHA.new(payload)
        return binascii.hexlify(signer.sign(h)).decode('ascii')

    # method to export the public key in DER formation and decodes it using ascii decode
    @property  # getter function for public key (identity)
    def pubkey(self) -> str:
        pubkey = binascii.hexlify(self._public_key.exportKey(format='DER'))
        return pubkey.decode('ascii')

    # method to export the private key in DER formation and decodes it using ascii decode
    @property  # getter function for private key
    def secret(self) -> str:
        seckey = binascii.hexlify(self._private_key.exportKey(format='DER'))
        return seckey.decode('ascii')

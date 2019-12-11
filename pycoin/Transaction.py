import binascii
import json

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

# EE4017 Lab 4


class Transaction:
    # constructor to define the sender, recipient and value in a transaction
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value

    # method to dump all contents (except signature) in the transaction as a dictionary
    def to_dict(self) -> dict:
        # Signature is not included here
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'value': self.value
        }

    # json encoding method
    def to_json(self) -> str:
        return json.dumps(self.__dict__, sort_keys=False)

    # method to add a signature to the transaction
    def add_signature(self, signature) -> None:
        self.signature = signature

    # method to verify the signature in the transaction
    def verify_transaction_signature(self) -> bool:
        if hasattr(self, 'signature'):
            pubkey = RSA.importKey(binascii.unhexlify(self.sender))
            verifier = PKCS1_v1_5.new(pubkey)
            payload = str(self.to_dict()).encode('utf-8')
            h = SHA.new(payload)
            try:
                return verifier.verify(h, binascii.unhexlify(self.signature))
            except ValueError:
                return False
        else:
            return False

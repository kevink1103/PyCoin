import binascii
import json

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value

    def to_dict(self) -> dict:
        # Signature is not included here
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'value': self.value
        }

    def to_json(self) -> str:
        return json.dumps(self.__dict__, sort_keys=False)
    
    def add_signature(self, signature) -> None:
        self.signature = signature

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

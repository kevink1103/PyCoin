import binascii
import json

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA

# EE4017 Lab 4

class Transaction:
    def __init__(self, sender, recipient, value):
        '''constructor to define the sender, recipient and value in a transactiom'''
        self.sender = sender
        self.recipient = recipient
        self.value = value

    
    def to_dict(self) -> dict:
        '''method to dump all contents (except signature) in the transaction as a dictionary'''
        # Signature is not included here
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'value': self.value
        }

    def to_json(self) -> str:
        '''method to generate JSON format from all contents of the transaction'''
        return json.dumps(self.__dict__, sort_keys=False)

    def add_signature(self, signature) -> None:
        '''method to add a signature to the transaction'''
        self.signature = signature

    def verify_transaction_signature(self) -> bool:
        '''method to verify the signature in the transaction'''
        if hasattr(self, 'signature'): # check if signature exists
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

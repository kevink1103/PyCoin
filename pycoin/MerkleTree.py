# https://ihpark92.tistory.com/57

from hashlib import sha256
from typing import List

from pyprnt import prnt

from pycoin import Transaction

# EE4017 Lab 7
# Implement partial validation by requesting Merkle Path from light node to full node

# These txHashes should already be hashed
txHashes = [
    "00baf6626abc2df808da36a518c69f09b0d2ed0a79421ccfde4f559d2e42128b",
    "91c5e9f288437262f218c60f986e8bc10fb35ab3b9f6de477ff0eb554da89dea",
    "46685c94b82b84fa05b6a0f36de6ff46475520113d5cb8c6fb060e043a0dbc5c",
    "ba7ed2544c78ad793ef5bb0ebe0b1c62e8eb9404691165ffcb08662d1733d7a8",
]


class MerkleTree:
    def __init__(self):
        pass
    
    @staticmethod
    def hash(a, b):
        a = str(a).encode()
        b = str(b).encode()
        result = sha256(a + b).hexdigest()
        return result

    @staticmethod
    def transactionHashes(transactions: List[str]):
        return [sha256(str(transaction).encode()).hexdigest() for transaction in transactions]

    @staticmethod
    def merkleRoot(leaves):
        # prnt("Root Calculation")
        # prnt(leaves)
        if len(leaves) <= 1:
            return leaves[0]

        roots = []
        index = 0
        while index < len(leaves):
            a = leaves[index]
            b = leaves[index+1] if index+1 < len(leaves) else leaves[index]
            root = MerkleTree.hash(a, b)
            roots.append(root)
            index += 2
        
        return MerkleTree.merkleRoot(roots)

    @staticmethod
    def merklePath(leaves, point, path):
        if len(leaves) <= 1:
            return path

        roots = []
        next_point = ""
        index = 0
        while index < len(leaves):
            a = leaves[index]
            b = leaves[index+1] if index+1 < len(leaves) else leaves[index]
            root = MerkleTree.hash(a, b)
            roots.append(root)

            if a == point:
                path.append(["1", b])
                next_point = root
            elif b == point:
                path.append(["0", a])
                next_point = root
            index += 2

        return MerkleTree.merklePath(roots, next_point, path)

    @staticmethod
    def partialValidation(path, target):
        result = target
        for p in path:
            direction = int(p[0])
            h = p[1]

            if direction == 0:
                result = MerkleTree.hash(h, result)
            else:
                result = MerkleTree.hash(result, h)
        return result

def main():
    # tree = MerkleTree(txHashes)
    # # Recursive Root Finder
    # root = tree.merkleRoot(txHashes)
    # print(root)
    # # Manual Root Finder
    # ab = tree.hash(txHashes[0], txHashes[1])
    # cd = tree.hash(txHashes[2], txHashes[3])
    # print(tree.hash(ab, cd))

    # # Path
    # target = txHashes[1]
    # path = tree.merklePath(txHashes, target, [])
    # prnt(path)

    # # Valid
    # valid = tree.partialValidation(path, target)
    # print(valid)

    # Transaction(sender, recipient, transferred value of coins)
    transaction1 = Transaction("Kevin", "Chronos", "5.0", "0.5")
    transaction2 = Transaction("Chronos", "Erica", "2.0", "0.2")
    transaction3 = Transaction("Erica", "Kevin", "1.0", "0.1")
    transaction4 = Transaction("Claire", "Kevin", "1.2", "0.1")
    transaction5 = Transaction("Lora", "Chronos", "3.3, ""0.3")
    transactions = [transaction1.to_json(), transaction2.to_json(), transaction3.to_json(), transaction4.to_json(), transaction5.to_json()]
    prnt(transactions)
    hashes = MerkleTree.transactionHashes(transactions)
    prnt(hashes)
    root = MerkleTree.merkleRoot(hashes)
    prnt("ROOT", root)

    target = transaction2.to_json()
    targetHash = MerkleTree.transactionHashes([target])[0]
    prnt(targetHash)
    path = MerkleTree.merklePath(hashes, targetHash, [])
    prnt(path)

    new_root = MerkleTree.partialValidation(path, targetHash)
    print(new_root)


if __name__ == "__main__":
    main()

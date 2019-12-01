# https://ihpark92.tistory.com/57

from hashlib import sha256

from pyprnt import prnt

# These txHashes should already be hashed
txHashes = [
    "00baf6626abc2df808da36a518c69f09b0d2ed0a79421ccfde4f559d2e42128b",
    "91c5e9f288437262f218c60f986e8bc10fb35ab3b9f6de477ff0eb554da89dea",
    "46685c94b82b84fa05b6a0f36de6ff46475520113d5cb8c6fb060e043a0dbc5c",
    "ba7ed2544c78ad793ef5bb0ebe0b1c62e8eb9404691165ffcb08662d1733d7a8",
]

class MerkleTree:
    def __init__(self, txHashes):
        pass

    def hash(self, a, b):
        a = str(a).encode()
        b = str(b).encode()
        result = sha256(a + b).hexdigest()
        return result

    def merkleRoot(self, leaves):
        prnt(leaves)
        if len(leaves) <= 1:
            return leaves[0]

        roots = []
        index = 0
        while index < len(leaves):
            a = leaves[index]
            b = leaves[index+1] if index+1 < len(leaves) else leaves[index]
            root = self.hash(a, b)
            roots.append(root)
            index += 2
        
        return self.merkleRoot(roots)

    def merklePath(self, leaves, point, path):
        if len(leaves) <= 1:
            return path

        roots = []
        next_point = ""
        index = 0
        while index < len(leaves):
            a = leaves[index]
            b = leaves[index+1] if index+1 < len(leaves) else leaves[index]
            root = self.hash(a, b)
            roots.append(root)

            if a == point:
                path.append(["1", b])
                next_point = root
            elif b == point:
                path.append(["0", a])
                next_point = root
            index += 2

        return self.merklePath(roots, next_point, path)
            

    def partialValidation(self, path, target):
        result = target
        for p in path:
            direction = int(p[0])
            h = p[1]

            if direction == 0:
                result = self.hash(h, result)
            else:
                result = self.hash(result, h)
        return result

def main():
    tree = MerkleTree(txHashes)
    # Recursive Root Finder
    root = tree.merkleRoot(txHashes)
    print(root)
    # Manual Root Finder
    ab = tree.hash(txHashes[0], txHashes[1])
    cd = tree.hash(txHashes[2], txHashes[3])
    print(tree.hash(ab, cd))

    # Path
    target = txHashes[1]
    path = tree.merklePath(txHashes, target, [])
    prnt(path)

    # Valid
    valid = tree.partialValidation(path, target)
    print(valid)

if __name__ == "__main__":
    main()

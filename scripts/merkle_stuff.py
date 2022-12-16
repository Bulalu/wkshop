from brownie import accounts, web3
from eth_utils import encode_hex
from eth_abi.packed import encode_abi_packed
from itertools import zip_longest
import pandas as pd
import csv

# to install 3rd party libraries use -> pipx inject eth-brownie <module>

def prepare_merkle_tree(white_list):
 
   
 
    elements = [
        (index, account )
        for index, (account ) in enumerate(white_list)
    ]

    # print(elements)

    nodes =   [
        encode_hex(encode_abi_packed(["uint", "address"], el))
        for el in elements
    ]

    # print(nodes)
   
    tree = MerkleTree(nodes)


    distribution = {
        "merkleRoot": encode_hex(tree.root),
        "claims": {
            user: {
                "index": index,
                "proof": tree.get_proof(nodes[index]),
            }
            for index, user in elements
        },
    }
    return distribution

class MerkleTree:
    def __init__(self, elements):
        self.elements = sorted(set(web3.keccak(hexstr=el) for el in elements))
        self.layers = MerkleTree.get_layers(self.elements)

    @property
    def root(self):
        return self.layers[-1][0]

    def get_proof(self, el):
        el = web3.keccak(hexstr=el)
        idx = self.elements.index(el)
        proof = []
        for layer in self.layers:
            pair_idx = idx + 1 if idx % 2 == 0 else idx - 1
            if pair_idx < len(layer):
                proof.append(encode_hex(layer[pair_idx]))
            idx //= 2
        return proof

    @staticmethod
    def get_layers(elements):
        layers = [elements]
        while len(layers[-1]) > 1:
            layers.append(MerkleTree.get_next_layer(layers[-1]))
        return layers

    @staticmethod
    def get_next_layer(elements):
        return [
            MerkleTree.combined_hash(a, b)
            for a, b in zip_longest(elements[::2], elements[1::2])
        ]

    @staticmethod
    def combined_hash(a, b):
        if a is None:
            return b
        if b is None:
            return a
        return web3.keccak(b"".join(sorted([a, b])))


def main():
    x = prepare_merkle_tree()
    print(x["merkleRoot"])
    print(x["claims"][accounts[2].address]["proof"])
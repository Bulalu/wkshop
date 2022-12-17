from brownie import NFT, accounts, config, network
from scripts.helpful_scripts import get_account
from scripts.merkle_stuff import prepare_merkle_tree
from merkletools import *
from scripts.address import whitelist_mainnet
import json

whiteList = [account.address for account in accounts]

TOKEN_URI = "https://gateway.pinata.cloud/ipfs/QmervZ8eAm9KenCvBnSaS9v4Y2nCiAzv3XhjpMR32TozTh"

# https://testnets.opensea.io/collection/hogwarts-lw66ez90bg

def deploy_nft():
    owner = get_account()
    name = "Hogwarts"
    symbol = "HGT"

    distribution = prepare_merkle_tree(whitelist_mainnet)
    merkle_root = distribution["merkleRoot"]
    if (len(NFT)!= 0):
        return NFT[-1], distribution
    filename = f'{merkle_root}.json'          
    with open(filename, 'w') as file_object: 
        json.dump(distribution, file_object, indent=4) 
        
    contract = NFT.deploy(name, symbol, merkle_root, {"from": owner})

    contract.setTokenURI(TOKEN_URI, {"from": owner}) 

    assert merkle_root == contract.merkleRoot()
    return contract, distribution


def grant_nft_to_users():

    owner = get_account()
    contract, distribution = deploy_nft()
   
    # merkle_proof = distribution["claims"][owner.address]["proof"]
    # index = distribution["claims"][owner.address]["index"]
   
    for address in whitelist_mainnet:
        merkle_proof = distribution["claims"][address]["proof"]
        index = distribution["claims"][address]["index"]
        tx = contract.grantNFT( 1, merkle_proof, index, address, {"from": owner})
        tx.wait(1)
    
    print("NFTs sent 🚢")


def main():
    # deploy_nft()
    grant_nft_to_users()


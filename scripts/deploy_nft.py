from brownie import NFT, accounts, config, network
from scripts.helpful_scripts import get_account
from scripts.merkle_stuff import prepare_merkle_tree
from merkletools import *

# mt = MerkleTools(hash_type="md5")



whiteList = [account.address for account in accounts]
whiteList_mainnet = ["0xa3dD11E7D3Aa89b9e0598ac0d678910417d63989", "0xA66F90C0B7be6955D6c8f9B16dfD0A56171e038e"]
TOKEN_URI = "https://gateway.pinata.cloud/ipfs/QmervZ8eAm9KenCvBnSaS9v4Y2nCiAzv3XhjpMR32TozTh"

# https://testnets.opensea.io/collection/hogwarts-lw66ez90bg

def deploy_nft():
    owner = get_account()
    name = "Hogwarts"
    symbol = "HGT"

    distribution = prepare_merkle_tree(whiteList_mainnet)
    merkle_root = distribution["merkleRoot"]

    print(f"Merkle root: {merkle_root}")
 
 
    contract = NFT.deploy(name, symbol, merkle_root, {"from": owner}, publish_source=config["networks"][network.show_active()]["verify"])

    contract.setTokenURI(TOKEN_URI, {"from": owner}) 

    assert merkle_root == contract.merkleRoot()
    return contract, distribution


def grant_nft_to_users():

    owner = get_account()
    contract, distribution = deploy_nft()
   
    merkle_proof = distribution["claims"][owner.address]["proof"]
    index = distribution["claims"][owner.address]["index"]

    contract.grantNFT( 1, merkle_proof, index, {"from": owner})
    


def main():
    # deploy_nft()
    grant_nft_to_users()


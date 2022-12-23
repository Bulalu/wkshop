from brownie import Contract, accounts, RewardNFT, config, network
from scripts.helpful_scripts import get_account
import pandas as pd
from scripts.address import whitelist_mainnet

#0.1059

def deploy_rewarder():
    deployer = get_account()
    new_admin = "0xFD0571eFf4aDE0cbAaeaf07b8ea9D24FDE01Ff0F"
    token_uri = "https://gateway.pinata.cloud/ipfs/QmX6imS35656Fwd1H7CBV9bE2Gs2XjTaCr82QsiRGwJbJ1"

    print("Launching on Mainnet in")
    print("3\n2\n1!")
    print("🚀 🚀 ")

    print(f"OWNER BALANCE BEFORE DEPLOYING", deployer.balance()/10**18)
    # Deploy the NFT contract
    contract = RewardNFT.deploy({"from": deployer}, publish_source=config["networks"][network.show_active()]["verify"])
    
    print(f"OWNER BALANCE AFTER DEPLOYING", deployer.balance()/10**18)
    
    print("Setting the URI")
    contract.setBaseURI(token_uri, {"from":deployer})

 
    #transfer ownership
    # print("Transfering ownership 😪")
    # contract.transferOwnership(new_admin, {"from": deployer})
    print("We are live on mainnet baby 🚢")
    # assert contract.owner() == new_admin
    return contract, deployer

def distribute_rewards():
   
    # contract, deployer = deploy_rewarder()
    deployer = get_account()
    contract = RewardNFT[-1]  
    
    for address in whitelist_mainnet:
       tx = contract.mint(address, 1, {"from": deployer})
       tx.wait(1)
  

def update_token_uri():
    deployer = get_account()
    contract = RewardNFT[-1]   
    token_uri = "https://gateway.pinata.cloud/ipfs/QmZUoy6DKSAJw6GsGa1tpHP8HVYXCqacHZvMeVYdMqKbpE"

    contract.setBaseURI(token_uri, {"from": deployer})


def main():
    deploy_rewarder()
    # distribute_rewards()
    # print(RewardNFT[-1])
    # update_token_uri()

  
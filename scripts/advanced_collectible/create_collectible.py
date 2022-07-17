import time
from scripts.utilities import get_account, get_contract, get_and_fund_subscription
from scripts.utilities import OPENSEA_URL, MockContract, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import config, network
from brownie import AdvancedCollectible


def main():
    account = get_account()
    ac = AdvancedCollectible[-1]
    ac.createCollectible({"from": account})

    print("Collectible created")
    time.sleep(1)

import time
from scripts.utilities import get_account
from brownie import AdvancedCollectible


def create_collectible():
    account = get_account()
    ac = AdvancedCollectible[-1]
    tx = ac.createCollectible({"from": account})

    print(f"Collectible created on contract {ac.address}")
    return tx


def main():
    create_collectible()
    time.sleep(1)

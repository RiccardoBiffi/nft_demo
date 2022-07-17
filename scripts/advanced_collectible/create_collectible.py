import time
from scripts.utilities import get_account
from brownie import AdvancedCollectible


def main():
    account = get_account()
    ac = AdvancedCollectible[-1]
    ac.createCollectible({"from": account})

    print(f"Collectible created on contract {ac.address}")
    time.sleep(1)

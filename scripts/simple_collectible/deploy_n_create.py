from scripts.utilities import get_account, OPENSEA_URL
from brownie import SimpleCollectible

sample_token_uri = (
    "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
)


def deploy_n_create():
    account = get_account()
    sc = SimpleCollectible.deploy({"from": account})
    tx = sc.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"You can see your NFT at {OPENSEA_URL.format(sc.address, sc.tokenCounter()-1)}"
    )
    print("Wait 20 minutes and hit the refresh metadata button.")
    return sc


def main():
    deploy_n_create()

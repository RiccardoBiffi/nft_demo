import time
from brownie import network, AdvancedCollectible
from scripts.utilities import OPENSEA_URL, get_account, get_breed
import json


def set_tokenURI():
    print(f"Working on {network.show_active()}")
    ac = AdvancedCollectible[-1]

    n_token = ac.tokenCounter()
    print(f"You have created {n_token} NFT on contract {ac.address}\n")

    for token_id in range(n_token):
        NFT_metadata_URI = get_metadata_URI(token_id)

        if not ac.tokenURI(token_id).startswith("https://"):
            print(f"Setting token URI to token id {token_id}")
            set_NFT_tokenURI(token_id, ac, NFT_metadata_URI)

    print("Give some minutes to OpenSea to link the token URI to your NFTs!")


def set_NFT_tokenURI(token_id, NFT_contract, token_URI):
    tx = NFT_contract.setTokenURI(token_id, token_URI, {"from": get_account()})
    tx.wait(1)
    print(
        f"You can see your NTF at {OPENSEA_URL.format(NFT_contract.address, token_id)}"
    )


def get_metadata_URI(token_id):
    with open(f"./metadata/{network.show_active()}/URIs.json") as fp:
        data = json.load(fp)

    return data[str(token_id)]


def set_tokenURI_test(ac, URI):
    set_NFT_tokenURI(0, ac, URI)


def main():
    set_tokenURI()
    time.sleep(1)

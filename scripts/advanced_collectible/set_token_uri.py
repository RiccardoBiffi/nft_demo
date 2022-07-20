from brownie import network, AdvancedCollectible
from scripts.utilities import OPENSEA_URL, get_account, get_breed
import json


def main():
    print(f"Working on {network.show_active()}")
    ac = AdvancedCollectible[-1]

    n_token = ac.tokenCounter()
    print(f"You have created {n_token} NFT on contract {ac.address}\n")

    for token_id in range(n_token):
        breed = get_breed(ac.tokenId_Breed(token_id))

        NFT_metadata_URI = get_metadata_URI(token_id, breed)

        if not ac.tokenURI(token_id).startswith("https://"):
            print(f"Setting token URI to token id {token_id}")
            set_tokenURI(token_id, ac, NFT_metadata_URI)

    print("Give some minutes to OpenSea to link the token URI to your NFTs!")


def set_tokenURI(token_id, NFT_contract, token_URI):
    tx = NFT_contract.setTokenURI(token_id, token_URI, {"from": get_account()})
    tx.wait(1)
    print(
        f"You can see your NTF at {OPENSEA_URL.format(NFT_contract.address, token_id)}"
    )


def get_metadata_URI(token_id, breed):
    with open(f"./metadata/{network.show_active()}/{token_id}-{breed}.hash.json") as fp:
        data = json.load(fp)

    return data["hash"]

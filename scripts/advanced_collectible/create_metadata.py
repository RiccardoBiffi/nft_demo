import imp
import time
from scripts.utilities import get_breed
from brownie import AdvancedCollectible, network
from metadata.metadata_template import metadata_template
from pathlib import Path


def main():
    ac = AdvancedCollectible[-1]
    n_token = ac.tokenCounter()
    print(f"You have created {n_token} NFT on contract {ac.address}")

    for token_id in range(n_token):
        breed = get_breed(ac.tokenId_Breed(token_id))
        md_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        print(f"{token_id}:  {md_file_name}")

        NFT_metadata = metadata_template
        if Path(md_file_name).exists():
            print(f"File {md_file_name} already exists. Delete it to overwrite it")
        else:
            print(f"Creating {md_file_name}")
            NFT_metadata["name"] = breed
            NFT_metadata["description"] = f"A beautiful {breed} pup. Such a good boy!"
            NFT_metadata["image"] = upload_to_IPFS()
            print(NFT_metadata)

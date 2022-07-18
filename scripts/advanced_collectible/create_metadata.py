import json
from pathlib import Path
from brownie import config
from scripts.utilities import get_breed, is_local_blockchain
from scripts.upload_to_ipfs import (
    upload_with_local_IPFS_node,
    upload_with_pinata,
    UploadType,
)
from brownie import AdvancedCollectible, network
from metadata.metadata_template import metadata_template


def create_NTFs_metadata():
    ac = AdvancedCollectible[-1]
    n_token = ac.tokenCounter()
    print(f"You have created {n_token} NFT on contract {ac.address}\n")

    for token_id in range(n_token):
        breed = get_breed(ac.tokenId_Breed(token_id))
        md_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"

        if config["ipfs"]["overwrite_metadata"] or not Path(md_file_name).exists():
            create_metadata(md_file_name, breed)

        else:
            print(f"File {md_file_name} already exists. Delete it to overwrite it")
            print("Check brownie-config > ipfs > overwrite_metadata\n")


def get_image_from(breed):
    return "./img/" + breed.lower().replace("_", "-") + ".png"


def create_metadata(md_file_name, breed):
    print(f"Creating {md_file_name}")

    NFT_metadata = metadata_template
    NFT_metadata["name"] = breed
    NFT_metadata["description"] = f"A beautiful {breed} pup. Such a good boy!"
    image_path = get_image_from(breed)
    image_uri = (
        upload_with_pinata(image_path)
        if config["ipfs"]["upload_type"] == UploadType.PINATA.value
        else upload_with_local_IPFS_node(image_path)
    )
    NFT_metadata["image"] = image_uri

    # save metadata on file
    with open(md_file_name, "w") as fp:
        json.dump(NFT_metadata, fp)

    if config["ipfs"]["upload_type"] == UploadType.PINATA.value:
        upload_with_pinata(md_file_name)
    else:
        upload_with_local_IPFS_node(md_file_name)


def main():
    if is_local_blockchain():
        print("\n!!!Run me on the rinkeby network!!!\n")
        return
    create_NTFs_metadata()

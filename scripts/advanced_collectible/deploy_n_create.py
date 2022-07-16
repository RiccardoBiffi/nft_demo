import time
from scripts.utilities import get_account, get_contract, get_and_fund_subscription
from scripts.utilities import OPENSEA_URL, MockContract, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import config, network
from brownie import AdvancedCollectible

GAS_LIMIT_PER_WORD = 200000
BLOCK_CONFIRMATIONS = 3
RANDOM_WORDS = 1


def deploy_n_create():
    account = get_account()
    vrf = get_contract(MockContract.VRF_COORDINATOR)
    link = get_contract(MockContract.LINK_TOKEN)
    sub_id = get_and_fund_subscription()

    ac = AdvancedCollectible.deploy(
        vrf.address,
        link.address,
        sub_id,
        config["networks"][network.show_active()]["keyhash"],
        GAS_LIMIT_PER_WORD * RANDOM_WORDS,
        BLOCK_CONFIRMATIONS,
        RANDOM_WORDS,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # add the contract as a consumer of the chainlink subscription
        vrf.addConsumer.transact(
            sub_id,
            ac.address,
            {"from": account},
        )

    tx = ac.createCollectible({"from": account, "gasPrice": 10**9})

    request_id = tx.events["RequestedRandomness"]["requestId"]
    sender = tx.events["RequestedCollectible"]["from"]
    print(f"Request {request_id} from {sender}\n")

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # call to fulfillRandomWords on the mock to activate my callback
        requestId = tx.events["RequestedRandomness"]["requestId"]
        vrf.fulfillRandomWords(requestId, ac.address, {"from": account})
    else:
        # waiting for the network callback
        time.sleep(30)


def main():
    deploy_n_create()
    time.sleep(1)

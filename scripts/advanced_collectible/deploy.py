import time
from scripts.utilities import (
    get_account,
    get_contract,
    get_and_fund_subscription,
    maybe_add_contract_as_VRF_consumer,
)
from scripts.utilities import MockContract
from brownie import config, network
from brownie import AdvancedCollectible

GAS_LIMIT_PER_WORD = 200000
BLOCK_CONFIRMATIONS = 3
RANDOM_WORDS = 1


def deploy():
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

    maybe_add_contract_as_VRF_consumer(sub_id, ac.address)

    return ac


def main():
    deploy()
    time.sleep(1)

import pytest
from scripts.advanced_collectible.deploy_n_create import deploy_n_create
from brownie import network
from scripts.utilities import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    MockContract,
    get_account,
    get_contract,
)


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    # Arrange
    account = get_account()

    # Act
    ac, tx = deploy_n_create()
    # call to mock's fulfillRandomWords to activate my callback
    requestId = tx.events["RequestedRandomness"]["requestId"]
    get_contract(MockContract.VRF_COORDINATOR).fulfillRandomWords(
        requestId, ac.address, {"from": account}
    )

    # Assert
    assert ac.ownerOf(0) == account
    assert ac.tokenCounter() > 0
    assert ac.tokenId_Breed(ac.tokenCounter() - 1) == 2

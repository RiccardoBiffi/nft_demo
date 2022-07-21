import pytest
from scripts.advanced_collectible.deploy import deploy
from scripts.advanced_collectible.create_collectible import create_collectible
from scripts.advanced_collectible.set_token_uri import set_tokenURI_test
from brownie import network
from scripts.utilities import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    MockContract,
    get_account,
    get_contract,
)


def test_can_deploy_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    # Arrange
    account = get_account()

    # Act
    ac = deploy()

    # Assert
    assert ac.address == "0xe0aA552A10d7EC8760Fc6c246D391E698a82dDf9"


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    # Arrange
    account = get_account()
    ac = deploy()

    # Act
    tx = create_collectible()

    # call to mock's fulfillRandomWords to activate my callback
    requestId = tx.events["RequestedRandomness"]["requestId"]
    get_contract(MockContract.VRF_COORDINATOR).fulfillRandomWords(
        requestId, ac.address, {"from": account}
    )

    # Assert
    assert ac.ownerOf(0) == account
    assert ac.tokenCounter() > 0
    assert ac.tokenId_Dog(ac.tokenCounter() - 1)[0] == 2
    assert ac.tokenId_Dog(ac.tokenCounter() - 1)[1] == 7
    assert ac.tokenId_Dog(ac.tokenCounter() - 1)[2] == 5
    assert ac.tokenId_Dog(ac.tokenCounter() - 1)[3] == 7
    assert ac.tokenId_Dog(ac.tokenCounter() - 1)[4] == 81


def test_can_set_token_URI_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    # Arrange
    account = get_account()
    ac = deploy()
    tx = create_collectible()
    # call to mock's fulfillRandomWords to activate my callback
    requestId = tx.events["RequestedRandomness"]["requestId"]
    get_contract(MockContract.VRF_COORDINATOR).fulfillRandomWords(
        requestId, ac.address, {"from": account}
    )

    # Act
    set_tokenURI_test(ac, "http://test")

    # Assert
    assert ac.tokenURI(0) == "http://test"

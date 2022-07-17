import pytest
from scripts.advanced_collectible.deploy_n_create import deploy_n_create
from brownie import network
from scripts.utilities import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import time


def test_can_create_advanced_collectible_integration():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")

    # Arrange
    account = get_account()

    # Act
    ac, _ = deploy_n_create()
    # waiting for the network to callback
    time.sleep(70)

    # Assert
    assert ac.ownerOf(0) == account
    assert ac.tokenCounter() > 0

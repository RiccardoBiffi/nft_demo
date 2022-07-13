import pytest
from scripts.deploy_n_create import deploy_n_create
from brownie import network, accounts
from scripts.utilities import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account


def test_can_create_simple_collectible():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    # Act
    sc = deploy_n_create()

    # Assert
    assert sc.ownerOf(0) == get_account()

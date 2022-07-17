from enum import Enum
from brownie import network, accounts, config, Contract
from brownie import LinkToken, VRFCoordinatorV2Mock
from brownie import web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"  # contract_address/token_ID


class MockContract(Enum):
    LINK_TOKEN = "link_token"
    VRF_COORDINATOR = "vrf_coordinator"


contract_to_mock = {
    MockContract.LINK_TOKEN: LinkToken,
    MockContract.VRF_COORDINATOR: VRFCoordinatorV2Mock,
}


def is_local_blockchain():
    return network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]  # Ganache's first account
    if id:
        return accounts.load(id)

    # mainnet
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_enum):
    """
    Get the specified contract.
    If the blockchain is a fork or external, it's got from brownie-config;
    otherwise, if we are on a local blockchain, a mock is deployed and returned.
    Args:
        contract_enum (MockContract): enum of the contract to get

    Returns:
        brownie.network.contract.ProjectContract : last deployed version of the contract,
        it can be a mock or a contract on a real chain.
    """
    contract_type = contract_to_mock[contract_enum]

    if is_local_blockchain():
        if len(contract_type) == 0:
            # never deployed contract
            deploy_mock(contract_enum)
        # last deployed contract
        contract = contract_type[-1]

    else:
        try:
            # contract already deployed on chain (fork or testnet)
            contract_address = config["networks"][network.show_active()][
                contract_enum.value
            ]
            contract = Contract.from_abi(
                contract_type._name, contract_address, contract_type.abi
            )
        except KeyError:
            print(
                f"{network.show_active()} address not found, perhaps you should add it to the config or deploy mocks?"
            )

    return contract


LINK_BASE_FEE = web3.toWei(0.1, "ether")
LINK_GAS_PRICE = web3.toWei(1, "gwei")
LINK_FUND_AMOUNT = web3.toWei(0.5, "ether")


def deploy_mock(contract_enum):
    """
    Deploys the contract mapped in the enum.
    """
    print(f"Deploying mock {contract_enum.value} to network: {network.show_active()}")
    if contract_enum == MockContract.LINK_TOKEN:
        LinkToken.deploy({"from": get_account()})
    elif contract_enum == MockContract.VRF_COORDINATOR:
        VRFCoordinatorV2Mock.deploy(
            LINK_BASE_FEE, LINK_GAS_PRICE, {"from": get_account()}
        )
    print(f"Mock {contract_enum.value} deployed!\n")


def get_and_fund_subscription():
    if is_local_blockchain():
        # on local development chains, I need to create the contract, subscribe and fund it
        vrf_contract = get_contract(MockContract.VRF_COORDINATOR)
        create_receipt = vrf_contract.createSubscription()

        sub_id = create_receipt.events["SubscriptionCreated"]["subId"]
        vrf_contract.fundSubscription(sub_id, LINK_FUND_AMOUNT)

    else:
        # contract already deployed, subscribed and funded. Check https://vrf.chain.link
        sub_id = config["subscriptions"]["chainlink"]

    return sub_id

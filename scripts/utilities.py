from brownie import network, accounts, config

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]  # primo account offerto da Ganache
    if id:
        return accounts.load(id)

    # siamo in mainnet
    return accounts.add(config["wallets"]["from_key"])


def is_local_blockchain():
    return network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS

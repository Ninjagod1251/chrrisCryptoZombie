"""
Shared fixtures for all CryptoZombies tests.
"""
import pytest

LEVEL_UP_FEE = 10 ** 15  # 0.001 ETH in wei


@pytest.fixture
def contract(project, accounts):
    """Deploy a fresh ZombieOwnership before each test."""
    return accounts[0].deploy(project.ZombieOwnership)


@pytest.fixture
def alice(accounts):
    return accounts[0]


@pytest.fixture
def bob(accounts):
    return accounts[1]


@pytest.fixture
def carol(accounts):
    return accounts[2]


def create_zombie(contract, account, name):
    """Helper: create a zombie and return its ID."""
    tx = contract.createRandomZombie(name, sender=account)
    return list(tx.decode_logs(contract.NewZombie))[0].zombieId

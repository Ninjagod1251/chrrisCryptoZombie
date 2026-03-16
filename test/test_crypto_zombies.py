"""
CryptoZombies test suite — Ape/pytest version
Mirrors the original Truffle tests in test/CryptoZombies.js
Run with: ape test
"""
import pytest
from ape import reverts


ZOMBIE_NAME_1 = "Zombie 1"
ZOMBIE_NAME_2 = "Zombie 2"


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


# ── Basic creation ────────────────────────────────────────────────────────────

def test_create_zombie(contract, alice):
    """Alice can create one zombie and the NewZombie event is emitted."""
    tx = contract.createRandomZombie(ZOMBIE_NAME_1, sender=alice)
    assert tx.status == 1, "transaction should succeed"

    logs = list(tx.decode_logs(contract.NewZombie))
    assert len(logs) == 1
    assert logs[0].name == ZOMBIE_NAME_1


def test_no_two_zombies_same_owner(contract, alice):
    """A second createRandomZombie from the same address must revert."""
    contract.createRandomZombie(ZOMBIE_NAME_1, sender=alice)
    with reverts():
        contract.createRandomZombie(ZOMBIE_NAME_2, sender=alice)


# ── Ownership / ERC-721 transfer ──────────────────────────────────────────────

def test_single_step_transfer(contract, alice, bob):
    """Alice creates a zombie and transfers it directly to Bob."""
    tx = contract.createRandomZombie(ZOMBIE_NAME_1, sender=alice)
    zombie_id = list(tx.decode_logs(contract.NewZombie))[0].zombieId

    contract.transferFrom(alice, bob, zombie_id, sender=alice)
    assert contract.ownerOf(zombie_id) == bob


def test_two_step_transfer_approved_calls(contract, alice, bob):
    """Alice approves Bob, then Bob calls transferFrom."""
    tx = contract.createRandomZombie(ZOMBIE_NAME_1, sender=alice)
    zombie_id = list(tx.decode_logs(contract.NewZombie))[0].zombieId

    contract.approve(bob, zombie_id, sender=alice)
    contract.transferFrom(alice, bob, zombie_id, sender=bob)
    assert contract.ownerOf(zombie_id) == bob


def test_two_step_transfer_owner_calls(contract, alice, bob):
    """Alice approves Bob, then Alice still calls transferFrom herself."""
    tx = contract.createRandomZombie(ZOMBIE_NAME_1, sender=alice)
    zombie_id = list(tx.decode_logs(contract.NewZombie))[0].zombieId

    contract.approve(bob, zombie_id, sender=alice)
    contract.transferFrom(alice, bob, zombie_id, sender=alice)
    assert contract.ownerOf(zombie_id) == bob


# ── Combat ────────────────────────────────────────────────────────────────────

def test_zombie_attack(contract, alice, bob, chain):
    """Alice's zombie can attack Bob's zombie after the cooldown."""
    tx1 = contract.createRandomZombie(ZOMBIE_NAME_1, sender=alice)
    first_id = list(tx1.decode_logs(contract.NewZombie))[0].zombieId

    tx2 = contract.createRandomZombie(ZOMBIE_NAME_2, sender=bob)
    second_id = list(tx2.decode_logs(contract.NewZombie))[0].zombieId

    # Advance time by 1 day to clear the cooldown
    chain.pending_timestamp += 86400

    tx = contract.attack(first_id, second_id, sender=alice)
    assert tx.status == 1, "attack transaction should succeed"


# ── Zombie army ───────────────────────────────────────────────────────────────

def test_get_zombies_by_owner(contract, alice, bob):
    """getZombiesByOwner returns only the caller's zombies."""
    contract.createRandomZombie(ZOMBIE_NAME_1, sender=alice)
    contract.createRandomZombie(ZOMBIE_NAME_2, sender=bob)

    alice_zombies = contract.getZombiesByOwner(alice)
    bob_zombies = contract.getZombiesByOwner(bob)

    assert len(alice_zombies) == 1
    assert len(bob_zombies) == 1
    assert alice_zombies[0] != bob_zombies[0]


def test_zombie_stats_default(contract, alice):
    """A freshly created zombie starts at level 1 with no wins or losses."""
    tx = contract.createRandomZombie(ZOMBIE_NAME_1, sender=alice)
    zombie_id = list(tx.decode_logs(contract.NewZombie))[0].zombieId

    zombie = contract.zombies(zombie_id)
    assert zombie.level == 1
    assert zombie.winCount == 0
    assert zombie.lossCount == 0

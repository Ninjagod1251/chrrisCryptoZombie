"""
Tests — Zombie Ownership & ERC-721 Transfer
"""
from ape import reverts
from conftest import create_zombie

ZOMBIE_NAME_1 = "Zombie 1"
ZOMBIE_NAME_2 = "Zombie 2"


def test_owner_of_zombie(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    assert contract.ownerOf(z_id) == alice


def test_balance_after_creation(contract, alice, bob):
    create_zombie(contract, alice, ZOMBIE_NAME_1)
    create_zombie(contract, bob,   ZOMBIE_NAME_2)
    assert contract.balanceOf(alice) == 1
    assert contract.balanceOf(bob)   == 1


def test_new_account_has_zero_balance(contract, carol):
    assert contract.balanceOf(carol) == 0


def test_get_zombies_by_owner(contract, alice, bob):
    create_zombie(contract, alice, ZOMBIE_NAME_1)
    create_zombie(contract, bob,   ZOMBIE_NAME_2)
    alice_ids = contract.getZombiesByOwner(alice)
    bob_ids   = contract.getZombiesByOwner(bob)
    assert len(alice_ids) == 1
    assert len(bob_ids)   == 1
    assert alice_ids[0] != bob_ids[0]


def test_direct_transfer(contract, alice, bob):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    contract.transferFrom(alice, bob, z_id, sender=alice)
    assert contract.ownerOf(z_id) == bob


def test_transfer_updates_balances(contract, alice, bob):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    contract.transferFrom(alice, bob, z_id, sender=alice)
    assert contract.balanceOf(alice) == 0
    assert contract.balanceOf(bob)   == 1


def test_approved_can_transfer(contract, alice, bob):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    contract.approve(bob, z_id, sender=alice)
    contract.transferFrom(alice, bob, z_id, sender=bob)
    assert contract.ownerOf(z_id) == bob


def test_unapproved_cannot_transfer(contract, alice, bob):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    with reverts():
        contract.transferFrom(alice, bob, z_id, sender=bob)


def test_owner_can_transfer_after_approving(contract, alice, bob):
    """Owner retains the right to transfer even after granting approval."""
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    contract.approve(bob, z_id, sender=alice)
    contract.transferFrom(alice, bob, z_id, sender=alice)
    assert contract.ownerOf(z_id) == bob


def test_transferred_zombie_in_new_owner_list(contract, alice, bob):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    contract.transferFrom(alice, bob, z_id, sender=alice)
    assert z_id in contract.getZombiesByOwner(bob)
    assert z_id not in contract.getZombiesByOwner(alice)

"""
Tests — Burn (Zombie Cemetery)
"""
from ape import reverts
from conftest import create_zombie

ZOMBIE_NAME = "Zombie 1"


def test_burn_removes_ownership(contract, alice):
    """After burn, zombie is owned by address(0)."""
    z_id = create_zombie(contract, alice, ZOMBIE_NAME)
    contract.burnZombie(z_id, sender=alice)
    assert contract.zombieToOwner(z_id) == "0x0000000000000000000000000000000000000000"


def test_burn_decrements_balance(contract, alice):
    """After burn, owner balance drops by 1."""
    z_id = create_zombie(contract, alice, ZOMBIE_NAME)
    assert contract.balanceOf(alice) == 1
    contract.burnZombie(z_id, sender=alice)
    assert contract.balanceOf(alice) == 0


def test_burn_emits_transfer_to_zero(contract, alice):
    """Burn emits Transfer event to address(0)."""
    z_id = create_zombie(contract, alice, ZOMBIE_NAME)
    tx = contract.burnZombie(z_id, sender=alice)
    logs = list(tx.decode_logs(contract.Transfer))
    assert len(logs) == 1
    assert logs[0]._to == "0x0000000000000000000000000000000000000000"
    assert logs[0]._tokenId == z_id


def test_only_owner_can_burn(contract, alice, bob):
    """Non-owner cannot burn a zombie."""
    z_id = create_zombie(contract, alice, ZOMBIE_NAME)
    with reverts():
        contract.burnZombie(z_id, sender=bob)


def test_burn_zombie_not_in_owner_list(contract, alice):
    """Burned zombie no longer appears in getZombiesByOwner."""
    z_id = create_zombie(contract, alice, ZOMBIE_NAME)
    contract.burnZombie(z_id, sender=alice)
    ids = contract.getZombiesByOwner(alice)
    assert z_id not in ids

"""
Tests — Zombie Creation
"""
from ape import reverts
from conftest import create_zombie

ZOMBIE_NAME_1 = "Zombie 1"
ZOMBIE_NAME_2 = "Zombie 2"


def test_create_zombie_emits_event(contract, alice):
    """createRandomZombie emits NewZombie with correct name."""
    tx = contract.createRandomZombie(ZOMBIE_NAME_1, sender=alice)
    assert tx.status == 1
    logs = list(tx.decode_logs(contract.NewZombie))
    assert len(logs) == 1
    assert logs[0].name == ZOMBIE_NAME_1


def test_owner_can_create_multiple_zombies(contract, alice):
    """Same owner can create multiple zombies — army mode."""
    contract.createRandomZombie(ZOMBIE_NAME_1, sender=alice)
    contract.createRandomZombie(ZOMBIE_NAME_2, sender=alice)
    assert contract.balanceOf(alice) == 2


def test_zombie_starts_at_level_1(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    assert contract.zombies(z_id).level == 1


def test_zombie_starts_with_zero_wins_and_losses(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    z = contract.zombies(z_id)
    assert z.winCount == 0
    assert z.lossCount == 0


def test_zombie_dna_is_valid(contract, alice):
    """DNA is a nonzero number under 10^16."""
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    dna = contract.zombies(z_id).dna
    assert 0 < dna < 10 ** 16


def test_zombie_name_stored_correctly(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    assert contract.zombies(z_id).name == ZOMBIE_NAME_1

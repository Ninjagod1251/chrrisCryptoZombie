"""
Tests — Zombie Combat & Cooldown
"""
from ape import reverts
from conftest import create_zombie

ZOMBIE_NAME_1 = "Zombie 1"
ZOMBIE_NAME_2 = "Zombie 2"
ONE_DAY = 86400


def test_attack_succeeds_after_cooldown(contract, alice, bob, chain):
    a_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    b_id = create_zombie(contract, bob,   ZOMBIE_NAME_2)
    chain.mine(deltatime=ONE_DAY)
    tx = contract.attack(a_id, b_id, sender=alice)
    assert tx.status == 1


def test_attack_updates_win_or_loss(contract, alice, bob, chain):
    """After one attack, attacker has exactly 1 win or 1 loss."""
    a_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    b_id = create_zombie(contract, bob,   ZOMBIE_NAME_2)
    chain.mine(deltatime=ONE_DAY)
    contract.attack(a_id, b_id, sender=alice)
    z = contract.zombies(a_id)
    assert z.winCount + z.lossCount == 1


def test_attack_respects_cooldown(contract, alice, bob):
    """Attacking immediately after creation reverts due to cooldown."""
    a_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    b_id = create_zombie(contract, bob,   ZOMBIE_NAME_2)
    with reverts():
        contract.attack(a_id, b_id, sender=alice)


def test_only_owner_can_attack(contract, alice, bob, chain):
    """Bob cannot use Alice's zombie to attack."""
    a_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    b_id = create_zombie(contract, bob,   ZOMBIE_NAME_2)
    chain.mine(deltatime=ONE_DAY)
    with reverts():
        contract.attack(a_id, b_id, sender=bob)


def test_defender_win_loss_updated(contract, alice, bob, chain):
    """Defender also gets a win or loss recorded after the attack."""
    a_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    b_id = create_zombie(contract, bob,   ZOMBIE_NAME_2)
    chain.mine(deltatime=ONE_DAY)
    contract.attack(a_id, b_id, sender=alice)
    defender = contract.zombies(b_id)
    assert defender.winCount + defender.lossCount == 1

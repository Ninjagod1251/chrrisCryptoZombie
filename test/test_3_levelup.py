"""
Tests — Level Up & Name Change
"""
import pytest
from ape import reverts
from conftest import create_zombie, LEVEL_UP_FEE

ZOMBIE_NAME_1 = "Zombie 1"


def test_level_up_increments_level(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    contract.levelUp(z_id, sender=alice, value=LEVEL_UP_FEE)
    assert contract.zombies(z_id).level == 2


def test_level_up_wrong_fee_reverts(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    with reverts():
        contract.levelUp(z_id, sender=alice, value=LEVEL_UP_FEE - 1)


def test_level_up_zero_fee_reverts(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    with reverts():
        contract.levelUp(z_id, sender=alice, value=0)


def test_level_up_twice_reaches_level_3(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    contract.levelUp(z_id, sender=alice, value=LEVEL_UP_FEE)
    contract.levelUp(z_id, sender=alice, value=LEVEL_UP_FEE)
    assert contract.zombies(z_id).level == 3


def test_batch_level_up_reaches_correct_level(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    contract.batchLevelUp(z_id, 4, sender=alice, value=LEVEL_UP_FEE * 4)
    assert contract.zombies(z_id).level == 5


def test_batch_level_up_wrong_fee_reverts(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    with reverts():
        contract.batchLevelUp(z_id, 3, sender=alice, value=LEVEL_UP_FEE * 2)


def test_batch_level_up_zero_times_reverts(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    with reverts():
        contract.batchLevelUp(z_id, 0, sender=alice, value=0)


def test_batch_level_up_over_cap_reverts(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    with reverts():
        contract.batchLevelUp(z_id, 21, sender=alice, value=LEVEL_UP_FEE * 21)


def test_change_name_requires_level_2(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    with reverts():
        contract.changeName(z_id, "NewName", sender=alice)


def test_change_name_works_at_level_2(contract, alice):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    contract.levelUp(z_id, sender=alice, value=LEVEL_UP_FEE)
    contract.changeName(z_id, "Brainzilla", sender=alice)
    assert contract.zombies(z_id).name == "Brainzilla"


def test_change_name_only_owner(contract, alice, bob):
    z_id = create_zombie(contract, alice, ZOMBIE_NAME_1)
    contract.levelUp(z_id, sender=alice, value=LEVEL_UP_FEE)
    with reverts():
        contract.changeName(z_id, "Hijack", sender=bob)

"""
Tests — Withdraw (owner-only)
"""
from ape import reverts
from conftest import create_zombie, LEVEL_UP_FEE

ZOMBIE_NAME_1 = "Zombie 1"


def test_owner_can_withdraw(contract, alice, bob):
    """Owner withdraws level-up fees accumulated in the contract."""
    z_id = create_zombie(contract, bob, ZOMBIE_NAME_1)
    contract.levelUp(z_id, sender=bob, value=LEVEL_UP_FEE)
    balance_before = alice.balance
    contract.withdraw(sender=alice)
    assert alice.balance > balance_before


def test_non_owner_cannot_withdraw(contract, bob):
    with reverts():
        contract.withdraw(sender=bob)


def test_withdraw_empties_contract_balance(contract, alice, bob):
    """After withdraw, contract holds 0 ETH."""
    z_id = create_zombie(contract, bob, ZOMBIE_NAME_1)
    contract.levelUp(z_id, sender=bob, value=LEVEL_UP_FEE)
    contract.withdraw(sender=alice)
    assert contract.provider.get_balance(contract.address) == 0

"""
Seed multiple zombies owned by account #0 for local demo/testing.

Each zombie must be created from a unique address (contract enforces 1 per address).
Accounts #1-#4 each create a zombie, then transfer it to account #0.
"""
import re
from pathlib import Path

from ape import accounts, project

ZOMBIE_NAMES = ["Alpha", "Bravo", "Charlie", "Delta"]


def main():
    owner = accounts.test_accounts[0]

    # Read contract address from index.html
    html = (Path(__file__).parent.parent / "index.html").read_text()
    m = re.search(r'var cryptoZombiesAddress\s*=\s*"(0x[0-9a-fA-F]+)"', html)
    assert m, "Contract address not found in index.html — run deploy first"
    contract = project.ZombieOwnership.at(m.group(1))
    print(f"Contract: {contract.address}")
    print(f"Owner:    {owner.address}\n")

    for i, name in enumerate(ZOMBIE_NAMES):
        creator = accounts.test_accounts[i + 1]
        contract.createRandomZombie(name, sender=creator, gas_limit=1000000)
        zombie_id = contract.getZombiesByOwner(creator.address)[0]
        print(f"Created zombie #{zombie_id} '{name}' from {creator.address}")

        contract.transferFrom(creator.address, owner.address, zombie_id, sender=creator, gas_limit=200000)
        print(f"  Transferred #{zombie_id} to owner\n")

    ids = contract.getZombiesByOwner(owner.address)
    print(f"Owner now has {len(ids)} zombies: {list(ids)}")

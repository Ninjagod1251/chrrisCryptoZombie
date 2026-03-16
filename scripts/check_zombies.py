"""
check_zombies.py — query all zombies on-chain and print their stats
Run with: ape run check_zombies --network ethereum:local:hardhat
"""
import re
from pathlib import Path
from ape import project


def main():
    # Read contract address from index.html (kept in sync by deploy.py)
    html = (Path(__file__).parent.parent / "index.html").read_text()
    match = re.search(r'var cryptoZombiesAddress\s*=\s*"(0x[0-9a-fA-F]+)"', html)
    if not match:
        print("ERROR: could not find contract address in index.html")
        return
    address = match.group(1)
    zombie_contract = project.ZombieOwnership.at(address)

    print(f"\n{'='*50}")
    print(f"Contract : {zombie_contract.address}")
    print(f"{'='*50}")

    # Read total zombie count by iterating until a call fails
    zombie_id = 0
    found = 0
    while True:
        try:
            z = zombie_contract.zombies(zombie_id)
            owner = zombie_contract.zombieToOwner(zombie_id)
            print(f"\nZombie #{zombie_id}")
            print(f"  Owner   : {owner}")
            print(f"  Name    : {z.name}")
            print(f"  DNA     : {z.dna}")
            print(f"  Level   : {z.level}")
            print(f"  Wins    : {z.winCount}")
            print(f"  Losses  : {z.lossCount}")
            print(f"  Ready   : {z.readyTime}")
            zombie_id += 1
            found += 1
        except Exception:
            break

    print(f"\n{'='*50}")
    print(f"Total zombies on-chain: {found}")
    print(f"{'='*50}\n")

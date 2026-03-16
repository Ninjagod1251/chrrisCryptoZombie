from ape import project, accounts


def main():
    alice = accounts.test_accounts[9]
    contract = project.ZombieOwnership.at("0x5FbDB2315678afecb367f032d93F642f64180aa3")
    print(f"Zombie count for alice: {contract.getZombiesByOwner(alice)}")
    tx = contract.createRandomZombie("TestZombie", sender=alice)
    print(f"TX status: {tx.status}")
    zombies = contract.getZombiesByOwner(alice)
    print(f"Zombies: {zombies}")
    z = contract.zombies(zombies[0])
    print(f"Name: {z.name}, Level: {z.level}, DNA: {z.dna}")

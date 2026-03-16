from ape import accounts, project

def main():
    acct = accounts.test_accounts[0]
    contract = acct.deploy(project.ZombieOwnership)
    print("Contract deployed at:", contract.address)
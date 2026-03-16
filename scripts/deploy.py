import re
from pathlib import Path

from ape import accounts, project


def main():
    # Use 'deployer' keyfile for live networks, test_accounts for local
    try:
        acct = accounts.load("deployer")
    except Exception:
        acct = accounts.test_accounts[0]
    contract = acct.deploy(project.ZombieOwnership)
    print("Contract deployed at:", contract.address)

    # Update contract address in index.html
    html_path = Path(__file__).parent.parent / "index.html"
    html = html_path.read_text()
    updated = re.sub(
        r'(var cryptoZombiesAddress\s*=\s*")[^"]*(")',
        rf'\g<1>{contract.address}\g<2>',
        html,
    )
    html_path.write_text(updated)
    print("Updated index.html with new contract address.")

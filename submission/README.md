# CryptoZombies DApp — Midterm Project

## Team Members

| Name | CWID | Email |
|------|------|-------|
| Chris Cao | 891811242 | darknite1251@csu.fullerton.edu |

---

## Project Overview

A CryptoZombies decentralized application built on Ethereum smart contracts.
The project is organized into two milestones:

| Step | Folder | Description |
|------|--------|-------------|
| 1 | `step1_truffle_ganache/` | Starter code running with Truffle + Ganache (minimum requirement) |
| 2 | `step2_ape_migration/` | Upgraded to Ape framework for deployment and scripting |

---

## Improvements Made

1. **Ape Framework Migration** — replaced Truffle deployment with Ape (`scripts/deploy.py`),
   supporting `ape compile`, `ape run deploy`, and `ape test`.

2. **Auto-update frontend** — `scripts/deploy.py` automatically writes the deployed
   `ZombieOwnership` address into `index.html` after each deploy, removing the need
   to manually hard-code the address.

3. **Demo startup script** — `start_demo.sh` starts the Hardhat node, deploys contracts,
   and prints MetaMask setup instructions in one command.

---

## How to Run (Ape version — Step 2)

```bash
# Activate venv
source ../advBlockchain/bin/activate
export PATH="../advBlockchain/nodeenv/bin:$PATH"

# Compile
ape compile

# Deploy (also updates index.html)
ape run deploy --network ethereum:local:hardhat

# Serve frontend
npx http-server -p 8080
# Open http://localhost:8080
```

MetaMask: add network `http://127.0.0.1:8545`, Chain ID `31337`.
Import test account private key: `0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80`

---

## GitHub Repository

https://github.com/Ninjagod1251/chrrisCryptoZombie

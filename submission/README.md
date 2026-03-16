# CryptoZombies DApp — Midterm Project

## Team Members

| Name | CWID | Email |
|------|------|-------|
| Chris Cao | 891811242 | darknite1251@csu.fullerton.edu |

---

## Project Overview

A CryptoZombies decentralized application built on Ethereum smart contracts.
The project is organized into steps, each building on the last:

| Step | Branch | Folder | Description | Rubric |
|------|--------|--------|-------------|--------|
| 1 | `step1-truffle-ganache` | `step1_truffle_ganache/` | Starter code running with Truffle + Ganache | Minimum requirement (18 pts) |
| 2 | `step2-ape-migration` | `step2_ape_migration/` | Migrated to Ape Framework + Hardhat | Improvement #1 + #2 |
| 3 | `step3-nicer-website` | `step3_nicer_website/` | Improved UI with zombie cards and styling | Improvement #3 |
| 4 | `step4-multiple-zombies` | `step4_multiple_zombies/` | Demo multiple zombies across accounts | Improvement #4 |
| 5 | `step5-transfer` | `step5_transfer/` | Transfer zombie between accounts via frontend | Improvement #5 |
| 6 | `step6-zombie-image` | `step6_zombie_image/` | Zombie avatar generated from DNA | Improvement #6 |

---

## Improvements Made

1. **Ape Framework Migration** — replaced Truffle deployment with Ape (`scripts/deploy.py`),
   supporting `ape compile`, `ape run deploy`, and `ape test`.

2. **Auto-update frontend** — `scripts/deploy.py` automatically writes the deployed
   `ZombieOwnership` address into `index.html` after each deploy, removing the need
   to manually hard-code the address.

3. **Nicer website** — *(in progress)* improved CSS, zombie card layout.

4. **Multiple zombies** — *(in progress)* demo multiple accounts each owning a zombie.

5. **Transfer zombie** — *(in progress)* transfer button added to the frontend.

6. **Zombie image** — *(in progress)* zombie avatar generated from DNA value.

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

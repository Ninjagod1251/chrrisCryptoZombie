# CryptoZombies DApp — Midterm Project

## Team Members

| Name | CWID | Email |
|------|------|-------|
| Chris Cao | 891811242 | darknite1251@csu.fullerton.edu |

---

## Project Overview

A CryptoZombies decentralized application built on Ethereum smart contracts.
Started from the provided starter code and progressively improved across 4 steps.

| Step | Branch | Description | Rubric |
|------|--------|-------------|--------|
| 1 | `step1-truffle-ganache` | Starter code running with Truffle + Ganache | Minimum requirement |
| 2 | `step2-ape-migration` | Migrated to Ape Framework + Hardhat, auto-deploy | Improvement #1 + #2 |
| 3 | `step3-nicer-website` | Dark theme UI, zombie cards, test suite | Improvement #3 |
| 4 | `step4-5-6-improvements` | PvZ avatars, Transfer, Attack, Rename, DNA change, Sepolia | Improvement #4 + #5 + #6 |

---

## Improvements Made

### 1. Ape Framework Migration
Replaced Truffle + Ganache with **Ape Framework** + Hardhat.
- Deploy with `ape run deploy` instead of `truffle migrate`
- Python-based scripts instead of JavaScript migrations
- Hardhat replaces Ganache (better error messages, actively maintained)

### 2. Auto-Update Frontend (Not Hard-Coded)
`scripts/deploy.py` automatically writes the deployed contract address into
`index.html` after every deploy — no more manual copy/paste.
`scripts/update_frontend.js` does the same for Truffle users.

### 3. Nicer Website
Complete redesign of `index.html`:
- Dark zombie-themed UI with glowing green accents
- Zombie cards showing DNA, Level badge, Wins, Losses, Ready time
- Color-coded styled buttons with hover effects
- Connected wallet shown in header
- Human-readable error messages (no more `[object Object]`)
- Zombie count display ("X zombies in your army")

### 4. PvZ-Style Zombie Avatars from DNA
Each zombie gets a unique SVG avatar generated from its DNA value.
7 zombie types inspired by Plants vs Zombies:
- Regular, Cone, Bucket, Flag, Football, Disco, Newspaper
- Skin tone, eye style, tie color all vary per zombie
- Stitches appear at Level 3+, star badge at Level 5+

### 5. Full Function Frontend
All contract functions wired up with buttons on each zombie card:
- **Transfer** — send zombie to another address
- **Attack** — attack another zombie by ID, updates wins/losses
- **Rename** — change zombie name (requires Level 2+)
- **Change DNA** — mutate zombie DNA and change avatar (requires Level 20+)
- **Level Up** — send 0.001 ETH to level up

### 6. Deployed to Sepolia Testnet
Contract deployed to Ethereum Sepolia testnet (not just local blockchain):
- **Contract:** `0x3dBD39B485546f40816849B10612C79275A9678b`
- **Verify:** https://sepolia.etherscan.io/address/0x3dBD39B485546f40816849B10612C79275A9678b
- Frontend connects to Sepolia via MetaMask with no changes needed

### 7. Test Suite (8 tests, all passing)
Full pytest test suite using Ape's built-in test provider:
```bash
ape test -v
```
Tests cover: create zombie, duplicate prevention, level up, cooldown,
attack mechanics, transfer, name/DNA change permissions.

---

## How to Run

### Option A — Sepolia (live testnet, no local node needed)
1. Set MetaMask to **Sepolia** network
2. Serve frontend: `npx http-server -p 8080`
3. Open `http://localhost:8080/index.html`

### Option B — Local Hardhat
```bash
# Activate venv
source ../advBlockchain/bin/activate
export PATH="../advBlockchain/nodeenv/bin:$PATH"

# Terminal 1 — keep node running
ape networks run --network ethereum:local:hardhat

# Terminal 2 — deploy (updates index.html automatically)
ape run deploy --network ethereum:local:hardhat

# Terminal 3 — serve frontend
npx http-server -p 8080
```
MetaMask: RPC `http://127.0.0.1:8545`, Chain ID `31337`
Import key: `0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80`

> **Note:** Reset MetaMask account (Settings → Advanced → Clear activity) every
> time the Hardhat node restarts, otherwise stale nonce will cause transactions to fail.

---

## GitHub Repository

https://github.com/Ninjagod1251/chrrisCryptoZombie

Branches: `main` (starter) → `step1-truffle-ganache` → `step2-ape-migration`
→ `step3-nicer-website` → `step4-5-6-improvements`

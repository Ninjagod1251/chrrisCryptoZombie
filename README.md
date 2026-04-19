# CryptoZombies — Advanced Blockchain Demo

Blockchain-powered zombie army on Ethereum. Built on CryptoZombies with production-grade extensions.

## Features

### Core (ERC721 NFT)

- Create zombies, attack enemies, transfer ownership, level up
- Robohash monster avatars generated from zombie DNA

### Beyond the Tutorial

| Feature           | What it does                                                     |
| ----------------- | ---------------------------------------------------------------- |
| **Army mode**     | No limit on zombies per wallet                                   |
| **Batch create**  | Mint up to 20 zombies in one transaction                         |
| **Batch level up**| Level up N times in one transaction                              |
| **Gas savings**   | Shows USD saved vs individual transactions (ZK rollup concept)   |
| **Burn + Cemetery**| Burn (ERC721) zombies, cemetery reconstructed from on-chain Transfer events |
| **zombieWatch bot**| Silverback bot sends Telegram alert on every `NewZombie` event |
| **ZK Ownership Proof** | Prove you own a zombie without revealing which one — Groth16 circuit, in-browser |

## Quick Start

```bash
./start_demo.sh
npx http-server -p 8080
```

Open `http://localhost:8080` — MetaMask network: `http://127.0.0.1:8545` Chain ID: `31337`

## Demo Flow

### 1. Create a Zombie

- Click **Create Zombie**, enter a name, confirm in MetaMask
- Robohash avatar appears, generated from DNA
- Telegram notification fires via zombieWatch bot

### 2. Build an Army (Batch Create)

- Enter a number (e.g. `5`) next to **Create Zombie**
- One transaction mints 5 zombies
- Gas savings displayed in USD

### 3. Level Up (Batch)

- Each zombie card has a level up input
- Enter `3` and click **Level Up** — 3 levels in one transaction

### 4. Attack

- Add MetaMask Account #1 (private key below)
- Switch to Account #1, create a zombie
- Switch back to Account #0, click **Attack** on your zombie, enter enemy zombie ID

### 5. Burn + Cemetery

- Click **Burn** on any zombie — confirm, it fades out
- Click **Cemetery** to see all burned zombies from on-chain history

### 6. zombieWatch Bot

- Telegram bot `@zombieWatchbot` sends alerts on every zombie creation
- Powered by [Silverback](https://docs.apeworx.io/silverback/stable) (ApeWorX event bot framework)

## Batch Transactions & Gas Optimization

Every Ethereum transaction has two cost components:

- **Base fee** — 21,000 gas, flat, paid just to submit any transaction to the network
- **Execution fee** — gas for the actual computation inside the contract

If you call `createZombie` 5 times separately, you pay the 21,000 base fee **5 times** — even though the logic is identical each time.

[`batchCreateZombies`](contracts/zombiefactory.sol#L65) sends **one transaction**. The EVM runs the loop internally — 5 zombies created, 1 base fee paid:

```text
gas saved = 21,000 × (count − 1)
```

The UI fetches the live ETH/USD price and shows the dollar amount saved after every batch operation.

### The Rollup Connection

ZK rollups and Optimistic rollups use this same principle at a larger scale:

1. Collect N user transactions **off-chain**
2. Execute them off-chain
3. Post **one** transaction to mainnet with a proof

Your batch function does the same thing — move the repetition inside a single EVM call instead of repeating the round-trip. The savings formula is identical. The difference is rollups also compress calldata and use cryptographic proofs to verify correctness, allowing untrusted off-chain execution. Batch transactions keep everything on-chain but eliminate redundant base fees.

**Code references:**

- [`batchCreateZombies`](contracts/zombiefactory.sol#L65) — Solidity loop, mints up to 20 zombies in one tx
- [`batchLevelUp`](contracts/zombiehelper.sol#L28) — single `.add(_times)` instead of N transactions
- [`calcSavingsMsg`](index.html#L696) — fetches ETH price, computes USD saved

## Architecture

```text
docker-compose.yml
├── hardhat      — local Ethereum node (persistent)
├── robohash     — monster avatar generator
└── zombiewatch  — Silverback bot (Telegram alerts)
```

## Test Accounts

| # | Address                                      | Private Key                                                        |
| - | -------------------------------------------- | ------------------------------------------------------------------ |
| 0 | `0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266` | `0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80` |
| 1 | `0x70997970C51812dc3A010C7d01b50e0d17dc79C8` | `0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d` |

## Tests

```bash
ape test
```

40 tests covering creation, feeding, level up, combat, and burn.

## ZK Ownership Proof

This is the most advanced feature in the project. Here is what it does and how to explain it.

### The idea in one sentence

> "Prove you own a zombie that meets a level requirement — without revealing your address, your zombie ID, or any private information."

### The real-world analogy

Imagine a bouncer checking IDs. Normally they see your name, birthdate, address — everything on the card. A ZK proof is like a magic credential that only proves "this person is over 21" with zero other information revealed. Same concept here: the proof says "this person owns a level-2+ zombie" and nothing else leaks.

### How it works (step by step)

1. **You pick a secret number** (your private salt — like a password only you know)
2. **The circuit computes** `Poseidon(zombieId, secret)` — a cryptographic hash called your *commitment*
3. **You generate a proof** that says: *"I know a (zombieId, secret) pair such that their hash equals this commitment AND the zombie's level is ≥ threshold"*
4. **Anyone can verify** the proof using only the commitment and threshold — no zombie ID, no address, no secret ever leaves your browser

The commitment is what you'd register on-chain when you claim a zombie. Later you prove you know the preimage without revealing it.

### What the circuit enforces

```
Private inputs (never revealed):  zombieId, secret, zombieLevel
Public  inputs (visible to all):  commitment, levelThreshold

Constraints:
  Poseidon(zombieId, secret) == commitment   ← proves knowledge / ownership
  zombieLevel >= levelThreshold              ← proves the zombie qualifies
```

Both constraints must hold simultaneously. If either fails, the proof is rejected.

### Why this matters

Normal smart contracts expose everything. Every call, every address, every token ID is public on-chain. ZK proofs let you do gated actions — enter a tournament, claim a badge, prove eligibility — without doxxing your wallet or revealing your strategy.

### Toolchain

| Tool | Role |
|------|------|
| [Circom 2.x](https://docs.circom.io) | Circuit language — defines the constraints |
| [snarkjs](https://github.com/iden3/snarkjs) | Groth16 proof generation + verification |
| [circomlibjs](https://github.com/iden3/circomlibjs) | Poseidon hash in JavaScript |
| Groth16 | Proving scheme — constant-size proof (3 elliptic curve points) |
| [ZombieVerifier.sol](contracts/ZombieVerifier.sol) | Auto-generated Solidity verifier — deployable on-chain |

### Demo script (what to say to your class)

> "Every transaction on Ethereum is public. Anyone can see your wallet, your NFTs, your history. ZK proofs flip that.
>
> Watch — I'm going to prove I own a zombie that's level 2 or higher. I'm not going to tell you which zombie. I'm not going to tell you my address. I'm just going to click this button.
>
> *[click Generate ZK Proof]*
>
> The proof generates in your browser in about 2 seconds. It's verified locally using the same math a smart contract would use. The green badge means the proof is cryptographically valid — nobody can fake it.
>
> The public output is just a hash and a number. The hash is a commitment I made when I registered my zombie. The number is the threshold I proved against. My zombie ID and my secret never left my machine.
>
> This is the same cryptography that zkSync Era uses to batch thousands of transactions and post one proof to mainnet instead of thousands of individual calls. We used it at both layers — the rollup layer for gas savings, and the application layer for privacy."

### Files

- [`circuits/zombie_ownership.circom`](circuits/zombie_ownership.circom) — the constraint system
- [`contracts/ZombieVerifier.sol`](contracts/ZombieVerifier.sol) — on-chain verifier (auto-generated)
- [`scripts/zk/generate_proof.js`](scripts/zk/generate_proof.js) — Node.js CLI proof generator
- [`scripts/zk/setup.sh`](scripts/zk/setup.sh) — regenerate trusted setup from scratch

---

## Milestones

| # | Description | Status |
|---|---|---|
| M1 | Solidity 0.8 migration, security fixes, 40/40 tests, browser verified | ✅ |
| M2-ZK | ZK Ownership Proof — Groth16 circuit, browser proof generation, Solidity verifier | ✅ |
| M2-FV | Formal Verification — Vyper rewrite + Certora/halmos specs | 🔜 |

## Stack

- Solidity 0.8.31 — ERC721 contracts (migrated from 0.4.25)
- Hardhat — local node + deployment
- Ape Framework + pytest — Python test suite (40 tests)
- Silverback — on-chain event bot
- Docker Compose — persistent dev environment

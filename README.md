# CryptoZombies — Advanced Blockchain Demo

Blockchain-powered zombie army on Ethereum. Built on CryptoZombies with production-grade extensions.

## Features

### Core (ERC721 NFT)
- Create zombies, attack enemies, transfer ownership, level up
- Robohash monster avatars generated from zombie DNA

### Beyond the Tutorial
| Feature | What it does |
|---|---|
| **Army mode** | No limit on zombies per wallet |
| **Batch create** | Mint up to 20 zombies in one transaction |
| **Batch level up** | Level up N times in one transaction |
| **Gas savings** | Shows USD saved vs individual transactions (ZK rollup concept) |
| **Burn + Cemetery** | Burn (ERC721) zombies, cemetery reconstructed from on-chain Transfer events |
| **zombieWatch bot** | Silverback bot sends Telegram alert on every `NewZombie` event |

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

## Architecture

```
docker-compose.yml
├── hardhat      — local Ethereum node (persistent)
├── robohash     — monster avatar generator
└── zombiewatch  — Silverback bot (Telegram alerts)
```

## Test Accounts

| # | Address | Private Key |
|---|---|---|
| 0 | `0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266` | `0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80` |
| 1 | `0x70997970C51812dc3A010C7d01b50e0d17dc79C8` | `0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d` |

## Tests

```bash
ape test
```

40 tests covering creation, feeding, level up, combat, and burn.

## Stack

- Solidity 0.4.25 — ERC721 contracts
- Hardhat — local node + deployment
- Ape Framework + pytest — Python test suite
- Silverback — on-chain event bot
- Docker Compose — persistent dev environment

# Step 2 — Ape Framework Migration

## Why We Switched to Ape

The original starter code used Truffle + Ganache, which are JavaScript-based tools.
We migrated to **Ape Framework** for several reasons:

- **Python-native tooling** — Ape uses Python for scripts and configuration, making it
  easier to write complex deployment logic, automate tasks, and integrate with the
  broader Python ecosystem (testing, data, automation).
- **Cleaner deploy scripts** — Truffle migration files are JavaScript with a rigid
  structure. Ape deploy scripts are plain Python functions, easier to read and extend.
- **Automatic frontend updates** — We added logic directly in `deploy.py` to update
  `index.html` with the new contract address after every deploy. With Truffle this was
  a manual copy/paste step that caused errors when forgotten.
- **Modern local network** — Replaced Ganache (no longer actively maintained) with
  Hardhat as the local network provider via `ape-hardhat`, giving better error messages
  and faster block times.
- **Single environment** — One Python virtual environment (`advBlockchain`) manages
  everything: compiler, network, deploy scripts. No need to manage separate Node
  global installs for Truffle and Ganache.

## What This Demonstrates

The project deployment is upgraded from Truffle to **Ape Framework**,
using `ape-solidity` for compilation and `ape-hardhat` as the local network provider.
The deploy script also auto-updates `index.html` with the live contract address.

## What Changed from Step 1

| Area | Step 1 (Truffle) | Step 2 (Ape) |
|------|-----------------|--------------|
| Compile | `truffle compile` | `ape compile` |
| Deploy | `truffle migrate` | `ape run deploy` |
| Local network | Ganache (port 7545) | Hardhat (port 8545) |
| Address update | Manual | Automatic via `deploy.py` |
| Config | `truffle-config.js` | `ape-config.yaml` |

## Prerequisites

```bash
# Python venv with ape installed
source ../advBlockchain/bin/activate
export PATH="../advBlockchain/nodeenv/bin:$PATH"
```

## Steps to Reproduce

### 1. Compile

```bash
ape compile
```

### 2. Deploy (auto-updates index.html)

```bash
ape run deploy --network ethereum:local:hardhat
```

Output will show the deployed `ZombieOwnership` address.

### 3. Serve the Frontend

```bash
npx http-server -p 8080
```

Open `http://localhost:8080`

### 4. Connect MetaMask

- Add network: `http://127.0.0.1:8545`, Chain ID `31337`
- Import test account:
  `0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80`

## Demo Video

See `step2_video.mp4` in this folder.

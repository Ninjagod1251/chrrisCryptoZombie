# Step 1 — Starter Code: Truffle + Ganache

## What This Demonstrates

Minimum requirement: the CryptoZombies starter code compiled and deployed
to a local Ganache blockchain, with the frontend connecting via MetaMask.

## Prerequisites

- Ganache v2.5.4 (GUI or CLI)
- Truffle v5.4.25 (`npm install -g truffle@5.4.25`)
- Node v14–v18
- MetaMask browser extension

## Steps to Reproduce

### 1. Start Ganache

Open Ganache GUI and start a workspace (or CLI: `ganache --port 7545 --networkId 1337`).

Make sure it matches `truffle-config.js`:
- Host: `127.0.0.1`
- Port: `7545`
- Network ID: `1337`

### 2. Compile & Deploy

```bash
cd /path/to/chrisCryptoZombie
truffle compile
truffle migrate --reset
```

### 3. Get the Deployed Address

After migration, run the helper script to update `index.html` automatically:

```bash
node scripts/update_frontend.js
```

Or manually: open `build/contracts/ZombieOwnership.json`, find the address
under `networks > 1337 > address`, and paste it into `index.html`:

```js
var cryptoZombiesAddress = "0xYOUR_ADDRESS_HERE";
```

### 4. Serve the Frontend

```bash
npx http-server -p 8080
# Open http://localhost:8080
```

### 5. Connect MetaMask

- Add network: `http://127.0.0.1:7545`, Chain ID `1337`
- Import an account from Ganache (copy a private key from the Ganache UI)

### 6. Demo

- Click **Create Zombie** — MetaMask prompts for confirmation
- Approve the transaction
- Click **Show Zombies** — your zombie appears

## Demo Video

See `step1_video.mp4` in this folder.

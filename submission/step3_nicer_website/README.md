# Step 3 — Nicer Website + Tests

## What This Demonstrates

- Redesigned frontend with a dark zombie-themed UI
- Zombie cards showing DNA, Level, Wins, Losses, Ready time
- Styled buttons with hover effects and color coding
- Connected wallet address shown in header
- Friendly error messages instead of raw JSON errors
- Full test suite using Ape/pytest (8 tests, all passing)
- Backend inspection scripts (`check_zombies.py`, `test_create.py`)

## What Changed from Step 2

| Area | Step 2 | Step 3 |
|------|--------|--------|
| UI | Plain white page, unstyled | Dark theme, zombie cards, glowing buttons |
| Error messages | `[object Object]` | Human-readable with fix instructions |
| Tests | None | 8 pytest tests via `ape test` |
| Debug tools | None | `check_zombies.py`, `test_create.py` |
| Level Up | Broken (passed array instead of ID) | Fixed |

## How to Run Tests

```bash
ape test -v
```

No node needed — uses Ape's built-in test provider. All 8 tests pass in ~1.5 seconds.

## How to Run the Frontend

```bash
# Terminal 1 — keep running
ape networks run --network ethereum:local:hardhat

# Terminal 2 — deploy after every node restart
ape run deploy --network ethereum:local:hardhat

# Terminal 3 — serve frontend
npx http-server -p 8080
```

## Check On-Chain State

```bash
ape run check_zombies --network ethereum:local:hardhat
```

Prints every zombie's owner, name, DNA, level, wins, losses directly from the contract.

---

## What I Learned

### MetaMask Stale Nonce Problem

**The problem:** Every time the Hardhat node restarts, the blockchain resets to block 0.
All transaction history is wiped. But MetaMask caches the nonce (transaction count)
from previous sessions. When you try to send a new transaction, MetaMask submits it
with a stale nonce (e.g. `5`) but the fresh chain expects nonce `0`. The chain rejects
it with `Internal JSON-RPC error` — with no clear explanation of why.

**How I discovered it:** The contract was deployed and verified on-chain. Python scripts
(`ape run test_create`) could create zombies successfully. But MetaMask kept failing.
The only difference was that Python talks directly to the node (always gets the correct
nonce), while MetaMask uses a cached value.

**The fix:**
- MetaMask → Settings → Advanced → **Clear activity and nonce data** after every node restart
- Or use a fresh MetaMask account that has never sent a transaction on the local network
- Or use `ape run test_create` to verify the contract works independently of MetaMask

**Key takeaway:** Local blockchain development requires resetting MetaMask state every
time the node resets. This is a common gotcha that is not obvious from the error message.

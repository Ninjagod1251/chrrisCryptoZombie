#!/usr/bin/env bash
# CryptoZombies demo startup script
# Usage: ./start_demo.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/../advBlockchain"
NODE_BIN="$VENV/nodeenv/bin"

export PATH="$NODE_BIN:$PATH"

echo "==> Starting Hardhat node in background..."
"$SCRIPT_DIR/node_modules/.bin/hardhat" node &
HARDHAT_PID=$!
echo "    Hardhat PID: $HARDHAT_PID"
sleep 3

echo "==> Deploying contracts via ape..."
"$VENV/bin/ape" run deploy --network ethereum:local:hardhat

echo ""
echo "==> Done! Contract deployed and index.html updated."
echo ""
echo "Next steps:"
echo "  1. Serve the frontend:  cd $SCRIPT_DIR && npx http-server -p 8080"
echo "  2. Open: http://localhost:8080"
echo "  3. In MetaMask: add network localhost:8545, Chain ID 31337"
echo "  4. Import a Hardhat test account using its private key"
echo ""
echo "Hardhat test account #0 private key:"
echo "  0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
echo ""
echo "To stop Hardhat: kill $HARDHAT_PID"

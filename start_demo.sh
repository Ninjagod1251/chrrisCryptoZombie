#!/usr/bin/env bash
# CryptoZombies demo startup script
# Usage: ./start_demo.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NODE_BIN="$SCRIPT_DIR/../advBlockchain/nodeenv/bin"

export PATH="$NODE_BIN:$PATH"

echo "==> Starting Hardhat node + Robohash via Docker..."
docker compose up -d
echo "    Waiting for Hardhat to be ready..."
until curl -sf -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' > /dev/null 2>&1; do
  sleep 1
done
echo "    Hardhat is up."

echo "==> Deploying contracts..."
npx hardhat run "$SCRIPT_DIR/scripts/deploy.js" --network localhost

echo ""
echo "==> Done! Now serve the frontend:"
echo "    npx http-server -p 8080"
echo ""
echo "    Open: http://localhost:8080"
echo "    MetaMask network: http://127.0.0.1:8545  Chain ID: 31337"
echo ""
echo "Hardhat test account #0 private key:"
echo "  0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
echo ""
echo "To stop everything: docker compose down"

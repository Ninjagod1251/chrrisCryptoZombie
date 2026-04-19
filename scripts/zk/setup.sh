#!/usr/bin/env bash
# Regenerate the ZK trusted setup and verifier contract from scratch.
# Run once after cloning, or after modifying the circuit.
set -e

CIRCUITS=circuits
CONTRACTS=contracts

echo "=== ZK Trusted Setup for zombie_ownership.circom ==="

# 1. Compile circuit
echo "[1/6] Compiling circuit..."
circom "$CIRCUITS/zombie_ownership.circom" --r1cs --wasm --sym -o "$CIRCUITS/" -l node_modules

# 2. Powers of Tau (Groth16 phase 1)
echo "[2/6] Powers of Tau..."
snarkjs powersoftau new bn128 12 "$CIRCUITS/pot12_0000.ptau" -v
snarkjs powersoftau contribute "$CIRCUITS/pot12_0000.ptau" "$CIRCUITS/pot12_0001.ptau" \
  --name="setup" -e="$(openssl rand -hex 32)"
snarkjs powersoftau prepare phase2 "$CIRCUITS/pot12_0001.ptau" "$CIRCUITS/pot12_final.ptau" -v

# 3. Groth16 phase 2 (circuit-specific setup)
echo "[3/6] Groth16 setup..."
snarkjs groth16 setup "$CIRCUITS/zombie_ownership.r1cs" "$CIRCUITS/pot12_final.ptau" \
  "$CIRCUITS/zombie_ownership_0000.zkey"

# 4. Contribute to phase 2
echo "[4/6] Phase 2 contribution..."
snarkjs zkey contribute "$CIRCUITS/zombie_ownership_0000.zkey" "$CIRCUITS/zombie_ownership_final.zkey" \
  --name="final" -e="$(openssl rand -hex 32)"

# 5. Export verification key
echo "[5/6] Exporting verification key..."
snarkjs zkey export verificationkey "$CIRCUITS/zombie_ownership_final.zkey" \
  "$CIRCUITS/verification_key.json"

# 6. Generate Solidity verifier
echo "[6/6] Generating Solidity verifier..."
snarkjs zkey export solidityverifier "$CIRCUITS/zombie_ownership_final.zkey" \
  "$CONTRACTS/ZombieVerifier.sol"

echo ""
echo "Done! Test with:"
echo "  node scripts/zk/generate_proof.js"

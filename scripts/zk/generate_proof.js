#!/usr/bin/env node
/**
 * generate_proof.js
 *
 * Generates a Groth16 ZK proof that:
 *   - Poseidon(zombieId, secret) == commitment  (proves knowledge / ownership)
 *   - zombieLevel >= levelThreshold             (proves zombie meets the bar)
 *
 * Usage:
 *   node scripts/zk/generate_proof.js [zombieId] [secret] [zombieLevel] [levelThreshold]
 *
 * Outputs proof.json + public.json, then prints the Solidity calldata.
 */

const { buildPoseidon } = require("circomlibjs");
const snarkjs = require("snarkjs");
const fs = require("fs");
const path = require("path");

const CIRCUITS_DIR = path.join(__dirname, "../../circuits");

async function main() {
  const zombieId      = BigInt(process.argv[2] ?? "1");
  const secret        = BigInt(process.argv[3] ?? "12345678");
  const zombieLevel   = BigInt(process.argv[4] ?? "3");
  const levelThreshold = BigInt(process.argv[5] ?? "2");

  // Build Poseidon commitment: hash(zombieId, secret)
  const poseidon = await buildPoseidon();
  const hashBuf  = poseidon([zombieId, secret]);
  const commitment = poseidon.F.toObject(hashBuf);

  console.log("=== ZK Proof Generation ===");
  console.log(`zombieId:       ${zombieId}`);
  console.log(`secret:         ${secret}`);
  console.log(`zombieLevel:    ${zombieLevel}`);
  console.log(`levelThreshold: ${levelThreshold}`);
  console.log(`commitment:     ${commitment}`);
  console.log("");

  const input = {
    zombieId:       zombieId.toString(),
    secret:         secret.toString(),
    zombieLevel:    zombieLevel.toString(),
    commitment:     commitment.toString(),
    levelThreshold: levelThreshold.toString(),
  };

  const wasmPath = path.join(CIRCUITS_DIR, "zombie_ownership_js", "zombie_ownership.wasm");
  const zkeyPath = path.join(CIRCUITS_DIR, "zombie_ownership_final.zkey");

  const { proof, publicSignals } = await snarkjs.groth16.fullProve(input, wasmPath, zkeyPath);

  const proofPath  = path.join(CIRCUITS_DIR, "proof.json");
  const publicPath = path.join(CIRCUITS_DIR, "public.json");
  fs.writeFileSync(proofPath, JSON.stringify(proof, null, 2));
  fs.writeFileSync(publicPath, JSON.stringify(publicSignals, null, 2));
  console.log("Proof written to circuits/proof.json");
  console.log("Public signals:", publicSignals);
  console.log("");

  // Verify locally before printing calldata
  const vkeyPath = path.join(CIRCUITS_DIR, "verification_key.json");
  const vkey = JSON.parse(fs.readFileSync(vkeyPath));
  const valid = await snarkjs.groth16.verify(vkey, publicSignals, proof);
  console.log(`Local verification: ${valid ? "VALID ✓" : "INVALID ✗"}`);

  // Print Solidity calldata
  const calldata = await snarkjs.groth16.exportSolidityCallData(proof, publicSignals);
  console.log("\nSolidity calldata (paste into verifyProof()):");
  console.log(calldata);
}

main().catch(console.error);

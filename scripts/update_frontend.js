/**
 * After `truffle migrate`, run this script to copy the deployed
 * ZombieOwnership address into index.html automatically.
 *
 * Usage: node scripts/update_frontend.js
 */

const fs = require("fs");
const path = require("path");

const artifactPath = path.join(__dirname, "../build/contracts/ZombieOwnership.json");
const htmlPath = path.join(__dirname, "../index.html");

if (!fs.existsSync(artifactPath)) {
  console.error("ERROR: build/contracts/ZombieOwnership.json not found.");
  console.error("Run `truffle migrate` first.");
  process.exit(1);
}

const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));
const networks = artifact.networks;
const networkIds = Object.keys(networks);

if (networkIds.length === 0) {
  console.error("ERROR: No deployed networks found in artifact.");
  console.error("Run `truffle migrate` first.");
  process.exit(1);
}

// Use the most recently deployed network
const latestNetworkId = networkIds[networkIds.length - 1];
const address = networks[latestNetworkId].address;

console.log(`Found ZombieOwnership at: ${address} (network ${latestNetworkId})`);

let html = fs.readFileSync(htmlPath, "utf8");
const updated = html.replace(
  /(var cryptoZombiesAddress\s*=\s*")[^"]*(")/,
  `$1${address}$2`
);

fs.writeFileSync(htmlPath, updated);
console.log("Updated index.html with new contract address.");

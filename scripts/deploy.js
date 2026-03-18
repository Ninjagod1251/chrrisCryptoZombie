const { ethers } = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const ZombieOwnership = await ethers.getContractFactory("ZombieOwnership");
  const contract = await ZombieOwnership.deploy();
  await contract.waitForDeployment();

  const address = await contract.getAddress();
  console.log("Contract deployed at:", address);

  // Update index.html with new address
  const htmlPath = path.join(__dirname, "../index.html");
  let html = fs.readFileSync(htmlPath, "utf8");
  html = html.replace(
    /(var cryptoZombiesAddress\s*=\s*")[^"]*(")/,
    `$1${address}$2`
  );
  fs.writeFileSync(htmlPath, html);
  console.log("Updated index.html with new contract address.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

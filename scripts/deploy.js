const { ethers } = require("ethers");
const fs = require("fs");
const path = require("path");

async function main() {
  const provider = new ethers.JsonRpcProvider("http://127.0.0.1:8545");
  const deployer = new ethers.Wallet(
    "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",
    provider
  );
  console.log("Deploying with:", deployer.address);

  const artifact = JSON.parse(
    fs.readFileSync(
      path.join(__dirname, "../artifacts/contracts/zombieownership.sol/ZombieOwnership.json")
    )
  );

  const factory = new ethers.ContractFactory(artifact.abi, artifact.bytecode, deployer);
  const contract = await factory.deploy();
  await contract.waitForDeployment();

  const address = await contract.getAddress();
  console.log("Contract deployed at:", address);

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

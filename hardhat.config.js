require("@nomicfoundation/hardhat-ethers");

module.exports = {
  solidity: {
    compilers: [
      { version: "0.4.26" },
      { version: "0.8.31" },
    ],
  },
  networks: {
    hardhat: {
      blockGasLimit: 30000000,
    },
  },
};
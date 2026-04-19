module.exports = {
  solidity: {
    compilers: [
      { version: "0.8.31" },
    ],
  },
  networks: {
    hardhat: {
      blockGasLimit: 30000000,
      mining: {
        auto: true,
        interval: 5000,
      },
    },
  },
};
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./zombiefeeding.sol";

contract ZombieHelper is ZombieFeeding {

  uint levelUpFee = 0.001 ether;

  modifier aboveLevel(uint _level, uint _zombieId) {
    require(zombies[_zombieId].level >= _level, "zombie level too low");
    _;
  }

  function withdraw() external onlyOwner {
    uint256 amount = address(this).balance;
    (bool success, ) = payable(owner()).call{value: amount}("");
    require(success, "withdraw failed");
  }

  function setLevelUpFee(uint _fee) external onlyOwner { levelUpFee = _fee; }

  function levelUp(uint _zombieId) external payable onlyOwnerOf(_zombieId) {
    require(msg.value == levelUpFee, "incorrect ETH");
    zombies[_zombieId].level++;
  }

  function batchLevelUp(uint _zombieId, uint _times) external payable onlyOwnerOf(_zombieId) {
    require(_times > 0 && _times <= 20, "times must be 1-20");
    require(msg.value == levelUpFee * _times, "incorrect ETH");
    zombies[_zombieId].level += uint32(_times);
  }

  function changeName(uint _zombieId, string memory _newName) external aboveLevel(2, _zombieId) onlyOwnerOf(_zombieId) {
    zombies[_zombieId].name = _newName;
  }

  function changeDna(uint _zombieId, uint _newDna) external aboveLevel(20, _zombieId) onlyOwnerOf(_zombieId) {
    zombies[_zombieId].dna = _newDna;
  }

  function getZombiesByOwner(address _owner) external view returns (uint[] memory) {
    uint[] memory result = new uint[](ownerZombieCount[_owner]);
    uint counter = 0;
    for (uint i = 0; i < zombies.length; i++) {
      if (zombieToOwner[i] == _owner) { result[counter] = i; counter++; }
    }
    return result;
  }
}

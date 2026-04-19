// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ownable.sol";

contract ZombieFactory is Ownable {

  event NewZombie(uint zombieId, string name, uint dna);

  uint dnaDigits = 16;
  uint dnaModulus = 10 ** dnaDigits;
  uint cooldownTime = 0;

  struct Zombie {
    string name;
    uint dna;
    uint32 level;
    uint32 readyTime;
    uint16 winCount;
    uint16 lossCount;
  }

  Zombie[] public zombies;

  mapping (uint => address) public zombieToOwner;
  mapping (address => uint) ownerZombieCount;

  function _createZombie(string memory _name, uint _dna) internal {
    uint id = zombies.length;
    zombies.push(Zombie(_name, _dna, 1, uint32(block.timestamp + cooldownTime), 0, 0));
    zombieToOwner[id] = msg.sender;
    ownerZombieCount[msg.sender]++;
    emit NewZombie(id, _name, _dna);
  }

  function _generateRandomDna(string memory _str) private view returns (uint) {
    uint rand = uint(keccak256(abi.encodePacked(_str, block.timestamp, ownerZombieCount[msg.sender])));
    return rand % dnaModulus;
  }

  function _uint2str(uint _i) internal pure returns (string memory) {
    if (_i == 0) return "0";
    uint j = _i; uint len;
    while (j != 0) { len++; j /= 10; }
    bytes memory bstr = new bytes(len);
    uint k = len;
    while (_i != 0) { k--; bstr[k] = bytes1(uint8(48 + _i % 10)); _i /= 10; }
    return string(bstr);
  }

  function createRandomZombie(string memory _name) public {
    require(bytes(_name).length > 0, "name cannot be empty");
    uint randDna = _generateRandomDna(_name);
    randDna = randDna - randDna % 100;
    _createZombie(_name, randDna);
  }

  function batchCreateZombies(uint _count) public {
    require(_count > 0 && _count <= 20, "count must be 1-20");
    for (uint i = 0; i < _count; i++) {
      string memory zombieName = string(abi.encodePacked("Zombie #", _uint2str(ownerZombieCount[msg.sender] + 1)));
      uint randDna = _generateRandomDna(zombieName);
      randDna = randDna - randDna % 100;
      _createZombie(zombieName, randDna);
    }
  }
}

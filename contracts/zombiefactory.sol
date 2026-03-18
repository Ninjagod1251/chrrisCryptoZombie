pragma solidity ^0.4.25;

import "./ownable.sol";
import "./safemath.sol";

contract ZombieFactory is Ownable {

  using SafeMath for uint256;
  using SafeMath32 for uint32;
  using SafeMath16 for uint16;

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

  function _createZombie(string _name, uint _dna) internal {
    uint id = zombies.push(Zombie(_name, _dna, 1, uint32(now + cooldownTime), 0, 0)) - 1;
    zombieToOwner[id] = msg.sender;
    ownerZombieCount[msg.sender] = ownerZombieCount[msg.sender].add(1);
    emit NewZombie(id, _name, _dna);
  }

  function _generateRandomDna(string _str) private view returns (uint) {
    uint rand = uint(keccak256(abi.encodePacked(_str, now, ownerZombieCount[msg.sender])));
    return rand % dnaModulus;
  }

  function _uint2str(uint _i) internal pure returns (string) {
    if (_i == 0) return "0";
    uint j = _i;
    uint len;
    while (j != 0) { len++; j /= 10; }
    bytes memory bstr = new bytes(len);
    uint k = len;
    while (_i != 0) {
      k--;
      bstr[k] = byte(48 + uint8(_i % 10));
      _i /= 10;
    }
    return string(bstr);
  }

  function createRandomZombie(string _name) public {
    uint randDna = _generateRandomDna(_name);
    randDna = randDna - randDna % 100;
    _createZombie(_name, randDna);
  }

  function batchCreateZombies(uint _count) public {
    require(_count > 0 && _count <= 20);
    for (uint i = 0; i < _count; i++) {
      string memory zombieName = string(abi.encodePacked(
        "Zombie #", _uint2str(ownerZombieCount[msg.sender] + 1)
      ));
      uint randDna = _generateRandomDna(zombieName);
      randDna = randDna - randDna % 100;
      _createZombie(zombieName, randDna);
    }
  }

}

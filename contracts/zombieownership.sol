// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./zombieattack.sol";
import "./erc721.sol";

contract ZombieOwnership is ZombieAttack, ERC721 {

  mapping (uint => address) zombieApprovals;

  function balanceOf(address _owner) external view override returns (uint256) {
    return ownerZombieCount[_owner];
  }

  function ownerOf(uint256 _tokenId) external view override returns (address) {
    return zombieToOwner[_tokenId];
  }

  function _transfer(address _from, address _to, uint256 _tokenId) private {
    require(_to != address(0), "transfer to zero address");
    ownerZombieCount[_to]++;
    ownerZombieCount[_from]--;
    zombieToOwner[_tokenId] = _to;
    emit Transfer(_from, _to, _tokenId);
  }

  function transferFrom(address _from, address _to, uint256 _tokenId) external payable override {
    require(
      zombieToOwner[_tokenId] == msg.sender || zombieApprovals[_tokenId] == msg.sender,
      "not owner nor approved"
    );
    require(zombieToOwner[_tokenId] == _from, "from is not current owner");
    _transfer(_from, _to, _tokenId);
  }

  function approve(address _approved, uint256 _tokenId) external payable override onlyOwnerOf(_tokenId) {
    zombieApprovals[_tokenId] = _approved;
    emit Approval(msg.sender, _approved, _tokenId);
  }

  function burnZombie(uint256 _zombieId) external onlyOwnerOf(_zombieId) {
    address zombieOwner = zombieToOwner[_zombieId];
    ownerZombieCount[zombieOwner]--;
    zombieToOwner[_zombieId] = address(0);
    delete zombieApprovals[_zombieId];
    emit Transfer(zombieOwner, address(0), _zombieId);
  }
}

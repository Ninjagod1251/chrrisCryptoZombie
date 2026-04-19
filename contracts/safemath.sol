// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library SafeMath {
  function add(uint256 a, uint256 b) internal pure returns (uint256) { return a + b; }
  function sub(uint256 a, uint256 b) internal pure returns (uint256) { return a - b; }
  function mul(uint256 a, uint256 b) internal pure returns (uint256) { return a * b; }
  function div(uint256 a, uint256 b) internal pure returns (uint256) { return a / b; }
}

library SafeMath32 {
  function add(uint32 a, uint32 b) internal pure returns (uint32) { return a + b; }
  function sub(uint32 a, uint32 b) internal pure returns (uint32) { return a - b; }
  function mul(uint32 a, uint32 b) internal pure returns (uint32) { return a * b; }
  function div(uint32 a, uint32 b) internal pure returns (uint32) { return a / b; }
}

library SafeMath16 {
  function add(uint16 a, uint16 b) internal pure returns (uint16) { return a + b; }
  function sub(uint16 a, uint16 b) internal pure returns (uint16) { return a - b; }
  function mul(uint16 a, uint16 b) internal pure returns (uint16) { return a * b; }
  function div(uint16 a, uint16 b) internal pure returns (uint16) { return a / b; }
}

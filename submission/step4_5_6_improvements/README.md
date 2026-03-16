# Steps 4, 5 & 6 — Multiple Zombies, Transfer, Zombie Avatar

## What This Demonstrates

### Step 4 — Multiple Zombies
- `getZombiesByOwner` already returns all zombie IDs for an account
- Frontend now loops through all IDs and renders a card for each
- Zombie count displayed in header ("3 zombies in your army")
- Demo: import 3 Hardhat accounts into MetaMask, each creates a zombie, switch between them to show separate armies

### Step 5 — Transfer Zombie
- Each zombie card has a **Transfer** button
- Clicking it reveals an address input field
- Calls `transferFrom(from, to, tokenId)` on the ERC-721 contract
- After transfer, the card disappears from sender's view and appears for recipient
- Input validated: checks valid Ethereum address, rejects self-transfer

### Step 6 — Zombie Avatar Generated from DNA
- 16-digit DNA is broken into segments controlling visual traits:
  - Digits 1-2: skin hue (greenish range)
  - Digits 3-4: eye color
  - Digits 5-6: shirt color
  - Digits 7-8: hair color
  - Digits 9-10: background color
  - Digits 11-12: skin lightness
  - Digits 13-14: eye shape (normal / wide / small)
  - Digits 15-16: mouth type (grin / flat / frown)
- Level bonuses: stitches appear at Level 3+, crown appears at Level 5+
- Pure SVG, no external images needed

## Demo Script

1. Show Zombies — cards appear with unique avatars
2. Show two different accounts with different zombies (different DNA = different face)
3. Click Transfer → enter Account #1 address → confirm → zombie moves
4. Switch to Account #1 in MetaMask → Show Zombies → transferred zombie appears
5. Level Up → avatar gains stitches at level 3, crown at level 5

## What I Learned

### ERC-721 Transfer
`transferFrom(from, to, tokenId)` requires the caller to be the owner OR approved.
Since the owner is calling it directly, no approval step is needed.
The token ID is the zombie's index in the `zombies` array, not arbitrary.

### SVG Generation from On-Chain Data
DNA is deterministic — same DNA always produces the same avatar.
This is how CryptoKitties and other NFT projects generate unique art on-chain.
The SVG is generated client-side from the DNA stored in the contract.

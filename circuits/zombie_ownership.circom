pragma circom 2.0.0;

include "circomlib/circuits/poseidon.circom";
include "circomlib/circuits/comparators.circom";

/*
 * ZombieOwnership circuit
 *
 * Proves: "I know a (zombieId, secret) such that:
 *   1. Poseidon(zombieId, secret) == commitment  (I know the preimage)
 *   2. zombieLevel >= levelThreshold             (zombie meets the bar)
 *
 * Private inputs: zombieId, secret, zombieLevel
 * Public  inputs: commitment, levelThreshold
 *
 * The commitment is stored off-chain (or on-chain in a registry) when the zombie
 * is created. Proving knowledge of the preimage == proving ownership without
 * revealing the zombie or owner address.
 */
template ZombieOwnership() {
    // private
    signal input zombieId;
    signal input secret;
    signal input zombieLevel;

    // public
    signal input commitment;
    signal input levelThreshold;

    // 1. Hash check: Poseidon(zombieId, secret) must equal commitment
    component hasher = Poseidon(2);
    hasher.inputs[0] <== zombieId;
    hasher.inputs[1] <== secret;
    hasher.out === commitment;

    // 2. Level check: zombieLevel >= levelThreshold
    //    GreaterEqThan(n) requires n bits — 32 bits covers levels up to 4B
    component gte = GreaterEqThan(32);
    gte.in[0] <== zombieLevel;
    gte.in[1] <== levelThreshold;
    gte.out === 1;
}

component main { public [commitment, levelThreshold] } = ZombieOwnership();

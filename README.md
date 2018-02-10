# Shitcoin

A project for playing around with blockchain technology.

We have no delusions about this being an absolute shitcoin.  The purpose isn't in any way to launch this and gain users, simply to experiment with block chain technology and learn how it works in order to later make something that might actually be useful.  You have been warned.

## Use case

The target use case is to create a public ledger for scientific article/experiment propositions and crowd funding.  By forcing experimental parameters, null hypotheses et c to be published publically in a tamper proof way ahead of funding it is our hope some issues in the scientific community, such as publication bias, will be mitigated.

## Web of trust

Reliability of scientists must be logged within the block chain.  This is required both to avoid outright scams where someone proposes a research project, creates sock puppet users in order to do false peer review and pockets the crowd funded money without actually doing any proper research.

## Message types

There will be several types of predefined message types, tailored to the needs of scientific publications:

* User registration - Formal association between a public key and a real-world person. Used to keep track of publications and reliability score etc.  Not necessary in order to use the coin part of the protocol.
* Proposal - Submitted by a scientist looking for funding and peer reviewers. Will contain unique ID of a document describing the research project, and a list of URLs where a copy of the document may be obtained as well as a hash of the document for verification purposes so that it can't be altered after the fact. It will also a list of the public keys of all the scientists working on the project, information about how payment will be distributed and when.  There may be different types of proposal messages depending on field and type of study.
* Peer review - A short summary of peer review, including score in some areas.  Optional(?) URL to full peer review text.  Signed using the private key of the registered user making the review.
* ...

## Blocks

This is obviously crap, have to look into how other crypto currencies work and see what is necessary for this blockchain. I have no illusions that I will think of all corner cases and pitfalls on my own.

Pseudo code will be C/C++ like and data types larger than one byte will be in network order, i.e. big endian.

### Generic block structure

```
struct GenericBlock {
    // Version of the blockchain protocol to use to interpret the rest of
    //  the block.
    uint16 blockVersion;

    // A hash of the entire block after this value.  Hash function to be
    //  decided.  Probably using SHA-256 during test/dev.
    uint256 blockId;
    // The hash of the previous block.
    uint256 previousBlockId;
    // A randomly chosen number altered to make the hash less than demanded
    //  by the current difficulty.
    uint256 nonce;

    // Pre-defined values showing how to interpret the rest of the block
    uint16 blockType;
    // The number of bytes used by the whole block, including the blockId,
    //  blockVersion, blockType, payload and blockHash.
    uint32 blockLength;

    // An array of bytes, exactly as many as are required for blockLength
    //  to be correct.
    uint8 payload[];
};
```

### Genesis block

The very first block in a block chain.  Assuming SHA-256 for now.
Probably wants some more defining values so different block chains
can run simultaneously and whatnot.

```
struct GenesisBlock {
    uint16 blockVersion = 1;

    uint256 blockId = 0xa86a6be3830cd99a5100014bc73366dbca3cc960ddbb4db8e25c5b7f99dd4537;
    uint256 previousBlockId = 0x0;
    uint256 nonce = 0x0;

    uint16 blockType = BLOCK_TYPE_GENESIS;
    uint32 blockSize = 84;

    // Definitions to be used in the subsequent block chain validation.
    uint256 chainIdentifier = 0x926a86a8a7dc535a2af990e79f47621092114da64b6838bae8776003d0af3bb3;
    uint32 maxBlockSize = 0x200000;
    uint32 hashDifficulty = 1;
    uint32 secondsBetweenBlocks = 600;
    uint32 blocksBetweenRecalculation = 1008;
};
```

Or, in hexadecimal format:

```
0001fc65 bcbfa4bb 3965aa2a 7820304f
b9ca153a 330f2401 7f14d018 cd61a15b
1e9e0000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
00000000 00000091 926a86a8 a7dc535a
2af990e7 9f476210 92114da6 4b6838ba
e8776003 d0af3bb3 00200000 00000001
00000258 000003f0
```

# Is your NEAR account quantum-safe?

**Live:** https://automationbot24x7.github.io/near-quantum-check/

Type any NEAR account (mainnet or testnet). The page reads the account's access keys from public RPC and tells you:

- **Quantum-safe**: every key is post-quantum (ML-DSA-65, NEP-645).
- **Half-way there**: a quantum-safe key was added, but a classic full-access key is still on the account and can still move everything.
- **Not quantum-safe**: only classic keys (Ed25519 / secp256k1), whose public keys are visible on-chain.

It also shows the three `near-cli-rs` commands to upgrade (add an ML-DSA key, sign with it, delete the old key).

No wallet connection, no tracking, nothing stored. One static `index.html`; RPC by FastNEAR (mainnet) and NEAR (testnet).

## Validator snapshot (18 Nov 2026)

`tools/scan-validators.py` reads the owner account of every active mainnet validator (`get_owner_id` on each pool) and lists its key types. Result in `data/validator-owners.json`:

| | |
|---|---|
| Active validator pools | 354 |
| Owner accounts with readable keys | 323 |
| Owners with at least one ML-DSA key | 3 |
| Owners with only ML-DSA keys | 0 |

## Demo account

`vault.bazaar-sovereign-2026.testnet` was upgraded on 18 Nov 2026 with near-cli-rs 0.31.1: ML-DSA key added (tx `56qt76ZggcjfYW3tjAkyZwM2XjAYTHCxdCTgAG4wqbH6`), a 0.01 NEAR transfer signed with it (tx `FoqStYXz8iKM4jH11LHjrPpibLoE42Gz8TWrLg6AfjoT`), then the Ed25519 key deleted using the ML-DSA key (tx `1sWb2bynxWf3kd55MsKrPUSGjSUb2MmM7PvSGtVxTWn`). See it on [NEAR Rocks](https://testnet.near.rocks/account/vault.bazaar-sovereign-2026.testnet).

## Sources

- [Quantum-Safe NEAR: The Roadmap to Post-Quantum Security](https://www.near.org/blog/near-quantum-safe-roadmap)
- [NEP-645: ML-DSA-65 post-quantum transaction signatures](https://github.com/near/NEPs/pull/645)
- [near-cli-rs docs](https://docs.near.org/tools/cli)

Unofficial community tool. Icons: [Phosphor](https://phosphoricons.com) (MIT). Code: MIT.

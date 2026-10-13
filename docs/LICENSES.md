# Source licensing review — 2026-10-13

This checkpoint records the published licenses inspected for the linked sources. It does not establish permissions for every paper cited upstream.

| Source snapshot | Code | Other material | Review evidence |
| --- | --- | --- | --- |
| OpenAI math `1581d4cbdd69a0faf34b2089614fe2a814316a6a` | Apache-2.0 | Repository license; external papers retain their own terms | [LICENSE](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/LICENSE) |
| Anthropic FLT `6e837e75355538c7f80bab5b956861e86c4eacc2` | Apache-2.0 | Original publications retain separate terms; third-party attribution recorded upstream | [LICENSE](https://github.com/anthropics/fermats-last-theorem/blob/6e837e75355538c7f80bab5b956861e86c4eacc2/LICENSE), [NOTICE](https://github.com/anthropics/fermats-last-theorem/blob/6e837e75355538c7f80bab5b956861e86c4eacc2/NOTICE), [ATTRIBUTION](https://github.com/anthropics/fermats-last-theorem/blob/6e837e75355538c7f80bab5b956861e86c4eacc2/ATTRIBUTION.md) |
| Anthropic formal-math `e1a4e6508154ea59f030480661590a9fe3018011` | Apache-2.0 | Individual projects include third-party notices; linked arXiv papers retain their publication terms | [Root license](https://github.com/anthropics/formal-math/blob/e1a4e6508154ea59f030480661590a9fe3018011/LICENSE), [README](https://github.com/anthropics/formal-math/blob/e1a4e6508154ea59f030480661590a9fe3018011/README.md) |
| AlphaProof Nexus `0647711a71183c1ea492ad60860776617ce1ea88` | Apache-2.0 | CC BY 4.0, subject to additional third-party source terms; OEIS is identified as CC BY-SA 4.0 | [License and disclaimer](https://github.com/google-deepmind/alphaproof-nexus-results/blob/0647711a71183c1ea492ad60860776617ce1ea88/README.md#license-and-disclaimer) |

## Implemented approach

The adapters store titles, identifiers, commit pins, locations, toolchain/dependency metadata, attribution, and license links. No upstream proof implementations, PDFs, prose proofs, sequence data, or conjecture descriptions are redistributed. File-derived titles are identified as such. Publication links do not imply that the publication's text is covered by its proof repository's license.

Every catalogue record includes source credit and a license link. The deployed Sources & licenses page gives source attribution, third-party notice links, and a modification/curation description. An Apache-2.0 license text is included for reference; it does not apply a new license to the project's original code or override upstream licenses.

## Conditions if copying is introduced later

- [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0): supply the license, retain relevant notices and attribution, identify modified files, and preserve applicable NOTICE contents when distributing derivative material.
- [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): provide appropriate credit, a license link, and change notices; do not imply endorsement.
- [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/): attribution and share-alike conditions can apply to adapted material. Check scope before importing OEIS material; it is not automatically Apache-2.0 because a Lean implementation links to it.
- Check each journal/arXiv publication's own terms before republishing its prose, figures, or PDF.

No licensing blocker was identified for the implemented attribution-and-link catalogue. This is a scoped review of the inspected notices, not an assurance about all possible future uses.

## Additional sources

- Harmonic IMO2025 `72b62405a176a7eaeadb335a7fa6ee80b6667161`: no repository-wide license located in the complete pinned tree or README. The catalogue links the artifacts without copying their code or problem prose.
- Math Inc. strongpnt `2f5835c322314f55f1026ec2f139d704b7c45c69`: no repository-wide license located. Its README documents reuse from PrimeNumberTheoremAnd; this does not establish a blanket license for generated project files. Linked only.
- DeepSeek-Prover-V2 `e598a57ea3284997d4a2a168a069fdd5064afbc8`: LICENSE-MODEL governs model usage and explicitly excludes Data. The archive contains only Lean files, with no separate license or toolchain manifest. The README has a code-license badge and model-license section but does not explicitly settle proof-archive licensing. Model weights and Lean code are not redistributed; only archive-member metadata and hashes are stored.
- Formal Conjectures `72dad3524e0174dea703f267664d3bc9298803a0`: Apache-2.0 repository license. Indexed at collection level as statements; not represented as proof coverage.

Unknown redistribution rights are recorded as unknown. The present link-and-metadata approach does not grant permission for future copying.

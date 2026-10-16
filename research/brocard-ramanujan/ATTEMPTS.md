# Research checkpoint — attempt1

Source controller: `c4f13e1a9e3111cfc1e228156d2fa43d395253bc`.
[Remote CI run38928647066](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38928647066), job117066628307. Artifact12058440606, digest `sha256:2ddd19fa655d23d23d9ffba6e6cf3b56934480a914e54472815e0ee9d2986069`.

The first search and compiler attempt succeeded. No failed compiler diagnostic or retry occurred. All seven initial focused tests passed. The original search output is preserved as [report](results/attempt-1-report.json) and [certificate](results/attempt-1-certificate.json); the metadata records exact source identity, assumptions, dependencies and trust scope. The certificate is retained byte-for-byte as emitted, with SHA256 `e51a62041eaf7c9826060c0c789abaf9e007cd5cfe1840447201ce3928b0df1b`. Use a parser with arbitrary-precision integers; JavaScript Number cannot exactly represent these bounds and primes. Do not round-trip the evidence through floating-point numbers.

Observed results:
-  Exact full-factorial baseline n=0 through2000 returned only (4,5),(5,11),(7,71).
- 1060 small-prime tail identities agreed with direct integer factorials.
- The inclusive interval **2305843009213683951 through2305843009213693950** contains exactly10000 values. Every value received a checked prime/nonresidue obstruction. No unresolved survivor and no new solution was identified.
- All32 prime certificates passed the stdlib checker. The first14 test primes accounted for all exclusions; later primes were available but unnecessary for these first-rejection witnesses.
- The search plus certificate checking took approximately0.62seconds in this particular runner, excluding environment preparation, focused tests and Lean compilation. This is a measurement of one small targeted experiment, not a throughput guarantee.
- `BrocardResearch.nonsquare_of_modular_obstruction` compiled, and `#print axioms` reported `[propext]`. No independent fresh replay or search-to-Lean instantiation was performed.

This excludes the named interval computationally under the documented checker/Wilson/Euler trust dependencies. It proves nothing about other large n, does not establish the global conjecture, and is not claimed to extend any published contiguous search bound or to be novel mathematics. The exact certificate can be replayed without SymPy by the separate checker; generating new certificates needs the pinned research environment.

## Proof-side checkpoint

The coprime consecutive-factor reformulation in README is a useful standard reduction but leaves an unbounded family of factor allocations to exclude. No uniform argument has been found.

A finite fixed set of modular tests alone cannot settle the problem: for each positive modulus q and n≥q, q divides n!, so n!+1≡1(mod q), which is a square residue. Therefore once n exceeds all fixed moduli, all such tests pass. Our prime choices grow with the selected search interval. This observation explains why a larger finite search cannot become a universal proof by extrapolation.

Next mathematical task: seek a genuinely uniform restriction on the coprime consecutive factors of n!/4, or a justified restricted family. Any candidate lemma must preserve the original problem's scope; label restricted results as restricted, retain failed attempts, and independently review source fidelity before claiming a proof. This bounded attempt stops at its predeclared checkpoint.

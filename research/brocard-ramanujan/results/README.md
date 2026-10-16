# Replaying the preserved attempt

The certificate contains integers above2^53. Preserve the exact bytes; load it with an arbitrary-precision integer JSON parser such as Python's standard json module. Do not deserialize and rewrite it through JavaScript Number.

On a clean remote runner with this checkout, the evidence-replay test requires only Python's standard library:

```sh
python3 -m unittest discover -s research/brocard-ramanujan -p 'test_*.py' -v
```

This test checks the original certificate SHA256, every recursive primality certificate, exact interval coverage, every assigned modular exclusion, and the full recorded result. It does not run the new-prime generator, need SymPy, or prove the computation in Lean.

attempt-1-provenance.json identifies the original source commit, CI run, artifact digest and separate generic Lean lemma. ATTEMPTS.md records scope and limitations. Repeated CI runs may have different elapsed_seconds; that timing field is observational, not part of the arithmetic certificate. No test here certifies the global conjecture or establishes novelty.

These instructions are for remote reproduction; no commands were run locally.

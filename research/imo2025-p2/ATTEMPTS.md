# Attempt checkpoint

Attempt1: source `abe224d7fd1fd36979d6211275a4ee26fd69cfd1`, [run40471794537](https://github.com/theorem-atlas/theorem-atlas/actions/runs/40471794537), job122080403134, artifact12719121086, digest `sha256:36b33675ba1ea99c6a7d96970446d279f9d9c814a72775949a4e8d8486ff9093`.

The coordinate file stopped at an uncached Mathlib.Data.Real.Basic import before its mathematics was checked. FullTargetAttempt.lean elaborated the exact upstream interface but ordinary proof search left the original affine-independence/tangency goal unsolved. No full proof or accepted coordinate result is claimed from this run. Full stdout/stderr and source hashes are retained in observations/attempt-1.json.

Next iteration fixes the explicit cached import, keeps all resolved dependency commits pinned, and adds concrete algebraic memberships plus a generic Mathlib tangency bridge. The full-target signature is unchanged; the proof attempt selects the proposed contact point T=(N-A)+M. Selecting this point does not prove it lies on the actual circumcircle or the target line. Those are still goals, not assumptions.

No local execution or catalogue status change. Four candidate CI iterations plus one unchanged-source checkpoint reproduction is the bounded budget. Independent fidelity/trust review remains unassigned.

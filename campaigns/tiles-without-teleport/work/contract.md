# Prepared contract

Source: `{"num_vars":n,"clauses":[[signed_literal,...],...]}` with at most three literals per clause. Output a satisfying Boolean `{"assignment":[...]}` or `{"status":"NO-SOLUTION"}`.

Target: `{"features":m,"tiles":[[feature,...],...]}` with at least one tile and features indexed `0..m-1`. Each tile lists a finite set, and repeated feature entries are invalid. A positive output `{"path":[tile_index,...]}` starts at any tile. Each subsequent tile differs from the current tile and shares at least one currently present feature; all features common to the two tiles are removed from both. Success means no tile has a feature left. Teleports and zero-effect moves are invalid. `NO-SOLUTION` is valid exactly when no such path exists.

`algorithm.py` reads source JSON from stdin and emits legal target JSON. `algorithm.py --extract` reads `{"source":source,"target_solution":output}` and emits a valid source output. Both commands are deterministic, polynomial time, independent subprocesses. Errors exit nonzero; diagnostics go to stderr. Recovery must handle every valid target output.

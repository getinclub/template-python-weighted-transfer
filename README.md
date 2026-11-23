# The Transfer Estimate That Chose the Wrong Route

P2 · A synthetic transfer estimate reports **90 cost units** for ingest → archive,
above the acceptance ceiling of **40**. You have a directed network of links with
supplied nonnegative integer costs. This is a path-estimation exercise, not a
live network measurement, currency quote or throughput benchmark.

## Task · 25 minutes
Repair `cheapest_cost` in `transfer.py`. Run `python monitor.py` and
`python -m unittest -v`. Open a PR against `main` with your invariant, complexity
argument and regression evidence. Do not weaken tests or alter the contract.

## Contract
- `nodes`: exact list of unique nonempty exact strings. Empty list is permitted
  as input shape but any source/target is then invalid.
- `edges`: exact list of exact tuples `(from_node, to_node, cost)`, with endpoints
  in nodes and cost an exact nonnegative int (not bool). Directed links only.
- `source` and `target`: exact strings present in nodes.
- Return the exact minimum sum of link costs, or `None` if unreachable. Source
  equal to target returns zero, **after validating every input edge**.
- Parallel links, self-loops, cycles and zero-cost links are legal. Arbitrarily
  large Python integers are legal. No floating-point rounding or infinity sentinel
  may alter the returned integer. Edge order must not affect the answer.
- Invalid inputs raise `ValueError`, including invalid disconnected edges. Do not
  mutate caller input, access network services, or retain state between calls.
- Target O(V + E log(E+2)) time and O(V+E) storage with an adjacency-based search.
  The package has deterministic functional tests and a large sparse smoke case,
  not a formal complexity proof. Explain why stale work and cycles stay bounded.
- Python 3.10+, standard library only. Heap utilities are allowed. Return cost
  only; no path reconstruction or tie-breaking between equal-cost paths needed.

Files: `transfer.py` faulty starter; `monitor.py` authored reproduction;
`test_transfer.py` public contract/oracle tests; GitHub workflow runs both checks.
No solution belongs in this learner template. Maintainer reference is separate.

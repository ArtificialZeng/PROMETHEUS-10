# Exact algebra supporting the missing-arc proof

Run from the project root, or the root of the eventual source handoff:

```sh
python3 manuscript/repro/verify_symbolic.py --output-dir build/replay-local
python3 manuscript/repro/verify_rational.py --output-dir build/replay-local
```

Both commands run in the foreground and read no cached answers or scientific
input files. They generate symbolic-results.json and rational-results.json.
The expected/ directory contains outputs from the writer's actual replay of
these packaged scripts. Each output records the hash of the executing script;
that metadata is not a scientific premise. A failing identity raises an error.

The symbolic script requires SymPy at the version in requirements.txt. The
rational script uses only the Python standard library, including
fractions.Fraction. No numerical tolerance or floating-point fit is used.
The actual environment and commands are recorded in environment.json.
No experimental data, meshes, random seeds, or external tables are needed.

The symbolic route reconstructs the companion determinant and arc, the biased
square spectrum and all linear slack terms, then computes the quadratic form
from reciprocal-edge and oriented-triangle invariants. It checks the optimizer,
completed square, triangle coefficient, and strict Jensen Hessian directly.

The rational route solves a bordered eigenvector-derivative system over
Gaussian rational numbers. Seven basis directions and all 21 pair sums check
every coefficient of a homogeneous quadratic in seven independent variables.
Five additional first-order directions check all four escape deficits and the
mean-affinity slack. This route neither imports SymPy nor reads the first
route's output.

These programs package the accepted referee's two implementations. The writer
changed only documentation, the output-directory interface, filenames and
workflow metadata; the mathematical calculation statements were preserved.
Original paths and hashes are given in ../source-map.md. The replays are not
new independent refereeing. They check finite algebra, while the manuscript
provides the uniform remainder estimates, coercive bootstrap, source-theorem
equality argument and compactness proof. They do not compute eta, determine
the point at t = 1/2, prove sharpness of 1/5, or certify an error enclosure at
any chosen nonzero displacement.

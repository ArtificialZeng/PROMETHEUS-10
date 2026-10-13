# Exact certificate regeneration

The central symbolic construction is `research/hadamard_involution.py`, included in this local source bundle with its exact output `evidence/hadamard-involution-exact.json`. It uses Python 3.12.14 and SymPy 1.14.0. From the project root, run:

```sh
python3 research/hadamard_involution.py > /tmp/hadamard-involution-regenerated.json
```

For a portable environment, use any Python 3.12 installation with `sympy==1.14.0` and run `python3 research/hadamard_involution.py`. The script emits JSON and asserts exact matrix identities using rational and symbolic arithmetic. Compare `rank_two_component.four_by_four_tangent_minor` with `211601016/7843564625`, `rank_two_component.tangent_rank_of_probability_image` with `4`, and all entries of `exact_checks` with `true`. The rank-two projector is constructed from the displayed vectors `v=(1,2,3,5)^T` and `w=(2,-1,0,0)^T`; the four determinant rows are `B11,B12,B13,B21`, and columns are rotations `K12,K13,K14,K23`.

The proof of the full interval is the algebra in the article. This finite exact calculation certifies the rational example and local Jacobian, not arbitrary `U(4)` star-shapedness. The standalone package contains authored code and instructions; it does not need or redistribute downloaded third-party PDFs.

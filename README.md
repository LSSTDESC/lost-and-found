# lost-and-found

Generalized metrics framework for catalogs and images

This repo corresponds to a joint effort by the BL and PZ WGs to establish a generic framework for metrics that can be called by both [BlendingToolKit](https://github.com/LSSTDESC/BlendingToolKit) and [RAIL](https://github.com/LSSTDESC/RAIL) (and perhaps be useful to other DESC entities, like SRV).
Both of the existing packages that inspired this work have some metrics of their own but would benefit from improved organization thereof and sharing of code, hence the need for a new package that can be a dependency of both.
Additional goals of this code are to support:

- metrics that do not assume a one-to-one correspondence between truth and recovered/estimated properties.
- metrics of intermediate derived data products (e.g. fluxes or ellipticities).
- empirical metrics of recovered/estimated properties in the absence of "truth" (that can be evaluated on real data and still convey something about performance).

## Installation

1. Download poetry from <https://python-poetry.org/docs/#installation>

2. Run `poetry install` in the root directory of this repository

3. Run `poetry shell` to enter the virtual environment

4. Update packages with `poetry update`

5. Add new dependencies with `poetry add <package_name>`

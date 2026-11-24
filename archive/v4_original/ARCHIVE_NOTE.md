# Synthium V4 (April 2026), archived as found

These files are the original Synthium V4 package, copied byte for byte from
`Synthium /V4/synthium_v4_final/` inside `Synthium.zip` on Sina's Google Drive.
The only change is the folder name (`synthium` became `synthium_v4`) so it cannot be
confused with the current package. Nothing here is imported by the current code.

V4 was retired in V6.1 together with the keyword word counts that fed it. The ideas
are now back as `synthium/geometry/`, fed with the case quality scores instead.

## What the V4 code actually did (read before reusing it)

- `manifold_geometry.py`: the metric is a single constant matrix, so the Christoffel
  symbols, the Riemann tensor and the scalar curvature are hard-coded to zero and every
  geodesic is a straight line. No curvature was ever computed.
- `learn_metric_from_data(method='covariance')`, the default, uses the covariance itself
  as the metric. That stretches the directions where cases already differ most. The usual
  statistical distance (Mahalanobis) uses the inverse covariance, which V4 offered as
  the second option.
- `infinite_calculus.py`: the derivative chain nests central differences with a step of
  1e-6. From about the third order on, the result is floating point noise, so the
  "chaos" test on the 6th derivative mostly measures rounding error.
- `reality_state.py`: enjoyment, meaning and perception are placeholder formulas of the
  distance from the origin, chosen so the numbers land between 0 and 1.
- `dimensional_discovery.py`: PCA, ICA, Isomap and LLE through scikit-learn. Sound tools;
  the variance threshold (1%) is arbitrary and has no chance baseline.
- `applications.py`: a gold-trading assistant and a text optimiser, unrelated to courts.

`synthium/geometry/` keeps every idea above and fixes or completes each of these points.
The original license of this folder is the MIT license in `LICENSE` here.

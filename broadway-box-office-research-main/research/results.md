# Results

## Exact aggregate production reproduction

The 67-production OLS model reproduces all four supplied verification benchmarks to the prespecified `1e-6` tolerance. R² is **0.607957** and adjusted R² is **0.425003**. The theatre-capacity coefficient is **1.007385** (HC3 95% CI **0.529649 to 1.485121**, p = **0.0000358**). Conditional on the recorded controls, a 1% capacity difference is therefore associated with approximately a 1.01% difference in average weekly gross.

| Benchmark | Paper result | Python result | Absolute difference |
|---|---:|---:|---:|
| R² | 0.607957 | 0.607957 | < 1e-15 |
| Capacity coefficient | 1.007385 | 1.007385 | < 1e-14 |
| Capacity HC3 p-value | 0.0000358 | 0.0000358 | < 1e-17 |
| Adapted coefficient | 0.286721 | 0.286721 | < 2e-11 |

Neither the adaptation coefficient (**0.286721**) nor the revival coefficient (**−0.284169**) has an HC3 95% interval that excludes zero. The creative-category coefficients are estimated imprecisely in this small, densely parameterized sample.

## Prespecified production sensitivity analysis

| Sample | N | R² | Capacity estimate | HC3 95% CI | HC3 p-value |
|---|---:|---:|---:|---:|---:|
| Full sample | 67 | 0.607957 | 1.007385 | 0.529649 to 1.485121 | 0.0000358 |
| Without Hamilton | 66 | 0.568097 | 1.007385 | 0.529649 to 1.485121 | 0.0000358 |
| Without top 5% by gross | 63 | 0.531122 | 0.923827 | 0.454106 to 1.393549 | 0.000116 |
| At least 20 observed weeks | 51 | 0.692047 | 0.796268 | 0.296038 to 1.296498 | 0.00181 |

The sign and practical scale of the capacity association persist under these alternatives. Identical capacity estimates after excluding `Hamilton` reflect the loss of the only HipHop observation and the resulting categorical reparameterization; they are not evidence that the observation has no influence. R² values across different samples are not model rankings.

## Exploratory market extensions

The market models below are newly specified extensions, not exact reproductions. Paper fit values are retained only as verification context because the original design matrices and upstream feature-construction code are unavailable.

| Model | N | Extension R² | Paper R² | Design rank | Columns | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| A | 501 | 0.506952 | 0.507 | 24 | 24 | Calendar extension, HAC(8) |
| B | 257 | 0.698749 | 0.699 | 21 | 21 | Complete-case monthly macro extension, HAC(8) |
| C | 236 | 0.707511 | 0.671 | 18 | 18 | Rank-repaired tourism extension, HAC(8) |
| D | 257 | 0.696198 | 0.696 | 21 | 21 | Complete-case semiannual sentiment extension, HAC(8) |

Model C replaces year fixed effects with elapsed time because annual tourism is collinear with a full set of year indicators. It also includes a coarse post-reopening indicator. This full-rank repair changes the estimand and raises R² relative to the reported paper value; it must not be described as an exact reproduction.

## Missingness and evidence boundary

Unemployment is unavailable for **244 of 501 weeks (48.7%)**. All observations in 2016–2019 are missing that field, as are 31 of 31 observed weeks in 2015 and 4 of 52 weeks in 2025. Complete-case macro models therefore characterize a later, time-selected subset. No missing values are imputed.

All dollar values are nominal. The analysis is associational, does not observe production costs or profit, and does not reconstruct the unavailable show-week microdata.

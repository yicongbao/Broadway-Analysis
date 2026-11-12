# Methodology

## Research design and units of observation

The study answers two related but distinct descriptive questions. The production analysis compares 67 musical titles and asks which observed production characteristics are associated with average weekly gross. The market analysis compares 501 observed Broadway weeks and asks how aggregate market gross varies with calendar and macroeconomic measures. These tables are never joined row by row because a production aggregate and a market week are different observational units with different dependent variables.

The supplied production table is an aggregate extract. The source paper describes approximately 4,972 underlying show-week records, but neither those records nor the complete title-selection trail is available. The public project therefore replicates the reported aggregate-level model; it does not claim to reconstruct the original microdata. The market table spans 2015-05-31 through 2026-05-24, with a long pandemic-related gap that is left visibly disconnected in time-series figures.

## Data loading and cleaning

The pipeline reads the authorized six-sheet Excel workbook and identifies the two analysis tables by their expected schema. Dates are parsed strictly, numeric columns retain missing values, and invalid values are never replaced with zero. Automated checks require the pre-derivation shapes to be exactly 67 by 19 and 501 by 21, unique production titles and market dates, positive gross values, and consistency between the supplied log variables and their level-scale counterparts.

The analysis checks `log_gross` against `log(Avg_Gross_USD)` and reports the range of `exp(log_seats)` as a plausibility diagnostic. That inverse transform is not an independent verification of theatre capacity. Gross is measured in nominal US dollars; no inflation adjustment is imposed. Creative classifications and some production attributes are provisional source labels rather than independently adjudicated categories.

Missing values are retained until a model explicitly requires complete cases. Unemployment is missing for 244 of 501 market weeks (48.7%), and its absence is concentrated in earlier years. Because this missingness is strongly related to calendar time, complete-case market estimates describe a selected period rather than a random subsample. The notebooks and pipeline publish the missingness count, rate, and year distribution.

## Why ordinary least squares

Ordinary least squares is used because the paper specifies continuous log gross as the outcome and the primary goal is a transparent conditional association that can be reproduced exactly from the supplied aggregate extract. With indicator variables and categorical controls, OLS estimates the best linear projection of log gross on the recorded predictors under the chosen specification. Its coefficients, confidence intervals, and benchmark statistics are directly comparable with the reported table.

This choice does not establish causality. Theatre capacity can reflect expected demand; omitted budget, advertising, pricing, reviews, and casting variables can affect both scale and revenue. Aggregation also removes within-production dynamics. The coefficient on `log_seats` is therefore interpreted as a conditional elasticity-like association, not the effect of physically adding seats.

## Production specification and inference

The primary formula is:

```text
log_gross ~ log_seats + Adapted + Revival
          + C(Year) + C(Music_Style)
          + Plot_Comedy + Plot_Tragedy + Plot_Romance
          + Plot_Mystery + Plot_Drama + Plot_Adventure
          + Plot_Crime + Plot_Biographical + Plot_Fantasy
```

`statsmodels` uses treatment coding for categorical variables, with the omitted level visible through the coefficient labels. Every production sensitivity case reuses this same formula. The model contains 22 estimated columns for only 67 observations, so uncertainty, leverage, sparse categories, and effective degrees of freedom are central to interpretation.

HC3 heteroskedasticity-consistent covariance is used for production inference. HC3 inflates each squared residual according to its leverage and is generally more conservative than the basic White covariance in small samples with uneven leverage. It addresses heteroskedasticity under the maintained linear specification; it cannot repair omitted variables, measurement error, sparse categories, or misspecification. The project reports both conventional model fit and HC3 standard errors, p-values, and 95% confidence intervals.

## Diagnostics and outlier handling

No observation is automatically deleted as an outlier. The diagnostics report design-matrix rank, condition number, leverage, Cook's distance, residual-versus-fitted patterns, and a Breusch-Pagan heteroskedasticity diagnostic. These measures are used to identify sensitivity, not to retroactively choose a preferred sample.

The four prespecified sensitivity samples are the full extract, exclusion of `Hamilton`, exclusion of productions above the empirical 95th-percentile gross threshold, and restriction to at least 20 observed weeks. The top-5% rule is implemented deterministically with the source threshold. Excluding `Hamilton` also removes the only HipHop observation, so that case changes categorical support in addition to removing a commercially unusual title. Differences in R-squared across these samples are not model rankings because the outcomes and variance are evaluated on different observations.

## Market extensions and HAC inference

The paper reports four market models using Newey-West heteroskedasticity-and-autocorrelation-consistent covariance with eight lags. The exact original design matrices and upstream feature-construction code are unavailable. The project therefore labels every rerun as an exploratory market extension, records its explicit formula, and places paper-reported fit statistics beside independently computed values without calling discrepancies matches.

HAC inference permits residual variance to change over time and allows autocorrelation through eight successive observed rows. This is appropriate for weekly outcomes, but it does not make monthly unemployment or sentiment values independent after they are repeated across weeks. Nor does it solve the irregular spacing created by calendar gaps. Annual tourism repeated across weeks is especially coarse and must not be interpreted as 52 independent annual measurements.

Full year fixed effects and annual tourism are structurally redundant in the same design. Likewise, `summer_week` and `december_week` are deterministic functions of month controls. The repaired tourism extension removes these aliases, uses month effects, a continuous year trend, and a post-reopening indicator, and verifies full column rank before fitting HAC covariance. This is a methodological repair and an independent extension, not an exact reconstruction of paper model C. The reopening indicator is a coarse break control rather than a causal pandemic adjustment.

## Sensitivity and interpretation

Sensitivity analysis asks whether the sign and practical scale of the capacity association persist under transparent alternative samples. It does not prove robustness to all outliers or establish stability under unobserved confounding. Confidence intervals and sample composition are interpreted together with point estimates. The market analysis similarly emphasizes sample coverage, matrix rank, repeated-frequency covariates, and structural breaks rather than selecting a model by the largest R-squared.

## Methodological contribution

The project's contribution is reproducibility and specification auditing. It independently verifies the aggregate production benchmark to numerical tolerance, makes categorical and plot controls explicit, exposes the public/private data boundary, tests sample definitions, publishes leverage and rank diagnostics, separates production and market units, and replaces a rank-deficient tourism extension with a documented full-rank alternative. It does not claim a new causal design, recover unavailable show-week records, or establish the original market specifications.

## Reproduction commands

After obtaining authorized access to the original workbook, set `BROADWAY_INPUT_DIR` to its containing directory and run:

```bash
python -m pip install -e .
python -m broadway_research.pipeline --input-dir "$BROADWAY_INPUT_DIR" --output-dir .
python -m pytest -q
```

Each notebook accepts the same `BROADWAY_INPUT_DIR` environment variable. The executed public notebooks contain aggregate results and unlabeled diagnostic graphics; the private workbook and row-level exports remain excluded.

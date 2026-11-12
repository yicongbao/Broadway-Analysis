# Broadway Box Office Research Report

## Abstract

This study reproduces an aggregate production-level analysis of Broadway musical gross and develops a separate set of transparent weekly market extensions. The production sample contains 67 titles; the market series contains 501 observed weeks from May 2015 through May 2026. Ordinary least squares with HC3 covariance exactly reproduces the paper's production benchmarks. The central result is a theatre-capacity coefficient of **1.007** (95% HC3 CI **0.530 to 1.485**, p < 0.001) in a log-gross model with production and creative controls. Prespecified sample restrictions retain a positive capacity association. Exploratory market models use HAC(8) covariance, explicit complete-case rules, and full-rank designs. They are not claimed as exact reproductions because the original market design matrices are unavailable. The results are descriptive associations, not causal estimates.

## Research questions and design

The project addresses two distinct questions:

1. Which observed production characteristics are associated with a musical's average weekly gross?
2. How does Broadway-wide weekly gross vary with calendar and macroeconomic measures?

The first question is cross-sectional at the production level. The second is longitudinal at the Broadway-market-week level. These records are never merged row by row, and results from one level are not interpreted as estimates at the other.

The production model follows the supplied paper and uses log average weekly gross as the outcome. Predictors include log theatre capacity, adaptation and revival indicators, year, music style, and plot indicators. The market extensions use log aggregate weekly gross with calendar and available macroeconomic measures. Gross is nominal US dollars.

## Main production results

The production model has R² **0.607957** and adjusted R² **0.425003**. The Python implementation matches the supplied R², capacity estimate, capacity p-value, and adaptation estimate within `1e-6`.

The capacity coefficient is **1.007385**, with HC3 standard error and confidence interval yielding p = **0.0000358** and a 95% interval of **0.529649 to 1.485121**. Because both gross and capacity are logged, the coefficient is elasticity-like: conditional on the model, a 1% capacity difference is associated with about a 1.01% gross difference.

That interpretation is not causal. Expected demand can influence theatre allocation, and larger theatres mechanically permit more tickets to be sold. Budget, advertising, reviews, star casting, price, performance count, and operating costs are not fully observed.

The adaptation estimate is **0.286721** and the revival estimate is **−0.284169**. Their HC3 intervals include zero. Several creative-category estimates are also imprecise, consistent with sparse cells and a 22-column design applied to only 67 records.

## Diagnostics and sensitivity

No record is automatically discarded as an outlier. The pipeline reports leverage, Cook's distance, residual behavior, the Breusch–Pagan diagnostic, matrix rank, and condition number. Sensitivity analysis holds the formula fixed while changing the sample according to four prespecified rules.

The capacity estimate is **0.923827** after removing the top 5% of productions by gross and **0.796268** among productions observed for at least 20 weeks; both HC3 intervals exclude zero. Excluding `Hamilton` also removes the only HipHop title, changing the support and parameterization of music style. Sensitivity results support persistence of the positive association under these samples, but they do not eliminate omitted-variable or selection concerns.

## Market analysis

The source paper reports four market specifications and Newey–West inference with eight lags. Because the exact original matrices and upstream construction code are unavailable, the repository records the reported results as benchmarks and labels every fitted market model as an exploratory extension.

Models A, B, and D have R² values of **0.506952**, **0.698749**, and **0.696198**, respectively, close to the reported fit values under explicit formulas. Model C required a methodological repair: annual tourism and complete year fixed effects are structurally collinear. The revised model uses elapsed time, a post-reopening indicator, month effects, and the documented macro variables. It is full rank (18 of 18 columns) and has R² **0.707511**, compared with the paper-reported **0.671**. The difference is documented as a changed exploratory result, not a successful exact reproduction.

HAC(8) covariance allows heteroskedasticity and short-run dependence across successive observed rows. It does not solve the coarse repetition of monthly, semiannual, or annual covariates, nor does it make observations equally spaced across calendar gaps.

## Missing data and structural breaks

Unemployment is missing for **244 of 501 weeks**. Missingness is concentrated in the earlier part of the series, making complete-case market models time-selected. No imputation is used. Annual tourism and monthly or semiannual sentiment measures are repeated across many weekly rows, so their nominal row count overstates independent variation.

The Broadway shutdown and reopening create a major structural break. Annual dashboard summaries leave the shutdown gap uninterpolated and flag partial observed years. The post-reopening indicator in model C is a coarse adjustment, not a causal pandemic design.

## Contribution and relation to prior research

The study's contribution is reproducibility and specification auditing. It verifies the aggregate production benchmark independently, makes the categorical design explicit, publishes robust uncertainty and influence diagnostics, tests prespecified samples, separates analytical levels, and replaces a rank-deficient market extension with a transparent alternative.

This scope is narrower than transaction-level studies of Broadway price discrimination or ticket resale. Those literatures show that observed revenue reflects pricing, seat quality, allocation, secondary-market behavior, and heterogeneous demand. Related work on Broadway recoupment also underscores that gross revenue is not profit. The current data cannot identify those mechanisms; the comparison is developed in [related_work.md](related_work.md).

## Reproducibility and public boundary

The repository provides an installable Python package, five executed computational notebooks, generated aggregate results, automated tests, figures, and a static interactive dashboard. The source workbook and row-level observations remain private pending redistribution permission. Authorized researchers can rerun the pipeline by setting `BROADWAY_INPUT_DIR`; complete instructions are in [reproducibility.md](reproducibility.md).

## Conclusion

The most defensible replicated finding is a positive conditional association between theatre capacity and average weekly production gross. The market analysis provides useful descriptive and diagnostic context but has a narrower evidence base because of missing macro data, repeated-frequency covariates, structural breaks, and unavailable original specifications. The repository therefore treats exact reproduction and exploratory evidence as separate claims throughout.

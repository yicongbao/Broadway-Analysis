# Limitations

## Production evidence

The 67 production records are title-level aggregates. The unavailable 4,972 show-week observations and the full selection trail cannot be reconstructed from the supplied workbook. Aggregation discards within-show trajectories, week-specific shocks, pricing changes, performance counts, and interactions with market conditions.

The sample is small relative to the 22-column design matrix. Several music-style cells are sparse, and `Hamilton` is the only HipHop title. Its exclusion therefore changes the support of a categorical variable as well as removing an influential production. High leverage, provisional creative labels, and omitted budget, marketing, reviews, casting, ticket price, and operating-cost measures limit interpretation.

The capacity coefficient is an association. Productions with greater expected demand may be assigned larger theatres, and capacity mechanically bounds tickets available. The estimate cannot be interpreted as the causal revenue effect of adding seats. Average weekly gross is revenue, not profit or investor return.

## Market evidence

Unemployment is missing for 244 of 501 weeks and is concentrated by period, so complete-case macroeconomic estimates are time-selected. Monthly unemployment and sentiment are repeated over multiple weekly rows; annual tourism is repeated over many more. Weekly row count therefore overstates the effective independent variation in these covariates.

The pandemic shutdown and reopening are major structural breaks. The series also contains calendar gaps, so an eight-row HAC lag does not always represent eight equally spaced calendar weeks. The repaired tourism extension controls for a trend and a coarse reopening indicator, but neither removes all pandemic-era confounding nor creates a causal design.

The paper's exact A-D matrices and upstream feature-construction code are unavailable. Paper statistics remain reported benchmarks. Current market regressions are independent exploratory extensions and should not be described as exact reproductions. The full-rank alternative removes known aliases between annual tourism and year effects and between calendar indicators and month effects, but its changed specification necessarily changes interpretation and fit.

## Measurement, scope, and external validity

Gross is nominal USD and is not adjusted for inflation. The number of operating shows and performances is not modeled explicitly even though aggregate market gross depends on market supply. Tourism is annual rather than weekly. Provisional creative categories may contain classification error.

The research period includes unusual pre-pandemic, shutdown, reopening, and recovery regimes. Results need not generalize to other theatrical markets or future Broadway seasons. Statistical significance does not establish commercial relevance, artistic value, or causality.

## Reproducibility and rights

The public code, aggregate model outputs, and executed notebooks are reproducible only after an authorized user supplies the original analysis workbook through `BROADWAY_INPUT_DIR`. The workbook, paper, and row-level exports are excluded because public redistribution rights have not been established. Provider links do not by themselves resolve licensing or version lineage.

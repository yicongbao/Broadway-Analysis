# Related work and source context

The project sits between cultural economics, ticket-market research, and reproducible empirical practice. The references below delimit the contribution rather than implying that this aggregate regression resolves questions studied with transaction-level or structural data.

## Broadway and ticket-market economics

Leslie's study of Broadway ticket pricing models price discrimination using detailed seat and performance information. It shows why observed revenue combines capacity, seat quality, demand heterogeneity, and pricing decisions, reinforcing this project's caution against interpreting a capacity coefficient as a causal supply effect.

- Phillip Leslie (2004), “Price Discrimination in Broadway Theater,” *RAND Journal of Economics* 35(3), 520–541. [DOI: 10.2307/1593706](https://doi.org/10.2307/1593706).

Detsky, Gutekunst, and Kopac assemble public gross and press-report evidence to estimate Broadway musical recoupment. Their analysis highlights the distinction between ticket gross and investor profitability: weekly gross does not observe capitalization, operating costs, commissions, or royalty waterfalls. This supports treating the current dependent variable as revenue rather than profit.

- Allan S. Detsky, Samuel C. Gutekunst, and Christopher Kopac (2025), “Defying gravity or failing to launch?”, *Significance* 22(4). [Oxford Academic article](https://academic.oup.com/jrssig/article/22/4/6/8151666).

Research on ticket resale demonstrates that ticket-market outcomes can reflect strategic primary pricing, allocation, secondary-market behavior, and demand uncertainty. Those mechanisms are outside the supplied Broadway aggregates and remain possible omitted channels.

- Phillip Leslie and Alan Sorensen (2014), “Resale and Rent-Seeking: An Application to Ticket Markets,” *Review of Economic Studies* 81(1), 266–300. [DOI: 10.1093/restud/rdt033](https://doi.org/10.1093/restud/rdt033).

## Inference methods

HC3 belongs to the family of leverage-adjusted heteroskedasticity-consistent covariance estimators developed for linear models. Its use here reflects the small production sample and uneven leverage, while retaining the paper's point estimates.

- James G. MacKinnon and Halbert White (1985), “Some heteroskedasticity-consistent covariance matrix estimators with improved finite sample properties,” *Journal of Econometrics* 29(3), 305–325. [DOI: 10.1016/0304-4076(85)90158-7](https://doi.org/10.1016/0304-4076(85)90158-7).

The market extensions use Newey-West covariance because weekly residuals may be both heteroskedastic and serially correlated. HAC changes inference, not the OLS coefficient estimates or the underlying identification.

- Whitney K. Newey and Kenneth D. West (1987), “A Simple, Positive Semi-definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix,” *Econometrica* 55(3), 703–708. [DOI: 10.2307/1913610](https://doi.org/10.2307/1913610).

## Data-provider references

The supplied paper cites the following providers. These links identify institutions and series, but they do not establish the precise acquisition date, version, transformation history, or redistribution license for the supplied workbook.

- [Internet Broadway Database](https://www.ibdb.com/)
- [The Broadway League](https://www.broadwayleague.com/)
- [FRED unemployment rate, UNRATE](https://fred.stlouisfed.org/series/UNRATE)
- [FRED University of Michigan consumer sentiment, UMCSENT](https://fred.stlouisfed.org/series/UMCSENT)
- [New York City Tourism + Conventions](https://www.nyctourism.com/)
- [TidyTuesday Broadway data, 2020-04-28](https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-04-28)

## Evidence boundary

This repository contributes a transparent replication of an aggregate production model and a diagnostic market extension. It does not claim novelty over structural ticket-pricing research, infer profitability from gross, or reproduce the original market models without their design matrices. The private source workbook remains outside the public repository until redistribution rights are confirmed.

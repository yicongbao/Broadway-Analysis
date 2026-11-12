# Data access and source boundary

The original analysis workbook is intentionally absent from this public repository because redistribution permission has not been established. The repository does not provide a synthetic substitute that could be mistaken for the research source.

Authorized researchers should place the six-sheet workbook in a private directory and set `BROADWAY_INPUT_DIR` to that directory. The pipeline validates the expected production and market schemas before analysis. Variable types and missing counts are published in [`results/data_dictionary.csv`](../results/data_dictionary.csv).

The supplied paper attributes source measures to the Internet Broadway Database, The Broadway League, FRED unemployment and consumer-sentiment series, New York City Tourism + Conventions, and TidyTuesday's Broadway release. Provider links, academic context, and provenance limitations are documented in [`research/related_work.md`](../research/related_work.md) and [`research/source_coverage.md`](../research/source_coverage.md). Provider pages do not by themselves establish the exact acquisition version, transformation history, or redistribution license of the supplied workbook.

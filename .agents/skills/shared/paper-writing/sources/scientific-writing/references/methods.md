# Methods

The Methods section should make the study inspectable: a competent reader should be able to understand what was done, why key choices were made, and what would be needed to repeat or critically evaluate the work.

## Describe the design before implementation detail

Start with the structure of the study or analysis rather than a sequence of software commands. Make clear:

- study design and units of analysis,
- population, system, or data source,
- inclusion/exclusion criteria,
- interventions, exposures, or experimental conditions,
- outcomes and measurements,
- preprocessing and quality control,
- statistical or computational analysis,
- sensitivity or robustness checks.

The reader should understand the inferential design before encountering low-level implementation details.

## Report choices that can change the result

Include consequential details such as:

- software and relevant versions,
- model formulas and parameterization,
- thresholds and filtering rules,
- normalization or transformations,
- randomization/blinding procedures,
- handling of missing data,
- sample exclusions,
- multiple-comparison handling,
- random seeds when relevant.

Do not rely on a package name or citation as a substitute for explaining an analysis choice.

## Explain why, not only what

For non-obvious design and analysis choices, state the scientific rationale. This is especially important when several reasonable alternatives exist and the choice affects interpretation.

## Preserve reproducibility outside the prose

The paper need not contain every line of code or every raw file. Use durable supplementary artifacts when appropriate:

- analysis scripts,
- protocol,
- data dictionary,
- computational environment,
- workflow definition,
- repository or archived release.

The Methods section should tell the reader where those artifacts are and how they relate to the reported result.

## Distinguish prespecified and post hoc analysis

When the distinction matters, state which analyses were planned before inspecting outcomes and which were added during exploration or revision. Transparency is more useful than pretending all decisions were predetermined.

## Methods diagnostics

The section is probably insufficient if:

- the unit of analysis is ambiguous,
- another researcher cannot identify which observations were excluded and why,
- the result depends on an undocumented parameter or manual step,
- an analysis is justified only by naming software,
- the reader cannot tell which version of data/code generated the published result,
- key protocol deviations are omitted.

## Sources

- Zhang W. *Ten Simple Rules for Writing Research Papers.* https://doi.org/10.1371/journal.pcbi.1003453
- Kass RE, et al. *Ten Simple Rules for Effective Statistical Practice.* https://doi.org/10.1371/journal.pcbi.1004961
- Sandve GK, et al. *Ten Simple Rules for Reproducible Computational Research.* https://doi.org/10.1371/journal.pcbi.1003285
- Schwab S, et al. *Ten simple rules for good research practice.* https://doi.org/10.1371/journal.pcbi.1010139

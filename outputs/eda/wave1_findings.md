# IndoToxic EDA Findings — Wave 1

Status: exploratory checkpoint
Dataset: `data/raw/indotoxic2024_annotated_data_v2_final.csv`
Scope: agreement, exact duplicates, topic conditioning, text length, sub-labels, raw social-text markers

## Rules

- Raw dataset remains unchanged.
- EDA methods return copied frames or aggregate tables.
- Duplicate, missing, borderline, and outlier rows remain available for audit.
- No preprocessing rule becomes default from one descriptive statistic.
- Learned transformations must fit on train split only when modeling starts.

## Dataset boundary

| Measure | Result |
|---|---:|
| Rows | 28,448 |
| Non-toxic consensus | 24,453 |
| Toxic consensus | 3,995 |
| Toxic prevalence | 14.04% |
| Missing `text` | 1 |
| Missing `initial_paragraph` | 26,779 |
| Exact duplicate text groups | 2,118 |
| Exact duplicate groups with label conflict | 343 |
| Rows inside conflicting duplicate groups | 742 |
| Borderline annotation rows | 3,858 |
| Unanimous annotation rows | 24,590 |

`initial_paragraph` is too sparse for a first-pass feature. Keep it for provenance; do not impute it during EDA.

## Finding 1 — agreement is a major label boundary

| Agreement band | Rows | Toxic rows | Toxic rate |
|---|---:|---:|---:|
| Borderline | 3,858 | 2,580 | 66.87% |
| Unanimous | 24,590 | 1,415 | 5.75% |

By consensus label:

- Toxic rows: 2,580 borderline and 1,415 unanimous.
- Non-toxic rows: 1,278 borderline and 23,175 unanimous.

### Interpretation

Consensus label alone hides annotation uncertainty. Most toxic rows are borderline, while most unanimous rows are non-toxic. Lexical and n-gram comparisons must therefore report at least two strata:

```text
all rows
unanimous rows
borderline rows
```

Do not treat borderline rows as noise or delete them. They are a high-value audit subset.

## Finding 2 — exact duplicates include annotation conflict

- 1,775 duplicate groups have consistent consensus labels.
- 343 duplicate groups have both labels.
- Conflicting duplicate groups contain 742 rows.

### Interpretation

Duplicate removal is unsafe before split design and provenance review. Exact duplicate text can represent repeated observations, annotator disagreement, or split leakage risk. Next audit:

1. group exact text before splitting;
2. keep one group in one partition;
3. compare results against a row-level stratified split as a sensitivity experiment;
4. preserve conflicting groups in an audit table.

## Finding 3 — topic changes toxic prevalence

For topic groups with at least 500 rows:

| Topic | Rows | Toxic rate |
|---|---:|---:|
| `LGBTQ+` | 878 | 34.28% |
| `Syiah` | 532 | 32.33% |
| `Jewish` | 8,607 | 17.73% |
| `UNKNOWN` | 2,263 | 12.64% |
| `Disabilitas` | 6,922 | 12.02% |
| `Kristen` | 1,381 | 9.41% |
| `Rohingya` | 1,488 | 7.33% |
| `Tionghoa` | 5,415 | 6.85% |

Topic values can be multi-topic, such as `Syiah, Jewish`. Treating them as unrelated atomic strings loses structure. First compare:

```text
topic string as observed
multi-topic membership
single-topic vs multi-topic
```

Then run `token × topic × label` analysis. Do not infer a topic causal effect from prevalence alone.

## Finding 4 — length has weak standalone separation

| Consensus label | Mean words | Median words | Mean chars | Median chars |
|---|---:|---:|---:|---:|
| Non-toxic | 45.50 | 21 | 319.66 | 144 |
| Toxic | 36.75 | 23 | 250.63 | 152 |

Outliers:

- `word_count <= 2`: 21 non-toxic, 2 toxic.
- `word_count > 500`: 153 non-toxic, 2 toxic.
- Empty text: 1 row.

### Interpretation

Mean length differs, but medians are close. Long-text outliers are concentrated in non-toxic rows and can distort aggregate statistics. Report median and quantiles with mean. Do not set a truncation limit from mean length.

Next check:

```text
length × label × topic × agreement_band
```

## Finding 5 — sub-labels do not map perfectly to binary toxicity

Consensus-positive counts:

| Sub-label | Positive rows | Rate |
|---|---:|---:|
| `insults` | 1,947 | 6.84% |
| `identity_attack` | 1,756 | 6.17% |
| `threat_incitement_to_violence` | 786 | 2.76% |
| `profanity_obscenity` | 669 | 2.35% |
| `sexually_explicit` | 122 | 0.43% |

Sub-label positives inside non-toxic consensus rows exist:

- `profanity_obscenity`: 5
- `threat_incitement_to_violence`: 255
- `insults`: 50
- `identity_attack`: 172
- `sexually_explicit`: 2

### Interpretation

Binary toxicity is not a simple OR projection of sub-label columns. These rows need example-level audit. Possible explanations include annotation threshold differences, task definitions, or vote aggregation behavior. Do not relabel them automatically.

## Finding 6 — raw social markers suggest selective preservation

| Marker | Non-toxic rate | Toxic rate |
|---|---:|---:|
| URL | 3.29% | 1.50% |
| Mention | 11.68% | 11.39% |
| Hashtag | 27.90% | 19.10% |
| Exclamation | 10.22% | 12.62% |
| Question | 9.70% | 14.19% |
| Emoji or symbol | 86.35% | 87.66% |
| Repeated character | 15.18% | 19.12% |

Uppercase ratio means are close: 0.141 for non-toxic and 0.144 for toxic. Median toxic uppercase ratio is lower.

### Interpretation

Do not delete all punctuation, emoji, hashtags, or repeated characters by default. The strongest first candidates for contextual experiments are:

```text
question + exclamation + repeated-character
marker × agreement_band
marker × topic
marker combinations × label
```

Mention and emoji presence alone are weak separators. Hashtag presence is more common in non-toxic rows, but hashtag content may still carry lexical signal.

## Implemented reusable API

`src/eda/text_eda.py` now exposes:

- `annotation_profile(frame)`
- `group_label_rates(frame, group_column, min_count=1)`
- `sublabel_summary(frame, columns)`
- `sublabel_cooccurrence(frame, columns)`
- `duplicate_profile(frame)`
- `marker_profile(frame)`
- `variant_comparison(frame, variants)`

All methods use analysis copies and preserve the input frame.

Example variant comparison:

```python
from src.eda import TextEDA
from src.preprocessing import TextCleaner, SlangNormalizer

eda = TextEDA()
result = eda.variant_comparison(
    frame,
    variants={
        "lowercase": str.lower,
        "keep_hashtag_content": lambda text: text.replace("#", ""),
        "normalize": SlangNormalizer().normalize,
        "clean": TextCleaner().clean,
    },
)
```

The comparison table measures document count, token count, vocabulary size, token retention, and raw-vocabulary overlap. It does not decide which variant is better.

## Next experiment — Wave 2

Run these in order:

1. Split lexical analysis into `all`, `unanimous`, and `borderline` subsets.
2. Compare shared words, log-odds, bigrams, trigrams, and KWIC by subset.
3. Condition token rates on topic membership, not only raw topic strings.
4. Compare preprocessing variants:
   - raw;
   - lowercase;
   - preserve hashtag content;
   - remove hashtag token;
   - collapse repeated characters;
   - leet decoding;
   - slang expansion;
   - full existing cleaner.
5. Re-run EDA after every single variant. Record vocabulary overlap and examples whose meaning-bearing markers changed.

Recommended first hypothesis:

> Repeated characters and question/exclamation patterns carry more label signal in borderline rows than in unanimous rows; removing them may erase useful context.

Falsification test:

```text
compare marker rates and n-gram log-odds for
(all, unanimous, borderline) × (raw, collapse-repetition)
```

Decision rule: keep a transformation only when it reduces irrelevant variation without collapsing label- or topic-conditioned patterns. Model training remains out of scope until this loop is reviewed.

## Verification

```text
14 passed, 2 warnings
ruff check passed
```

Warnings come from existing seaborn/matplotlib boxplot deprecation behavior. Full project tests currently require PostgreSQL on `localhost:5434`; EDA unit tests were run with repository DB fixture disabled because that service is not running.

# IndoToxic EDA Findings — Wave 5

Status: sub-label taxonomy audit; no model training

## Method

- Sub-label votes use same majority threshold as primary toxicity label.
- Topic values are expanded as membership for conditioned descriptive rates.
- Non-toxic sub-label positives are retained as annotation evidence, not removed.
- Co-occurrence counts are row-level joint-positive counts.

## Sub-label profile

| sublabel | positive_count | positive_rate | toxic_positive_count | toxic_positive_rate | nontoxic_positive_count | nontoxic_positive_rate |
|---|---|---|---|---|---|---|
| profanity_obscenity | 669 | 0.0235 | 664 | 0.1662 | 5 | 0.0002 |
| threat_incitement_to_violence | 786 | 0.0276 | 531 | 0.1329 | 255 | 0.0104 |
| insults | 1947 | 0.0684 | 1897 | 0.4748 | 50 | 0.0020 |
| identity_attack | 1756 | 0.0617 | 1584 | 0.3965 | 172 | 0.0070 |
| sexually_explicit | 122 | 0.0043 | 120 | 0.0300 | 2 | 0.0001 |

## Label mismatch

| sublabel | positive_sublabel_non_toxic | toxic_without_sublabel |
|---|---|---|
| profanity_obscenity | 5 | 3331 |
| threat_incitement_to_violence | 255 | 3464 |
| insults | 50 | 2098 |
| identity_attack | 172 | 2411 |
| sexually_explicit | 2 | 3875 |

## Agreement-conditioned rates

| sublabel | group_column | group | count | positive_count | positive_rate |
|---|---|---|---|---|---|
| profanity_obscenity | agreement_band | borderline | 3858 | 370 | 0.0959 |
| profanity_obscenity | agreement_band | unanimous | 24590 | 299 | 0.0122 |
| threat_incitement_to_violence | agreement_band | borderline | 3858 | 415 | 0.1076 |
| threat_incitement_to_violence | agreement_band | unanimous | 24590 | 371 | 0.0151 |
| insults | agreement_band | borderline | 3858 | 1097 | 0.2843 |
| insults | agreement_band | unanimous | 24590 | 850 | 0.0346 |
| identity_attack | agreement_band | borderline | 3858 | 752 | 0.1949 |
| identity_attack | agreement_band | unanimous | 24590 | 1004 | 0.0408 |
| sexually_explicit | agreement_band | borderline | 3858 | 94 | 0.0244 |
| sexually_explicit | agreement_band | unanimous | 24590 | 28 | 0.0011 |

## Decision

- Treat sub-labels as descriptive taxonomy, not automatically equivalent to primary toxicity.
- Audit non-toxic sub-label positives before using them as auxiliary targets.
- Preserve co-occurrence structure; one text may express multiple categories.
- Use topic-conditioned tables to separate category prevalence from topic composition.

# IndoToxic EDA Findings — Wave 6

Status: punctuation, marker, and context audit; no model training

## Method

- Raw text remains unchanged.
- Punctuation is counted, not removed.
- Topic values are expanded as membership for topic-conditioned rates.
- Rates are descriptive and do not establish causal effects.
- Extreme punctuation examples are saved for manual KWIC/context review.

## Label-conditioned marker rates

| marker | group_column | group | count | marker_count | marker_rate |
|---|---|---|---|---|---|
| has_question | label | 0 | 24453 | 2372 | 0.0970 |
| has_question | label | 1 | 3995 | 567 | 0.1419 |
| has_exclamation | label | 0 | 24453 | 2498 | 0.1022 |
| has_exclamation | label | 1 | 3995 | 504 | 0.1262 |
| has_question_exclamation | label | 0 | 24453 | 70 | 0.0029 |
| has_question_exclamation | label | 1 | 3995 | 23 | 0.0058 |
| has_exclamation_question | label | 0 | 24453 | 24 | 0.0010 |
| has_exclamation_question | label | 1 | 3995 | 6 | 0.0015 |
| has_url | label | 0 | 24453 | 804 | 0.0329 |
| has_url | label | 1 | 3995 | 60 | 0.0150 |
| has_mention | label | 0 | 24453 | 2857 | 0.1168 |
| has_mention | label | 1 | 3995 | 455 | 0.1139 |
| has_hashtag | label | 0 | 24453 | 6822 | 0.2790 |
| has_hashtag | label | 1 | 3995 | 763 | 0.1910 |
| has_emoji_or_symbol | label | 0 | 24453 | 21114 | 0.8635 |
| has_emoji_or_symbol | label | 1 | 3995 | 3502 | 0.8766 |
| has_repeated_character | label | 0 | 24453 | 3711 | 0.1518 |
| has_repeated_character | label | 1 | 3995 | 764 | 0.1912 |

## Decision

- Preserve `?`, `!`, mixed `?!`, repeated punctuation, and punctuation density in raw analysis.
- `remove_punctuation` remains an ablation control, not a default decision.
- Interpret marker signals jointly with agreement and topic context.
- Review `wave6_punctuation_evidence.csv` manually before final preprocessing policy.

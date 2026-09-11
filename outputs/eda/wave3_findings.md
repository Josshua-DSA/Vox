# IndoToxic EDA Findings — Wave 3

Status: preprocessing variant signal ablation

## Method

- Each variant is a single-purpose transform applied to raw text.
- Signal preservation compares top-N discriminating tokens (document-presence
  log-odds) against the raw baseline via Jaccard overlap.
- `raw_vocabulary_overlap` = variant vocab retained from raw vocab.
- Vocabulary collapse is expected for leet/slang normalization (merges
  obfuscated forms); a drop in overlap without collapse signals signal loss.

## Signal ablation

| variant | vocabulary_size | raw_vocabulary_overlap | toxic_top_overlap | nontoxic_top_overlap |
|---|---|---|---|---|
| raw | 88393 | 1.0000 | 1.0000 | 1.0000 |
| lowercase | 88390 | 0.9999 | 1.0000 | 1.0000 |
| leet_decode | 88273 | 0.9556 | 1.0000 | 1.0000 |
| collapse_repetition | 87858 | 0.9844 | 1.0000 | 0.9048 |
| expand_emoji | 88373 | 0.9994 | 1.0000 | 1.0000 |
| expand_slang | 88376 | 0.9998 | 0.9048 | 1.0000 |
| keep_hashtag_content | 88293 | 0.9976 | 1.0000 | 0.9048 |
| remove_hashtag | 79472 | 0.8991 | 1.0000 | 0.7391 |
| remove_url | 87428 | 0.9891 | 1.0000 | 0.9048 |
| remove_mention | 85865 | 0.9714 | 1.0000 | 1.0000 |
| remove_punctuation | 88393 | 1.0000 | 1.0000 | 1.0000 |
| remove_emoji | 85866 | 0.9618 | 1.0000 | 1.0000 |
| full_normalize | 87644 | 0.9402 | 0.9048 | 0.9048 |
| existing_cleaner | 75774 | 0.8571 | 1.0000 | 0.6667 |

## Agreement-stratified vocabulary retention

| group_column | group | variant | document_count | token_count | vocabulary_size | token_retention | raw_vocabulary_overlap |
|---|---|---|---|---|---|---|---|
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | raw | 12 | 3206 | 1019 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | lowercase | 12 | 3206 | 1019 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | leet_decode | 12 | 3207 | 1020 | 1.0003 | 0.9912 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | collapse_repetition | 12 | 3206 | 1019 | 1.0000 | 0.9980 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | expand_emoji | 12 | 3244 | 1025 | 1.0119 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | expand_slang | 12 | 3206 | 1017 | 1.0000 | 0.9980 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | keep_hashtag_content | 12 | 3206 | 1019 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | remove_hashtag | 12 | 3203 | 1017 | 0.9991 | 0.9980 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | remove_url | 12 | 3081 | 986 | 0.9610 | 0.9676 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | remove_mention | 12 | 3205 | 1019 | 0.9997 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | remove_punctuation | 12 | 3206 | 1019 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | remove_emoji | 12 | 3042 | 984 | 0.9488 | 0.9627 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | full_normalize | 12 | 3245 | 1021 | 1.0122 | 0.9853 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah | existing_cleaner | 12 | 3077 | 984 | 0.9598 | 0.9657 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | raw | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | lowercase | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | leet_decode | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | collapse_repetition | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | expand_emoji | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | expand_slang | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | keep_hashtag_content | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | remove_hashtag | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | remove_url | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | remove_mention | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | remove_punctuation | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | remove_emoji | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | full_normalize | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Ahmadiyah, Kristen | existing_cleaner | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | raw | 400 | 10489 | 3695 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | lowercase | 400 | 10489 | 3695 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | leet_decode | 400 | 10489 | 3693 | 1.0000 | 0.9857 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | collapse_repetition | 400 | 10489 | 3687 | 1.0000 | 0.9878 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | expand_emoji | 400 | 10736 | 3710 | 1.0235 | 0.9981 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | expand_slang | 400 | 10494 | 3658 | 1.0005 | 0.9876 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | keep_hashtag_content | 400 | 10489 | 3695 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | remove_hashtag | 400 | 10323 | 3571 | 0.9842 | 0.9664 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | remove_url | 400 | 10467 | 3684 | 0.9979 | 0.9970 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | remove_mention | 400 | 10440 | 3665 | 0.9953 | 0.9919 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | remove_punctuation | 400 | 10489 | 3695 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | remove_emoji | 400 | 10451 | 3669 | 0.9964 | 0.9916 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | full_normalize | 400 | 10692 | 3637 | 1.0194 | 0.9507 |
| label__agreement_band__topic | 0\|borderline\|Disabilitas | existing_cleaner | 400 | 10252 | 3527 | 0.9774 | 0.9545 |
| label__agreement_band__topic | 0\|borderline\|Jewish | raw | 384 | 14130 | 4065 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish | lowercase | 384 | 14131 | 4064 | 1.0001 | 0.9998 |
| label__agreement_band__topic | 0\|borderline\|Jewish | leet_decode | 384 | 14131 | 4064 | 1.0001 | 0.9882 |
| label__agreement_band__topic | 0\|borderline\|Jewish | collapse_repetition | 384 | 14130 | 4063 | 1.0000 | 0.9961 |
| label__agreement_band__topic | 0\|borderline\|Jewish | expand_emoji | 384 | 14257 | 4075 | 1.0090 | 0.9998 |
| label__agreement_band__topic | 0\|borderline\|Jewish | expand_slang | 384 | 14133 | 4038 | 1.0002 | 0.9921 |
| label__agreement_band__topic | 0\|borderline\|Jewish | keep_hashtag_content | 384 | 14121 | 4057 | 0.9994 | 0.9958 |
| label__agreement_band__topic | 0\|borderline\|Jewish | remove_hashtag | 384 | 13632 | 3843 | 0.9648 | 0.9454 |
| label__agreement_band__topic | 0\|borderline\|Jewish | remove_url | 384 | 14126 | 4063 | 0.9997 | 0.9995 |
| label__agreement_band__topic | 0\|borderline\|Jewish | remove_mention | 384 | 14051 | 4020 | 0.9944 | 0.9889 |
| label__agreement_band__topic | 0\|borderline\|Jewish | remove_punctuation | 384 | 14130 | 4065 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish | remove_emoji | 384 | 14063 | 4043 | 0.9953 | 0.9902 |
| label__agreement_band__topic | 0\|borderline\|Jewish | full_normalize | 384 | 14237 | 4031 | 1.0076 | 0.9717 |
| label__agreement_band__topic | 0\|borderline\|Jewish | existing_cleaner | 384 | 13550 | 3791 | 0.9590 | 0.9326 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | raw | 2 | 82 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | lowercase | 2 | 82 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | leet_decode | 2 | 82 | 69 | 1.0000 | 0.9710 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | collapse_repetition | 2 | 82 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | expand_emoji | 2 | 83 | 70 | 1.0122 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | expand_slang | 2 | 82 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | keep_hashtag_content | 2 | 82 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | remove_hashtag | 2 | 59 | 49 | 0.7195 | 0.7101 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | remove_url | 2 | 82 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | remove_mention | 2 | 82 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | remove_punctuation | 2 | 82 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | remove_emoji | 2 | 82 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | full_normalize | 2 | 83 | 70 | 1.0122 | 0.9710 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Disabilitas | existing_cleaner | 2 | 59 | 49 | 0.7195 | 0.7101 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | raw | 9 | 669 | 292 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | lowercase | 9 | 669 | 292 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | leet_decode | 9 | 669 | 294 | 1.0000 | 0.9932 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | collapse_repetition | 9 | 669 | 292 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | expand_emoji | 9 | 669 | 292 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | expand_slang | 9 | 669 | 290 | 1.0000 | 0.9897 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | keep_hashtag_content | 9 | 668 | 291 | 0.9985 | 0.9932 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | remove_hashtag | 9 | 645 | 280 | 0.9641 | 0.9589 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | remove_url | 9 | 641 | 289 | 0.9581 | 0.9897 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | remove_mention | 9 | 663 | 291 | 0.9910 | 0.9966 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | remove_punctuation | 9 | 669 | 292 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | remove_emoji | 9 | 669 | 292 | 1.0000 | 0.9966 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | full_normalize | 9 | 669 | 292 | 1.0000 | 0.9829 |
| label__agreement_band__topic | 0\|borderline\|Jewish, Rohingya | existing_cleaner | 9 | 611 | 275 | 0.9133 | 0.9418 |
| label__agreement_band__topic | 0\|borderline\|Kristen | raw | 52 | 6508 | 1690 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen | lowercase | 52 | 6508 | 1690 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen | leet_decode | 52 | 6508 | 1692 | 1.0000 | 0.9899 |
| label__agreement_band__topic | 0\|borderline\|Kristen | collapse_repetition | 52 | 6508 | 1689 | 1.0000 | 0.9982 |
| label__agreement_band__topic | 0\|borderline\|Kristen | expand_emoji | 52 | 6524 | 1690 | 1.0025 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen | expand_slang | 52 | 6515 | 1685 | 1.0011 | 0.9941 |
| label__agreement_band__topic | 0\|borderline\|Kristen | keep_hashtag_content | 52 | 6508 | 1690 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen | remove_hashtag | 52 | 6307 | 1584 | 0.9691 | 0.9373 |
| label__agreement_band__topic | 0\|borderline\|Kristen | remove_url | 52 | 6493 | 1683 | 0.9977 | 0.9959 |
| label__agreement_band__topic | 0\|borderline\|Kristen | remove_mention | 52 | 6494 | 1682 | 0.9978 | 0.9953 |
| label__agreement_band__topic | 0\|borderline\|Kristen | remove_punctuation | 52 | 6508 | 1690 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen | remove_emoji | 52 | 6506 | 1688 | 0.9997 | 0.9982 |
| label__agreement_band__topic | 0\|borderline\|Kristen | full_normalize | 52 | 6524 | 1684 | 1.0025 | 0.9805 |
| label__agreement_band__topic | 0\|borderline\|Kristen | existing_cleaner | 52 | 6278 | 1568 | 0.9647 | 0.9278 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | raw | 15 | 1091 | 470 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | lowercase | 15 | 1091 | 470 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | leet_decode | 15 | 1091 | 470 | 1.0000 | 0.9957 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | collapse_repetition | 15 | 1091 | 470 | 1.0000 | 0.9979 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | expand_emoji | 15 | 1091 | 470 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | expand_slang | 15 | 1091 | 469 | 1.0000 | 0.9957 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | keep_hashtag_content | 15 | 1091 | 470 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | remove_hashtag | 15 | 1081 | 464 | 0.9908 | 0.9872 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | remove_url | 15 | 1088 | 469 | 0.9973 | 0.9979 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | remove_mention | 15 | 1091 | 470 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | remove_punctuation | 15 | 1091 | 470 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | remove_emoji | 15 | 1087 | 468 | 0.9963 | 0.9957 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | full_normalize | 15 | 1091 | 468 | 1.0000 | 0.9872 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Jewish | existing_cleaner | 15 | 1078 | 463 | 0.9881 | 0.9851 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | raw | 2 | 562 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | lowercase | 2 | 562 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | leet_decode | 2 | 562 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | collapse_repetition | 2 | 562 | 173 | 1.0000 | 0.9884 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | expand_emoji | 2 | 562 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | expand_slang | 2 | 562 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | keep_hashtag_content | 2 | 562 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | remove_hashtag | 2 | 542 | 163 | 0.9644 | 0.9422 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | remove_url | 2 | 562 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | remove_mention | 2 | 562 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | remove_punctuation | 2 | 562 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | remove_emoji | 2 | 562 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | full_normalize | 2 | 562 | 173 | 1.0000 | 0.9884 |
| label__agreement_band__topic | 0\|borderline\|Kristen, Rohingya | existing_cleaner | 2 | 542 | 163 | 0.9644 | 0.9422 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | raw | 83 | 2805 | 1418 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | lowercase | 83 | 2805 | 1418 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | leet_decode | 83 | 2805 | 1418 | 1.0000 | 0.9795 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | collapse_repetition | 83 | 2805 | 1418 | 1.0000 | 0.9979 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | expand_emoji | 83 | 2843 | 1429 | 1.0135 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | expand_slang | 83 | 2805 | 1404 | 1.0000 | 0.9866 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | keep_hashtag_content | 83 | 2805 | 1418 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | remove_hashtag | 83 | 2682 | 1310 | 0.9561 | 0.9238 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | remove_url | 83 | 2791 | 1409 | 0.9950 | 0.9937 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | remove_mention | 83 | 2798 | 1413 | 0.9975 | 0.9965 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | remove_punctuation | 83 | 2805 | 1418 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | remove_emoji | 83 | 2794 | 1410 | 0.9961 | 0.9922 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | full_normalize | 83 | 2839 | 1410 | 1.0121 | 0.9577 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+ | existing_cleaner | 83 | 2661 | 1296 | 0.9487 | 0.9140 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | raw | 2 | 50 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | lowercase | 2 | 50 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | leet_decode | 2 | 50 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | collapse_repetition | 2 | 50 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | expand_emoji | 2 | 50 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | expand_slang | 2 | 51 | 46 | 1.0200 | 0.9778 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | keep_hashtag_content | 2 | 50 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | remove_hashtag | 2 | 47 | 42 | 0.9400 | 0.9333 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | remove_url | 2 | 50 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | remove_mention | 2 | 50 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | remove_punctuation | 2 | 50 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | remove_emoji | 2 | 50 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | full_normalize | 2 | 51 | 46 | 1.0200 | 0.9778 |
| label__agreement_band__topic | 0\|borderline\|LGBTQ+, Jewish | existing_cleaner | 2 | 47 | 42 | 0.9400 | 0.9333 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | raw | 18 | 1421 | 558 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | lowercase | 18 | 1421 | 558 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | leet_decode | 18 | 1420 | 557 | 0.9993 | 0.9892 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | collapse_repetition | 18 | 1421 | 558 | 1.0000 | 0.9982 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | expand_emoji | 18 | 1422 | 559 | 1.0007 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | expand_slang | 18 | 1421 | 555 | 1.0000 | 0.9910 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | keep_hashtag_content | 18 | 1421 | 558 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | remove_hashtag | 18 | 1393 | 544 | 0.9803 | 0.9749 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | remove_url | 18 | 1382 | 547 | 0.9726 | 0.9803 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | remove_mention | 18 | 1412 | 551 | 0.9937 | 0.9875 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | remove_punctuation | 18 | 1421 | 558 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | remove_emoji | 18 | 1421 | 558 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | full_normalize | 18 | 1421 | 555 | 1.0000 | 0.9785 |
| label__agreement_band__topic | 0\|borderline\|Rohingya | existing_cleaner | 18 | 1346 | 525 | 0.9472 | 0.9409 |
| label__agreement_band__topic | 0\|borderline\|Syiah | raw | 17 | 2247 | 814 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah | lowercase | 17 | 2247 | 814 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah | leet_decode | 17 | 2247 | 815 | 1.0000 | 0.9975 |
| label__agreement_band__topic | 0\|borderline\|Syiah | collapse_repetition | 17 | 2247 | 814 | 1.0000 | 0.9988 |
| label__agreement_band__topic | 0\|borderline\|Syiah | expand_emoji | 17 | 2249 | 815 | 1.0009 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah | expand_slang | 17 | 2247 | 810 | 1.0000 | 0.9914 |
| label__agreement_band__topic | 0\|borderline\|Syiah | keep_hashtag_content | 17 | 2247 | 814 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah | remove_hashtag | 17 | 2223 | 807 | 0.9893 | 0.9914 |
| label__agreement_band__topic | 0\|borderline\|Syiah | remove_url | 17 | 2247 | 814 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah | remove_mention | 17 | 2244 | 813 | 0.9987 | 0.9988 |
| label__agreement_band__topic | 0\|borderline\|Syiah | remove_punctuation | 17 | 2247 | 814 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah | remove_emoji | 17 | 2134 | 751 | 0.9497 | 0.9079 |
| label__agreement_band__topic | 0\|borderline\|Syiah | full_normalize | 17 | 2249 | 811 | 1.0009 | 0.9865 |
| label__agreement_band__topic | 0\|borderline\|Syiah | existing_cleaner | 17 | 2220 | 806 | 0.9880 | 0.9902 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | raw | 2 | 365 | 248 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | lowercase | 2 | 365 | 248 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | leet_decode | 2 | 343 | 237 | 0.9397 | 0.9435 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | collapse_repetition | 2 | 365 | 247 | 1.0000 | 0.9960 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | expand_emoji | 2 | 365 | 248 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | expand_slang | 2 | 365 | 248 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | keep_hashtag_content | 2 | 365 | 248 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | remove_hashtag | 2 | 363 | 246 | 0.9945 | 0.9919 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | remove_url | 2 | 317 | 225 | 0.8685 | 0.9073 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | remove_mention | 2 | 365 | 248 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | remove_punctuation | 2 | 365 | 248 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | remove_emoji | 2 | 352 | 235 | 0.9644 | 0.9395 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | full_normalize | 2 | 343 | 235 | 0.9397 | 0.9355 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah | existing_cleaner | 2 | 315 | 223 | 0.8630 | 0.8992 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | raw | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | lowercase | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | leet_decode | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | collapse_repetition | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | expand_emoji | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | expand_slang | 1 | 292 | 148 | 1.0000 | 0.9933 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | keep_hashtag_content | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | remove_hashtag | 1 | 261 | 134 | 0.8938 | 0.8993 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | remove_url | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | remove_mention | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | remove_punctuation | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | remove_emoji | 1 | 292 | 148 | 1.0000 | 0.9799 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | full_normalize | 1 | 292 | 147 | 1.0000 | 0.9799 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Ahmadiyah, Jewish | existing_cleaner | 1 | 261 | 134 | 0.8938 | 0.8993 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | raw | 3 | 438 | 264 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | lowercase | 3 | 438 | 264 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | leet_decode | 3 | 438 | 264 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | collapse_repetition | 3 | 438 | 264 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | expand_emoji | 3 | 441 | 265 | 1.0068 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | expand_slang | 3 | 438 | 263 | 1.0000 | 0.9924 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | keep_hashtag_content | 3 | 438 | 264 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | remove_hashtag | 3 | 438 | 264 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | remove_url | 3 | 438 | 264 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | remove_mention | 3 | 438 | 264 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | remove_punctuation | 3 | 438 | 264 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | remove_emoji | 3 | 430 | 257 | 0.9817 | 0.9659 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | full_normalize | 3 | 440 | 263 | 1.0046 | 0.9886 |
| label__agreement_band__topic | 0\|borderline\|Syiah, Jewish | existing_cleaner | 3 | 438 | 264 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | raw | 1 | 280 | 181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | lowercase | 1 | 280 | 181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | leet_decode | 1 | 280 | 181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | collapse_repetition | 1 | 280 | 181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | expand_emoji | 1 | 280 | 181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | expand_slang | 1 | 280 | 180 | 1.0000 | 0.9945 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | keep_hashtag_content | 1 | 280 | 181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | remove_hashtag | 1 | 279 | 180 | 0.9964 | 0.9945 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | remove_url | 1 | 280 | 181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | remove_mention | 1 | 280 | 181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | remove_punctuation | 1 | 280 | 181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | remove_emoji | 1 | 259 | 164 | 0.9250 | 0.9006 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | full_normalize | 1 | 280 | 180 | 1.0000 | 0.9945 |
| label__agreement_band__topic | 0\|borderline\|Syiah, LGBTQ+, Jewish | existing_cleaner | 1 | 279 | 180 | 0.9964 | 0.9945 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | raw | 97 | 3670 | 1789 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | lowercase | 97 | 3670 | 1789 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | leet_decode | 97 | 3669 | 1791 | 0.9997 | 0.9866 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | collapse_repetition | 97 | 3670 | 1788 | 1.0000 | 0.9972 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | expand_emoji | 97 | 3687 | 1796 | 1.0046 | 0.9994 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | expand_slang | 97 | 3673 | 1775 | 1.0008 | 0.9888 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | keep_hashtag_content | 97 | 3670 | 1789 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | remove_hashtag | 97 | 3571 | 1719 | 0.9730 | 0.9609 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | remove_url | 97 | 3670 | 1789 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | remove_mention | 97 | 3658 | 1782 | 0.9967 | 0.9961 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | remove_punctuation | 97 | 3670 | 1789 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | remove_emoji | 97 | 3661 | 1783 | 0.9975 | 0.9950 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | full_normalize | 97 | 3689 | 1774 | 1.0052 | 0.9659 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa | existing_cleaner | 97 | 3559 | 1710 | 0.9698 | 0.9558 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | raw | 4 | 594 | 201 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | lowercase | 4 | 594 | 201 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | leet_decode | 4 | 594 | 201 | 1.0000 | 0.9950 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | collapse_repetition | 4 | 594 | 201 | 1.0000 | 0.9950 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | expand_emoji | 4 | 626 | 207 | 1.0539 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | expand_slang | 4 | 594 | 198 | 1.0000 | 0.9602 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | keep_hashtag_content | 4 | 594 | 201 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | remove_hashtag | 4 | 576 | 194 | 0.9697 | 0.9652 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | remove_url | 4 | 594 | 201 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | remove_mention | 4 | 594 | 201 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | remove_punctuation | 4 | 594 | 201 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | remove_emoji | 4 | 594 | 201 | 1.0000 | 0.9751 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | full_normalize | 4 | 626 | 203 | 1.0539 | 0.9453 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Disabilitas | existing_cleaner | 4 | 576 | 194 | 0.9697 | 0.9652 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | raw | 3 | 78 | 57 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | lowercase | 3 | 78 | 57 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | leet_decode | 3 | 78 | 57 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | collapse_repetition | 3 | 78 | 57 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | expand_emoji | 3 | 78 | 57 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | expand_slang | 3 | 78 | 57 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | keep_hashtag_content | 3 | 78 | 57 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | remove_hashtag | 3 | 73 | 56 | 0.9359 | 0.9825 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | remove_url | 3 | 78 | 57 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | remove_mention | 3 | 78 | 57 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | remove_punctuation | 3 | 78 | 57 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | remove_emoji | 3 | 78 | 57 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | full_normalize | 3 | 78 | 57 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|Tionghoa, Jewish | existing_cleaner | 3 | 73 | 56 | 0.9359 | 0.9825 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | raw | 170 | 3933 | 1666 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | lowercase | 170 | 3933 | 1666 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | leet_decode | 170 | 3931 | 1664 | 0.9995 | 0.9892 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | collapse_repetition | 170 | 3933 | 1665 | 1.0000 | 0.9988 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | expand_emoji | 170 | 3953 | 1670 | 1.0051 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | expand_slang | 170 | 3939 | 1661 | 1.0015 | 0.9952 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | keep_hashtag_content | 170 | 3933 | 1666 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | remove_hashtag | 170 | 3804 | 1574 | 0.9672 | 0.9448 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | remove_url | 170 | 3933 | 1666 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | remove_mention | 170 | 3933 | 1666 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | remove_punctuation | 170 | 3933 | 1666 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | remove_emoji | 170 | 3929 | 1664 | 0.9990 | 0.9952 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | full_normalize | 170 | 3964 | 1654 | 1.0079 | 0.9772 |
| label__agreement_band__topic | 0\|borderline\|UNKNOWN | existing_cleaner | 170 | 3804 | 1574 | 0.9672 | 0.9448 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | raw | 93 | 8883 | 4486 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | lowercase | 93 | 8883 | 4486 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | leet_decode | 93 | 8879 | 4481 | 0.9995 | 0.9906 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | collapse_repetition | 93 | 8883 | 4485 | 1.0000 | 0.9989 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | expand_emoji | 93 | 8911 | 4494 | 1.0032 | 0.9996 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | expand_slang | 93 | 8883 | 4485 | 1.0000 | 0.9991 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | keep_hashtag_content | 93 | 8883 | 4486 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | remove_hashtag | 93 | 8870 | 4480 | 0.9985 | 0.9987 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | remove_url | 93 | 8701 | 4452 | 0.9795 | 0.9924 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | remove_mention | 93 | 8881 | 4485 | 0.9998 | 0.9998 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | remove_punctuation | 93 | 8883 | 4486 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | remove_emoji | 93 | 8681 | 4405 | 0.9773 | 0.9773 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | full_normalize | 93 | 8907 | 4482 | 1.0027 | 0.9866 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah | existing_cleaner | 93 | 8686 | 4445 | 0.9778 | 0.9909 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | raw | 1 | 608 | 546 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | lowercase | 1 | 608 | 546 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | leet_decode | 1 | 608 | 546 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | collapse_repetition | 1 | 608 | 546 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | expand_emoji | 1 | 608 | 546 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | expand_slang | 1 | 608 | 546 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | keep_hashtag_content | 1 | 608 | 546 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | remove_hashtag | 1 | 608 | 546 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | remove_url | 1 | 608 | 546 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | remove_mention | 1 | 608 | 546 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | remove_punctuation | 1 | 608 | 546 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | remove_emoji | 1 | 604 | 543 | 0.9934 | 0.9945 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | full_normalize | 1 | 608 | 546 | 1.0000 | 0.9963 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Jewish | existing_cleaner | 1 | 608 | 546 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | raw | 2 | 199 | 135 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | lowercase | 2 | 199 | 135 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | leet_decode | 2 | 199 | 135 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | collapse_repetition | 2 | 199 | 135 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | expand_emoji | 2 | 199 | 135 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | expand_slang | 2 | 199 | 134 | 1.0000 | 0.9926 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | keep_hashtag_content | 2 | 199 | 135 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | remove_hashtag | 2 | 198 | 134 | 0.9950 | 0.9926 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | remove_url | 2 | 199 | 135 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | remove_mention | 2 | 199 | 135 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | remove_punctuation | 2 | 199 | 135 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | remove_emoji | 2 | 199 | 135 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | full_normalize | 2 | 199 | 134 | 1.0000 | 0.9926 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Kristen | existing_cleaner | 2 | 198 | 134 | 0.9950 | 0.9926 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | raw | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | lowercase | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | leet_decode | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | collapse_repetition | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | expand_emoji | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | expand_slang | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | keep_hashtag_content | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | remove_hashtag | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | remove_url | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | remove_mention | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | remove_punctuation | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | remove_emoji | 2 | 236 | 110 | 0.9365 | 0.9402 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | full_normalize | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Ahmadiyah, Tionghoa | existing_cleaner | 2 | 252 | 117 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | raw | 5690 | 165113 | 26763 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | lowercase | 5690 | 165116 | 26764 | 1.0000 | 0.9999 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | leet_decode | 5690 | 165078 | 26724 | 0.9998 | 0.9724 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | collapse_repetition | 5690 | 165113 | 26549 | 1.0000 | 0.9773 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | expand_emoji | 5690 | 169044 | 26757 | 1.0238 | 0.9990 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | expand_slang | 5690 | 165194 | 26734 | 1.0005 | 0.9987 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | keep_hashtag_content | 5690 | 165027 | 26734 | 0.9995 | 0.9980 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | remove_hashtag | 5690 | 160276 | 24759 | 0.9707 | 0.9251 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | remove_url | 5690 | 164846 | 26716 | 0.9984 | 0.9982 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | remove_mention | 5690 | 164001 | 26230 | 0.9933 | 0.9801 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | remove_punctuation | 5690 | 165113 | 26763 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | remove_emoji | 5690 | 164368 | 26374 | 0.9955 | 0.9814 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | full_normalize | 5690 | 168720 | 26426 | 1.0218 | 0.9464 |
| label__agreement_band__topic | 0\|unanimous\|Disabilitas | existing_cleaner | 5690 | 158900 | 24140 | 0.9624 | 0.9018 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | raw | 6697 | 276788 | 27329 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | lowercase | 6697 | 276788 | 27329 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | leet_decode | 6697 | 276735 | 27360 | 0.9998 | 0.9783 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | collapse_repetition | 6697 | 276788 | 27283 | 1.0000 | 0.9935 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | expand_emoji | 6697 | 277794 | 27333 | 1.0036 | 0.9997 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | expand_slang | 6697 | 276831 | 27290 | 1.0002 | 0.9984 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | keep_hashtag_content | 6697 | 276655 | 27300 | 0.9995 | 0.9980 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | remove_hashtag | 6697 | 266517 | 25331 | 0.9629 | 0.9269 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | remove_url | 6697 | 276170 | 27270 | 0.9978 | 0.9978 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | remove_mention | 6697 | 275455 | 26883 | 0.9952 | 0.9837 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | remove_punctuation | 6697 | 276788 | 27329 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | remove_emoji | 6697 | 275131 | 26784 | 0.9940 | 0.9733 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | full_normalize | 6697 | 277791 | 27231 | 1.0036 | 0.9703 |
| label__agreement_band__topic | 0\|unanimous\|Jewish | existing_cleaner | 6697 | 264566 | 24782 | 0.9558 | 0.9068 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | raw | 57 | 4084 | 1584 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | lowercase | 57 | 4084 | 1584 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | leet_decode | 57 | 4084 | 1584 | 1.0000 | 0.9975 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | collapse_repetition | 57 | 4084 | 1580 | 1.0000 | 0.9943 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | expand_emoji | 57 | 4106 | 1591 | 1.0054 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | expand_slang | 57 | 4088 | 1563 | 1.0010 | 0.9817 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | keep_hashtag_content | 57 | 4084 | 1584 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | remove_hashtag | 57 | 4006 | 1538 | 0.9809 | 0.9710 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | remove_url | 57 | 4081 | 1582 | 0.9993 | 0.9987 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | remove_mention | 57 | 4074 | 1576 | 0.9976 | 0.9949 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | remove_punctuation | 57 | 4084 | 1584 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | remove_emoji | 57 | 4074 | 1581 | 0.9976 | 0.9949 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | full_normalize | 57 | 4108 | 1563 | 1.0059 | 0.9697 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Disabilitas | existing_cleaner | 57 | 3993 | 1528 | 0.9777 | 0.9646 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | raw | 152 | 10658 | 2362 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | lowercase | 152 | 10658 | 2362 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | leet_decode | 152 | 10658 | 2366 | 1.0000 | 0.9945 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | collapse_repetition | 152 | 10658 | 2361 | 1.0000 | 0.9953 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | expand_emoji | 152 | 10695 | 2369 | 1.0035 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | expand_slang | 152 | 10660 | 2352 | 1.0002 | 0.9945 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | keep_hashtag_content | 152 | 10658 | 2362 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | remove_hashtag | 152 | 10255 | 2241 | 0.9622 | 0.9488 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | remove_url | 152 | 10618 | 2352 | 0.9962 | 0.9958 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | remove_mention | 152 | 10590 | 2339 | 0.9936 | 0.9903 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | remove_punctuation | 152 | 10658 | 2362 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | remove_emoji | 152 | 10644 | 2363 | 0.9987 | 0.9962 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | full_normalize | 152 | 10696 | 2360 | 1.0036 | 0.9839 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya | existing_cleaner | 152 | 10147 | 2207 | 0.9521 | 0.9344 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | raw | 1 | 226 | 128 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | lowercase | 1 | 226 | 128 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | leet_decode | 1 | 226 | 128 | 1.0000 | 0.9922 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | collapse_repetition | 1 | 226 | 128 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | expand_emoji | 1 | 226 | 128 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | expand_slang | 1 | 226 | 128 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | keep_hashtag_content | 1 | 226 | 128 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | remove_hashtag | 1 | 226 | 128 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | remove_url | 1 | 226 | 128 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | remove_mention | 1 | 226 | 128 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | remove_punctuation | 1 | 226 | 128 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | remove_emoji | 1 | 226 | 128 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | full_normalize | 1 | 226 | 128 | 1.0000 | 0.9922 |
| label__agreement_band__topic | 0\|unanimous\|Jewish, Rohingya, Disabilitas | existing_cleaner | 1 | 226 | 128 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | raw | 1199 | 94211 | 14263 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | lowercase | 1199 | 94220 | 14264 | 1.0001 | 0.9996 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | leet_decode | 1199 | 94200 | 14289 | 0.9999 | 0.9724 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | collapse_repetition | 1199 | 94211 | 14234 | 1.0000 | 0.9931 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | expand_emoji | 1199 | 94798 | 14266 | 1.0062 | 0.9996 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | expand_slang | 1199 | 94226 | 14233 | 1.0002 | 0.9970 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | keep_hashtag_content | 1199 | 94149 | 14234 | 0.9993 | 0.9965 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | remove_hashtag | 1199 | 89711 | 12815 | 0.9522 | 0.8985 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | remove_url | 1199 | 93407 | 14157 | 0.9915 | 0.9926 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | remove_mention | 1199 | 92959 | 13841 | 0.9867 | 0.9704 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | remove_punctuation | 1199 | 94211 | 14263 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | remove_emoji | 1199 | 93672 | 14154 | 0.9943 | 0.9852 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | full_normalize | 1199 | 94756 | 14206 | 1.0058 | 0.9608 |
| label__agreement_band__topic | 0\|unanimous\|Kristen | existing_cleaner | 1199 | 87664 | 12246 | 0.9305 | 0.8582 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | raw | 1 | 51 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | lowercase | 1 | 51 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | leet_decode | 1 | 51 | 40 | 1.0000 | 0.9750 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | collapse_repetition | 1 | 51 | 41 | 1.0000 | 0.9750 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | expand_emoji | 1 | 53 | 41 | 1.0392 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | expand_slang | 1 | 51 | 40 | 1.0000 | 0.9000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | keep_hashtag_content | 1 | 51 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | remove_hashtag | 1 | 51 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | remove_url | 1 | 47 | 36 | 0.9216 | 0.9000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | remove_mention | 1 | 51 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | remove_punctuation | 1 | 51 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | remove_emoji | 1 | 51 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | full_normalize | 1 | 53 | 41 | 1.0392 | 0.8250 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Disabilitas | existing_cleaner | 1 | 47 | 36 | 0.9216 | 0.9000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | raw | 107 | 6939 | 1980 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | lowercase | 107 | 6939 | 1980 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | leet_decode | 107 | 6939 | 1980 | 1.0000 | 0.9798 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | collapse_repetition | 107 | 6939 | 1979 | 1.0000 | 0.9980 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | expand_emoji | 107 | 6953 | 1985 | 1.0020 | 0.9990 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | expand_slang | 107 | 6939 | 1964 | 1.0000 | 0.9909 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | keep_hashtag_content | 107 | 6933 | 1975 | 0.9991 | 0.9970 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | remove_hashtag | 107 | 6755 | 1908 | 0.9735 | 0.9636 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | remove_url | 107 | 6861 | 1959 | 0.9888 | 0.9894 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | remove_mention | 107 | 6849 | 1905 | 0.9870 | 0.9621 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | remove_punctuation | 107 | 6939 | 1980 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | remove_emoji | 107 | 6906 | 1963 | 0.9952 | 0.9889 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | full_normalize | 107 | 6951 | 1963 | 1.0017 | 0.9662 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish | existing_cleaner | 107 | 6588 | 1808 | 0.9494 | 0.9131 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | raw | 1 | 286 | 171 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | lowercase | 1 | 286 | 171 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | leet_decode | 1 | 286 | 170 | 1.0000 | 0.9883 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | collapse_repetition | 1 | 286 | 171 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | expand_emoji | 1 | 286 | 171 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | expand_slang | 1 | 286 | 171 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | keep_hashtag_content | 1 | 286 | 171 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | remove_hashtag | 1 | 286 | 171 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | remove_url | 1 | 286 | 171 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | remove_mention | 1 | 286 | 171 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | remove_punctuation | 1 | 286 | 171 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | remove_emoji | 1 | 286 | 171 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | full_normalize | 1 | 286 | 170 | 1.0000 | 0.9883 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Disabilitas | existing_cleaner | 1 | 286 | 171 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | raw | 5 | 717 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | lowercase | 5 | 717 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | leet_decode | 5 | 717 | 364 | 1.0000 | 0.9973 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | collapse_repetition | 5 | 717 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | expand_emoji | 5 | 717 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | expand_slang | 5 | 717 | 364 | 1.0000 | 0.9973 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | keep_hashtag_content | 5 | 717 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | remove_hashtag | 5 | 681 | 338 | 0.9498 | 0.9286 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | remove_url | 5 | 717 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | remove_mention | 5 | 715 | 363 | 0.9972 | 0.9973 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | remove_punctuation | 5 | 717 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | remove_emoji | 5 | 704 | 357 | 0.9819 | 0.9698 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | full_normalize | 5 | 717 | 364 | 1.0000 | 0.9945 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Jewish, Rohingya | existing_cleaner | 5 | 679 | 336 | 0.9470 | 0.9231 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | raw | 7 | 730 | 342 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | lowercase | 7 | 730 | 342 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | leet_decode | 7 | 730 | 342 | 1.0000 | 0.9912 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | collapse_repetition | 7 | 730 | 342 | 1.0000 | 0.9942 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | expand_emoji | 7 | 731 | 343 | 1.0014 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | expand_slang | 7 | 730 | 341 | 1.0000 | 0.9971 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | keep_hashtag_content | 7 | 730 | 342 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | remove_hashtag | 7 | 730 | 342 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | remove_url | 7 | 700 | 333 | 0.9589 | 0.9737 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | remove_mention | 7 | 729 | 341 | 0.9986 | 0.9971 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | remove_punctuation | 7 | 730 | 342 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | remove_emoji | 7 | 730 | 342 | 1.0000 | 0.9971 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | full_normalize | 7 | 731 | 342 | 1.0014 | 0.9825 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+ | existing_cleaner | 7 | 699 | 332 | 0.9575 | 0.9708 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | raw | 1 | 408 | 127 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | lowercase | 1 | 408 | 127 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | leet_decode | 1 | 408 | 127 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | collapse_repetition | 1 | 408 | 127 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | expand_emoji | 1 | 408 | 127 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | expand_slang | 1 | 408 | 127 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | keep_hashtag_content | 1 | 408 | 127 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | remove_hashtag | 1 | 388 | 118 | 0.9510 | 0.9291 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | remove_url | 1 | 408 | 127 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | remove_mention | 1 | 408 | 127 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | remove_punctuation | 1 | 408 | 127 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | remove_emoji | 1 | 408 | 127 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | full_normalize | 1 | 408 | 127 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, LGBTQ+, Jewish, Rohingya | existing_cleaner | 1 | 388 | 118 | 0.9510 | 0.9291 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | raw | 2 | 699 | 301 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | lowercase | 2 | 699 | 301 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | leet_decode | 2 | 699 | 301 | 1.0000 | 0.9934 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | collapse_repetition | 2 | 699 | 301 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | expand_emoji | 2 | 699 | 301 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | expand_slang | 2 | 699 | 301 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | keep_hashtag_content | 2 | 699 | 301 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | remove_hashtag | 2 | 661 | 273 | 0.9456 | 0.9070 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | remove_url | 2 | 699 | 301 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | remove_mention | 2 | 697 | 300 | 0.9971 | 0.9967 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | remove_punctuation | 2 | 699 | 301 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | remove_emoji | 2 | 690 | 292 | 0.9871 | 0.9701 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | full_normalize | 2 | 699 | 301 | 1.0000 | 0.9934 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Rohingya | existing_cleaner | 2 | 659 | 271 | 0.9428 | 0.9003 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | raw | 8 | 446 | 281 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | lowercase | 8 | 446 | 281 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | leet_decode | 8 | 446 | 282 | 1.0000 | 0.9929 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | collapse_repetition | 8 | 446 | 281 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | expand_emoji | 8 | 452 | 284 | 1.0135 | 0.9929 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | expand_slang | 8 | 446 | 277 | 1.0000 | 0.9680 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | keep_hashtag_content | 8 | 446 | 281 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | remove_hashtag | 8 | 438 | 275 | 0.9821 | 0.9786 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | remove_url | 8 | 446 | 281 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | remove_mention | 8 | 424 | 265 | 0.9507 | 0.9431 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | remove_punctuation | 8 | 446 | 281 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | remove_emoji | 8 | 446 | 281 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | full_normalize | 8 | 453 | 279 | 1.0157 | 0.9431 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa | existing_cleaner | 8 | 416 | 259 | 0.9327 | 0.9217 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | raw | 2 | 269 | 174 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | lowercase | 2 | 269 | 174 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | leet_decode | 2 | 269 | 174 | 1.0000 | 0.9655 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | collapse_repetition | 2 | 269 | 174 | 1.0000 | 0.9943 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | expand_emoji | 2 | 269 | 174 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | expand_slang | 2 | 269 | 174 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | keep_hashtag_content | 2 | 269 | 174 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | remove_hashtag | 2 | 269 | 174 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | remove_url | 2 | 269 | 174 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | remove_mention | 2 | 269 | 174 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | remove_punctuation | 2 | 269 | 174 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | remove_emoji | 2 | 269 | 174 | 1.0000 | 0.9943 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | full_normalize | 2 | 269 | 174 | 1.0000 | 0.9598 |
| label__agreement_band__topic | 0\|unanimous\|Kristen, Tionghoa, Jewish | existing_cleaner | 2 | 269 | 174 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | raw | 494 | 21509 | 7774 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | lowercase | 494 | 21509 | 7774 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | leet_decode | 494 | 21509 | 7780 | 1.0000 | 0.9830 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | collapse_repetition | 494 | 21509 | 7767 | 1.0000 | 0.9956 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | expand_emoji | 494 | 21691 | 7789 | 1.0085 | 0.9995 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | expand_slang | 494 | 21512 | 7741 | 1.0001 | 0.9946 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | keep_hashtag_content | 494 | 21505 | 7774 | 0.9998 | 0.9997 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | remove_hashtag | 494 | 20972 | 7469 | 0.9750 | 0.9608 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | remove_url | 494 | 21298 | 7727 | 0.9902 | 0.9940 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | remove_mention | 494 | 21391 | 7678 | 0.9945 | 0.9877 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | remove_punctuation | 494 | 21509 | 7774 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | remove_emoji | 494 | 21219 | 7622 | 0.9865 | 0.9765 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | full_normalize | 494 | 21683 | 7738 | 1.0081 | 0.9709 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+ | existing_cleaner | 494 | 20643 | 7325 | 0.9597 | 0.9422 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | raw | 4 | 561 | 224 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | lowercase | 4 | 561 | 224 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | leet_decode | 4 | 529 | 208 | 0.9430 | 0.9241 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | collapse_repetition | 4 | 561 | 224 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | expand_emoji | 4 | 565 | 226 | 1.0071 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | expand_slang | 4 | 561 | 222 | 1.0000 | 0.9911 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | keep_hashtag_content | 4 | 529 | 208 | 0.9430 | 0.9241 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | remove_hashtag | 4 | 525 | 207 | 0.9358 | 0.9241 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | remove_url | 4 | 561 | 224 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | remove_mention | 4 | 561 | 224 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | remove_punctuation | 4 | 561 | 224 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | remove_emoji | 4 | 561 | 224 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | full_normalize | 4 | 532 | 208 | 0.9483 | 0.9152 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Disabilitas | existing_cleaner | 4 | 525 | 207 | 0.9358 | 0.9241 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | raw | 3 | 75 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | lowercase | 3 | 75 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | leet_decode | 3 | 75 | 40 | 1.0000 | 0.9000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | collapse_repetition | 3 | 75 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | expand_emoji | 3 | 75 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | expand_slang | 3 | 75 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | keep_hashtag_content | 3 | 75 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | remove_hashtag | 3 | 65 | 35 | 0.8667 | 0.8750 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | remove_url | 3 | 67 | 35 | 0.8933 | 0.8750 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | remove_mention | 3 | 74 | 40 | 0.9867 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | remove_punctuation | 3 | 75 | 40 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | remove_emoji | 3 | 69 | 37 | 0.9200 | 0.8750 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | full_normalize | 3 | 75 | 40 | 1.0000 | 0.8750 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Jewish | existing_cleaner | 3 | 56 | 30 | 0.7467 | 0.7500 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | raw | 2 | 66 | 32 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | lowercase | 2 | 66 | 32 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | leet_decode | 2 | 66 | 32 | 1.0000 | 0.9062 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | collapse_repetition | 2 | 66 | 32 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | expand_emoji | 2 | 66 | 32 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | expand_slang | 2 | 66 | 32 | 1.0000 | 0.9688 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | keep_hashtag_content | 2 | 66 | 32 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | remove_hashtag | 2 | 62 | 30 | 0.9394 | 0.9375 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | remove_url | 2 | 58 | 27 | 0.8788 | 0.8438 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | remove_mention | 2 | 66 | 32 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | remove_punctuation | 2 | 66 | 32 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | remove_emoji | 2 | 66 | 32 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | full_normalize | 2 | 66 | 32 | 1.0000 | 0.8750 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Rohingya | existing_cleaner | 2 | 54 | 25 | 0.8182 | 0.7812 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | raw | 3 | 52 | 50 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | lowercase | 3 | 52 | 50 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | leet_decode | 3 | 52 | 50 | 1.0000 | 0.9800 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | collapse_repetition | 3 | 52 | 50 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | expand_emoji | 3 | 52 | 50 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | expand_slang | 3 | 52 | 50 | 1.0000 | 0.9800 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | keep_hashtag_content | 3 | 52 | 50 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | remove_hashtag | 3 | 44 | 43 | 0.8462 | 0.8600 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | remove_url | 3 | 52 | 50 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | remove_mention | 3 | 52 | 50 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | remove_punctuation | 3 | 52 | 50 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | remove_emoji | 3 | 52 | 50 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | full_normalize | 3 | 52 | 49 | 1.0000 | 0.9400 |
| label__agreement_band__topic | 0\|unanimous\|LGBTQ+, Tionghoa | existing_cleaner | 3 | 44 | 43 | 0.8462 | 0.8600 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | raw | 1361 | 149067 | 11545 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | lowercase | 1361 | 149067 | 11545 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | leet_decode | 1361 | 149045 | 11557 | 0.9999 | 0.9584 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | collapse_repetition | 1361 | 149067 | 11531 | 1.0000 | 0.9955 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | expand_emoji | 1361 | 149418 | 11557 | 1.0024 | 0.9997 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | expand_slang | 1361 | 149079 | 11515 | 1.0001 | 0.9966 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | keep_hashtag_content | 1361 | 149027 | 11526 | 0.9997 | 0.9981 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | remove_hashtag | 1361 | 145768 | 10768 | 0.9779 | 0.9327 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | remove_url | 1361 | 145536 | 11202 | 0.9763 | 0.9703 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | remove_mention | 1361 | 147969 | 11099 | 0.9926 | 0.9614 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | remove_punctuation | 1361 | 149067 | 11545 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | remove_emoji | 1361 | 148560 | 11541 | 0.9966 | 0.9900 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | full_normalize | 1361 | 149407 | 11506 | 1.0023 | 0.9491 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya | existing_cleaner | 1361 | 141148 | 9947 | 0.9469 | 0.8616 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | raw | 2 | 47 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | lowercase | 2 | 47 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | leet_decode | 2 | 47 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | collapse_repetition | 2 | 47 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | expand_emoji | 2 | 47 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | expand_slang | 2 | 47 | 46 | 1.0000 | 0.9778 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | keep_hashtag_content | 2 | 47 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | remove_hashtag | 2 | 47 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | remove_url | 2 | 47 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | remove_mention | 2 | 47 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | remove_punctuation | 2 | 47 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | remove_emoji | 2 | 47 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | full_normalize | 2 | 47 | 45 | 1.0000 | 0.9333 |
| label__agreement_band__topic | 0\|unanimous\|Rohingya, Disabilitas | existing_cleaner | 2 | 47 | 45 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | raw | 343 | 40999 | 10989 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | lowercase | 343 | 40999 | 10989 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | leet_decode | 343 | 40999 | 10997 | 1.0000 | 0.9860 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | collapse_repetition | 343 | 40999 | 10980 | 1.0000 | 0.9967 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | expand_emoji | 343 | 41179 | 11005 | 1.0044 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | expand_slang | 343 | 41014 | 10966 | 1.0004 | 0.9975 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | keep_hashtag_content | 343 | 40996 | 10991 | 0.9999 | 0.9999 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | remove_hashtag | 343 | 40370 | 10751 | 0.9847 | 0.9783 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | remove_url | 343 | 40365 | 10910 | 0.9845 | 0.9928 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | remove_mention | 343 | 40769 | 10886 | 0.9944 | 0.9906 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | remove_punctuation | 343 | 40999 | 10989 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | remove_emoji | 343 | 40717 | 10808 | 0.9931 | 0.9802 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | full_normalize | 343 | 41200 | 10964 | 1.0049 | 0.9792 |
| label__agreement_band__topic | 0\|unanimous\|Syiah | existing_cleaner | 343 | 39507 | 10566 | 0.9636 | 0.9615 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | raw | 4 | 684 | 387 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | lowercase | 4 | 684 | 387 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | leet_decode | 4 | 663 | 377 | 0.9693 | 0.9587 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | collapse_repetition | 4 | 684 | 386 | 1.0000 | 0.9974 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | expand_emoji | 4 | 684 | 387 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | expand_slang | 4 | 684 | 387 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | keep_hashtag_content | 4 | 684 | 387 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | remove_hashtag | 4 | 682 | 385 | 0.9971 | 0.9948 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | remove_url | 4 | 636 | 364 | 0.9298 | 0.9406 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | remove_mention | 4 | 682 | 386 | 0.9971 | 0.9974 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | remove_punctuation | 4 | 684 | 387 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | remove_emoji | 4 | 667 | 375 | 0.9751 | 0.9612 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | full_normalize | 4 | 663 | 375 | 0.9693 | 0.9535 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Ahmadiyah | existing_cleaner | 4 | 632 | 361 | 0.9240 | 0.9328 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | raw | 2 | 334 | 190 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | lowercase | 2 | 334 | 190 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | leet_decode | 2 | 334 | 189 | 1.0000 | 0.9895 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | collapse_repetition | 2 | 334 | 190 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | expand_emoji | 2 | 334 | 190 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | expand_slang | 2 | 334 | 189 | 1.0000 | 0.9895 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | keep_hashtag_content | 2 | 334 | 190 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | remove_hashtag | 2 | 334 | 190 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | remove_url | 2 | 334 | 190 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | remove_mention | 2 | 334 | 190 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | remove_punctuation | 2 | 334 | 190 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | remove_emoji | 2 | 330 | 189 | 0.9880 | 0.9842 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | full_normalize | 2 | 334 | 188 | 1.0000 | 0.9789 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Disabilitas | existing_cleaner | 2 | 334 | 190 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | raw | 33 | 1977 | 1062 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | lowercase | 33 | 1977 | 1062 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | leet_decode | 33 | 1978 | 1062 | 1.0005 | 0.9831 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | collapse_repetition | 33 | 1977 | 1062 | 1.0000 | 0.9972 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | expand_emoji | 33 | 1982 | 1065 | 1.0025 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | expand_slang | 33 | 1977 | 1053 | 1.0000 | 0.9896 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | keep_hashtag_content | 33 | 1976 | 1062 | 0.9995 | 0.9991 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | remove_hashtag | 33 | 1912 | 1021 | 0.9671 | 0.9614 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | remove_url | 33 | 1969 | 1058 | 0.9960 | 0.9962 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | remove_mention | 33 | 1960 | 1047 | 0.9914 | 0.9859 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | remove_punctuation | 33 | 1977 | 1062 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | remove_emoji | 33 | 1800 | 983 | 0.9105 | 0.9181 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | full_normalize | 33 | 1983 | 1053 | 1.0030 | 0.9652 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Jewish | existing_cleaner | 33 | 1887 | 1002 | 0.9545 | 0.9435 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | raw | 3 | 397 | 225 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | lowercase | 3 | 397 | 225 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | leet_decode | 3 | 397 | 225 | 1.0000 | 0.9956 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | collapse_repetition | 3 | 397 | 225 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | expand_emoji | 3 | 397 | 225 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | expand_slang | 3 | 397 | 225 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | keep_hashtag_content | 3 | 397 | 225 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | remove_hashtag | 3 | 367 | 200 | 0.9244 | 0.8889 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | remove_url | 3 | 397 | 225 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | remove_mention | 3 | 397 | 225 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | remove_punctuation | 3 | 397 | 225 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | remove_emoji | 3 | 397 | 225 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | full_normalize | 3 | 397 | 225 | 1.0000 | 0.9956 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen | existing_cleaner | 3 | 367 | 200 | 0.9244 | 0.8889 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | raw | 2 | 386 | 317 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | lowercase | 2 | 386 | 317 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | leet_decode | 2 | 386 | 317 | 1.0000 | 0.9811 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | collapse_repetition | 2 | 386 | 317 | 1.0000 | 0.9968 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | expand_emoji | 2 | 386 | 317 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | expand_slang | 2 | 386 | 316 | 1.0000 | 0.9968 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | keep_hashtag_content | 2 | 386 | 317 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | remove_hashtag | 2 | 386 | 317 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | remove_url | 2 | 386 | 317 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | remove_mention | 2 | 386 | 317 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | remove_punctuation | 2 | 386 | 317 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | remove_emoji | 2 | 364 | 297 | 0.9430 | 0.9369 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | full_normalize | 2 | 386 | 316 | 1.0000 | 0.9779 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Kristen, Jewish | existing_cleaner | 2 | 386 | 317 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | raw | 30 | 6193 | 566 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | lowercase | 30 | 6193 | 566 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | leet_decode | 30 | 6193 | 569 | 1.0000 | 0.9929 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | collapse_repetition | 30 | 6193 | 566 | 1.0000 | 0.9982 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | expand_emoji | 30 | 6193 | 566 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | expand_slang | 30 | 6193 | 566 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | keep_hashtag_content | 30 | 6193 | 566 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | remove_hashtag | 30 | 6165 | 556 | 0.9955 | 0.9823 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | remove_url | 30 | 6087 | 546 | 0.9829 | 0.9647 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | remove_mention | 30 | 6183 | 564 | 0.9984 | 0.9965 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | remove_punctuation | 30 | 6193 | 566 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | remove_emoji | 30 | 6191 | 566 | 0.9997 | 0.9947 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | full_normalize | 30 | 6193 | 570 | 1.0000 | 0.9894 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Rohingya | existing_cleaner | 30 | 6049 | 533 | 0.9767 | 0.9417 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | raw | 2 | 746 | 659 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | lowercase | 2 | 746 | 659 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | leet_decode | 2 | 746 | 659 | 1.0000 | 0.9985 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | collapse_repetition | 2 | 746 | 659 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | expand_emoji | 2 | 747 | 660 | 1.0013 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | expand_slang | 2 | 746 | 659 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | keep_hashtag_content | 2 | 746 | 659 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | remove_hashtag | 2 | 746 | 659 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | remove_url | 2 | 746 | 659 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | remove_mention | 2 | 746 | 659 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | remove_punctuation | 2 | 746 | 659 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | remove_emoji | 2 | 743 | 656 | 0.9960 | 0.9924 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | full_normalize | 2 | 747 | 660 | 1.0013 | 0.9985 |
| label__agreement_band__topic | 0\|unanimous\|Syiah, Tionghoa | existing_cleaner | 2 | 746 | 659 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | raw | 4947 | 211298 | 24740 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | lowercase | 4947 | 211302 | 24741 | 1.0000 | 0.9999 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | leet_decode | 4947 | 211232 | 24804 | 0.9997 | 0.9473 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | collapse_repetition | 4947 | 211298 | 24641 | 1.0000 | 0.9876 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | expand_emoji | 4947 | 213496 | 24750 | 1.0104 | 0.9992 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | expand_slang | 4947 | 211322 | 24715 | 1.0001 | 0.9987 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | keep_hashtag_content | 4947 | 211121 | 24724 | 0.9992 | 0.9979 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | remove_hashtag | 4947 | 195438 | 21747 | 0.9249 | 0.8790 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | remove_url | 4947 | 209877 | 24520 | 0.9933 | 0.9911 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | remove_mention | 4947 | 210248 | 24360 | 0.9950 | 0.9846 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | remove_punctuation | 4947 | 211298 | 24740 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | remove_emoji | 4947 | 209906 | 24207 | 0.9934 | 0.9736 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | full_normalize | 4947 | 213327 | 24638 | 1.0096 | 0.9324 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa | existing_cleaner | 4947 | 192973 | 21091 | 0.9133 | 0.8523 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | raw | 22 | 1286 | 689 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | lowercase | 22 | 1286 | 689 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | leet_decode | 22 | 1286 | 689 | 1.0000 | 0.9884 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | collapse_repetition | 22 | 1286 | 689 | 1.0000 | 0.9971 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | expand_emoji | 22 | 1302 | 696 | 1.0124 | 0.9985 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | expand_slang | 22 | 1289 | 688 | 1.0023 | 0.9927 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | keep_hashtag_content | 22 | 1279 | 682 | 0.9946 | 0.9797 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | remove_hashtag | 22 | 1241 | 647 | 0.9650 | 0.9390 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | remove_url | 22 | 1282 | 685 | 0.9969 | 0.9942 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | remove_mention | 22 | 1278 | 685 | 0.9938 | 0.9942 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | remove_punctuation | 22 | 1286 | 689 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | remove_emoji | 22 | 1281 | 685 | 0.9961 | 0.9898 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | full_normalize | 22 | 1302 | 691 | 1.0124 | 0.9710 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Disabilitas | existing_cleaner | 22 | 1229 | 639 | 0.9557 | 0.9274 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | raw | 76 | 5488 | 1560 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | lowercase | 76 | 5488 | 1560 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | leet_decode | 76 | 5488 | 1560 | 1.0000 | 0.9936 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | collapse_repetition | 76 | 5488 | 1560 | 1.0000 | 0.9994 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | expand_emoji | 76 | 5498 | 1562 | 1.0018 | 0.9994 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | expand_slang | 76 | 5490 | 1553 | 1.0004 | 0.9936 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | keep_hashtag_content | 76 | 5488 | 1560 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | remove_hashtag | 76 | 5333 | 1496 | 0.9718 | 0.9590 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | remove_url | 76 | 5488 | 1560 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | remove_mention | 76 | 5476 | 1554 | 0.9978 | 0.9962 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | remove_punctuation | 76 | 5488 | 1560 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | remove_emoji | 76 | 5440 | 1551 | 0.9913 | 0.9872 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | full_normalize | 76 | 5496 | 1551 | 1.0015 | 0.9840 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish | existing_cleaner | 76 | 5321 | 1489 | 0.9696 | 0.9545 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | raw | 1 | 378 | 122 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | lowercase | 1 | 378 | 122 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | leet_decode | 1 | 378 | 122 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | collapse_repetition | 1 | 378 | 122 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | expand_emoji | 1 | 378 | 122 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | expand_slang | 1 | 378 | 121 | 1.0000 | 0.9836 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | keep_hashtag_content | 1 | 378 | 122 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | remove_hashtag | 1 | 378 | 122 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | remove_url | 1 | 378 | 122 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | remove_mention | 1 | 378 | 122 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | remove_punctuation | 1 | 378 | 122 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | remove_emoji | 1 | 378 | 122 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | full_normalize | 1 | 378 | 121 | 1.0000 | 0.9836 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Disabilitas | existing_cleaner | 1 | 378 | 122 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | raw | 1 | 312 | 170 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | lowercase | 1 | 312 | 170 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | leet_decode | 1 | 312 | 170 | 1.0000 | 0.9765 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | collapse_repetition | 1 | 312 | 170 | 1.0000 | 0.9941 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | expand_emoji | 1 | 312 | 170 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | expand_slang | 1 | 312 | 170 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | keep_hashtag_content | 1 | 312 | 170 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | remove_hashtag | 1 | 312 | 170 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | remove_url | 1 | 312 | 170 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | remove_mention | 1 | 312 | 170 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | remove_punctuation | 1 | 312 | 170 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | remove_emoji | 1 | 312 | 170 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | full_normalize | 1 | 312 | 170 | 1.0000 | 0.9706 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Jewish, Rohingya | existing_cleaner | 1 | 312 | 170 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | raw | 5 | 162 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | lowercase | 5 | 162 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | leet_decode | 5 | 162 | 132 | 1.0000 | 0.9924 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | collapse_repetition | 5 | 162 | 132 | 1.0000 | 0.9848 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | expand_emoji | 5 | 163 | 133 | 1.0062 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | expand_slang | 5 | 162 | 131 | 1.0000 | 0.9848 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | keep_hashtag_content | 5 | 162 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | remove_hashtag | 5 | 156 | 126 | 0.9630 | 0.9545 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | remove_url | 5 | 158 | 128 | 0.9753 | 0.9697 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | remove_mention | 5 | 162 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | remove_punctuation | 5 | 162 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | remove_emoji | 5 | 162 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | full_normalize | 5 | 163 | 130 | 1.0062 | 0.9470 |
| label__agreement_band__topic | 0\|unanimous\|Tionghoa, Rohingya | existing_cleaner | 5 | 152 | 122 | 0.9383 | 0.9242 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | raw | 1807 | 45996 | 10888 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | lowercase | 1807 | 45996 | 10888 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | leet_decode | 1807 | 45991 | 10903 | 0.9999 | 0.9833 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | collapse_repetition | 1807 | 45996 | 10875 | 1.0000 | 0.9957 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | expand_emoji | 1807 | 46323 | 10897 | 1.0071 | 0.9998 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | expand_slang | 1807 | 46035 | 10860 | 1.0008 | 0.9972 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | keep_hashtag_content | 1807 | 45991 | 10890 | 0.9999 | 0.9998 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | remove_hashtag | 1807 | 44933 | 10406 | 0.9769 | 0.9557 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | remove_url | 1807 | 45850 | 10865 | 0.9968 | 0.9979 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | remove_mention | 1807 | 45908 | 10846 | 0.9981 | 0.9961 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | remove_punctuation | 1807 | 45996 | 10888 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | remove_emoji | 1807 | 44000 | 10611 | 0.9566 | 0.9679 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | full_normalize | 1807 | 46440 | 10850 | 1.0097 | 0.9748 |
| label__agreement_band__topic | 0\|unanimous\|UNKNOWN | existing_cleaner | 1807 | 44699 | 10333 | 0.9718 | 0.9490 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | raw | 11 | 1463 | 391 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | lowercase | 11 | 1463 | 391 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | leet_decode | 11 | 1463 | 391 | 1.0000 | 0.9872 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | collapse_repetition | 11 | 1463 | 391 | 1.0000 | 0.9974 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | expand_emoji | 11 | 1492 | 395 | 1.0198 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | expand_slang | 11 | 1463 | 390 | 1.0000 | 0.9974 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | keep_hashtag_content | 11 | 1463 | 391 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | remove_hashtag | 11 | 1459 | 387 | 0.9973 | 0.9898 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | remove_url | 11 | 1463 | 391 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | remove_mention | 11 | 1462 | 390 | 0.9993 | 0.9974 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | remove_punctuation | 11 | 1463 | 391 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | remove_emoji | 11 | 1425 | 367 | 0.9740 | 0.9284 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | full_normalize | 11 | 1492 | 394 | 1.0198 | 0.9795 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah | existing_cleaner | 11 | 1458 | 386 | 0.9966 | 0.9872 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | raw | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | lowercase | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | leet_decode | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | collapse_repetition | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | expand_emoji | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | expand_slang | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | keep_hashtag_content | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | remove_hashtag | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | remove_url | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | remove_mention | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | remove_punctuation | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | remove_emoji | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | full_normalize | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Ahmadiyah, Kristen | existing_cleaner | 1 | 79 | 62 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | raw | 594 | 15218 | 4831 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | lowercase | 594 | 15218 | 4831 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | leet_decode | 594 | 15217 | 4833 | 0.9999 | 0.9892 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | collapse_repetition | 594 | 15218 | 4814 | 1.0000 | 0.9868 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | expand_emoji | 594 | 15476 | 4840 | 1.0170 | 0.9990 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | expand_slang | 594 | 15280 | 4801 | 1.0041 | 0.9921 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | keep_hashtag_content | 594 | 15218 | 4831 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | remove_hashtag | 594 | 14982 | 4665 | 0.9845 | 0.9656 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | remove_url | 594 | 15218 | 4831 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | remove_mention | 594 | 15147 | 4779 | 0.9953 | 0.9892 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | remove_punctuation | 594 | 15218 | 4831 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | remove_emoji | 594 | 15136 | 4760 | 0.9946 | 0.9814 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | full_normalize | 594 | 15569 | 4763 | 1.0231 | 0.9598 |
| label__agreement_band__topic | 1\|borderline\|Disabilitas | existing_cleaner | 594 | 14911 | 4613 | 0.9798 | 0.9549 |
| label__agreement_band__topic | 1\|borderline\|Jewish | raw | 943 | 37078 | 7803 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish | lowercase | 943 | 37078 | 7803 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish | leet_decode | 943 | 37072 | 7788 | 0.9998 | 0.9851 |
| label__agreement_band__topic | 1\|borderline\|Jewish | collapse_repetition | 943 | 37078 | 7792 | 1.0000 | 0.9946 |
| label__agreement_band__topic | 1\|borderline\|Jewish | expand_emoji | 943 | 37379 | 7815 | 1.0081 | 0.9994 |
| label__agreement_band__topic | 1\|borderline\|Jewish | expand_slang | 943 | 37090 | 7774 | 1.0003 | 0.9947 |
| label__agreement_band__topic | 1\|borderline\|Jewish | keep_hashtag_content | 943 | 37051 | 7783 | 0.9993 | 0.9971 |
| label__agreement_band__topic | 1\|borderline\|Jewish | remove_hashtag | 943 | 35902 | 7350 | 0.9683 | 0.9419 |
| label__agreement_band__topic | 1\|borderline\|Jewish | remove_url | 943 | 37058 | 7797 | 0.9995 | 0.9992 |
| label__agreement_band__topic | 1\|borderline\|Jewish | remove_mention | 943 | 36885 | 7700 | 0.9948 | 0.9868 |
| label__agreement_band__topic | 1\|borderline\|Jewish | remove_punctuation | 943 | 37078 | 7803 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish | remove_emoji | 943 | 36747 | 7652 | 0.9911 | 0.9744 |
| label__agreement_band__topic | 1\|borderline\|Jewish | full_normalize | 943 | 37345 | 7727 | 1.0072 | 0.9704 |
| label__agreement_band__topic | 1\|borderline\|Jewish | existing_cleaner | 943 | 35689 | 7232 | 0.9625 | 0.9268 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | raw | 20 | 851 | 488 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | lowercase | 20 | 851 | 488 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | leet_decode | 20 | 851 | 488 | 1.0000 | 0.9980 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | collapse_repetition | 20 | 851 | 488 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | expand_emoji | 20 | 854 | 491 | 1.0035 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | expand_slang | 20 | 852 | 482 | 1.0012 | 0.9734 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | keep_hashtag_content | 20 | 851 | 488 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | remove_hashtag | 20 | 832 | 474 | 0.9777 | 0.9713 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | remove_url | 20 | 851 | 488 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | remove_mention | 20 | 845 | 485 | 0.9929 | 0.9939 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | remove_punctuation | 20 | 851 | 488 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | remove_emoji | 20 | 846 | 488 | 0.9941 | 0.9898 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | full_normalize | 20 | 856 | 483 | 1.0059 | 0.9652 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Disabilitas | existing_cleaner | 20 | 826 | 471 | 0.9706 | 0.9652 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | raw | 14 | 685 | 380 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | lowercase | 14 | 685 | 380 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | leet_decode | 14 | 685 | 380 | 1.0000 | 0.9974 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | collapse_repetition | 14 | 685 | 380 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | expand_emoji | 14 | 691 | 384 | 1.0088 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | expand_slang | 14 | 685 | 379 | 1.0000 | 0.9974 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | keep_hashtag_content | 14 | 685 | 380 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | remove_hashtag | 14 | 656 | 359 | 0.9577 | 0.9447 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | remove_url | 14 | 685 | 380 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | remove_mention | 14 | 681 | 376 | 0.9942 | 0.9895 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | remove_punctuation | 14 | 685 | 380 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | remove_emoji | 14 | 684 | 379 | 0.9985 | 0.9921 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | full_normalize | 14 | 691 | 383 | 1.0088 | 0.9947 |
| label__agreement_band__topic | 1\|borderline\|Jewish, Rohingya | existing_cleaner | 14 | 652 | 355 | 0.9518 | 0.9342 |
| label__agreement_band__topic | 1\|borderline\|Kristen | raw | 77 | 4000 | 1628 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen | lowercase | 77 | 4000 | 1628 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen | leet_decode | 77 | 4000 | 1628 | 1.0000 | 0.9859 |
| label__agreement_band__topic | 1\|borderline\|Kristen | collapse_repetition | 77 | 4000 | 1626 | 1.0000 | 0.9926 |
| label__agreement_band__topic | 1\|borderline\|Kristen | expand_emoji | 77 | 4059 | 1635 | 1.0148 | 0.9988 |
| label__agreement_band__topic | 1\|borderline\|Kristen | expand_slang | 77 | 4001 | 1608 | 1.0003 | 0.9810 |
| label__agreement_band__topic | 1\|borderline\|Kristen | keep_hashtag_content | 77 | 4000 | 1628 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen | remove_hashtag | 77 | 3941 | 1574 | 0.9852 | 0.9668 |
| label__agreement_band__topic | 1\|borderline\|Kristen | remove_url | 77 | 4000 | 1628 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen | remove_mention | 77 | 3927 | 1564 | 0.9818 | 0.9607 |
| label__agreement_band__topic | 1\|borderline\|Kristen | remove_punctuation | 77 | 4000 | 1628 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen | remove_emoji | 77 | 3999 | 1626 | 0.9998 | 0.9975 |
| label__agreement_band__topic | 1\|borderline\|Kristen | full_normalize | 77 | 4053 | 1604 | 1.0132 | 0.9527 |
| label__agreement_band__topic | 1\|borderline\|Kristen | existing_cleaner | 77 | 3868 | 1508 | 0.9670 | 0.9263 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | raw | 2 | 216 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | lowercase | 2 | 216 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | leet_decode | 2 | 216 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | collapse_repetition | 2 | 216 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | expand_emoji | 2 | 218 | 133 | 1.0093 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | expand_slang | 2 | 216 | 131 | 1.0000 | 0.9924 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | keep_hashtag_content | 2 | 216 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | remove_hashtag | 2 | 216 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | remove_url | 2 | 216 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | remove_mention | 2 | 216 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | remove_punctuation | 2 | 216 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | remove_emoji | 2 | 216 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | full_normalize | 2 | 218 | 132 | 1.0093 | 0.9924 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Disabilitas | existing_cleaner | 2 | 216 | 132 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | raw | 27 | 1528 | 748 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | lowercase | 27 | 1528 | 748 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | leet_decode | 27 | 1528 | 748 | 1.0000 | 0.9947 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | collapse_repetition | 27 | 1528 | 748 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | expand_emoji | 27 | 1535 | 751 | 1.0046 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | expand_slang | 27 | 1528 | 736 | 1.0000 | 0.9813 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | keep_hashtag_content | 27 | 1528 | 748 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | remove_hashtag | 27 | 1504 | 737 | 0.9843 | 0.9853 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | remove_url | 27 | 1524 | 744 | 0.9974 | 0.9947 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | remove_mention | 27 | 1515 | 735 | 0.9915 | 0.9826 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | remove_punctuation | 27 | 1528 | 748 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | remove_emoji | 27 | 1526 | 747 | 0.9987 | 0.9947 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | full_normalize | 27 | 1534 | 736 | 1.0039 | 0.9693 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Jewish | existing_cleaner | 27 | 1487 | 720 | 0.9732 | 0.9626 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | raw | 1 | 32 | 27 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | lowercase | 1 | 32 | 27 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | leet_decode | 1 | 32 | 27 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | collapse_repetition | 1 | 32 | 27 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | expand_emoji | 1 | 33 | 28 | 1.0312 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | expand_slang | 1 | 32 | 27 | 1.0000 | 0.9630 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | keep_hashtag_content | 1 | 32 | 27 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | remove_hashtag | 1 | 32 | 27 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | remove_url | 1 | 32 | 27 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | remove_mention | 1 | 31 | 26 | 0.9688 | 0.9630 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | remove_punctuation | 1 | 32 | 27 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | remove_emoji | 1 | 32 | 27 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | full_normalize | 1 | 33 | 28 | 1.0312 | 0.9630 |
| label__agreement_band__topic | 1\|borderline\|Kristen, LGBTQ+ | existing_cleaner | 1 | 31 | 26 | 0.9688 | 0.9630 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | raw | 2 | 259 | 188 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | lowercase | 2 | 259 | 188 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | leet_decode | 2 | 259 | 188 | 1.0000 | 0.9947 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | collapse_repetition | 2 | 259 | 188 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | expand_emoji | 2 | 263 | 189 | 1.0154 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | expand_slang | 2 | 259 | 187 | 1.0000 | 0.9894 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | keep_hashtag_content | 2 | 259 | 188 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | remove_hashtag | 2 | 259 | 188 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | remove_url | 2 | 259 | 188 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | remove_mention | 2 | 259 | 188 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | remove_punctuation | 2 | 259 | 188 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | remove_emoji | 2 | 259 | 187 | 1.0000 | 0.9787 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | full_normalize | 2 | 261 | 188 | 1.0077 | 0.9840 |
| label__agreement_band__topic | 1\|borderline\|Kristen, Tionghoa | existing_cleaner | 2 | 259 | 188 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | raw | 238 | 8012 | 3184 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | lowercase | 238 | 8013 | 3184 | 1.0001 | 0.9997 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | leet_decode | 238 | 8013 | 3190 | 1.0001 | 0.9821 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | collapse_repetition | 238 | 8012 | 3177 | 1.0000 | 0.9912 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | expand_emoji | 238 | 8099 | 3197 | 1.0109 | 0.9981 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | expand_slang | 238 | 8014 | 3165 | 1.0002 | 0.9909 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | keep_hashtag_content | 238 | 8009 | 3182 | 0.9996 | 0.9984 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | remove_hashtag | 238 | 7518 | 2901 | 0.9383 | 0.9111 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | remove_url | 238 | 7991 | 3174 | 0.9974 | 0.9969 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | remove_mention | 238 | 7952 | 3143 | 0.9925 | 0.9871 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | remove_punctuation | 238 | 8012 | 3184 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | remove_emoji | 238 | 7998 | 3170 | 0.9983 | 0.9909 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | full_normalize | 238 | 8097 | 3157 | 1.0106 | 0.9551 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+ | existing_cleaner | 238 | 7438 | 2846 | 0.9284 | 0.8935 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | raw | 4 | 124 | 93 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | lowercase | 4 | 124 | 93 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | leet_decode | 4 | 124 | 93 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | collapse_repetition | 4 | 124 | 93 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | expand_emoji | 4 | 125 | 94 | 1.0081 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | expand_slang | 4 | 124 | 91 | 1.0000 | 0.9032 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | keep_hashtag_content | 4 | 124 | 93 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | remove_hashtag | 4 | 124 | 93 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | remove_url | 4 | 124 | 93 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | remove_mention | 4 | 124 | 93 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | remove_punctuation | 4 | 124 | 93 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | remove_emoji | 4 | 124 | 93 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | full_normalize | 4 | 125 | 91 | 1.0081 | 0.8925 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Disabilitas | existing_cleaner | 4 | 124 | 93 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | raw | 4 | 88 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | lowercase | 4 | 88 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | leet_decode | 4 | 88 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | collapse_repetition | 4 | 88 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | expand_emoji | 4 | 90 | 71 | 1.0227 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | expand_slang | 4 | 88 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | keep_hashtag_content | 4 | 88 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | remove_hashtag | 4 | 87 | 68 | 0.9886 | 0.9855 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | remove_url | 4 | 88 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | remove_mention | 4 | 84 | 68 | 0.9545 | 0.9855 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | remove_punctuation | 4 | 88 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | remove_emoji | 4 | 88 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | full_normalize | 4 | 90 | 71 | 1.0227 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|LGBTQ+, Jewish | existing_cleaner | 4 | 83 | 67 | 0.9432 | 0.9710 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | raw | 23 | 821 | 449 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | lowercase | 23 | 821 | 449 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | leet_decode | 23 | 821 | 449 | 1.0000 | 0.9955 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | collapse_repetition | 23 | 821 | 449 | 1.0000 | 0.9933 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | expand_emoji | 23 | 836 | 452 | 1.0183 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | expand_slang | 23 | 821 | 439 | 1.0000 | 0.9688 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | keep_hashtag_content | 23 | 821 | 449 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | remove_hashtag | 23 | 805 | 435 | 0.9805 | 0.9688 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | remove_url | 23 | 813 | 445 | 0.9903 | 0.9911 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | remove_mention | 23 | 811 | 440 | 0.9878 | 0.9800 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | remove_punctuation | 23 | 821 | 449 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | remove_emoji | 23 | 821 | 449 | 1.0000 | 0.9955 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | full_normalize | 23 | 836 | 441 | 1.0183 | 0.9577 |
| label__agreement_band__topic | 1\|borderline\|Rohingya | existing_cleaner | 23 | 787 | 422 | 0.9586 | 0.9399 |
| label__agreement_band__topic | 1\|borderline\|Syiah | raw | 69 | 7424 | 2280 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah | lowercase | 69 | 7424 | 2280 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah | leet_decode | 69 | 7425 | 2274 | 1.0001 | 0.9882 |
| label__agreement_band__topic | 1\|borderline\|Syiah | collapse_repetition | 69 | 7424 | 2279 | 1.0000 | 0.9956 |
| label__agreement_band__topic | 1\|borderline\|Syiah | expand_emoji | 69 | 7458 | 2291 | 1.0046 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah | expand_slang | 69 | 7424 | 2264 | 1.0000 | 0.9921 |
| label__agreement_band__topic | 1\|borderline\|Syiah | keep_hashtag_content | 69 | 7424 | 2280 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah | remove_hashtag | 69 | 7409 | 2268 | 0.9980 | 0.9947 |
| label__agreement_band__topic | 1\|borderline\|Syiah | remove_url | 69 | 7424 | 2280 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah | remove_mention | 69 | 7416 | 2274 | 0.9989 | 0.9974 |
| label__agreement_band__topic | 1\|borderline\|Syiah | remove_punctuation | 69 | 7424 | 2280 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah | remove_emoji | 69 | 7058 | 2204 | 0.9507 | 0.9575 |
| label__agreement_band__topic | 1\|borderline\|Syiah | full_normalize | 69 | 7455 | 2261 | 1.0042 | 0.9732 |
| label__agreement_band__topic | 1\|borderline\|Syiah | existing_cleaner | 69 | 7401 | 2262 | 0.9969 | 0.9921 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | raw | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | lowercase | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | leet_decode | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | collapse_repetition | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | expand_emoji | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | expand_slang | 1 | 292 | 148 | 1.0000 | 0.9933 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | keep_hashtag_content | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | remove_hashtag | 1 | 261 | 134 | 0.8938 | 0.8993 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | remove_url | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | remove_mention | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | remove_punctuation | 1 | 292 | 149 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | remove_emoji | 1 | 292 | 148 | 1.0000 | 0.9799 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | full_normalize | 1 | 292 | 147 | 1.0000 | 0.9799 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Ahmadiyah, Jewish | existing_cleaner | 1 | 261 | 134 | 0.8938 | 0.8993 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | raw | 4 | 948 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | lowercase | 4 | 948 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | leet_decode | 4 | 948 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | collapse_repetition | 4 | 948 | 364 | 1.0000 | 0.9945 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | expand_emoji | 4 | 962 | 368 | 1.0148 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | expand_slang | 4 | 948 | 360 | 1.0000 | 0.9835 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | keep_hashtag_content | 4 | 948 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | remove_hashtag | 4 | 946 | 363 | 0.9979 | 0.9973 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | remove_url | 4 | 948 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | remove_mention | 4 | 948 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | remove_punctuation | 4 | 948 | 364 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | remove_emoji | 4 | 922 | 353 | 0.9726 | 0.9560 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | full_normalize | 4 | 959 | 362 | 1.0116 | 0.9753 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Disabilitas | existing_cleaner | 4 | 946 | 363 | 0.9979 | 0.9973 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | raw | 33 | 3156 | 1181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | lowercase | 33 | 3156 | 1181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | leet_decode | 33 | 3156 | 1181 | 1.0000 | 0.9966 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | collapse_repetition | 33 | 3156 | 1181 | 1.0000 | 0.9992 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | expand_emoji | 33 | 3167 | 1183 | 1.0035 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | expand_slang | 33 | 3156 | 1175 | 1.0000 | 0.9915 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | keep_hashtag_content | 33 | 3155 | 1182 | 0.9997 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | remove_hashtag | 33 | 3108 | 1173 | 0.9848 | 0.9932 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | remove_url | 33 | 3156 | 1181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | remove_mention | 33 | 3150 | 1177 | 0.9981 | 0.9966 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | remove_punctuation | 33 | 3156 | 1181 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | remove_emoji | 33 | 3122 | 1148 | 0.9892 | 0.9619 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | full_normalize | 33 | 3165 | 1173 | 1.0029 | 0.9839 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish | existing_cleaner | 33 | 3102 | 1168 | 0.9829 | 0.9890 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | raw | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | lowercase | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | leet_decode | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | collapse_repetition | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | expand_emoji | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | expand_slang | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | keep_hashtag_content | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | remove_hashtag | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | remove_url | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | remove_mention | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | remove_punctuation | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | remove_emoji | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | full_normalize | 1 | 114 | 85 | 1.0000 | 0.9647 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Disabilitas | existing_cleaner | 1 | 114 | 85 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | raw | 1 | 42 | 37 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | lowercase | 1 | 42 | 37 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | leet_decode | 1 | 42 | 37 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | collapse_repetition | 1 | 42 | 37 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | expand_emoji | 1 | 46 | 39 | 1.0952 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | expand_slang | 1 | 42 | 37 | 1.0000 | 0.9730 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | keep_hashtag_content | 1 | 42 | 37 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | remove_hashtag | 1 | 42 | 37 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | remove_url | 1 | 42 | 37 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | remove_mention | 1 | 42 | 37 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | remove_punctuation | 1 | 42 | 37 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | remove_emoji | 1 | 42 | 37 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | full_normalize | 1 | 46 | 38 | 1.0952 | 0.9459 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Jewish, Rohingya | existing_cleaner | 1 | 42 | 37 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | raw | 1 | 17 | 15 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | lowercase | 1 | 17 | 15 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | leet_decode | 1 | 17 | 15 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | collapse_repetition | 1 | 17 | 15 | 1.0000 | 0.9333 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | expand_emoji | 1 | 17 | 15 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | expand_slang | 1 | 17 | 15 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | keep_hashtag_content | 1 | 17 | 15 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | remove_hashtag | 1 | 17 | 15 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | remove_url | 1 | 17 | 15 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | remove_mention | 1 | 16 | 14 | 0.9412 | 0.9333 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | remove_punctuation | 1 | 17 | 15 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | remove_emoji | 1 | 17 | 15 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | full_normalize | 1 | 17 | 15 | 1.0000 | 0.9333 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen | existing_cleaner | 1 | 16 | 14 | 0.9412 | 0.9333 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | raw | 2 | 85 | 60 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | lowercase | 2 | 85 | 60 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | leet_decode | 2 | 85 | 60 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | collapse_repetition | 2 | 85 | 60 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | expand_emoji | 2 | 85 | 60 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | expand_slang | 2 | 85 | 60 | 1.0000 | 0.9833 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | keep_hashtag_content | 2 | 85 | 60 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | remove_hashtag | 2 | 85 | 60 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | remove_url | 2 | 85 | 60 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | remove_mention | 2 | 85 | 60 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | remove_punctuation | 2 | 85 | 60 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | remove_emoji | 2 | 85 | 60 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | full_normalize | 2 | 85 | 60 | 1.0000 | 0.9833 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Kristen, Jewish | existing_cleaner | 2 | 85 | 60 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | raw | 1 | 200 | 131 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | lowercase | 1 | 200 | 131 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | leet_decode | 1 | 200 | 131 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | collapse_repetition | 1 | 200 | 131 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | expand_emoji | 1 | 200 | 131 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | expand_slang | 1 | 200 | 131 | 1.0000 | 0.9924 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | keep_hashtag_content | 1 | 200 | 131 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | remove_hashtag | 1 | 200 | 131 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | remove_url | 1 | 200 | 131 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | remove_mention | 1 | 199 | 131 | 0.9950 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | remove_punctuation | 1 | 200 | 131 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | remove_emoji | 1 | 200 | 131 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | full_normalize | 1 | 200 | 131 | 1.0000 | 0.9924 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Rohingya, Disabilitas | existing_cleaner | 1 | 199 | 131 | 0.9950 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | raw | 1 | 287 | 141 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | lowercase | 1 | 287 | 141 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | leet_decode | 1 | 287 | 141 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | collapse_repetition | 1 | 287 | 141 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | expand_emoji | 1 | 287 | 141 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | expand_slang | 1 | 287 | 142 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | keep_hashtag_content | 1 | 287 | 141 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | remove_hashtag | 1 | 287 | 141 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | remove_url | 1 | 287 | 141 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | remove_mention | 1 | 287 | 141 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | remove_punctuation | 1 | 287 | 141 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | remove_emoji | 1 | 248 | 124 | 0.8641 | 0.8794 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | full_normalize | 1 | 287 | 142 | 1.0000 | 0.9929 |
| label__agreement_band__topic | 1\|borderline\|Syiah, Tionghoa, Jewish | existing_cleaner | 1 | 287 | 141 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | raw | 261 | 8998 | 3224 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | lowercase | 261 | 8998 | 3224 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | leet_decode | 261 | 8998 | 3229 | 1.0000 | 0.9929 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | collapse_repetition | 261 | 8998 | 3222 | 1.0000 | 0.9935 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | expand_emoji | 261 | 9134 | 3245 | 1.0151 | 0.9994 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | expand_slang | 261 | 9001 | 3198 | 1.0003 | 0.9898 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | keep_hashtag_content | 261 | 8998 | 3224 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | remove_hashtag | 261 | 8760 | 3086 | 0.9735 | 0.9572 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | remove_url | 261 | 8998 | 3224 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | remove_mention | 261 | 8971 | 3207 | 0.9970 | 0.9947 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | remove_punctuation | 261 | 8998 | 3224 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | remove_emoji | 261 | 8985 | 3213 | 0.9986 | 0.9950 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | full_normalize | 261 | 9129 | 3199 | 1.0146 | 0.9687 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa | existing_cleaner | 261 | 8733 | 3067 | 0.9705 | 0.9513 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | raw | 8 | 275 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | lowercase | 8 | 275 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | leet_decode | 8 | 275 | 173 | 1.0000 | 0.9942 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | collapse_repetition | 8 | 275 | 173 | 1.0000 | 0.9884 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | expand_emoji | 8 | 275 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | expand_slang | 8 | 278 | 169 | 1.0109 | 0.8902 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | keep_hashtag_content | 8 | 275 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | remove_hashtag | 8 | 275 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | remove_url | 8 | 275 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | remove_mention | 8 | 275 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | remove_punctuation | 8 | 275 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | remove_emoji | 8 | 275 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | full_normalize | 8 | 278 | 166 | 1.0109 | 0.8497 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Disabilitas | existing_cleaner | 8 | 275 | 173 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | raw | 8 | 422 | 258 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | lowercase | 8 | 422 | 258 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | leet_decode | 8 | 422 | 258 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | collapse_repetition | 8 | 422 | 258 | 1.0000 | 0.9961 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | expand_emoji | 8 | 432 | 261 | 1.0237 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | expand_slang | 8 | 422 | 252 | 1.0000 | 0.9729 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | keep_hashtag_content | 8 | 422 | 258 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | remove_hashtag | 8 | 416 | 253 | 0.9858 | 0.9806 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | remove_url | 8 | 422 | 258 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | remove_mention | 8 | 422 | 258 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | remove_punctuation | 8 | 422 | 258 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | remove_emoji | 8 | 414 | 250 | 0.9810 | 0.9690 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | full_normalize | 8 | 432 | 254 | 1.0237 | 0.9612 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Jewish | existing_cleaner | 8 | 416 | 253 | 0.9858 | 0.9806 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | raw | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | lowercase | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | leet_decode | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | collapse_repetition | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | expand_emoji | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | expand_slang | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | keep_hashtag_content | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | remove_hashtag | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | remove_url | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | remove_mention | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | remove_punctuation | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | remove_emoji | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | full_normalize | 1 | 26 | 20 | 1.0000 | 0.9500 |
| label__agreement_band__topic | 1\|borderline\|Tionghoa, Rohingya | existing_cleaner | 1 | 26 | 20 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | raw | 227 | 8928 | 3012 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | lowercase | 227 | 8928 | 3012 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | leet_decode | 227 | 8868 | 2996 | 0.9933 | 0.9824 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | collapse_repetition | 227 | 8928 | 3011 | 1.0000 | 0.9960 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | expand_emoji | 227 | 9094 | 3023 | 1.0186 | 0.9997 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | expand_slang | 227 | 8938 | 2998 | 1.0011 | 0.9937 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | keep_hashtag_content | 227 | 8928 | 3012 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | remove_hashtag | 227 | 8832 | 2963 | 0.9892 | 0.9837 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | remove_url | 227 | 8928 | 3012 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | remove_mention | 227 | 8918 | 3005 | 0.9989 | 0.9977 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | remove_punctuation | 227 | 8928 | 3012 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | remove_emoji | 227 | 8488 | 2898 | 0.9507 | 0.9598 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | full_normalize | 227 | 9077 | 2983 | 1.0167 | 0.9648 |
| label__agreement_band__topic | 1\|borderline\|UNKNOWN | existing_cleaner | 227 | 8822 | 2956 | 0.9881 | 0.9814 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | raw | 10 | 758 | 449 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | lowercase | 10 | 758 | 449 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | leet_decode | 10 | 758 | 449 | 1.0000 | 0.9889 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | collapse_repetition | 10 | 758 | 449 | 1.0000 | 0.9978 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | expand_emoji | 10 | 760 | 451 | 1.0026 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | expand_slang | 10 | 758 | 443 | 1.0000 | 0.9822 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | keep_hashtag_content | 10 | 758 | 449 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | remove_hashtag | 10 | 754 | 445 | 0.9947 | 0.9911 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | remove_url | 10 | 758 | 449 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | remove_mention | 10 | 750 | 443 | 0.9894 | 0.9866 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | remove_punctuation | 10 | 758 | 449 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | remove_emoji | 10 | 737 | 428 | 0.9723 | 0.9465 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | full_normalize | 10 | 760 | 442 | 1.0026 | 0.9644 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah | existing_cleaner | 10 | 746 | 439 | 0.9842 | 0.9777 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | raw | 1 | 40 | 36 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | lowercase | 1 | 40 | 36 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | leet_decode | 1 | 40 | 36 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | collapse_repetition | 1 | 40 | 36 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | expand_emoji | 1 | 47 | 37 | 1.1750 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | expand_slang | 1 | 40 | 36 | 1.0000 | 0.9722 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | keep_hashtag_content | 1 | 40 | 36 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | remove_hashtag | 1 | 40 | 36 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | remove_url | 1 | 40 | 36 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | remove_mention | 1 | 40 | 36 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | remove_punctuation | 1 | 40 | 36 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | remove_emoji | 1 | 40 | 36 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | full_normalize | 1 | 42 | 37 | 1.0500 | 0.9722 |
| label__agreement_band__topic | 1\|unanimous\|Ahmadiyah, Kristen, Jewish | existing_cleaner | 1 | 40 | 36 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | raw | 238 | 5451 | 2162 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | lowercase | 238 | 5451 | 2162 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | leet_decode | 238 | 5451 | 2160 | 1.0000 | 0.9907 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | collapse_repetition | 238 | 5451 | 2159 | 1.0000 | 0.9894 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | expand_emoji | 238 | 5546 | 2176 | 1.0174 | 0.9981 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | expand_slang | 238 | 5484 | 2134 | 1.0061 | 0.9829 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | keep_hashtag_content | 238 | 5450 | 2162 | 0.9998 | 0.9995 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | remove_hashtag | 238 | 5398 | 2129 | 0.9903 | 0.9847 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | remove_url | 238 | 5447 | 2159 | 0.9993 | 0.9986 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | remove_mention | 238 | 5416 | 2130 | 0.9936 | 0.9852 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | remove_punctuation | 238 | 5451 | 2162 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | remove_emoji | 238 | 5442 | 2158 | 0.9983 | 0.9940 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | full_normalize | 238 | 5629 | 2120 | 1.0327 | 0.9514 |
| label__agreement_band__topic | 1\|unanimous\|Disabilitas | existing_cleaner | 238 | 5359 | 2094 | 0.9831 | 0.9685 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | raw | 583 | 15963 | 4605 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | lowercase | 583 | 15963 | 4605 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | leet_decode | 583 | 15962 | 4603 | 0.9999 | 0.9894 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | collapse_repetition | 583 | 15963 | 4592 | 1.0000 | 0.9917 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | expand_emoji | 583 | 16240 | 4617 | 1.0174 | 0.9993 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | expand_slang | 583 | 15970 | 4569 | 1.0004 | 0.9902 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | keep_hashtag_content | 583 | 15963 | 4605 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | remove_hashtag | 583 | 15515 | 4424 | 0.9719 | 0.9607 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | remove_url | 583 | 15909 | 4589 | 0.9966 | 0.9965 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | remove_mention | 583 | 15871 | 4541 | 0.9942 | 0.9861 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | remove_punctuation | 583 | 15963 | 4605 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | remove_emoji | 583 | 15911 | 4555 | 0.9967 | 0.9852 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | full_normalize | 583 | 16201 | 4535 | 1.0149 | 0.9640 |
| label__agreement_band__topic | 1\|unanimous\|Jewish | existing_cleaner | 583 | 15369 | 4340 | 0.9628 | 0.9425 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | raw | 14 | 328 | 238 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | lowercase | 14 | 328 | 238 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | leet_decode | 14 | 328 | 238 | 1.0000 | 0.9958 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | collapse_repetition | 14 | 328 | 238 | 1.0000 | 0.9916 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | expand_emoji | 14 | 330 | 240 | 1.0061 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | expand_slang | 14 | 328 | 233 | 1.0000 | 0.9664 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | keep_hashtag_content | 14 | 328 | 238 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | remove_hashtag | 14 | 327 | 237 | 0.9970 | 0.9958 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | remove_url | 14 | 324 | 234 | 0.9878 | 0.9832 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | remove_mention | 14 | 324 | 234 | 0.9878 | 0.9832 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | remove_punctuation | 14 | 328 | 238 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | remove_emoji | 14 | 328 | 238 | 1.0000 | 0.9958 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | full_normalize | 14 | 330 | 234 | 1.0061 | 0.9454 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Disabilitas | existing_cleaner | 14 | 319 | 229 | 0.9726 | 0.9622 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | raw | 12 | 343 | 207 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | lowercase | 12 | 343 | 207 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | leet_decode | 12 | 343 | 207 | 1.0000 | 0.9903 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | collapse_repetition | 12 | 343 | 207 | 1.0000 | 0.9952 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | expand_emoji | 12 | 343 | 207 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | expand_slang | 12 | 343 | 206 | 1.0000 | 0.9952 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | keep_hashtag_content | 12 | 343 | 207 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | remove_hashtag | 12 | 323 | 196 | 0.9417 | 0.9469 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | remove_url | 12 | 343 | 207 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | remove_mention | 12 | 341 | 205 | 0.9942 | 0.9903 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | remove_punctuation | 12 | 343 | 207 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | remove_emoji | 12 | 343 | 206 | 1.0000 | 0.9952 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | full_normalize | 12 | 343 | 206 | 1.0000 | 0.9758 |
| label__agreement_band__topic | 1\|unanimous\|Jewish, Rohingya | existing_cleaner | 12 | 321 | 194 | 0.9359 | 0.9372 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | raw | 53 | 1988 | 1017 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | lowercase | 53 | 1988 | 1017 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | leet_decode | 53 | 1988 | 1018 | 1.0000 | 0.9705 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | collapse_repetition | 53 | 1988 | 1017 | 1.0000 | 0.9941 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | expand_emoji | 53 | 2021 | 1021 | 1.0166 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | expand_slang | 53 | 1990 | 1006 | 1.0010 | 0.9823 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | keep_hashtag_content | 53 | 1988 | 1017 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | remove_hashtag | 53 | 1984 | 1013 | 0.9980 | 0.9961 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | remove_url | 53 | 1984 | 1013 | 0.9980 | 0.9961 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | remove_mention | 53 | 1906 | 939 | 0.9588 | 0.9233 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | remove_punctuation | 53 | 1988 | 1017 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | remove_emoji | 53 | 1987 | 1015 | 0.9995 | 0.9902 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | full_normalize | 53 | 2016 | 1003 | 1.0141 | 0.9381 |
| label__agreement_band__topic | 1\|unanimous\|Kristen | existing_cleaner | 53 | 1898 | 931 | 0.9547 | 0.9154 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | raw | 1 | 33 | 29 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | lowercase | 1 | 33 | 29 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | leet_decode | 1 | 33 | 29 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | collapse_repetition | 1 | 33 | 29 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | expand_emoji | 1 | 33 | 29 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | expand_slang | 1 | 33 | 29 | 1.0000 | 0.9655 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | keep_hashtag_content | 1 | 33 | 29 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | remove_hashtag | 1 | 33 | 29 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | remove_url | 1 | 33 | 29 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | remove_mention | 1 | 33 | 29 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | remove_punctuation | 1 | 33 | 29 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | remove_emoji | 1 | 33 | 29 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | full_normalize | 1 | 33 | 29 | 1.0000 | 0.9655 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Disabilitas | existing_cleaner | 1 | 33 | 29 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | raw | 13 | 465 | 287 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | lowercase | 13 | 465 | 287 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | leet_decode | 13 | 465 | 287 | 1.0000 | 0.9930 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | collapse_repetition | 13 | 465 | 287 | 1.0000 | 0.9965 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | expand_emoji | 13 | 472 | 288 | 1.0151 | 0.9965 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | expand_slang | 13 | 465 | 283 | 1.0000 | 0.9721 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | keep_hashtag_content | 13 | 465 | 287 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | remove_hashtag | 13 | 465 | 287 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | remove_url | 13 | 461 | 283 | 0.9914 | 0.9861 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | remove_mention | 13 | 463 | 285 | 0.9957 | 0.9930 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | remove_punctuation | 13 | 465 | 287 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | remove_emoji | 13 | 465 | 287 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | full_normalize | 13 | 471 | 284 | 1.0129 | 0.9512 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish | existing_cleaner | 13 | 459 | 281 | 0.9871 | 0.9791 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | raw | 1 | 9 | 9 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | lowercase | 1 | 9 | 9 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | leet_decode | 1 | 9 | 9 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | collapse_repetition | 1 | 9 | 9 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | expand_emoji | 1 | 9 | 9 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | expand_slang | 1 | 9 | 9 | 1.0000 | 0.8889 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | keep_hashtag_content | 1 | 9 | 9 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | remove_hashtag | 1 | 9 | 9 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | remove_url | 1 | 9 | 9 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | remove_mention | 1 | 9 | 9 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | remove_punctuation | 1 | 9 | 9 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | remove_emoji | 1 | 9 | 9 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | full_normalize | 1 | 9 | 9 | 1.0000 | 0.7778 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, Jewish, Disabilitas | existing_cleaner | 1 | 9 | 9 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | raw | 1 | 52 | 48 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | lowercase | 1 | 52 | 48 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | leet_decode | 1 | 52 | 48 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | collapse_repetition | 1 | 52 | 48 | 1.0000 | 0.9792 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | expand_emoji | 1 | 56 | 49 | 1.0769 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | expand_slang | 1 | 52 | 48 | 1.0000 | 0.9375 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | keep_hashtag_content | 1 | 52 | 48 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | remove_hashtag | 1 | 52 | 48 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | remove_url | 1 | 52 | 48 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | remove_mention | 1 | 52 | 48 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | remove_punctuation | 1 | 52 | 48 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | remove_emoji | 1 | 52 | 48 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | full_normalize | 1 | 54 | 49 | 1.0385 | 0.9167 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+ | existing_cleaner | 1 | 52 | 48 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | raw | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | lowercase | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | leet_decode | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | collapse_repetition | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | expand_emoji | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | expand_slang | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | keep_hashtag_content | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | remove_hashtag | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | remove_url | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | remove_mention | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | remove_punctuation | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | remove_emoji | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | full_normalize | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Kristen, LGBTQ+, Disabilitas | existing_cleaner | 1 | 43 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | raw | 63 | 1600 | 974 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | lowercase | 63 | 1600 | 974 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | leet_decode | 63 | 1600 | 974 | 1.0000 | 0.9846 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | collapse_repetition | 63 | 1600 | 974 | 1.0000 | 0.9918 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | expand_emoji | 63 | 1646 | 986 | 1.0288 | 0.9990 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | expand_slang | 63 | 1600 | 953 | 1.0000 | 0.9692 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | keep_hashtag_content | 63 | 1599 | 974 | 0.9994 | 0.9990 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | remove_hashtag | 63 | 1560 | 941 | 0.9750 | 0.9661 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | remove_url | 63 | 1584 | 968 | 0.9900 | 0.9938 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | remove_mention | 63 | 1584 | 958 | 0.9900 | 0.9836 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | remove_punctuation | 63 | 1600 | 974 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | remove_emoji | 63 | 1599 | 974 | 0.9994 | 0.9959 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | full_normalize | 63 | 1642 | 956 | 1.0263 | 0.9343 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+ | existing_cleaner | 63 | 1528 | 919 | 0.9550 | 0.9435 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | raw | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | lowercase | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | leet_decode | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | collapse_repetition | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | expand_emoji | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | expand_slang | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | keep_hashtag_content | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | remove_hashtag | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | remove_url | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | remove_mention | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | remove_punctuation | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | remove_emoji | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | full_normalize | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Disabilitas | existing_cleaner | 1 | 15 | 14 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | raw | 4 | 89 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | lowercase | 4 | 89 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | leet_decode | 4 | 89 | 69 | 1.0000 | 0.9565 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | collapse_repetition | 4 | 89 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | expand_emoji | 4 | 92 | 71 | 1.0337 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | expand_slang | 4 | 89 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | keep_hashtag_content | 4 | 89 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | remove_hashtag | 4 | 88 | 68 | 0.9888 | 0.9855 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | remove_url | 4 | 85 | 65 | 0.9551 | 0.9420 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | remove_mention | 4 | 80 | 64 | 0.8989 | 0.9275 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | remove_punctuation | 4 | 89 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | remove_emoji | 4 | 89 | 69 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | full_normalize | 4 | 92 | 71 | 1.0337 | 0.9275 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish | existing_cleaner | 4 | 75 | 59 | 0.8427 | 0.8551 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | raw | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | lowercase | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | leet_decode | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | collapse_repetition | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | expand_emoji | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | expand_slang | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | keep_hashtag_content | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | remove_hashtag | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | remove_url | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | remove_mention | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | remove_punctuation | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | remove_emoji | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | full_normalize | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|LGBTQ+, Jewish, Disabilitas | existing_cleaner | 1 | 13 | 13 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | raw | 86 | 2907 | 1283 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | lowercase | 86 | 2907 | 1283 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | leet_decode | 86 | 2907 | 1287 | 1.0000 | 0.9797 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | collapse_repetition | 86 | 2907 | 1281 | 1.0000 | 0.9883 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | expand_emoji | 86 | 2943 | 1293 | 1.0124 | 0.9984 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | expand_slang | 86 | 2914 | 1266 | 1.0024 | 0.9813 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | keep_hashtag_content | 86 | 2907 | 1283 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | remove_hashtag | 86 | 2866 | 1262 | 0.9859 | 0.9836 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | remove_url | 86 | 2784 | 1255 | 0.9577 | 0.9782 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | remove_mention | 86 | 2836 | 1230 | 0.9756 | 0.9587 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | remove_punctuation | 86 | 2907 | 1283 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | remove_emoji | 86 | 2906 | 1283 | 0.9997 | 0.9977 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | full_normalize | 86 | 2949 | 1265 | 1.0144 | 0.9361 |
| label__agreement_band__topic | 1\|unanimous\|Rohingya | existing_cleaner | 86 | 2673 | 1181 | 0.9195 | 0.9205 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | raw | 103 | 5883 | 2087 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | lowercase | 103 | 5883 | 2087 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | leet_decode | 103 | 5881 | 2082 | 0.9997 | 0.9689 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | collapse_repetition | 103 | 5883 | 2086 | 1.0000 | 0.9943 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | expand_emoji | 103 | 5920 | 2094 | 1.0063 | 0.9995 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | expand_slang | 103 | 5884 | 2077 | 1.0002 | 0.9923 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | keep_hashtag_content | 103 | 5883 | 2087 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | remove_hashtag | 103 | 5863 | 2073 | 0.9966 | 0.9933 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | remove_url | 103 | 5678 | 2020 | 0.9652 | 0.9679 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | remove_mention | 103 | 5791 | 2012 | 0.9844 | 0.9641 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | remove_punctuation | 103 | 5883 | 2087 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | remove_emoji | 103 | 5488 | 1967 | 0.9329 | 0.9363 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | full_normalize | 103 | 5908 | 2069 | 1.0042 | 0.9502 |
| label__agreement_band__topic | 1\|unanimous\|Syiah | existing_cleaner | 103 | 5567 | 1932 | 0.9463 | 0.9257 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | raw | 2 | 98 | 33 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | lowercase | 2 | 98 | 33 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | leet_decode | 2 | 98 | 33 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | collapse_repetition | 2 | 98 | 33 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | expand_emoji | 2 | 98 | 33 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | expand_slang | 2 | 98 | 33 | 1.0000 | 0.9091 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | keep_hashtag_content | 2 | 98 | 33 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | remove_hashtag | 2 | 98 | 33 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | remove_url | 2 | 98 | 33 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | remove_mention | 2 | 98 | 33 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | remove_punctuation | 2 | 98 | 33 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | remove_emoji | 2 | 98 | 33 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | full_normalize | 2 | 98 | 33 | 1.0000 | 0.9091 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Ahmadiyah | existing_cleaner | 2 | 98 | 33 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | raw | 5 | 545 | 214 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | lowercase | 5 | 545 | 214 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | leet_decode | 5 | 545 | 214 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | collapse_repetition | 5 | 545 | 214 | 1.0000 | 0.9953 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | expand_emoji | 5 | 545 | 214 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | expand_slang | 5 | 545 | 213 | 1.0000 | 0.9953 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | keep_hashtag_content | 5 | 545 | 214 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | remove_hashtag | 5 | 545 | 214 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | remove_url | 5 | 545 | 214 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | remove_mention | 5 | 545 | 214 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | remove_punctuation | 5 | 545 | 214 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | remove_emoji | 5 | 537 | 213 | 0.9853 | 0.9907 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | full_normalize | 5 | 545 | 213 | 1.0000 | 0.9860 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Disabilitas | existing_cleaner | 5 | 545 | 214 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | raw | 38 | 2168 | 1055 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | lowercase | 38 | 2168 | 1055 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | leet_decode | 38 | 2168 | 1055 | 1.0000 | 0.9905 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | collapse_repetition | 38 | 2168 | 1055 | 1.0000 | 0.9972 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | expand_emoji | 38 | 2189 | 1059 | 1.0097 | 0.9991 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | expand_slang | 38 | 2168 | 1050 | 1.0000 | 0.9896 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | keep_hashtag_content | 38 | 2168 | 1055 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | remove_hashtag | 38 | 2165 | 1054 | 0.9986 | 0.9991 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | remove_url | 38 | 2164 | 1051 | 0.9982 | 0.9962 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | remove_mention | 38 | 2145 | 1032 | 0.9894 | 0.9782 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | remove_punctuation | 38 | 2168 | 1055 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | remove_emoji | 38 | 2085 | 999 | 0.9617 | 0.9403 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | full_normalize | 38 | 2189 | 1050 | 1.0097 | 0.9735 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish | existing_cleaner | 38 | 2138 | 1027 | 0.9862 | 0.9735 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | raw | 2 | 562 | 198 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | lowercase | 2 | 562 | 198 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | leet_decode | 2 | 562 | 198 | 1.0000 | 0.9949 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | collapse_repetition | 2 | 562 | 198 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | expand_emoji | 2 | 562 | 198 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | expand_slang | 2 | 562 | 200 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | keep_hashtag_content | 2 | 562 | 198 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | remove_hashtag | 2 | 562 | 198 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | remove_url | 2 | 562 | 198 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | remove_mention | 2 | 562 | 198 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | remove_punctuation | 2 | 562 | 198 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | remove_emoji | 2 | 514 | 188 | 0.9146 | 0.9242 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | full_normalize | 2 | 562 | 197 | 1.0000 | 0.9646 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Jewish, Rohingya | existing_cleaner | 2 | 562 | 198 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | raw | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | lowercase | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | leet_decode | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | collapse_repetition | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | expand_emoji | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | expand_slang | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | keep_hashtag_content | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | remove_hashtag | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | remove_url | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | remove_mention | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | remove_punctuation | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | remove_emoji | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | full_normalize | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, LGBTQ+ | existing_cleaner | 1 | 77 | 63 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | raw | 1 | 47 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | lowercase | 1 | 47 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | leet_decode | 1 | 47 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | collapse_repetition | 1 | 47 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | expand_emoji | 1 | 47 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | expand_slang | 1 | 47 | 41 | 1.0000 | 0.9756 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | keep_hashtag_content | 1 | 47 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | remove_hashtag | 1 | 47 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | remove_url | 1 | 47 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | remove_mention | 1 | 46 | 40 | 0.9787 | 0.9756 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | remove_punctuation | 1 | 47 | 41 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | remove_emoji | 1 | 47 | 41 | 1.0000 | 0.9268 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | full_normalize | 1 | 47 | 41 | 1.0000 | 0.9512 |
| label__agreement_band__topic | 1\|unanimous\|Syiah, Rohingya, Disabilitas | existing_cleaner | 1 | 46 | 40 | 0.9787 | 0.9756 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | raw | 110 | 2700 | 1434 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | lowercase | 110 | 2700 | 1434 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | leet_decode | 110 | 2700 | 1434 | 1.0000 | 0.9916 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | collapse_repetition | 110 | 2700 | 1434 | 1.0000 | 0.9958 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | expand_emoji | 110 | 2743 | 1442 | 1.0159 | 0.9986 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | expand_slang | 110 | 2703 | 1411 | 1.0011 | 0.9777 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | keep_hashtag_content | 110 | 2700 | 1434 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | remove_hashtag | 110 | 2670 | 1413 | 0.9889 | 0.9854 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | remove_url | 110 | 2696 | 1431 | 0.9985 | 0.9979 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | remove_mention | 110 | 2674 | 1411 | 0.9904 | 0.9840 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | remove_punctuation | 110 | 2700 | 1434 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | remove_emoji | 110 | 2700 | 1431 | 1.0000 | 0.9972 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | full_normalize | 110 | 2739 | 1406 | 1.0144 | 0.9533 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa | existing_cleaner | 110 | 2640 | 1386 | 0.9778 | 0.9665 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | raw | 4 | 178 | 120 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | lowercase | 4 | 178 | 120 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | leet_decode | 4 | 178 | 120 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | collapse_repetition | 4 | 178 | 120 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | expand_emoji | 4 | 178 | 120 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | expand_slang | 4 | 178 | 116 | 1.0000 | 0.9000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | keep_hashtag_content | 4 | 178 | 120 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | remove_hashtag | 4 | 178 | 120 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | remove_url | 4 | 178 | 120 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | remove_mention | 4 | 178 | 120 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | remove_punctuation | 4 | 178 | 120 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | remove_emoji | 4 | 178 | 120 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | full_normalize | 4 | 178 | 115 | 1.0000 | 0.8917 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Disabilitas | existing_cleaner | 4 | 178 | 120 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | raw | 3 | 59 | 44 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | lowercase | 3 | 59 | 44 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | leet_decode | 3 | 59 | 44 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | collapse_repetition | 3 | 59 | 44 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | expand_emoji | 3 | 59 | 44 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | expand_slang | 3 | 59 | 43 | 1.0000 | 0.9545 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | keep_hashtag_content | 3 | 59 | 44 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | remove_hashtag | 3 | 59 | 44 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | remove_url | 3 | 59 | 44 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | remove_mention | 3 | 59 | 44 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | remove_punctuation | 3 | 59 | 44 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | remove_emoji | 3 | 59 | 44 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | full_normalize | 3 | 59 | 43 | 1.0000 | 0.9318 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish | existing_cleaner | 3 | 59 | 44 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | raw | 1 | 243 | 140 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | lowercase | 1 | 243 | 140 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | leet_decode | 1 | 243 | 140 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | collapse_repetition | 1 | 243 | 140 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | expand_emoji | 1 | 275 | 148 | 1.1317 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | expand_slang | 1 | 243 | 140 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | keep_hashtag_content | 1 | 243 | 140 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | remove_hashtag | 1 | 243 | 140 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | remove_url | 1 | 243 | 140 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | remove_mention | 1 | 243 | 140 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | remove_punctuation | 1 | 243 | 140 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | remove_emoji | 1 | 243 | 140 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | full_normalize | 1 | 273 | 152 | 1.1235 | 0.9643 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Jewish, Rohingya | existing_cleaner | 1 | 243 | 140 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | raw | 3 | 126 | 66 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | lowercase | 3 | 126 | 66 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | leet_decode | 3 | 126 | 66 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | collapse_repetition | 3 | 126 | 66 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | expand_emoji | 3 | 127 | 67 | 1.0079 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | expand_slang | 3 | 126 | 65 | 1.0000 | 0.9848 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | keep_hashtag_content | 3 | 126 | 66 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | remove_hashtag | 3 | 126 | 66 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | remove_url | 3 | 126 | 66 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | remove_mention | 3 | 125 | 65 | 0.9921 | 0.9848 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | remove_punctuation | 3 | 126 | 66 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | remove_emoji | 3 | 126 | 66 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | full_normalize | 3 | 127 | 65 | 1.0079 | 0.9697 |
| label__agreement_band__topic | 1\|unanimous\|Tionghoa, Rohingya | existing_cleaner | 3 | 125 | 65 | 0.9921 | 0.9848 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | raw | 59 | 2370 | 1133 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | lowercase | 59 | 2370 | 1133 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | leet_decode | 59 | 2370 | 1132 | 1.0000 | 0.9956 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | collapse_repetition | 59 | 2370 | 1132 | 1.0000 | 0.9965 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | expand_emoji | 59 | 2390 | 1137 | 1.0084 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | expand_slang | 59 | 2372 | 1130 | 1.0008 | 0.9921 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | keep_hashtag_content | 59 | 2370 | 1133 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | remove_hashtag | 59 | 2334 | 1109 | 0.9848 | 0.9788 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | remove_url | 59 | 2370 | 1133 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | remove_mention | 59 | 2368 | 1132 | 0.9992 | 0.9991 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | remove_punctuation | 59 | 2370 | 1133 | 1.0000 | 1.0000 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | remove_emoji | 59 | 2309 | 1102 | 0.9743 | 0.9691 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | full_normalize | 59 | 2398 | 1125 | 1.0118 | 0.9762 |
| label__agreement_band__topic | 1\|unanimous\|UNKNOWN | existing_cleaner | 59 | 2332 | 1108 | 0.9840 | 0.9779 |

## Marker retention

| variant | label_rate | raw_label_rate | label_delta | word_count_rate | raw_word_count_rate | word_count_delta | char_count_rate | raw_char_count_rate | char_count_delta | has_url_rate | raw_has_url_rate | has_url_delta | has_mention_rate | raw_has_mention_rate | has_mention_delta | has_hashtag_rate | raw_has_hashtag_rate | has_hashtag_delta | has_exclamation_rate | raw_has_exclamation_rate | has_exclamation_delta | has_question_rate | raw_has_question_rate | has_question_delta | has_emoji_or_symbol_rate | raw_has_emoji_or_symbol_rate | has_emoji_or_symbol_delta | has_repeated_character_rate | raw_has_repeated_character_rate | has_repeated_character_delta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| raw | 0.1404 | 0.1404 | 0.0000 | 44.2699 | 44.2699 | 0.0000 | 309.9632 | 309.9632 | 0.0000 | 0.0304 | 0.0304 | 0.0000 | 0.1164 | 0.1164 | 0.0000 | 0.2666 | 0.2666 | 0.0000 | 0.1055 | 0.1055 | 0.0000 | 0.1033 | 0.1033 | 0.0000 | 0.8653 | 0.8653 | 0.0000 | 0.1573 | 0.1573 | 0.0000 |
| lowercase | 0.1404 | 0.1404 | 0.0000 | 44.2705 | 44.2699 | 0.0006 | 309.9639 | 309.9632 | 0.0006 | 0.0310 | 0.0304 | 0.0006 | 0.1164 | 0.1164 | 0.0000 | 0.2666 | 0.2666 | 0.0000 | 0.1055 | 0.1055 | 0.0000 | 0.1033 | 0.1033 | 0.0000 | 0.8653 | 0.8653 | 0.0000 | 0.1581 | 0.1573 | 0.0008 |
| leet_decode | 0.1404 | 0.1404 | 0.0000 | 44.2579 | 44.2699 | -0.0120 | 309.9639 | 309.9632 | 0.0006 | 0.0310 | 0.0304 | 0.0006 | 0.1071 | 0.1164 | -0.0093 | 0.2552 | 0.2666 | -0.0114 | 0.1046 | 0.1055 | -0.0009 | 0.1033 | 0.1033 | 0.0000 | 0.8635 | 0.8653 | -0.0018 | 0.1587 | 0.1573 | 0.0014 |
| collapse_repetition | 0.1404 | 0.1404 | 0.0000 | 44.2699 | 44.2699 | 0.0000 | 309.1256 | 309.9632 | -0.8376 | 0.0275 | 0.0304 | -0.0029 | 0.1164 | 0.1164 | 0.0000 | 0.2666 | 0.2666 | 0.0000 | 0.1055 | 0.1055 | 0.0000 | 0.1033 | 0.1033 | 0.0000 | 0.8653 | 0.8653 | 0.0000 | 0.0000 | 0.1573 | -0.1573 |
| expand_emoji | 0.1404 | 0.1404 | 0.0000 | 44.6660 | 44.2699 | 0.3961 | 312.6958 | 309.9632 | 2.7325 | 0.0304 | 0.0304 | 0.0000 | 0.1164 | 0.1164 | 0.0000 | 0.2666 | 0.2666 | 0.0000 | 0.1055 | 0.1055 | 0.0000 | 0.1033 | 0.1033 | 0.0000 | 0.8426 | 0.8653 | -0.0227 | 0.1424 | 0.1573 | -0.0149 |
| expand_slang | 0.1404 | 0.1404 | 0.0000 | 44.2846 | 44.2699 | 0.0147 | 311.1540 | 309.9632 | 1.1908 | 0.0304 | 0.0304 | 0.0000 | 0.1164 | 0.1164 | 0.0000 | 0.2666 | 0.2666 | 0.0000 | 0.1055 | 0.1055 | 0.0000 | 0.1033 | 0.1033 | 0.0000 | 0.8653 | 0.8653 | 0.0000 | 0.1573 | 0.1573 | 0.0000 |
| keep_hashtag_content | 0.1404 | 0.1404 | 0.0000 | 44.2488 | 44.2699 | -0.0211 | 308.3192 | 309.9632 | -1.6440 | 0.0304 | 0.0304 | 0.0000 | 0.1167 | 0.1164 | 0.0002 | 0.0001 | 0.2666 | -0.2665 | 0.1055 | 0.1055 | 0.0000 | 0.1033 | 0.1033 | 0.0000 | 0.8468 | 0.8653 | -0.0185 | 0.1573 | 0.1573 | 0.0000 |
| remove_hashtag | 0.1404 | 0.1404 | 0.0000 | 42.6259 | 44.2699 | -1.6440 | 291.9735 | 309.9632 | -17.9897 | 0.0304 | 0.0304 | 0.0000 | 0.1164 | 0.1164 | 0.0000 | 0.0000 | 0.2666 | -0.2666 | 0.1055 | 0.1055 | 0.0000 | 0.1033 | 0.1033 | 0.0000 | 0.8464 | 0.8653 | -0.0189 | 0.3197 | 0.1573 | 0.1624 |
| remove_url | 0.1404 | 0.1404 | 0.0000 | 43.9559 | 44.2699 | -0.3140 | 307.8827 | 309.9632 | -2.0805 | 0.0001 | 0.0304 | -0.0302 | 0.1162 | 0.1164 | -0.0002 | 0.2666 | 0.2666 | -0.0001 | 0.1055 | 0.1055 | 0.0000 | 0.1017 | 0.1033 | -0.0016 | 0.8642 | 0.8653 | -0.0011 | 0.1592 | 0.1573 | 0.0019 |
| remove_mention | 0.1404 | 0.1404 | 0.0000 | 44.0005 | 44.2699 | -0.2694 | 307.0418 | 309.9632 | -2.9214 | 0.0304 | 0.0304 | 0.0000 | 0.0000 | 0.1164 | -0.1164 | 0.2666 | 0.2666 | 0.0000 | 0.1055 | 0.1055 | 0.0000 | 0.1033 | 0.1033 | 0.0000 | 0.8571 | 0.8653 | -0.0082 | 0.2029 | 0.1573 | 0.0456 |
| remove_punctuation | 0.1404 | 0.1404 | 0.0000 | 44.2699 | 44.2699 | 0.0000 | 309.9632 | 309.9632 | 0.0000 | 0.0000 | 0.0304 | -0.0304 | 0.0000 | 0.1164 | -0.1164 | 0.0000 | 0.2666 | -0.2666 | 0.0000 | 0.1055 | -0.1055 | 0.0000 | 0.1033 | -0.1033 | 0.0679 | 0.8653 | -0.7973 | 0.5199 | 0.1573 | 0.3626 |
| remove_emoji | 0.1404 | 0.1404 | 0.0000 | 43.8999 | 44.2699 | -0.3700 | 307.3429 | 309.9632 | -2.6204 | 0.0304 | 0.0304 | 0.0000 | 0.1165 | 0.1164 | 0.0000 | 0.2668 | 0.2666 | 0.0001 | 0.1055 | 0.1055 | 0.0000 | 0.1033 | 0.1033 | 0.0000 | 0.8259 | 0.8653 | -0.0394 | 0.1428 | 0.1573 | -0.0145 |
| full_normalize | 0.1404 | 0.1404 | 0.0000 | 44.6481 | 44.2699 | 0.3782 | 311.4106 | 309.9632 | 1.4474 | 0.0277 | 0.0304 | -0.0027 | 0.1071 | 0.1164 | -0.0093 | 0.2552 | 0.2666 | -0.0114 | 0.1046 | 0.1055 | -0.0009 | 0.1033 | 0.1033 | 0.0000 | 0.8403 | 0.8653 | -0.0250 | 0.0000 | 0.1573 | -0.1573 |
| existing_cleaner | 0.1404 | 0.1404 | 0.0000 | 42.0437 | 44.2699 | -2.2262 | 272.4312 | 309.9632 | -37.5320 | 0.0000 | 0.0304 | -0.0304 | 0.0000 | 0.1164 | -0.1164 | 0.0000 | 0.2666 | -0.2666 | 0.0000 | 0.1055 | -0.1055 | 0.0000 | 0.1033 | -0.1033 | 0.0515 | 0.8653 | -0.8138 | 0.0796 | 0.1573 | -0.0777 |

## Reading

- High `toxic_top_overlap` + vocabulary collapse = safe normalization.
- Low `toxic_top_overlap` = the variant removes or rewrites toxic cues.
- Removing hashtags or punctuation must be checked against KWIC before adoption.

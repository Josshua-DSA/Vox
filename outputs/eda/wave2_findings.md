# IndoToxic EDA Findings — Wave 2

Status: exploratory lexical/context checkpoint

## Method

- Lexical contrast uses document-presence log-odds with additive smoothing 0.5.
- Results are separated into `all`, `unanimous`, and `borderline` subsets.
- N-grams use document rates, not raw token totals.
- Comma-separated topics are expanded as membership for analysis only.
- KWIC preserves raw sentence evidence for manual review.

## Evidence summary

### All lexical contrast

- Rows: 10,234
- Toxic-associated: `kontol`, `bego`, `pengecut`, `kadrun`, `bangsat`, `tolol`, `pesek`, `wahabi`, `iblis`, `kesesatan`
- Non-toxic-associated: `jp`, `2d`, `whatsapp`, `order`, `200`, `night`, `shio`, `hubungi`, `colok`, `balai`

### Unanimous lexical contrast

- Rows: 9,804
- Toxic-associated: `tolol`, `pesek`, `wahabi`, `kadrun`, `sesat`, `laknatullah`, `bid`, `dajjal`, `neraka`, `sunnah`
- Non-toxic-associated: `shio`, `result`, `september`, `prediksi`, `senin`, `togel`, `pemenang`, `jp`, `kesehatan`, `28`

### Borderline lexical contrast

- Rows: 1,250
- Toxic-associated: `kadrun`, `pesek`, `yaman`, `sadar`, `kitab`, `dg`, `lawan`, `laknatullah`, `biadab`, `pendukung`
- Non-toxic-associated: `com`, `selatan`, `tempat`, `4`, `membawa`, `pranowo`, `6`, `9`, `pengungsi`, `liat`

### N-gram context

- Agreement-band rows: 3,008
- Topic-membership rows: 2,137
- Inspect support counts and KWIC before treating n-grams as toxic cues.

### KWIC

- Evidence rows: 300
- Check insult, quotation, negation, and topic-dependent usage manually.

## Next experiment

- Keep punctuation, hashtag content, emoji, and repetition as parallel variants.
- Compare variants within unanimous and borderline subsets.
- Do not turn lexical log-odds into an automatic removal list.

# Architecture Specification – Context‑Aware Dual‑Input Multi‑Kernel CNN

## 1. Text branch

- **Input**: token id sequence `t ∈ ℕ^{L}` (padded/truncated to fixed length `L`).
- **Embedding**:
  - Option 1 – trainable: `E` dimensions (e.g., `E = 300`).
  - Option 2 – pre‑trained FastText: load FastText matrix `W_fast ∈ ℝ^{V×E}` (freeze or fine‑tune).
  - Output `X ∈ ℝ^{L×E}`.
- **Parallel Conv1D** (kernel sizes `k ∈ {3,4,5}`, filters `F = 128`):
  - For each `k`:
    - `Z_k = relu(conv1d(X, W_k) + b_k)` where `W_k ∈ ℝ^{k×E×F}`.
    - Shape `Z_k ∈ ℝ^{(L‑k+1)×F}`.
    - `g_k = max_{i=1..L‑k+1} Z_k[i,:]` → `g_k ∈ ℝ^{F}`.
- **Concatenation**: `g = concat(g_3, g_4, g_5) ∈ ℝ^{3F}=ℝ^{384}`.
- **Result**: `Text_Vec = g` (batch dimension omitted for brevity).

## 2. Topic metadata branch

- **Input**: integer topic id `c ∈ {0,…,N‑1}`.
- **Categorical Embedding**: `E_t ∈ ℤ^{d}` → `y = embed_topic(c) ∈ ℝ^{d}` where `d ∈ [16,32]` (choose 32).
- **Optional Dense** (if richer transformation needed): `y' = relu(W_t y + b_t)` with `W_t ∈ ℝ^{d'×d}` (e.g., `d'=32`).
- **Result**: `Topic_Vec = y` (or `y'`).

## 3. Fusion layer

- **Concatenate**: `h = concat(Text_Vec, Topic_Vec) ∈ ℝ^{384+d}` (e.g., `384+32 = 416`).
- **Dropout**: `h_drop = Dropout(p=0.5)(h)`.
- **Dense hidden**: `u = relu(W_h h_drop + b_h)` with `W_h ∈ ℝ^{128×(384+d)}` → `u ∈ ℝ^{128}`.

## 4. Output heads

### Binary head (single‑label)
- `p = sigmoid(w_bᵀ u + b_b)` → scalar probability.
- Loss: `binary_crossentropy`.

### Multi‑label head (5 sub‑labels)
- `p_i = sigmoid(w_iᵀ u + b_i)` for `i = 1..5` → vector `p ∈ ℝ^{5}`.
- Loss: `binary_crossentropy` per label (or `sigmoid_focal` if needed).

## Tensor‑flow style pseudo‑code (Keras)
```python
# Text input
text_input = Input(shape=(L,), dtype='int32', name='text')
if use_fasttext:
    embed = Embedding(input_dim=V, output_dim=E,
                      weights=[fasttext_matrix], trainable=ft_trainable)(text_input)
else:
    embed = Embedding(input_dim=V, output_dim=E)(text_input)
# Parallel convs
conv_outputs = []
for k in (3,4,5):
    conv = Conv1D(filters=128, kernel_size=k, activation='relu')(embed)
    pool = GlobalMaxPooling1D()(conv)
    conv_outputs.append(pool)
text_vec = Concatenate()(conv_outputs)  # shape (384,)

# Topic input
topic_input = Input(shape=(1,), dtype='int32', name='topic')
topic_emb = Embedding(input_dim=N, output_dim=d)(topic_input)
# optionally: topic_vec = Dense(32, activation='relu')(Flatten()(topic_emb))
topic_vec = Flatten()(topic_emb)  # shape (d,)

# Fusion
fusion = Concatenate()([text_vec, topic_vec])
fusion = Dropout(0.5)(fusion)
fusion = Dense(128, activation='relu')(fusion)

# Heads
binary_out = Dense(1, activation='sigmoid', name='binary')(fusion)
multilabel_out = Dense(5, activation='sigmoid', name='multilabel')(fusion)

model = Model(inputs=[text_input, topic_input], outputs=[binary_out, multilabel_out])
```

**Key dimensions**
- `L` – max token length (e.g., 200).
- `V` – vocab size (e.g., 50 k).
- `E` – embedding dim (300).
- `F` – filters per kernel (128).
- `d` – topic embedding dim (32).
- Fusion dim before dense = `384 + d`.
- Hidden dense = 128.

**Formulas**
- `X = Embedding(t)`
- `g_k = max_{i} relu(X[i:i+k]·W_k + b_k)`
- `g = [g_3; g_4; g_5]`
- `y = Embedding_topic(c)`
- `h = [g; y]`
- `u = relu(W_h h + b_h)`
- `p_binary = σ(w_bᵀ u + b_b)`
- `p_multi_i = σ(w_iᵀ u + b_i)`

---
**Use**: feed tokenized Indonesian text (FastText pretrained on ID) and integer topic id (e.g., tweet category). Model learns joint representation.
```
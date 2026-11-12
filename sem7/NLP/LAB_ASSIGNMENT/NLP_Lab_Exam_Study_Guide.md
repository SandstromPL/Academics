# NLP Lab Exam — Complete Study Guide (Labs 1–12)

Built from your own submissions, the blank templates, and the instructor tutorials in `LAB_ASSIGNMENT/01 … 12`.
All code below is copied from your **correct submissions** (prints, plots and docstrings trimmed).

**How to read this guide**
- Every lab has the same six parts: **N.1** what it is → **N.2** concepts and formulas → **N.3** data pipeline → **N.4 exam-critical code** → **N.5 fill-in-the-blank practice** → **N.6 quick recall**.
- In N.4, **★★★** = most likely to be blanked, **★★** = likely, **★** = good to know.
- "TEMPLATE BLANK" / "TODO BLANK" marks code that was **empty in the original assignment template**. Those are the strongest predictors of what the exam will blank out.
- `# <-- KEY` comments mark the single lines most likely to be removed.

**If you only have…**
- **30 minutes:** read Part 0 (this page) and then every lab's **N.6 Quick recall**.
- **2 hours:** add all the **★★★** blocks in N.4, then try the N.5 blanks without looking.
- **More:** do everything, top to bottom.

---

## 0.1 Course map

| Lab | Topic | Framework | The thing you must be able to write by hand |
|---|---|---|---|
| 1 | Spelling correction, noisy channel | pure Python + `re` | Levenshtein DP table; `argmax_c P(w\|c)·P(c)` |
| 2 | Trigram LM: Add-k, interpolation, perplexity | pure Python | n-gram extraction, add-k prob, log-prob sum, `2 ** (-L/N)` |
| 3 | CFG→CNF, CKY, PCFG/Viterbi, spaCy deps | Python + NLTK + spaCy | CKY triple loop (`length → i → k`) |
| 4 | MST dependency parsing, Chu-Liu/Edmonds, structured perceptron | pure Python | best-incoming → detect cycle → contract → recurse → expand; `w += Φ(gold) − Φ(pred)` |
| 5 | BoW → GloVe → Word2Vec (CBOW, Skip-gram) | **NumPy** (+gensim) | context pairs, forward/softmax/CE, gradients `outer(h, e)`, cosine |
| 6 | RNN LM vs fixed-window NLM vs bigram, perplexity | **PyTorch** | sliding windows, `nn.Embedding → nn.RNN → nn.Linear`, train loop, `exp(mean NLL)` |
| 7 | SimpleRNN/LSTM sentiment + POS tagging | **Keras** (Sequential) | `Embedding(mask_zero) → LSTM(return_sequences) → TimeDistributed(Dense)`, masked accuracy |
| 8 | Char-level LSTM encoder–decoder NMT (EN→DE) | **Keras** (Functional) | `return_state`, `initial_state`, teacher-forcing shift, inference models, greedy/beam decode |
| 9 | Fine-tune MarianMT (EN→DE), BLEU, attention viz | **HuggingFace** + PyTorch | `text_target` tokenization, `compute_metrics` with −100, `Seq2SeqTrainer`, `generate` |
| 10 | Attention & MHA from scratch, encoder block, BERT on SST-2 | **PyTorch** + HF | `softmax(QKᵀ/√d_k)V`, split/merge heads, sinusoidal PE, Post-LN block, `Trainer` |
| 11 | Coreference (FCoref) + extractive QA (SQuAD) | HF + fastcoref + spaCy | best span over start/end logits, B³, EM / token-F1 |
| 12 | Mixture of Experts inside a Transformer | **PyTorch** | noisy top-k router, sparse dispatch with `index_add_`, load-balancing loss, capacity |

---

## 0.2 The top-15 blocks to be able to write from a blank page

If you can write these without looking, you can cover most of the exam.

1. **Edit distance DP** (Lab 1, §1.4 Block B): `dp[i][0]=i`, `dp[0][j]=j`; match → diagonal, else `1 + min(up, left, diag)`.
2. **Add-k trigram probability + sentence log-prob + perplexity** (Lab 2, §2.4 C–E): `(C(w1w2w3)+k)/(C(w1w2)+k·V)`; `PP = 2 ** (-L/N)`.
3. **Linear interpolation** (Lab 2, §2.4 F): `λ1·P(w3|w1,w2) + λ2·P(w3|w2) + λ3·P(w3)`, built from raw MLE pieces.
4. **CKY recognizer** (Lab 3, §3.4.1): `for length in range(2,n+1): for i in range(n-length+1): j=i+length; for k in range(i+1,j)`.
5. **Chu-Liu/Edmonds pieces** (Lab 4, §4.4.3–4.4.7): best incoming per node, cycle detection, the contraction score `w(u→v) + W_C − w(parent(v)→v)`.
6. **Structured perceptron update** (Lab 4, §4.4.9–4.4.10): predict with CLE, and on a mistake `w += Φ(gold) − Φ(pred)`.
7. **CBOW forward + backward** (Lab 5, §5.4 B–C): `h = mean(W1[ctx])`, `y_hat = softmax(h @ W2)`, `e = y_hat − y`, `dW2 = outer(h, e)`, `dh = W2 @ e`.
8. **Cosine similarity / most_similar** (Lab 5, §5.4 F).
9. **RNN LM class + PyTorch training loop + perplexity** (Lab 6, §6.4 B–D): `zero_grad → forward → loss → backward → clip → step`; `PP = exp(total_loss / N)`.
10. **Keras LSTM tagger** (Lab 7, §7.4 B): `Embedding(V, d, mask_zero=True) → LSTM(u, return_sequences=True) → TimeDistributed(Dense(n_tags+1, softmax))`.
11. **Seq2seq encoder–decoder + inference** (Lab 8, §8.4 B–E): teacher-forcing shift, `return_state`, `initial_state=encoder_states`, reuse trained layers, the greedy decode loop.
12. **HF seq2seq fine-tuning** (Lab 9, §9.4 A–D): `tokenizer(text_target=...)`, `labels`, −100 → pad before decoding, sacreBLEU with `[[ref]]`.
13. **Scaled dot-product attention + multi-head attention** (Lab 10, §10.4 A–B): `masked_fill(mask==0, -1e9)` **before** softmax; `view(B,T,h,d_k).transpose(1,2)`, then `transpose(1,2).reshape(B,T,d)`.
14. **QA best span** (Lab 11, §11.4 A): only context tokens (`sequence_ids == 1`), `s ≤ e`, length cap, score = `start[s] + end[e]`, then slice by `offset_mapping`.
15. **MoE router + dispatch + load-balancing loss** (Lab 12, §12.4 A–C): `topk` → `full_like(-inf).scatter` → softmax; `index_add_`; `N · Σ fᵢ·Pᵢ`.

---

## 0.3 Patterns that repeat across labs (learn once, use many times)

### (a) Vocabulary and ids (Labs 5, 6, 7, 8)
| Lab | Convention |
|---|---|
| 5 | `vocab = sorted(set(tokens))`; `word_to_int = {w:i for i,w in enumerate(vocab)}`; `int_to_word` is the reverse |
| 6 | vocab from the **train split only**, `"<unk>"` at index 0; lookups use `dict.get(tok, unk_idx)` |
| 7 | `<pad>` = 0, `<unk>` = 1, real words start at 2; tags start at 1; output units = `len(tags) + 1` |
| 8 | character vocab, `'\t'` = start, `'\n'` = end; one-hot input, so there is **no Embedding layer** |

### (b) Perplexity: same idea, two bases
| Lab | Formula used in the code | Note |
|---|---|---|
| 2 | `L = Σ log2 p`; `PP = 2 ** (-L / N)`; N = words + 1 (counts `</s>`, not `<s>`) | `-inf` log-prob → PP = `inf` |
| 6 | `PP = float(np.exp(total_loss / total_tokens))`, where `total_loss += loss.item() * x_batch.size(0)` | PyTorch CE uses ln, so use `exp`, not `2**` |
| 6 (bigram) | add-one: `(C(prev,w) + 1) / (C(prev) + V)` | uniform model → PP = V |

### (c) Softmax + cross-entropy (Labs 5, 6, 7, 8, 10, 12)
- Stable softmax (Lab 5): `e = np.exp(x - np.max(x)); return e / e.sum()`.
- CE for one example (Lab 5): `-np.log(y_hat[target] + 1e-12)`. At initialisation the loss is about `ln V`.
- PyTorch `nn.CrossEntropyLoss()(logits, targets)` takes **raw logits** (it applies log-softmax itself) and **long** targets.
- Keras: one sigmoid unit → `binary_crossentropy`; integer labels → `sparse_categorical_crossentropy`; one-hot labels → `categorical_crossentropy`.

### (d) The PyTorch training loop (Labs 6, 10)
```python
model.train()
for x_batch, y_batch in batches:
    optimizer.zero_grad()          # 1
    logits = model(x_batch)        # 2
    loss = criterion(logits, y_batch)   # 3  (input, target), in that order
    loss.backward()                # 4
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # 5 (RNNs), between backward and step
    optimizer.step()               # 6
# eval: model.eval(); with torch.no_grad(): ...
```

### (e) Keras recurrent layer flags (Labs 7, 8)
| You need | Write | Output shape |
|---|---|---|
| one vector per sentence (classification) | `LSTM(u)` | `(n, u)` |
| one vector per token (tagging, decoder) | `LSTM(u, return_sequences=True)` | `(n, T, u)` |
| the final states (encoder) | `LSTM(u, return_state=True)` | `[out, h, c]` |
| decoder that starts from the encoder | `decoder_lstm(x, initial_state=[h, c])` | — |
| the same Dense layer at every time step | `TimeDistributed(Dense(k, activation='softmax'))` | `(n, T, k)` |

### (f) The HuggingFace recipe (Labs 9, 10, 11)
```
AutoTokenizer.from_pretrained(name)  +  AutoModelFor<Task>.from_pretrained(name, ...)
   → dataset.map(tokenize_fn, batched=True, remove_columns=[...])
   → DataCollator (ForSeq2Seq | WithPadding)
   → (Seq2Seq)TrainingArguments(output_dir, eval_strategy="epoch", learning_rate=2e-5, ...)
   → (Seq2Seq)Trainer(model, args, train_dataset, eval_dataset, data_collator, compute_metrics)
   → .train() / .evaluate() / .predict()
```
| Task | `AutoModelFor…` | compute_metrics receives | Metric |
|---|---|---|---|
| MT (Lab 9) | `Seq2SeqLM` | generated ids, labels with −100 | sacreBLEU, references as `[[ref]]` |
| Sentiment (Lab 10) | `SequenceClassification(num_labels=2)` | logits, labels | `argmax(-1)` → accuracy |
| QA (Lab 11) | `QuestionAnswering` (inference only) | — | EM, token F1 |

### (g) Dynamic programming and graph algorithms (Labs 1, 3, 4)
| Algorithm | Table / structure | Fill order | Answer |
|---|---|---|---|
| Edit distance | `(m+1)×(n+1)` | row by row | `dp[m][n]` |
| CKY | `chart[i][j]` = set of non-terminals covering `words[i:j]` | by span length | `start in chart[0][n]` |
| Chu-Liu/Edmonds | `{dep: head}` greedy picks | recursive contraction | sum of arc scores |
| BFS (spaCy dependency path) | `deque` of `(node, path)` | FIFO | first time the target is reached |

### (h) Picking the best output (Labs 1, 8, 9, 11, 12)
- `max(cands, key=score)` gives the argmax (Lab 1).
- Greedy decoding: `np.argmax(output_tokens[0, -1, :])` each step until `'\n'` or the length cap (Lab 8).
- Beam search: keep the top k by summed `log p`; normalise the final pick by `len ** α` (Lab 8).
- `model.generate(**batch, num_beams=4)` → `batch_decode(skip_special_tokens=True)` (Lab 9).
- Best QA span: maximise `start[s] + end[e]` subject to `s ≤ e` and the length cap (Lab 11).
- Router: `logits.topk(k, dim=-1)` (Lab 12).

---

## 0.4 Metrics cheat sheet

| Metric | Lab | Definition |
|---|---|---|
| Perplexity | 2, 6 | $PP = P(w_1..w_N)^{-1/N}$; lower is better |
| Accuracy (masked) | 7 | `mask = y != 0; (pred[mask] == y[mask]).mean()` |
| BLEU | 9 | sacreBLEU corpus score 0–100: n-gram precision × brevity penalty |
| EM | 11 | `int(any(normalize(pred) == normalize(g) for g in golds))` |
| Token F1 | 11 | bag-of-words overlap (`Counter &`), max over the gold answers |
| B³ | 11 | per mention: P = \|sys ∩ gold\| / \|sys\|, R = \|sys ∩ gold\| / \|gold\|; average over mentions |
| CoNLL F1 | 11 | average of MUC, B³, CEAF-e |
| LB loss / CV | 12 | `N · Σ fᵢ·Pᵢ` (1 = balanced, N = collapsed); CV of expert load is used only for evaluation |

---

## 0.5 Gotchas that cost marks (one line each)

1. Trigram padding: **two** `<s>` and **one** `</s>`. Your code writes these as `"<.s>"` and `"<./s>"`.
2. Add-k denominator: `C(w1,w2) + k·V`, not `+ k`. The history count is the **bigram** count.
3. Edit distance compares `s1[i-1]` with `s2[j-1]`: the table is shifted by one from the string.
4. CKY split point: `k in range(i+1, j)`, never `i` or `j`.
5. CLE expansion keeps every cycle arc **except** the one into the node where the external arc enters.
6. Word2Vec: `dW2 = np.outer(h, e)` has shape (d, V); in CBOW each context row gets `dh / m`.
7. PyTorch: `zero_grad` first; clip **after** `backward` and **before** `step`; accumulate `loss.item() * batch_size`.
8. `nn.RNN(batch_first=True)` makes `out` batch-first, but `h_n` is **always** `(layers, B, H)`. Take `out[:, -1, :]`, not `out[-1]`.
9. Keras tagging: `padding='post'`, `mask_zero=True`, `return_sequences=True`, and output units = `len(tags) + 1`.
10. Seq2seq target shift: `decoder_target[i, t-1] = decoder_input[i, t]` (the target is the input moved one step left).
11. In inference, **reuse** the trained `decoder_lstm` / `decoder_dense` objects; do not create new layers.
12. HF seq2seq labels: replace `-100` with `pad_token_id` **before** `batch_decode`; sacreBLEU references are a list of lists.
13. Attention mask: `masked_fill(mask == 0, -1e9)` **before** softmax; softmax over `dim=-1` (the keys).
14. Merging heads: `transpose(1, 2)` then `.reshape(...)`. `.view` fails on a non-contiguous tensor.
15. MoE: add router noise only when `self.training`; Switch argmax needs `keepdim=True`; use `index_add_`, not assignment.

---

## 0.6 Things that are *not* what you might assume

- **Lab 1:** the template's regex hint `targ="..."` matches **nothing**, because the `.dat` tags are unquoted (`<ERR targ=word> wrong </ERR>`).
- **Lab 3:** Task 2 does **not** implement a general CFG→CNF converter. It binarizes one PCFG rule by hand (`VP → V NP PP` becomes `VP → V VP_PP` + `VP_PP → NP PP [1.0]`). The START/TERM/BIN/DEL/UNIT steps are covered as theory only.
- **Lab 5:** there is **no TF-IDF** in your notebooks; the guide adds a short note on it anyway. Lab 5 is pure **NumPy**, not Keras or PyTorch. Your corpus is *Alice in Wonderland* (`pg11.txt`).
- **Lab 6:** uses **sliding windows** (5 words predict the next one, from the last RNN step), not the `x = seq[:-1], y = seq[1:]` setup.
- **Lab 8:** **character-level**, one-hot input, **no attention, no BLEU, no Embedding layer**. Beam search is the extension task.
- **Lab 11:** QA is **inference only** with `deepset/bert-base-cased-squad2`; nothing is fine-tuned. The SQuAD training-label loop is included as background (★) in case it is asked.
- **Lab 12:** capacity uses **floor** (`int(cf · T · k / N)`), not ceil. The load-balancing loss is the Switch `N · Σ fᵢPᵢ`; CV is only an evaluation metric.

---

## Contents
- [Lab 1 — Spelling Correction with the Noisy Channel Model](#lab-1)
- [Lab 2 — Trigram LMs: Add-k, Interpolation, Perplexity](#lab-2)
- [Lab 3 — CFG → CNF, CKY, PCFG/Viterbi, spaCy dependencies](#lab-3)
- [Lab 4 — MST Dependency Parsing, Chu-Liu/Edmonds, Structured Perceptron](#lab-4)
- [Lab 5 — BoW → Word2Vec (CBOW & Skip-gram)](#lab-5)
- [Lab 6 — RNN LM vs Fixed-Window NLM vs Bigram, Perplexity](#lab-6)
- [Lab 7 — SimpleRNN → LSTM, Classification → POS Tagging](#lab-7)
- [Lab 8 — LSTM Encoder–Decoder NMT (EN → DE)](#lab-8)
- [Lab 9 — Fine-tuning MarianMT, BLEU, Attention Visualization](#lab-9)
- [Lab 10 — Attention from Scratch, Transformer Encoder, BERT](#lab-10)
- [Lab 11 — Coreference Resolution & Question Answering](#lab-11)
- [Lab 12 — Mixture of Experts inside a Transformer](#lab-12)


---

<a id="lab-1"></a>

# Lab 1 — Spelling Correction with the Noisy Channel Model

## 1.1 What this lab is about

You build a tiny spell-checker. A misspelled word `w` is treated as a "noisy" version of an intended word `c`.
You read a corpus of children's essays where every spelling error is tagged with its correction, build a word-frequency
vocabulary from those tags, generate candidate corrections that are within edit distance 2, and pick the candidate that
maximises $P(w \mid c)\,P(c)$. Finally you compare against the `pyspellchecker` library.

**Template vs submission:** in the Lab 1 template, **only the Task 1 cell (data loading + regex + vocab) had TODO blanks**.
Everything else (`P_c`, `P_w_given_c`, `noisy_channel_score`, `edit_distance`, `generate_candidates`, `correct_word`,
`correct_sentence`, the comparison cell) was already written. In a paper exam any of those can be blanked, though,
and edit-distance DP is the classic hand-write question.

## 1.2 Core concepts & formulas

**Noisy channel = Bayes' rule.** We want the most probable intended word given what was typed:

$$\hat c = \arg\max_c P(c \mid w) = \arg\max_c \frac{P(w \mid c)\,P(c)}{P(w)} = \arg\max_c P(w \mid c)\,P(c)$$

$P(w)$ is the same for every candidate, so it is dropped (it does not change the argmax).

| Piece | Name | How this lab estimates it |
|---|---|---|
| $P(c)$ | language model / prior | $\dfrac{\text{count}(c)}{\sum_x \text{count}(x)}$ from the `vocab` Counter |
| $P(w \mid c)$ | error / channel model | $\dfrac{1}{\text{edit\_distance}(w,c) + 1}$ (a heuristic; not a normalised distribution, but fine for ranking) |

Why `+1`: if $d = 0$ we would divide by zero; with `+1`, $d=0 \to 1$, $d=1 \to 0.5$, $d=2 \to 0.333$.

**Levenshtein edit distance** = minimum number of single-character **insertions, deletions, substitutions** (each cost 1)
to turn `s1` into `s2`. A transposition (`ei` ↔ `ie`) costs **2** here (two substitutions).

DP table `dp` of size $(m+1)\times(n+1)$, where `dp[i][j]` = distance between the first `i` chars of `s1` and the first `j` chars of `s2`:

$$dp[i][0] = i, \quad dp[0][j] = j$$

$$dp[i][j] = \begin{cases} dp[i-1][j-1] & \text{if } s_1[i-1] = s_2[j-1] \\ 1 + \min\big(dp[i-1][j],\ dp[i][j-1],\ dp[i-1][j-1]\big) & \text{otherwise} \end{cases}$$

- `dp[i-1][j]` → **deletion** (drop `s1[i-1]`), `dp[i][j-1]` → **insertion**, `dp[i-1][j-1]` → **substitution**.
- Answer is `dp[m][n]` (bottom-right cell).

**Worked example (computed on this code): `edit_distance("wach", "watch")`** — rows = `s1`, columns = `s2`:

```
        ""  w  a  t  c  h
   ""    0  1  2  3  4  5
   w     1  0  1  2  3  4
   a     2  1  0  1  2  3
   c     3  2  1  1  1  2
   h     4  3  2  2  2  1   <- dp[4][5] = 1  (insert 't')
```

So $P(\text{wach} \mid \text{watch}) = 1/(1+1) = 0.5$.

**Worked noisy-channel example (real numbers from this dataset; total vocab count = 5130):**

| typed `w` | candidate `c` | dist | count(c) | $P(w\mid c)\cdot P(c)$ | |
|---|---|---|---|---|---|
| `sloowly` | `slowly` | 1 | 1 | $\frac12 \cdot \frac{1}{5130} = 9.7\times10^{-5}$ | **wins** |
| `sloowly` | `slolly` | 2 | 1 | $\frac13 \cdot \frac{1}{5130} = 6.5\times10^{-5}$ | |
| `freind` | `frend` | 1 | 3 | $\frac12 \cdot \frac{3}{5130} = 2.92\times10^{-4}$ | **wins** (wrong!) |
| `freind` | `friend` | 2 | 4 | $\frac13 \cdot \frac{4}{5130} = 2.60\times10^{-4}$ | |
| `good` | `too` | 2 | 27 | $\frac13 \cdot \frac{27}{5130} = 1.75\times10^{-3}$ | **wins** (wrong!) |

Lessons: (1) the transposition `ei→ie` costs 2, so `friend` loses; (2) `vocab` also contains *misspellings* (`frend`),
so the model can "correct" to a wrong word; (3) `good` is not in `vocab` at all (vocab only has words that appear inside
`<ERR>` tags), so a correct word gets "fixed" to a frequent neighbour. The flat error model (only 3 possible values)
lets the prior $P(c)$ dominate.

## 1.3 Data & pipeline

**Dataset:** `holbrook-tagged-1.dat` (Holbrook corpus of children's writing), 1530 lines, **latin-1** encoded (not UTF-8).
Errors are inline XML-like tags. The `targ` value is **unquoted** in this file, with spaces around the wrong word:

```
My <ERR targ=sister> siter </ERR> <ERR targ=goes> go </ERR> to Tonbury.
I <ERR targ=watch> wach </ERR> TV there is BBC and I.T.V.
On thursday nights I go <ERR targ=bellringing> bell ringing </ERR> ...
```

Note: the targ can contain spaces (e.g. `targ=Comment allez-vous`) and the wrong text can be several words (`some times`).

**Pipeline (in order):**
1. Upload / locate the file (Colab `files.upload()` returns `{filename: bytes}`).
2. `open(..., encoding="latin-1")` and `f.read()` the whole text.
3. `re.findall` with the ERR regex → list of `(correct, wrong)` pairs.
4. Build `vocab = Counter()`: for every pair, add **both** `correct` and `wrong`, each `.lower().strip()`.
5. $P(c)$ = count / total; $P(w\mid c) = 1/(d+1)$.
6. `generate_candidates(w, max_dist=2)`: brute-force scan of every vocab word, keep those with distance ≤ 2.
7. `correct_word`: if already in vocab → return it; else argmax of the noisy-channel score over candidates.
8. `correct_sentence`: regex-tokenise into words / punctuation / whitespace, correct only words, `"".join` back.
9. Compare against `SpellChecker().correction(word)`.

**Key values / outputs:** `max_dist = 2`; 2565 annotations found; vocab size 2569 types; sum of counts 5130.
Example vocab entries: `('sister', 4), ('siter', 2), ('go', 23), ('some times', 4)`.

## 1.4 Exam-critical code blocks

### ★★★ Block A — Load data, regex-extract pairs, build vocab (TEMPLATE BLANK)

**What it does:** reads the corpus and turns every `<ERR targ=X> Y </ERR>` into a `(correct, wrong)` pair, then counts
both spellings. **TEMPLATE BLANK** — `uploaded`, `data_path`, `encoding=`, `text`, `pattern`, and the vocab loop body
were all `...` in the template.

Submission (verbatim):

```python
from pathlib import Path
import re
from collections import Counter

try:
    from google.colab import files
except ImportError:
    files = None

data_path = Path("holbrook-tagged-1.dat")
uploaded = {}
if not data_path.exists() and files is not None:
    uploaded = files.upload()                                   # <-- KEY
    data_path = Path(next(iter(uploaded)))                      # <-- KEY  first key = filename

# The dataset uses latin-1 encoded text.
with open(data_path, "r", encoding="latin-1") as f:             # <-- KEY
    text = f.read()                                             # <-- KEY

# Match both quoted and unquoted targ attributes.
pattern = r'<ERR targ=(?:"([^"]+)"|([^\s>]+))>(.*?)</ERR>'      # <-- KEY
raw_matches = re.findall(pattern, text, flags=re.DOTALL)        # <-- KEY
matches = []
for quoted_correct, bare_correct, wrong in raw_matches:
    correct = quoted_correct or bare_correct
    matches.append((correct, wrong))

vocab = Counter()
for correct, wrong in matches:
    vocab[correct.lower().strip()] += 1                         # <-- KEY
    vocab[wrong.lower().strip()] += 1                           # <-- KEY
```

The same thing written to the **template's shape** (what a blank most likely expects):

```python
uploaded = files.upload()
data_path = next(iter(uploaded))            # the dict key is the filename
with open(data_path, 'r', encoding='latin-1') as f:
  text = f.read()
pattern = r'<ERR targ=(.*?)>(.*?)</ERR>'    # group 1 = correct, group 2 = wrong
matches = re.findall(pattern, text)
vocab = Counter()
for correct, wrong in matches:
    vocab[correct.lower().strip()] += 1
    vocab[wrong.lower().strip()] += 1
```

(I ran both patterns on the file: the two-group `(.*?)` version gives 2599 pairs; the submission's version gives 2565
because `[^\s>]+` cannot match a targ that contains a space. The template hint's quoted form `targ="(.*?)"` gives
**0** matches on this file, because the file has no quotes.)

**Line-by-line notes**
- `files.upload()` → dict `{filename: bytes}`; `next(iter(uploaded))` grabs the first key (the name), not the bytes.
- `encoding="latin-1"` — the file has non-UTF-8 bytes; the default UTF-8 raises `UnicodeDecodeError`.
- `re.findall` with **k capture groups returns a list of k-tuples**. 2 groups → `(correct, wrong)`. The submission's
  pattern has **3** groups (quoted targ, bare targ, wrong), so it unpacks 3 values and merges with `or` (an empty
  string `""` is falsy, so `quoted or bare` picks whichever matched).
- `(?: ... | ... )` is a non-capturing group; it does not add a tuple slot.
- `(.*?)` is **non-greedy**: stops at the first `</ERR>`. Greedy `(.*)` would swallow everything up to the last
  `</ERR>` on the line.
- `flags=re.DOTALL` lets `.` match `\n` too, in case a tag spans lines.
- `.strip()` matters: the wrong word is stored as `" siter "` with spaces; without strip `" siter "` ≠ `"siter"`.
- Both spellings are counted "so both are in vocab" (template hint), which is why misspellings end up as candidates.

**Common mistakes**
- Forgetting `.strip()` / `.lower()` → duplicates like `"Go"`, `" go "`, `"go"`.
- Greedy `.*` instead of `.*?`.
- Unpacking 2 values from a 3-group findall (`ValueError: too many values to unpack`).

---

### ★★★ Block B — Levenshtein edit distance (DP)

**What it does:** minimum insert/delete/substitute operations between two strings. Given in the template (not blank),
but it is the most "write it by hand" function in the lab.

```python
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]        # <-- KEY  (m+1) x (n+1)

    for i in range(m + 1):
        dp[i][0] = i                                   # <-- KEY  delete all i chars
    for j in range(n + 1):
        dp[0][j] = j                                   # <-- KEY  insert all j chars

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:                 # <-- KEY  i-1 / j-1 (table is 1-indexed)
                dp[i][j] = dp[i - 1][j - 1]            # <-- KEY  match: free diagonal
            else:
                dp[i][j] = 1 + min(                    # <-- KEY
                    dp[i - 1][j],    # deletion
                    dp[i][j - 1],    # insertion
                    dp[i - 1][j - 1] # substitution
                )
    return dp[m][n]                                    # <-- KEY
```

The template also has a NumPy variant, `calculate_edit_distance(s1, s2)`, that returns `(distance, dp)`. Same base
cases (`dp[i, 0] = i`, `dp[0, j] = j`); only the fill step differs:

```python
    dp = np.zeros((m + 1, n + 1), dtype=int)
    ...
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1 # Cost for substitution
            deletion_cost = dp[i - 1, j] + 1
            insertion_cost = dp[i, j - 1] + 1
            substitution_cost = dp[i - 1, j - 1] + cost
            dp[i, j] = min(deletion_cost, insertion_cost, substitution_cost)
    edit_distance = dp[m, n]
    return edit_distance, dp
```

**Line-by-line notes**
- Table is `(m+1) x (n+1)` because row/column 0 represent the **empty prefix**.
- `[[0]*(n+1) for _ in range(m+1)]` — never `[[0]*(n+1)]*(m+1)` (that makes m+1 references to the same row).
- Ranges for base cases go to `m + 1` / `n + 1` (inclusive of the full length).
- Fill loops start at **1**, and compare `s1[i-1]`, `s2[j-1]` because `dp` index `i` means "first i characters".
- Version 1 adds the `+1` outside `min`; version 2 adds `+1` to deletion/insertion and `+cost` to the diagonal. Same result.

**Common mistakes**
- Comparing `s1[i] == s2[j]` (off by one; `IndexError` at the last row).
- Returning `dp[m-1][n-1]` instead of `dp[m][n]`.
- Swapping insertion/deletion labels is harmless for the number, but examiners may ask which is which: `dp[i-1][j]` = deletion.

---

### ★★★ Block C — Noisy-channel scoring and `correct_word`

**What it does:** the three model functions plus the argmax. Given in the template.

```python
def P_c(c):
    # Language model probability P(c).
    c = c.lower().strip()
    total = sum(vocab.values())                                  # <-- KEY
    return vocab.get(c, 0) / total if total else 0.0             # <-- KEY

def P_w_given_c(w, c):
    # Error model P(w|c) based on inverse edit distance.
    distance = edit_distance(w.lower().strip(), c.lower().strip())
    return 1 / (distance + 1)                                    # <-- KEY

def noisy_channel_score(w, c):
    return P_w_given_c(w, c) * P_c(c)                            # <-- KEY  P(w|c) * P(c)


def correct_word(w):
    cleaned = w.lower().strip()
    if cleaned in vocab:                                         # <-- KEY  known word: keep it
        return cleaned

    candidates = generate_candidates(cleaned)
    if not candidates:                                           # <-- KEY  nothing close: give up
        return cleaned

    return max(candidates, key=lambda candidate: noisy_channel_score(cleaned, candidate))   # <-- KEY
```

**Line-by-line notes**
- `total = sum(vocab.values())` = total **tokens** (5130), not `len(vocab)` (2569 types).
- `vocab.get(c, 0)` → 0 for unseen words (a `Counter` would also return 0 with `vocab[c]`).
- `if total else 0.0` guards division by zero on an empty vocab.
- `1 / (distance + 1)`: the `+1` avoids division by zero at distance 0.
- The score is the **product** $P(w\mid c)P(c)$; $P(w)$ is omitted (constant).
- `max(iterable, key=f)` returns the **element** with the largest `f`, not the score. This is the argmax.
- Ties: candidates are a `set`, so on equal scores the winner depends on set iteration order (this is why
  `today` became `modal` in one run; `modal` and `tod` both score $\frac13\cdot\frac{2}{5130}$).

**Common mistakes**
- Using `min` instead of `max`, or `key=noisy_channel_score` (wrong arity: key gets one argument).
- Dividing by `len(vocab)` in `P_c`.
- Writing `P_w_given_c = distance` (bigger distance should mean *smaller* probability).

---

### ★★ Block D — Candidate generation

**What it does:** returns every vocab word within `max_dist` edits of `w`. Given in template.

```python
def generate_candidates(w, max_dist=2):
    w = w.lower().strip()
    candidates = set()
    for word in vocab:                                 # <-- KEY  scan the whole vocab
        if edit_distance(w, word) <= max_dist:         # <-- KEY  <= (inclusive), default 2
            candidates.add(word)
    return candidates
```

**Notes:** brute force, cost $O(|V| \cdot m \cdot n)$. Uses `<=` so distance-2 words are included. Returns a `set`
(no duplicates). Candidates can include misspellings, because `vocab` contains wrong words too.

**Common mistakes:** `< max_dist` (drops distance-2 words); generating edits of `w` instead (that is Norvig's approach,
not this lab's).

---

### ★★ Block E — Sentence-level correction

**What it does:** splits a sentence into word / punctuation / whitespace tokens, corrects only words, and glues it back.

```python
def correct_sentence(sentence):
    tokens = re.findall(r"\w+(?:'\w+)?|[^\w\s]+|\s+", sentence)       # <-- KEY
    corrected = []
    for token in tokens:
        if token.isspace() or re.fullmatch(r"[^\w\s]+", token):        # <-- KEY  keep spaces & punctuation
            corrected.append(token)
        else:
            corrected.append(correct_word(token))
    return "".join(corrected)                                          # <-- KEY  "" not " "
```

**Notes:**
- Regex alternatives: `\w+(?:'\w+)?` = a word with optional apostrophe part (`I'll` stays one token);
  `[^\w\s]+` = run of punctuation; `\s+` = run of whitespace.
- Because whitespace is kept as tokens, joining with `""` reproduces the original spacing.
- Output is all lowercase (since `correct_word` lowercases).

**Common mistake:** `" ".join(...)` doubles the spaces; `sentence.split()` glues punctuation to words (`"today."`),
which is what the Task 5 cell does (`"today."` has no candidates and comes back unchanged).

---

### ★ Block F — Comparison with `pyspellchecker`

```python
from spellchecker import SpellChecker
spell = SpellChecker()
for sent in test_sentences:
    words = sent.split()
    our_correction = [w if w.lower().strip() in vocab else correct_word(w) for w in words]
    spell_correction = []
    for w in words:
        cleaned = re.sub(r"^\W+|\W+$", "", w)          # strip leading/trailing punctuation
        if not cleaned:
            spell_correction.append(w)
        else:
            corrected = spell.correction(cleaned)       # may return None
            spell_correction.append(corrected if corrected is not None else cleaned)
```

**Notes:** `spell.correction(word)` returns the best correction or `None`. `^\W+|\W+$` removes non-word characters
only at the ends. The library has a full English dictionary, so it fixes `freind→friend`, `pleasent→pleasant`
(our model gives `frend`, `please`); both get `runing sloowly → running slowly`. Neither fixes `wether`.

## 1.5 Fill-in-the-blank practice

**Q1.** Read the file.
```python
with open(data_path, 'r', encoding=________) as f:
    text = ________
```

**Q2.** Extract (correct, wrong) pairs from lines like `<ERR targ=sister> siter </ERR>`.
```python
pattern = r'<ERR targ=____>____</ERR>'
matches = re.________(pattern, text)
```

**Q3.** Build the vocabulary.
```python
vocab = Counter()
for correct, wrong in matches:
    vocab[________] += 1
    vocab[________] += 1
```

**Q4.** Edit-distance initialisation.
```python
m, n = len(s1), len(s2)
dp = [[0] * (____) for _ in range(____)]
for i in range(____):
    dp[i][0] = ____
for j in range(____):
    dp[0][j] = ____
```

**Q5.** Edit-distance recurrence.
```python
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if s1[____] == s2[____]:
            dp[i][j] = ________
        else:
            dp[i][j] = 1 + min(dp[____][j], dp[i][____], dp[____][____])
return ________
```

**Q6.** Models.
```python
def P_c(c):
    total = ________
    return vocab.get(c, 0) / total if total else 0.0

def P_w_given_c(w, c):
    distance = edit_distance(w, c)
    return ________
```

**Q7.** Argmax.
```python
return ____(candidates, key=lambda candidate: ________________)
```

**Q8.** Candidate filter.
```python
for word in vocab:
    if edit_distance(w, word) ____ max_dist:
        candidates.add(word)
```

**Q9 (numeric).** Compute `edit_distance("clob", "club")` and $P(\text{clob}\mid\text{club})$. If `club` has count 2 and the
total count is 5130, what is the noisy-channel score?

**Q10 (concept).** Why can `P(w)` be dropped, and why does the model turn `freind` into `frend` instead of `friend`?

<details><summary>Answers</summary>

1. `'latin-1'`, `f.read()`
2. `(.*?)`, `(.*?)` (non-greedy; group 1 = correct, group 2 = wrong); `findall`
3. `correct.lower().strip()`, `wrong.lower().strip()`
4. `n + 1`, `m + 1`, `m + 1`, `i`, `n + 1`, `j`
5. `i - 1`, `j - 1`, `dp[i - 1][j - 1]`, `i - 1`, `j - 1`, `i - 1`, `j - 1`; `dp[m][n]`
6. `sum(vocab.values())`; `1 / (distance + 1)`
7. `max`, `noisy_channel_score(cleaned, candidate)` (i.e. `P_w_given_c(cleaned, candidate) * P_c(candidate)`)
8. `<=`
9. One substitution (`o→u`), distance 1, $P = 1/2$; score $= 0.5 \times 2/5130 \approx 1.95\times10^{-4}$.
10. $P(w)$ is the same for every candidate `c`, so it does not change the argmax. `freind→friend` is a
    transposition, which Levenshtein counts as 2 substitutions ($P=1/3$), while the misspelling `frend` is in vocab at
    distance 1 ($P=1/2$): $\frac12\cdot\frac3{5130} > \frac13\cdot\frac4{5130}$.

</details>

## 1.6 Quick recall

- $\hat c = \arg\max_c P(w\mid c)\,P(c)$; drop $P(w)$.
- $P(c) = \text{vocab}[c] / \text{sum(vocab.values())}$; $P(w\mid c) = 1/(d+1)$.
- Edit-distance DP: table `(m+1) x (n+1)`; `dp[i][0]=i`, `dp[0][j]=j`; compare `s1[i-1]`, `s2[j-1]`; match → diagonal;
  else `1 + min(up, left, diag)`; answer `dp[m][n]`. up = deletion, left = insertion, diag = substitution.
- Transposition costs 2 in plain Levenshtein.
- `re.findall` with k groups → list of k-tuples; `(.*?)` non-greedy; `re.DOTALL` lets `.` match newlines.
- File: `encoding="latin-1"`; tag format `<ERR targ=correct> wrong </ERR>` (unquoted, spaces inside).
- `files.upload()` → `{filename: bytes}`; filename = `next(iter(uploaded))`.
- `max(cands, key=lambda c: score(w, c))` = argmax. `max_dist=2`, test is `<=`.
- Signatures: `P_c(c)`, `P_w_given_c(w, c)`, `noisy_channel_score(w, c)`, `edit_distance(s1, s2)`,
  `calculate_edit_distance(s1, s2) -> (dist, dp)`, `generate_candidates(w, max_dist=2)`, `correct_word(w)`,
  `correct_sentence(sentence)`.
- Outputs: 2565 annotations, vocab 2569 types, total 5130. `runing sloowly → running slowly` works;
  `good → too`, `freind → frend`, `pleasent → please` are failures.
- Weaknesses: vocab contains misspellings; vocab only has words that appear in ERR tags; flat error model; no context.
- `pyspellchecker`: `SpellChecker().correction(word)` → string or `None`.

---


---

<a id="lab-2"></a>

# Lab 2 — Trigram Language Models: Add-k Smoothing, Linear Interpolation, Perplexity

## 2.1 What this lab is about

You build a trigram language model (predict a word from the previous two) on a 50-sentence restaurant corpus.
Unseen trigrams get probability 0, so you fix that two ways: **Add-k smoothing** and **linear interpolation**
(mix trigram, bigram, and unigram MLE estimates). You score sentences with log2 probability, compare models using
**perplexity**, tune `k` and the λ weights, and report which model wins. **Every code cell in the template was a TODO**,
so every function below is a candidate exam blank.

## 2.2 Core concepts & formulas

**Chain rule + Markov assumption.** The exact sentence probability conditions each word on the whole history; we cut the
history to the last two words:

$$P(w_1\dots w_n) \approx \prod_i P(w_i \mid w_{i-2}, w_{i-1})$$

**MLE trigram.** The denominator is a **bigram** count (the two-word history):

$$P_{ML}(w_3 \mid w_1,w_2) = \frac{C(w_1,w_2,w_3)}{C(w_1,w_2)}$$

**Padding rule:** an n-gram model needs **n − 1** start tokens. Trigram → `<.s> <.s>` in front, one `<./s>` at the end.
`"I am here"` → `['<.s>', '<.s>', 'i', 'am', 'here', '<./s>']`, so the first word has history `(<.s>, <.s>)`.

**Add-k smoothing** (k = 1 is Laplace / Add-1; k = 0 is MLE):

$$P_{k}(w_3 \mid w_1,w_2) = \frac{C(w_1,w_2,w_3) + k}{C(w_1,w_2) + k\cdot V}$$

Denominator gets `k·V` because you added `k` to each of the `V` possible next words; this keeps the distribution summing to 1.

**Log probability** (avoid underflow, product → sum):
$L = \sum_i \log_2 P(w_i \mid w_{i-2}, w_{i-1})$. Start the sum at 0.0.

**Perplexity** (lower is better; roughly "average number of equally likely choices per word"):

$$PP(W) = P(w_1\dots w_N)^{-1/N} = 2^{-L/N}$$

`N` = number of **words + 1** (counts `<./s>`, excludes the two `<.s>` pads; equals the number of trigrams).
A model that learned nothing (uniform) has $PP = V$.

**Linear interpolation** (λ's sum to 1; each piece is **unsmoothed** MLE):

$$P_{interp}(w_3\mid w_1,w_2) = \lambda_1 \frac{C(w_1,w_2,w_3)}{C(w_1,w_2)} + \lambda_2 \frac{C(w_2,w_3)}{C(w_2)} + \lambda_3 \frac{C(w_3)}{\text{total\_tokens}}$$

Why it helps: Add-k gives every unseen trigram the same tiny mass; interpolation backs off to the bigram/unigram, so
`('want','to','eat')` (common `to eat`) scores far higher than `('credit','card','eat')`. The unigram term is the
safety net: if $\lambda_3 > 0$ and the word was seen in training, the probability can't be 0.

**Worked example A — tutorial toy corpus** (6 sentences, `V = 14`, `C(i,want)=3`, `C(i,want,to)=2`):

| estimate | computation | value |
|---|---|---|
| MLE | 2 / 3 | 0.6667 |
| Add-1 | (2+1)/(3+14) | 0.1765 |
| Add-0.1 | (2+0.1)/(3+1.4) | 0.4773 |
| Add-1, unseen `(i,want,a)` | (0+1)/(3+14) | 0.0588 |

Add-1 crushes a well-supported 0.67 down to 0.18 (14 fake counts vs 3 real) — that is why `k` is tuned.

`"i want food"` → 4 trigrams (Add-1): $P(i\mid\langle s\rangle,\langle s\rangle)=\frac{5+1}{6+14}=0.3$,
$P(want\mid\langle s\rangle,i)=\frac{3+1}{5+14}=0.2105$, $P(food\mid i,want)=\frac{0+1}{3+14}=0.0588$,
$P(\langle/s\rangle\mid want,food)=\frac{0+1}{0+14}=0.0714$. $L=-11.88$, $N=4$, $PP=2^{11.88/4}\approx 7.83$.

**Worked example B — assignment corpus** (`V = 174`, `total_tokens = 585`, `C(i,want)=8`, `C(i,want,to)=6`,
`C(want,to)=8`, `C(want)=10`, `C(to)=16`):
- Add-1: $P(to\mid i,want) = (6+1)/(8+174) = 7/182 = 0.0385$; unseen `(i,want,pizza)`: $1/182 = 0.0055$; `k=0` unseen → 0.0.
- Interpolated with $(0.5, 0.3, 0.2)$: $0.5\cdot\frac68 + 0.3\cdot\frac8{10} + 0.2\cdot\frac{16}{585} = 0.375+0.24+0.0055 = 0.6205$.
- Sentence 1 (Add-1): $L = -40.28$, $N = 6+1 = 7$, $PP = 2^{40.28/7} = 53.99$.

## 2.3 Data & pipeline

**Data:** `corpus_text` = 50 restaurant sentences (one per line) → `corpus_sentences` via
`[s.strip() for s in corpus_text.strip().split("\n") if s.strip()]`. Test sentences (not in training, each has ≥1 unseen trigram):
`"I want to eat italian food"`, `"My friend would like to eat pizza"`, `"The waiter will bring the menu"`.

**Pipeline:**
1. `preprocess`: lowercase → strip punctuation with `re.sub(r"[^a-z\s]", "", s.lower())` → `split()` → pad `[<.s>,<.s>] + words + [<./s>]`.
2. `extract_ngrams(tokens, n)` for n = 1, 2, 3 → lists of **tuples**.
3. Three `Counter`s updated sentence by sentence; `V = len(unigram_counts)` (distinct), `total_tokens = sum(unigram_counts.values())`.
4. Add-k trigram prob → sentence log2 prob → perplexity.
5. ML trigram / bigram / unigram → interpolated prob → interpolated perplexity.
6. Tune `k ∈ [0.01, 0.1, 0.5, 1, 2, 5, 10]`; tune λ over the 66-point grid (step 0.1, sum 1); compare averages.

**Shapes / values:** `V = 174`, `total_tokens = 585` (both **include** the pad tokens: `<.s>` appears 100 times,
`<./s>` 50 times). Tokens for a 6-word sentence: length 9 → 7 trigrams → N = 7.
Tokens are `START = "<.s>"`, `END = "<./s>"` (dotted spellings, so they never clash with real words).

## 2.4 Exam-critical code blocks

### ★★★ Block A — `preprocess` and `extract_ngrams` (TEMPLATE BLANK)

**What it does:** tokenise + pad for a trigram model; slide a window to get n-grams as tuples. **TEMPLATE BLANK** (both bodies were `pass`).

```python
START = "<.s>"
END = "<./s>"

def preprocess(sentence):
    cleaned = re.sub(r"[^a-z\s]", "", sentence.lower())      # <-- KEY  lower FIRST, then strip non a-z
    words = cleaned.split()
    return [START, START] + words + [END]                    # <-- KEY  TWO starts, ONE end

def extract_ngrams(tokens, n):
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]   # <-- KEY
```

**Line-by-line notes**
- `.lower()` must come before `[^a-z\s]`, otherwise capital letters are deleted (`"I"` → `""`).
- `[^a-z\s]` keeps letters and whitespace only; `"food."` → `"food"`, `"great,"` → `"great"`.
- `[START, START] + words + [END]` — list concatenation; n − 1 = 2 start pads.
- `range(len(tokens) - n + 1)`: a list of length L has L − n + 1 windows. `['a','b','c','d']`, n=3 → 2 trigrams.
- `tuple(...)` because lists are unhashable and cannot be `Counter`/dict keys. Unigrams are 1-tuples: `('i',)`.

**Common mistakes**
- Only one `<.s>` (bigram padding).
- `range(len(tokens) - n)` → drops the last n-gram (the one ending in `<./s>`).
- Returning lists instead of tuples (`TypeError: unhashable type: 'list'`).

Tutorial version (no punctuation removal): `return [START, START] + sentence.lower().split() + [END]`.

---

### ★★★ Block B — Counting, `V`, `total_tokens` (TEMPLATE BLANK)

```python
unigram_counts = Counter()
bigram_counts = Counter()
trigram_counts = Counter()

for sentence in corpus_sentences:
    tokens = preprocess(sentence)
    unigram_counts.update(extract_ngrams(tokens, 1))          # <-- KEY
    bigram_counts.update(extract_ngrams(tokens, 2))           # <-- KEY
    trigram_counts.update(extract_ngrams(tokens, 3))          # <-- KEY

V = len(unigram_counts)                                       # <-- KEY  distinct tokens
total_tokens = sum(unigram_counts.values())                   # <-- KEY  all tokens
```

**Notes:** `Counter.update(list)` adds 1 for each element of the list (it counts, it does not overwrite).
`V` = number of **types** (174), `total_tokens` = number of **tokens** (585). `V` is for Add-k; `total_tokens` is for the
unigram MLE. Output: `V = 174, total tokens = 585`, `Count('i','want') = 8`, `Count('i','want','to') = 6`.

**Common mistakes:** swapping `V` and `total_tokens`; `dict.update` semantics (overwrite) confusion; using `+=` on a
Counter with a list (`counter += list` fails — `update` is the method).

---

### ★★★ Block C — Add-k trigram probability (TEMPLATE BLANK)

```python
def calculate_trigram_prob(trigram, trigram_counts, bigram_counts, V, k=1.0):
    history = trigram[:2]                                     # <-- KEY  (w1, w2) = BIGRAM key
    trigram_count = trigram_counts.get(trigram, 0)            # <-- KEY
    history_count = bigram_counts.get(history, 0)             # <-- KEY  bigram_counts, not unigram

    if k == 0:                                                # <-- KEY  MLE branch
        if history_count == 0:
            return 0.0
        return trigram_count / history_count

    return (trigram_count + k) / (history_count + k * V)      # <-- KEY  + k*V, not + k
```

**Line-by-line notes**
- `trigram[:2]` = first two tokens as a tuple → look up in **`bigram_counts`**.
- `.get(key, 0)` → unseen n-gram gives 0 instead of `KeyError` (a Counter returns 0 anyway, but `.get` is what the hint asks for).
- `k == 0` must guard division by zero when the history was never seen.
- Unseen history with k > 0: $(0+k)/(0+kV) = 1/V$ → uniform, which is sensible.
- Outputs: seen `(i,want,to)` k=1 → **0.03846**; unseen `(i,want,pizza)` k=1 → **0.00549**; k=0 → **0.0**.

Tutorial Add-1 version: `return (tri_count + 1) / (hist_count + V)`.

**Common mistakes:** denominator `+ k` instead of `+ k*V`; dividing by the unigram count; `trigram[1:]` (wrong history).

---

### ★★★ Block D — Sentence log probability (TEMPLATE BLANK)

```python
def calculate_sentence_log_prob_trigram(sentence, trigram_counts, bigram_counts, V, k=1.0):
    tokens = preprocess(sentence)
    total = 0.0                                               # <-- KEY  0.0, not 1.0
    for trigram in extract_ngrams(tokens, 3):                 # <-- KEY  n = 3
        prob = calculate_trigram_prob(trigram, trigram_counts, bigram_counts, V, k)
        if prob == 0:
            return -float("inf")                              # <-- KEY  log(0) guard
        total += math.log(prob, 2)                            # <-- KEY  base 2, +=
    return total
```

**Notes:** adding logs = multiplying probabilities ($\log(ab) = \log a + \log b$) without underflow. Base 2 because
perplexity is $2^{-L/N}$ (bases must match). `math.log(0)` raises `ValueError`, so check first. Remember to pass `k`
through. Result is always ≤ 0. Outputs (k=1): **−40.28, −53.11, −47.12**.

**Common mistakes:** `total = 1.0`; `total *= prob` (mixing styles); natural log with a base-2 perplexity; forgetting `k`.

---

### ★★★ Block E — Perplexity (TEMPLATE BLANK)

```python
def calculate_perplexity(sentence, trigram_counts, bigram_counts, V, k=1.0):
    L = calculate_sentence_log_prob_trigram(sentence, trigram_counts, bigram_counts, V, k)
    N = len(re.sub(r"[^a-z\s]", "", sentence.lower()).split()) + 1     # <-- KEY  words + 1
    if L == -float("inf"):
        return float("inf")                                            # <-- KEY
    return 2 ** (-L / N)                                               # <-- KEY  minus sign
```

**Line-by-line notes**
- `N` = words + 1 for `<./s>`; the two `<.s>` are never predicted, so they are not counted.
  `len(preprocess(sentence))` would be 2 too big. (Equivalently `N = len(preprocess(sentence)) - 2` = number of trigrams.)
- Clean with the same regex as `preprocess` so `N` matches the number of trigrams.
- `-L` because `L` is negative; `2 ** (-L/N)` is ≥ 1.
- Outputs (k=1): **53.99, 99.61, 106.23**.

Tutorial version: `N = len(sentence.lower().split()) + 1` (no punctuation removal).

**Common mistakes:** `2 ** (L / N)` (gives a value < 1); `N = len(tokens)`; `math.exp` with a log2 `L`.

---

### ★★★ Block F — ML estimates + interpolated probability (TEMPLATE BLANK)

```python
def ml_trigram_prob(trigram, trigram_counts, bigram_counts):
    history_count = bigram_counts.get(trigram[:2], 0)                 # <-- KEY  C(w1,w2)
    if history_count == 0:
        return 0.0
    return trigram_counts.get(trigram, 0) / history_count             # <-- KEY  C(w1,w2,w3)


def ml_bigram_prob(trigram, bigram_counts, unigram_counts):
    history = (trigram[1],)                                           # <-- KEY  1-tuple (w2,)
    history_count = unigram_counts.get(history, 0)
    if history_count == 0:
        return 0.0
    return bigram_counts.get(trigram[1:], 0) / history_count          # <-- KEY  (w2, w3)


def ml_unigram_prob(trigram, unigram_counts, total_tokens):
    return unigram_counts.get((trigram[2],), 0) / total_tokens        # <-- KEY  (w3,) / total_tokens


def calculate_interpolated_prob(trigram, trigram_counts, bigram_counts,
                                unigram_counts, total_tokens, lambdas):
    l1, l2, l3 = lambdas                                              # <-- KEY
    p3 = ml_trigram_prob(trigram, trigram_counts, bigram_counts)
    p2 = ml_bigram_prob(trigram, bigram_counts, unigram_counts)
    p1 = ml_unigram_prob(trigram, unigram_counts, total_tokens)
    return l1 * p3 + l2 * p2 + l3 * p1                                # <-- KEY  l1 pairs with TRIGRAM
```

**Line-by-line notes**
- `(trigram[1],)` — the trailing comma makes a 1-tuple. `(trigram[1])` is just a string and will never match a key
  (it silently returns 0).
- `trigram[1:]` = `(w2, w3)` (the bigram); `trigram[:2]` = `(w1, w2)` (the trigram's history). Do not mix them up.
- Unigram divides by `total_tokens` (585), **not** `V` (174).
- Naming trap: `p3` = trigram estimate goes with `l1`; `p1` = unigram goes with `l3`.
- Sanity value: `(i,want,to)` with `(0.5,0.3,0.2)` → **0.6205**.

**Common mistakes:** missing comma in the 1-tuple; dividing the unigram by `V`; smoothing the pieces (they must be raw MLE).

---

### ★★ Block G — Interpolated perplexity (TEMPLATE BLANK)

```python
def calculate_perplexity_interpolated(sentence, trigram_counts, bigram_counts,
                                      unigram_counts, total_tokens, lambdas):
    tokens = preprocess(sentence)
    L = 0.0
    for trigram in extract_ngrams(tokens, 3):
        prob = calculate_interpolated_prob(
            trigram, trigram_counts, bigram_counts,
            unigram_counts, total_tokens, lambdas
        )
        if prob == 0:
            return float("inf")                     # <-- KEY  +inf (we return PP directly here)
        L += math.log(prob, 2)
    N = len(re.sub(r"[^a-z\s]", "", sentence.lower()).split()) + 1
    return 2 ** (-L / N)
```

**Notes:** same as Blocks D + E fused. Here the zero-guard returns **`+inf`** (a perplexity), whereas Block D returns
**`-inf`** (a log probability). Zero happens only when λ3 = 0 and both the trigram and bigram MLE are 0 (e.g. the bigram
`(will, bring)` never occurs in training).

---

### ★★ Block H — 6b: λ grid search (TEMPLATE BLANK)

```python
lambda_grid = []
for i1 in range(0, 11):                                   # <-- KEY  0..10
    for i2 in range(0, 11 - i1):                          # <-- KEY  so i1 + i2 <= 10
        i3 = 10 - i1 - i2                                 # <-- KEY  forces sum = 10
        lambda_grid.append((i1 / 10, i2 / 10, i3 / 10))   # 66 combos

interp_results = {}
infinite_combos = []
for lambdas in lambda_grid:
    pps = [
        calculate_perplexity_interpolated(
            s, trigram_counts, bigram_counts, unigram_counts, total_tokens, lambdas
        )
        for s in test_sentences
    ]
    avg_pp = sum(pps) / len(pps)
    if math.isinf(avg_pp):                                # <-- KEY  skip infinite
        infinite_combos.append(lambdas)
        continue
    interp_results[lambdas] = avg_pp

best_lambdas = min(interp_results, key=interp_results.get)            # <-- KEY  argmin over dict
for lambdas, avg_pp in sorted(interp_results.items(), key=lambda item: item[1])[:10]:
    print(f"{str(lambdas):>20}  {avg_pp:10.2f}")
```

**Notes:** integer loops then divide by 10 → no float drift (0.1+0.2 ≠ 0.3). Count = $\binom{12}{2} = 66$.
`min(d, key=d.get)` returns the **key** with the smallest value. One `inf` sentence makes the average `inf`.
Result: best **(0.0, 0.6, 0.4)**, avg PP **23.38**; **11** infinite combos, which are exactly the 11 with λ3 = 0.

---

### ★★ Block I — 6a: tune `k` (TEMPLATE BLANK)

```python
k_values = [0.01, 0.1, 0.5, 1, 2, 5, 10]
addk_results = {}
for k in k_values:
    pps = [calculate_perplexity(s, trigram_counts, bigram_counts, V, k) for s in test_sentences]
    avg_pp = sum(pps) / len(pps)
    addk_results[k] = avg_pp
    print(f"{k:6}  {avg_pp:10.2f}  {pps[0]:10.2f}  {pps[1]:10.2f}  {pps[2]:10.2f}")

best_k = min(addk_results, key=addk_results.get)
```

**Results (avg PP):** 0.01 → **49.78** (best), 0.1 → 50.63, 0.5 → 71.67, 1 → 86.61, 2 → 104.22, 5 → 128.25, 10 → 143.97.
Large k flattens toward uniform. In the tutorial the curve was U-shaped (best k = 0.1, PP 5.29: too-small k punishes
unseen trigrams, too-large k washes out evidence); here the minimum is at the smallest k tried.

---

### ★ Block J — 6c: compare

```python
best_addk_pp = addk_results[best_k]
best_interp_pp = interp_results[best_lambdas]
if best_interp_pp < best_addk_pp:
    winner = "Linear interpolation"
    margin = best_addk_pp - best_interp_pp
else:
    winner = "Add-k"
    margin = best_interp_pp - best_addk_pp
```

**Result:** interpolation wins, 23.38 vs 49.78 (lower by 26.40).
**Written answers:** (1) λ1 = 0: the corpus is tiny (~50 sentences), so most test trigrams are unseen and trigram MLE is
almost always 0; the model relies on bigram + unigram, which shows there is too little data for trigrams.
(2) All 11 combos with λ3 = 0 give infinite PP: when both the trigram and bigram MLE are 0, the mixture is 0, the log is
−∞, and PP = ∞. Any λ3 > 0 fixes this for words seen in training.

## 2.5 Fill-in-the-blank practice

**Q1.** Pad for a trigram model.
```python
def preprocess(sentence):
    cleaned = re.sub(r"________", "", sentence.________())
    words = cleaned.split()
    return ________ + words + ________
```

**Q2.** n-grams.
```python
def extract_ngrams(tokens, n):
    return [________(tokens[i:i + ____]) for i in range(________________)]
```

**Q3.** Counting.
```python
for sentence in corpus_sentences:
    tokens = preprocess(sentence)
    trigram_counts.________(extract_ngrams(tokens, 3))
V = ________________
total_tokens = ________________
```

**Q4.** Add-k.
```python
history = trigram[____]
trigram_count = trigram_counts.get(trigram, 0)
history_count = ________.get(history, 0)
...
return (trigram_count + ____) / (history_count + ________)
```

**Q5.** Log probability.
```python
total = ____
for trigram in extract_ngrams(tokens, ____):
    prob = calculate_trigram_prob(trigram, trigram_counts, bigram_counts, V, k)
    if prob == 0:
        return ________
    total ____ math.log(prob, ____)
```

**Q6.** Perplexity.
```python
N = len(re.sub(r"[^a-z\s]", "", sentence.lower()).split()) ________
return ________
```

**Q7.** Bigram MLE inside interpolation.
```python
history = ________          # unigram key for w2
history_count = unigram_counts.get(history, 0)
if history_count == 0:
    return 0.0
return bigram_counts.get(________, 0) / history_count
```

**Q8.** Unigram MLE and mixture.
```python
p1 = unigram_counts.get(________, 0) / ________
return l1 * ____ + l2 * ____ + l3 * ____
```

**Q9.** λ grid.
```python
for i1 in range(0, ____):
    for i2 in range(0, ________):
        i3 = ________
        lambda_grid.append((i1 / 10, i2 / 10, i3 / 10))
best_lambdas = min(interp_results, key=________)
```

**Q10 (numeric).** Toy corpus: `C(i,want,to)=2`, `C(i,want)=3`, `V=14`. Give the Add-1 and Add-0.5 values of
$P(to \mid i, want)$. A sentence has $L = -12$ over 3 words; what is its perplexity?

<details><summary>Answers</summary>

1. `[^a-z\s]`, `lower`, `[START, START]`, `[END]`
2. `tuple`, `n`, `len(tokens) - n + 1`
3. `update`; `len(unigram_counts)`; `sum(unigram_counts.values())`
4. `:2`; `bigram_counts`; `k`, `k * V`
5. `0.0`; `3`; `-float("inf")`; `+=`, `2`
6. `+ 1`; `2 ** (-L / N)`
7. `(trigram[1],)` (comma!); `trigram[1:]`
8. `(trigram[2],)`, `total_tokens`; `p3`, `p2`, `p1` (trigram, bigram, unigram)
9. `11`, `11 - i1`, `10 - i1 - i2`; `interp_results.get`
10. Add-1: $3/17 = 0.1765$. Add-0.5: $2.5/(3+7) = 0.25$. $N = 3+1 = 4$, $PP = 2^{12/4} = 2^3 = 8$.

</details>

## 2.6 Quick recall

- Tokens: `START = "<.s>"`, `END = "<./s>"`; trigram → **2** starts + **1** end (n − 1 starts).
- `extract_ngrams`: `[tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]`.
- `V = len(unigram_counts)` (types, 174); `total_tokens = sum(unigram_counts.values())` (tokens, 585). Both include pads.
- Add-k: `(C(w1,w2,w3) + k) / (C(w1,w2) + k*V)`; history `trigram[:2]` looked up in `bigram_counts`. k=1 Add-1, k=0 MLE (guard /0).
- Log prob: start `0.0`, `+= math.log(p, 2)`, zero → `-float("inf")`.
- PP: `2 ** (-L / N)`, `N = words + 1`; `inf` if `L` is `-inf`. Lower is better; uniform model PP = V.
- Interp: `l1*P(w3|w1,w2) + l2*P(w3|w2) + l3*P(w3)`, λ's sum to 1, pieces are raw MLE.
  Keys: trigram history `trigram[:2]`; bigram `trigram[1:]`, its history `(trigram[1],)`; unigram `(trigram[2],)` / `total_tokens`.
- Grid: `i1 in range(11)`, `i2 in range(11 - i1)`, `i3 = 10 - i1 - i2` → 66 combos. `min(d, key=d.get)` = argmin key.
- Signatures: `preprocess(sentence)`, `extract_ngrams(tokens, n)`,
  `calculate_trigram_prob(trigram, trigram_counts, bigram_counts, V, k=1.0)`,
  `calculate_sentence_log_prob_trigram(sentence, trigram_counts, bigram_counts, V, k=1.0)`,
  `calculate_perplexity(sentence, trigram_counts, bigram_counts, V, k=1.0)`,
  `ml_trigram_prob(trigram, trigram_counts, bigram_counts)`, `ml_bigram_prob(trigram, bigram_counts, unigram_counts)`,
  `ml_unigram_prob(trigram, unigram_counts, total_tokens)`,
  `calculate_interpolated_prob(trigram, trigram_counts, bigram_counts, unigram_counts, total_tokens, lambdas)`,
  `calculate_perplexity_interpolated(sentence, trigram_counts, bigram_counts, unigram_counts, total_tokens, lambdas)`.
- Numbers: Add-1 `(i,want,to)` = 0.0385, unseen = 0.0055; Add-1 PPs 53.99 / 99.61 / 106.23; best k = 0.01 (49.78);
  best λ = (0.0, 0.6, 0.4) (23.38); 11 infinite combos (λ3 = 0); interpolation wins by 26.40.
- Tutorial toy: V = 14; MLE 0.667 vs Add-1 0.176 vs Add-0.1 0.477; best k = 0.1 (PP 5.29), U-shaped curve.
- The four "mistakes that cost marks" (from the tutorial): one `<.s>` instead of two; dividing by the unigram count
  instead of the bigram count; `+ k` instead of `+ k*V`; counting `<.s>` pads in `N`.

---

<a id="lab-3"></a>

# Lab 3 — CFG → CNF, CKY Parsing, PCFG/Viterbi, Dependency Parsing (spaCy)

## 3.1 What this lab is about
- A **CFG** says which phrase structures are allowed; **CNF** is the restricted form (`A → B C` or `A → 'word'`) that CKY needs.
- **Task 1:** hand-write the **CKY** recognizer, print its triangular chart, and check against NLTK's `ChartParser`.
- **Task 2 (Part 1):** a PCFG has one non-CNF rule (`VP → V NP PP`). Binarize it, parse *"I saw the man with a telescope"* with `ViterbiParser`, and show by multiplying rule probabilities why NP-attachment wins.
- **Task 2 (Part 2):** spaCy dependency parse, find ROOT, then BFS over the head/children graph to get the shortest path `researchers → … → mutation`.
- Lab 3 had **no `TODO` markers**. Each assignment cell was an open "write the code here" cell, so expect to write **whole functions** (mainly `cky_parse`).

## 3.2 Core concepts & formulas

### CFG vs CNF
- CFG rule: $A \to \alpha$, where $\alpha$ is any string of terminals and non-terminals.
- CNF allows only $A \to B\,C$ (two non-terminals) or $A \to a$ (one terminal).
- Why CKY needs CNF: every span of length ≥ 2 is built from **exactly two** smaller adjacent spans. A ternary rule would need two split points, and a unit rule would need a span to "become" another label without combining anything.

### CFG → CNF conversion (textbook order: START, TERM, BIN, DEL, UNIT)
The lab only performed **BIN** by hand. Know all five steps for theory questions.

| Step | Problem rule | Fix |
|---|---|---|
| **START** | start symbol S appears on a RHS | add `S0 → S` and make S0 the new start symbol |
| **TERM** | terminal mixed into a long RHS: `PP → 'with' NP` | `PP → P_with NP`, `P_with → 'with'` |
| **BIN** | RHS longer than 2: `VP → V NP PP` | `VP → V VP_PP`, `VP_PP → NP PP` (fresh non-terminal) |
| **DEL** | ε-rule `C → ε` used in `A → B C` | add `A → B`, delete `C → ε` |
| **UNIT** | `NP → N`, with `N → 'student' \| 'books'` | replace with `NP → 'student' \| 'books'` |

**PCFG probability bookkeeping** (Task 2 asked to *preserve the probability*):
- BIN: `VP → V NP PP [0.3]` becomes `VP → V VP_PP [0.3]` plus `VP_PP → NP PP [1.0]`. Product: $0.3 \times 1.0 = 0.3$, unchanged. Each LHS still sums to 1 (`VP`: 0.7 + 0.3; `VP_PP`: 1.0).
- UNIT: $P(NP \to \text{'books'}) = P(NP \to N)\cdot P(N \to \text{'books'})$.
- The Lab 3 demo did *not* remove the unit rule `NP → N`. It patched it inside CKY instead: `if "N" in chart[i][i+1]: chart[i][i+1].add("NP")`.

### CKY — the recurrence
`chart[i][j]` = the set of non-terminals that can derive `words[i:j]` (fenceposts: `i` is the left boundary, `j` the right boundary, exclusive).

$$\text{chart}[i][i+1] = \{A : A \to w_i\}$$
$$\text{chart}[i][j] \mathrel{{+}{=}} \{A : A \to B\,C,\ B \in \text{chart}[i][k],\ C \in \text{chart}[k][j],\ i<k<j\}$$
$$\text{accept} \iff S \in \text{chart}[0][n]$$

Loop order: **span length** 2..n → **start** i → **end** j = i+length → **split** k from i+1 to j−1 → **rules**.
Cost: $O(n^3 \cdot |R|)$ time and $O(n^2)$ cells.

### Hand trace — Task 1: "the man saw the dog" (n = 5)
Grammar: `S→NP VP, NP→Det N, VP→V NP, Det→'the', N→'man'|'dog', V→'saw'`

Fenceposts: `0 the 1 man 2 saw 3 the 4 dog 5`

| step | cell | splits tried (k) | result |
|---|---|---|---|
| lexical | [0][1],[1][2],[2][3],[3][4],[4][5] | — | Det, N, V, Det, N |
| len 2 | [0][2] | k=1: Det+N | **NP** |
| len 2 | [1][3] | k=2: N+V | ∅ |
| len 2 | [2][4] | k=3: V+Det | ∅ |
| len 2 | [3][5] | k=4: Det+N | **NP** |
| len 3 | [0][3] | k=1: Det+∅; k=2: NP+V | ∅ |
| len 3 | [1][4] | k=2: N+∅; k=3: ∅+Det | ∅ |
| len 3 | [2][5] | **k=3: V+NP** → VP; k=4: ∅+N | **VP** |
| len 4 | [0][4], [1][5] | all k (e.g. [1][5] k=2: N+VP, no rule) | ∅ |
| len 5 | [0][5] | k=1: Det+∅; **k=2: NP+VP** → S; k=3,4: ∅ | **S** ✔ |

Printed chart (row = i, column = j = 1..5). This matches the notebook output:
```
 0 | Det | NP | . | . | S
 1 | — | N | . | . | .
 2 | — | — | V | . | VP
 3 | — | — | — | Det | NP
 4 | — | — | — | — | N
```

### PCFG and Viterbi
- $P(\text{tree}) = \prod_{\text{rules } r \text{ used}} P(r)$. `ViterbiParser` returns $\arg\max_{\text{tree}} P(\text{tree})$. It is CKY that keeps the **max probability** per (span, non-terminal) instead of a set.
- PP-attachment, *"I saw the man with a telescope"*. The two trees share 11 rules. They differ only in:
  - **A (NP-attach, PP modifies "man"):** `VP→V NP [0.7]` × `NP→NP PP [0.6]` = **0.42**
  - **B (VP-attach, "saw … with telescope"):** `VP→V VP_PP [0.3]` × `VP_PP→NP PP [1.0]` = **0.30**
- Shared factor: $1.0\cdot0.1\cdot1.0\cdot0.3\cdot0.8\cdot0.5\cdot1.0\cdot1.0\cdot0.3\cdot0.2\cdot0.5 = 0.00036$
- $P(A) = 0.00036 \times 0.42 = \mathbf{1.512\times10^{-4}}$ (printed `p=0.0001512`). $P(B) = 0.00036\times0.30 = \mathbf{1.08\times10^{-4}}$. Ratio A/B = 1.4, so Viterbi picks A.

### Dependency parsing (spaCy)
- Every token has exactly one `head`. The ROOT token's head **is itself** in spaCy (`token.head is token`).
- Attributes: `token.text`, `token.pos_`, `token.dep_` (`nsubj`, `dobj`, `relcl`, `ROOT`, …), `token.head`, `token.children`.
- Treat the parse as an **undirected** graph (neighbors = children + head). BFS then gives the shortest path: `researchers → discovered → vaccine → prevents → mutation`.

## 3.3 Data & pipeline
**Grammar formats**
- Demo: `grammar = {"binary": [("S","NP","VP"), ...], "lexical": {"the": ["Det"], ...}}`.
- Task 1: NLTK `CFG.fromstring("""S -> NP VP ...""")`, then `grammar_to_rules` turns it into:
  - `binary`: a **list of triples** `(lhs, B, C)`
  - `lexical`: a **dict** `word → [list of POS non-terminals]`
- PCFG string: one rule per line with probabilities in brackets: `NP -> 'I' [0.1] | Det N [0.3] | NP PP [0.6]`.

**Chart:** `n` rows × `n+1` columns, each cell a `set()`. Only cells with `j > i` are used (upper triangle).

**Pipeline, Task 1:** `CFG.fromstring` → `grammar_to_rules` → `sentence.split()` → `cky_parse` → `print_chart` → `ChartParser(cky_grammar).parse(words)` to cross-check.

**Pipeline, Task 2 Part 1:** spot the non-CNF rule → write the CNF string → `PCFG.fromstring` → `ViterbiParser(pcfg)` → `parses[0]` → multiply `pcfg_prod.prob()` over `best_tree.productions()` → compute the competing tree by hand.

**Pipeline, Task 2 Part 2:** `spacy.load("en_core_web_sm")` → `parsed_doc = nlp(text)` → `find_root` → `extract_terminals` (nsubj child of root, token "mutation") → `bfs_shortest_path` (uses `collections.deque`) → print table → `displacy.render(parsed_doc, style='dep', jupyter=True)`.

## 3.4 Exam-critical code blocks

### ★★★ 3.4.1 `cky_parse` — CKY recognizer (Task 1)
**What it does:** fills the chart bottom-up and returns `(chart, S ∈ chart[0][n])`. The Task 1 cell was **entirely blank**, so the whole function is a *write-from-memory* candidate.
```python
def cky_parse(words, binary, lexical, start='S'):
    n = len(words)
    chart = [[set() for _ in range(n + 1)] for _ in range(n)]   # <-- KEY  n rows, n+1 cols

    # lexical fill
    for i, w in enumerate(words):
        chart[i][i+1].update(lexical.get(w, []))                 # <-- KEY  diagonal = span length 1

    # build spans
    for length in range(2, n + 1):                               # <-- KEY  span length 2..n
        for i in range(n - length + 1):                          # <-- KEY  start positions
            j = i + length                                       # <-- KEY  end (exclusive)
            for k in range(i + 1, j):                            # <-- KEY  split point
                for lhs, b, c in binary:
                    if b in chart[i][k] and c in chart[k][j]:    # <-- KEY  left part [i,k), right part [k,j)
                        chart[i][j].add(lhs)

    return chart, start in chart[0][n]                           # <-- KEY  whole sentence = [0][n]
```
**Line-by-line notes**
- `range(n + 1)` columns because `j` reaches `n`. Using `[[set()]*(n+1)]` would alias one shared set object. Use the comprehension.
- `lexical.get(w, [])`: an unknown word gives an empty cell, not a `KeyError`.
- `range(n - length + 1)`: for length `L` there are `n−L+1` spans, so the last start is `n−L`.
- `k in range(i+1, j)`: both halves must be non-empty, so `k ≠ i` and `k ≠ j`.
- Length must be the **outer** loop. Both halves of a span are shorter, so all shorter spans must be finished first.
- Demo version only: after the lexical fill, `if "N" in chart[i][i+1]: chart[i][i+1].add("NP")` handles the unit rule `NP → N`.

**Common mistakes**
- Looping `for i … for j …` instead of over length, which reads cells before they are filled.
- Checking `chart[i][k]` and `chart[k+1][j]`. That is the *inclusive-index* convention; this code uses fenceposts, so it is `[k][j]`.
- Returning `chart[0][n-1]` or `chart[0][-1]`. The final cell is `chart[0][n]`.

### ★★★ 3.4.2 CNF conversion of the PCFG + `ViterbiParser` (Task 2 Part 1)
**What it does:** binarizes `VP → V NP PP [0.3]`, builds the PCFG, gets the best parse, and recomputes its probability from the rules it used. The whole cell was blank.
```python
cnf_grammar_str = """
    S -> NP VP [1.0]
    NP -> 'I' [0.1] | Det N [0.3] | NP PP [0.6]
    VP -> V NP [0.7] | V VP_PP [0.3]
    VP_PP -> NP PP [1.0]
    PP -> P NP [1.0]
    Det -> 'the' [0.8] | 'a' [0.2]
    N -> 'man' [0.5] | 'telescope' [0.5]
    V -> 'saw' [1.0]
    P -> 'with' [1.0]
"""
pcfg = PCFG.fromstring(cnf_grammar_str)          # <-- KEY
parser = ViterbiParser(pcfg)                     # <-- KEY
words = sentence.split()
parses = list(parser.parse(words))               # <-- KEY  generator -> list
best_tree = parses[0]

total_prob = 1.0
for prod in best_tree.productions():             # <-- KEY  rules used by the tree
    lhs_str = prod.lhs().symbol()
    rhs_list = [r.symbol() if hasattr(r, 'symbol') else r for r in prod.rhs()]
    for pcfg_prod in pcfg.productions():
        if pcfg_prod.lhs().symbol() == lhs_str:
            pcfg_rhs = [r.symbol() if hasattr(r, 'symbol') else r for r in pcfg_prod.rhs()]
            if pcfg_rhs == rhs_list:
                total_prob *= float(pcfg_prod.prob())   # <-- KEY  multiply rule probs
                break
```
**Line-by-line notes**
- `VP -> V VP_PP [0.3]` keeps the original 0.3. The new `VP_PP -> NP PP` gets **1.0**, so the tree probability is preserved.
- Imports: `from nltk import PCFG`, `from nltk.parse import ViterbiParser`.
- `hasattr(r, 'symbol')` distinguishes a `Nonterminal` (has `.symbol()`) from a terminal (a plain `str`).
- The helper `get_prod_prob(grammar, lhs, rhs_tuple)` does the same lookup and is used to multiply out the competing tree B rule by rule (`VP -> V VP_PP`, `VP_PP -> NP PP`, …). It returns `0.0` if the rule is missing.
- Brackets: `NP -> 'I' [0.1] | Det N [0.3]`, one probability per alternative.

**Common mistakes**
- Giving the new rule probability 0.3, which double-counts (0.09), or making the alternatives for one LHS not sum to 1. NLTK raises an error in that case.
- Converting `NP -> 'I'`, which is already CNF. Only `V NP PP` violates CNF.
- Hard-coding the final probability. The task explicitly required computing it from the tree's productions.

### ★★ 3.4.3 `grammar_to_rules` — NLTK CFG → (binary, lexical)
**What it does:** splits an NLTK grammar into binary triples and a word→POS dict. This is the bridge between `CFG.fromstring` and `cky_parse`.
```python
def grammar_to_rules(nltk_grammar):
    binary = []
    lexical = {}
    for prod in nltk_grammar.productions():
        lhs = prod.lhs().symbol()                                  # <-- KEY  Nonterminal -> str
        rhs = prod.rhs()
        if len(rhs) == 1 and isinstance(rhs[0], str):              # <-- KEY  terminal rule
            lexical.setdefault(rhs[0], []).append(lhs)             # <-- KEY
        elif len(rhs) == 2:
            b = rhs[0].symbol()
            c = rhs[1].symbol()
            binary.append((lhs, b, c))
    return binary, lexical
```
**Notes:** terminals in NLTK RHS are plain `str`; non-terminals are `Nonterminal` objects, so you need `.symbol()`. `setdefault(word, [])` handles ambiguous words that have several POS tags.
**Common mistake:** forgetting `.symbol()`. Then `"NP" in chart[i][k]` never matches, because the set holds `Nonterminal` objects.

### ★★ 3.4.4 `print_chart` — triangular chart
```python
def print_chart(chart, words):
    n = len(words)
    for i in range(n):
        row = []
        for j in range(1, n+1):                       # <-- KEY  columns are end positions 1..n
            if j <= i:
                row.append('—')                       # lower triangle unused
            else:
                s = chart[i][j]
                row.append(','.join(sorted(s)) if s else '.')
        print(f"{i:2d} | " + " | ".join(row))
```
**Note:** the diagonal of the printed table (`j = i+1`) holds the POS tags, and the top-right cell (`i=0, j=n`) must contain `S`.

### ★★ 3.4.5 spaCy: root, terminals, BFS shortest path (Task 2 Part 2)
```python
nlp = spacy.load("en_core_web_sm")
parsed_doc = nlp(text)

def find_root(doc):
    for token in doc:
        if token.dep_ == 'ROOT':                      # <-- KEY
            return token
    return None

def extract_terminals(root, doc):
    start_node = None
    for child in root.children:                       # <-- KEY  only direct children of root
        if child.dep_ == 'nsubj':
            start_node = child
            break
    end_node = None
    for token in doc:
        if token.text.lower() == 'mutation':
            end_node = token
            break
    return start_node, end_node

def bfs_shortest_path(start, end):
    if start is None or end is None:
        return []
    q = deque()
    q.append((start, [start]))                        # <-- KEY  (node, path so far)
    visited = {start}
    while q:
        node, path = q.popleft()                      # <-- KEY  FIFO => shortest path
        if node == end:
            return path
        neighbors = list(node.children)               # <-- KEY  down-edges
        if node.head is not node:                     # <-- KEY  root's head is itself
            neighbors.append(node.head)               #          up-edge
        for nb in neighbors:
            if nb not in visited:
                visited.add(nb)                       # mark when enqueued
                q.append((nb, path + [nb]))
    return []                                         # end unreachable

def print_path_details(path):
    print('| Word | POS | Head | Dependency |')
    print('|---|---|---|---|')
    for tok in path:
        head_text = tok.head.text if tok.head else ''
        print(f'| {tok.text} | {tok.pos_} | {head_text} | {tok.dep_} |')
```
**Notes:** `popleft()` gives FIFO order, which is what makes it BFS (shortest in edges). `pop()` would be DFS. Output path: `researchers(nsubj) → discovered(ROOT) → vaccine(dobj) → prevents(relcl) → mutation(dobj)`.
**Common mistakes:** following only `.children`, which makes the graph directed so you can never go "up" from `researchers`. Not guarding `node.head is not node`. Using `token.dep` or `token.pos` (integer IDs) instead of `dep_` and `pos_` (strings).

### ★ 3.4.6 Demo one-liners
```python
parser = ChartParser(nltk_grammar)                       # from nltk.parse import ChartParser
trees = list(parser.parse("the student reads books".split()))
for token in doc:
    if token.dep_ != "ROOT":
        print(f"{token.head.text} → {token.text} : {token.dep_}")   # head -> dependent : relation
```

## 3.5 Fill-in-the-blank practice
**Q1.** CKY chart allocation and lexical fill:
```python
chart = [[set() for _ in range(____)] for _ in range(____)]
for i, w in enumerate(words):
    chart[i][____].update(lexical.get(w, ____))
```
**Q2.** CKY loops:
```python
for length in range(____, ____):
    for i in range(____):
        j = ____
        for k in range(____, ____):
            for lhs, b, c in binary:
                if b in chart[____][____] and c in chart[____][____]:
                    chart[i][j].add(____)
return chart, start in chart[____][____]
```
**Q3.** In `grammar_to_rules`: `if len(rhs) == 1 and isinstance(rhs[0], ____): lexical.____(rhs[0], []).append(lhs)` and `b = rhs[0].____()`.
**Q4.** Convert to CNF, keeping probabilities: `VP -> V NP [0.7] | V NP PP [0.3]`.
**Q5.** Fill in: `pcfg = ____.fromstring(s)`, `parser = ____(pcfg)`, `parses = list(parser.____(words))`, `for prod in best_tree.____():  total_prob *= float(pcfg_prod.____())`.
**Q6.** For the grammar in 3.4.2, compute P(NP-attach) and P(VP-attach) for "I saw the man with a telescope". Which does Viterbi return, and by what ratio?
**Q7.** BFS neighbours in spaCy:
```python
node, path = q.____()
neighbors = list(node.____)
if node.head is not ____:
    neighbors.append(node.____)
...
q.append((nb, ____))
```
**Q8.** For "the man saw the dog", which cells of the chart are non-empty, and at which `k` is `S` formed in `chart[0][5]`?
**Q9.** Apply TERM and UNIT to `PP -> 'with' NP` and to `NP -> N` (where `N -> 'cat' | 'dog'`).

<details><summary>Answers</summary>

1. `n + 1`, `n`, `i+1`, `[]`
2. `2, n + 1`; `n - length + 1`; `i + length`; `i + 1, j`; `chart[i][k]`, `chart[k][j]`; `lhs`; `chart[0][n]`
3. `str`, `setdefault`, `symbol`
4. `VP -> V NP [0.7] | V VP_PP [0.3]` and `VP_PP -> NP PP [1.0]`
5. `PCFG`, `ViterbiParser`, `parse`, `productions`, `prob`
6. A = 0.00036 × (0.7 × 0.6) = 1.512e-4; B = 0.00036 × (0.3 × 1.0) = 1.08e-4. Viterbi returns A (NP-attach); A/B = 1.4.
7. `popleft`, `children`, `node`, `head`, `path + [nb]`
8. [0][1] Det, [1][2] N, [2][3] V, [3][4] Det, [4][5] N, [0][2] NP, [3][5] NP, [2][5] VP, [0][5] S. S is formed at k = 2 (NP in [0][2] + VP in [2][5]).
9. `PP -> P_with NP`, `P_with -> 'with'`; `NP -> 'cat' | 'dog'` (for a PCFG, multiply the probabilities).
</details>

## 3.6 Quick recall
- CNF: `A → B C` or `A → 'w'`. Conversion order: START → TERM → BIN → DEL → UNIT.
- BIN for a PCFG: the old rule keeps p, the new helper rule gets 1.0. UNIT: multiply the probabilities.
- `chart[i][j]` covers `words[i:j]`. Size `n × (n+1)`. Accept iff `start in chart[0][n]`.
- Loops: `length 2..n` → `i in range(n-length+1)` → `j=i+length` → `k in range(i+1, j)`.
- CKY is $O(n^3|R|)$ time and $O(n^2)$ space. It is a **recognizer** (yes/no); add backpointers to recover trees.
- NLTK: `CFG.fromstring`, `PCFG.fromstring`, `ChartParser(g).parse(words)`, `ViterbiParser(pcfg).parse(words)`, `prod.lhs().symbol()`, `prod.rhs()`, `prod.prob()`, `tree.productions()`.
- PCFG: P(tree) = product of rule probabilities. Viterbi = argmax tree. In the PP-attachment example, NP-attach wins because 0.7 × 0.6 = 0.42 > 0.3 × 1.0.
- spaCy: `nlp = spacy.load("en_core_web_sm")`, `doc = nlp(text)`, `token.dep_ == "ROOT"`, `token.head`, `token.children`, `token.pos_`. The root's head is itself.
- BFS: `deque`, `popleft`, mark `visited` on enqueue, store `(node, path)`.

---


---

<a id="lab-4"></a>

# Lab 4 — MST Dependency Parsing, Chu-Liu/Edmonds & Structured Perceptron

## 4.1 What this lab is about
- Dependency parsing as a graph problem: every arc `head → dependent` has a score, and the parse is the **maximum-scoring rooted spanning tree** (arborescence).
- You implement tree validation, a brute-force reference parser, and **Chu-Liu/Edmonds (CLE)** from scratch: greedy best-incoming edges → cycle detection → contraction → recursion → expansion.
- Then you **train** the arc scores with a structured perceptron. CLE does inference inside the training loop, and the weights are updated by Φ(gold) − Φ(pred).
- The notebook had **28 `TODO` markers**: every function below was a blank, worth 20 marks in total.

## 4.2 Core concepts & formulas

### Valid rooted dependency tree (Task 1 conditions)
1. ROOT has no incoming arc.
2. Every non-root word has exactly one head.
3. No self-loop.
4. No directed cycle.
5. Everything is reachable from ROOT.
6. Number of arcs = number of tokens − 1 (= number of non-root words).

Trick used in the code: if you follow head pointers upward from every word and always reach ROOT without repeating a node, then conditions 4 and 5 both hold.

### MST formulation
$$Score(G)=\sum_{(h,d)\in G} Score(h\to d) \qquad G^*=\arg\max_{G\in T(x)} Score(G)$$
- Exhaustive search tries every head assignment: with $n$ non-root words each has $n$ candidate heads, so there are $n^n$ candidates. It is exponential and only used as a correctness check.
- Lab graph (Researchers analyze data carefully): best tree = `ROOT→analyze(7), analyze→Researchers(6), analyze→data(7), analyze→carefully(6)`, **score 26**. CLE gives the same.

### Chu-Liu/Edmonds — step by step
1. **Greedy:** for each non-root $v$, $parent(v)=\arg\max_{u\neq v} Score(u\to v)$.
2. **No cycle?** Then the greedy arcs form a tree, and it is optimal. Return it.
3. **Cycle $C$:** contract it into a supernode $c$. Let $W_C$ = the sum of the selected cycle arc scores.
   - Edge entering, $u\to v$ with $v\in C$: $\;w'(u\to c)=w(u\to v)+W_C-w(parent(v)\to v)$. Keep the max over all $v$, and remember which $v$ it came from.
   - Edge leaving, $v\to u$ with $v\in C$: $w'(c\to u)=\max_v w(v\to u)$. Remember the original arc.
   - Edges inside $C$ are dropped. Edges outside $C$ are copied unchanged.
4. **Recurse** on the contracted graph.
5. **Expand:** keep all cycle arcs **except** $parent(v)\to v$ for the $v$ the chosen entering edge targets. Map every supernode arc back to its original arc.

Why the adjustment works: entering at $v$ means you keep the whole cycle ($W_C$) minus the one cycle arc you must break ($parent(v)\to v$), plus the new arc. So $w'$ equals the true score change. **Invariant: score of the contracted solution = score of the expanded tree.**

### Hand trace — the lab's cycle graph
Scores: `ROOT→A 5, ROOT→B 4, ROOT→C 3, A→B 10, B→A 10, A→C 7, B→C 8, C→A 2, C→B 2`

**Step 1, greedy.** A: max(ROOT 5, **B 10**, C 2) → `B→A`. B: max(ROOT 4, **A 10**, C 2) → `A→B`. C: max(ROOT 3, A 7, **B 8**) → `B→C`.
**Step 2, cycle.** Parent map `{A:B, B:A, C:B}`. Walk from A: A → B → A, which repeats, so the cycle is `['A','B']`. $W_C = 10+10 = 20$.
**Step 3, contract** {A,B} into S = `("CYCLE", ("A","B"))`:

| original edge | type | computation | contracted edge |
|---|---|---|---|
| ROOT→A (5) | enter | 5 + 20 − w(B→A)=10 → **15** | ROOT→S = 15, kept (removes B→A) |
| ROOT→B (4) | enter | 4 + 20 − w(A→B)=10 → 14 | not > 15, dropped |
| C→A (2) | enter | 2 + 20 − 10 → **12** | C→S = 12 (removes B→A) |
| C→B (2) | enter | 2 + 20 − 10 → 12 | not > 12 (strict `>`), dropped |
| A→C (7), B→C (8) | leave | max → **8** via B→C | S→C = 8 |
| ROOT→C (3) | outside | unchanged | ROOT→C = 3 |
| A→B, B→A | inside | dropped | — |

**Step 4, recurse** on {ROOT, C, S}. C: max(ROOT 3, **S 8**). S: max(**ROOT 15**, C 12). The arcs `S→C, ROOT→S` have no cycle, so return them (score 23).
**Step 5, expand.** Start with the cycle arcs `[B→A, A→B]`. `S→C` maps back to `B→C`. `ROOT→S` maps back to `ROOT→A`, and `B→A` is removed.
**Result:** `[A→B, B→C, ROOT→A]`, score 10 + 8 + 5 = **23** (= 15 + 8 ✔; the exhaustive search also gives 23).

**Nested contraction** happened during training (sentence "Dogs chase cats", right after the first update). Greedy gave `chase→Dogs 4`, `cats→chase 2`, `chase→cats 2`, so the cycle is {chase, cats} with $W=4$. Contracted to S1: `ROOT→S1 = −5+4−2 = −3`, `Dogs→S1 = 0+4−2 = 2`, `S1→Dogs = 4`. Greedy again gives `S1→Dogs`, `Dogs→S1`: a cycle {Dogs, S1}, which is contracted again into S2. `ROOT→S2 = max(ROOT→Dogs: −4+6−4, ROOT→S1: −3+6−2) = 1`. Expanding twice gives `ROOT→chase, chase→Dogs, chase→cats`, the gold tree. The recursion handles this automatically.

### Structured perceptron (inference-based learning)
- Arc score: $score(h\to d)=\mathbf w\cdot \mathbf f(h\to d)$. Tree features: $\Phi(x,G)=\sum_{(h,d)\in G}\mathbf f(h\to d)$.
- **Inference:** $G_{pred}=\arg\max_{G\in T(x)}\mathbf w\cdot\Phi(x,G)$, computed with CLE.
- **Update (only if $G_{pred}\neq G_{gold}$):** $\mathbf w \leftarrow \mathbf w + \eta\,[\Phi(x,G_{gold})-\Phi(x,G_{pred})]$, with η = 1.
  - Gold-only features go up, prediction-only features go down, and shared features cancel.
- Feature templates (7): head word, dependent word, head POS, dependent POS, direction (`RIGHT` if head index < dependent index), distance `|h−d|`, word pair.

### Hand trace — epoch 1, sentence "ROOT John saw Mary"
With **w = 0**, every arc scores 0. `max()` returns the **first** maximum, and ROOT comes first in `tokens`, so pred = `ROOT→John, ROOT→saw, ROOT→Mary`. That differs from gold (`ROOT→saw, saw→John, saw→Mary`), so mistakes = 1.

| feature | Φ(gold) | Φ(pred) | Δ = new w |
|---|---|---|---|
| HEAD_WORD=ROOT / HEAD_POS=ROOT | 1 | 3 | **−2** |
| HEAD_WORD=saw / HEAD_POS=VERB | 2 | 0 | **+2** |
| DIRECTION=RIGHT | 2 (ROOT→saw, saw→Mary) | 3 | **−1** |
| DIRECTION=LEFT | 1 (saw→John) | 0 | **+1** |
| DISTANCE=1 | 2 | 1 | **+1** |
| DISTANCE=2 | 1 | 1 | 0 |
| DISTANCE=3 | 0 | 1 (ROOT→Mary) | **−1** |
| WORD_PAIR (saw,John), (saw,Mary) | 1 | 0 | **+1** each |
| WORD_PAIR (ROOT,John), (ROOT,Mary) | 0 | 1 | **−1** each |
| WORD_PAIR (ROOT,saw), DEP_WORD/DEP_POS | equal | equal | 0 |

These are exactly the learned weights printed in the notebook. Sentences 2 and 3 are then parsed correctly, because `HEAD_POS=VERB` and the direction/distance features generalize to `chase` and `likes`. Mistakes per epoch: 1, 0, 0, 0, 0.

## 4.3 Data & pipeline
| object | type / shape | example |
|---|---|---|
| `tokens` | list, ROOT first | `["ROOT","John","saw","Mary"]` |
| `score` / `edges` | dict `{(head, dep): score}`, no arcs into ROOT, no self-loops | `{("ROOT","A"):5, ...}`. Full graph has n² arcs for n words |
| arcs / tree | list of `(head, dep)` tuples | `[("ROOT","saw"),("saw","John")]` |
| Task 3 greedy | dict `dep → (head, dep, score)` | `{'A': ('B','A',10), ...}` |
| Task 5 selected | dict `dep → (head, dep)`; then `list(selected.values())` | |
| parent map | dict `dep → head` | `{A:B, B:A, C:B}` |
| supernode | hashable tuple | `("CYCLE", ("A","B"))`, and it can nest |
| `mapping_information` | `{"supernode", "cycle", "incoming": {new_arc: {"original_arc", "removed_cycle_arc"}}, "outgoing": {new_arc: {"original_arc"}}}` | |
| weights / Φ | `Counter` feature → float (missing = 0) | `{("HEAD_POS","VERB"): 2.0}` |
| feature | tuple | `("DIRECTION","LEFT")`, `("WORD_PAIR","saw","Mary")` |
| `training_data` | list of `{"tokens", "pos": {word: POS}, "gold": [arcs]}` | 3 sentences |

**Pipeline:** validate (`is_valid_tree`) → reference (`exhaustive_mst`) → greedy + cycle (`best_incoming`, `find_cycle`) → contraction table (`entering_cycle_table`) → CLE (`select_best_incoming`, `detect_cycle`, `contract_cycle`, `expand_cycle`, `chu_liu_edmonds`) → features (`arc_features`, `tree_feature_vector`) → scoring (`score_arc`, `build_score_graph`, `score_tree`) → `perceptron_update` → `train_perceptron`.

## 4.4 Exam-critical code blocks
Every block below was a **TODO BLANK**. The tutorial showed `is_valid_tree`, `exhaustive_mst`, the greedy loop, and `arc_features` almost verbatim, so those are the most likely to be asked word for word. The long CLE helpers (`contract_cycle`, `expand_cycle`) are more likely to appear as "fill the key lines".

### ★★★ 4.4.1 `is_valid_tree` — TODO BLANK (Task 1, 2 marks)
```python
def is_valid_tree(tokens, arcs, root="ROOT"):
    non_root = [w for w in tokens if w != root]

    if len(arcs) != len(non_root):              # <-- KEY  exactly n arcs
        return False

    heads = {}
    for head, dep in arcs:
        if head == dep or dep == root:          # <-- KEY  self-loop / arc into ROOT
            return False
        if dep in heads:                        # <-- KEY  duplicate head
            return False
        heads[dep] = head

    if set(heads) != set(non_root):             # <-- KEY  every word has a head
        return False

    for start in non_root:                      # <-- KEY  climb to ROOT from every word
        cur = start
        seen = set()
        while cur != root:
            if cur in seen or cur not in heads: # <-- KEY  cycle / dangling head
                return False
            seen.add(cur)
            cur = heads[cur]

    return True
```
**Line-by-line notes**
- `heads` is the parent map `dep → head`. `set(heads)` gives its keys, i.e. the dependents.
- The climbing loop checks both acyclicity (`cur in seen`) and reachability: you must hit `root`.
- `cur not in heads` catches a head that is not a real token.
- Tests: `[("ROOT","A"),("B","C"),("C","B")]` fails on the cycle; `[("ROOT","A"),("A","B"),("C","B")]` fails on the duplicate head for B.

**Common mistakes:** resetting `seen` outside the `for start` loop (it must be per start); checking only the arc count, which a cycle can still satisfy; forgetting `dep == root`.

### ★★★ 4.4.2 `exhaustive_mst` — TODO BLANK (Task 2, 3 marks)
```python
def exhaustive_mst(tokens, score, root="ROOT"):
    non_root = [w for w in tokens if w != root]
    choices = [[h for h in tokens if h != dep] for dep in non_root]   # <-- KEY  candidate heads per word
    best_score = float("-inf")
    best_tree = None

    for heads in product(*choices):                 # <-- KEY  itertools.product, one head per word
        tree = list(zip(heads, non_root))           # <-- KEY  (head, dep) pairs
        if is_valid_tree(tokens, tree, root):       # <-- KEY  reject invalid structures
            total = sum(score[a] for a in tree)     # <-- KEY  tree score = sum of arc scores
            if total > best_score:
                best_score = total
                best_tree = tree

    return best_score, best_tree                    # note order: (score, tree)
```
**Notes:** `product(*choices)` unpacks the list of lists. `heads[i]` is the head of `non_root[i]`. ROOT appears among the candidate heads, but never as a dependent.
**Common mistakes:** `zip(non_root, heads)` gives reversed arcs; starting at `best_score = 0` fails with negative scores; returning `(tree, score)`.

### ★★★ 4.4.3 Greedy best incoming — TODO BLANK (Task 3 `best_incoming` and Task 5 `select_best_incoming`)
```python
# Task 3 version: returns {dep: (head, dep, score)}
def best_incoming(tokens, score, root="ROOT"):
    greedy = {}
    for dep in tokens:
        if dep == root:                              # <-- KEY  no edges into ROOT
            continue
        candidates = [
            (head, dep, score[(head, dep)])
            for head in tokens
            if head != dep                           # <-- KEY  no self-loop
        ]
        greedy[dep] = max(candidates, key=lambda x: x[2])   # <-- KEY  argmax over score
    return greedy

# Task 5 version (used inside CLE): returns {dep: (head, dep)}
def select_best_incoming(nodes, edges, root="ROOT"):
    selected = {}
    for dep in nodes:
        if dep == root:
            continue
        candidates = [
            (head, dep)
            for head in nodes
            if head != dep and (head, dep) in edges  # <-- KEY  contracted graph is NOT complete
        ]
        if not candidates:
            raise ValueError(f"No incoming edge for {dep}")
        best = max(candidates, key=lambda arc: edges[arc])  # <-- KEY
        selected[dep] = best
    return selected
```
**Notes:** the `(head, dep) in edges` check matters because after contraction some pairs no longer exist (for example, there is no S→ROOT). Ties resolve to the **first** candidate in node order, which is why an all-zero model attaches everything to ROOT.
**Common mistake:** taking the max over *outgoing* edges `score[(dep, head)]`. CLE picks the best **incoming** edge (best head) for each word.

### ★★★ 4.4.4 Cycle detection — TODO BLANK (Task 3 `find_cycle` and Task 5 `detect_cycle`)
```python
# Task 3: arcs is {dep: (head, dep, score)}
def find_cycle(arcs):
    parent = {}
    for dep, (head, _, _) in arcs.items():
        parent[dep] = head                           # <-- KEY  build parent map
    for start in parent:
        visited = set()
        current = start
        path = []
        while current is not None:                   # ROOT has no parent -> get() gives None -> stop
            if current in visited:
                cycle_start_idx = path.index(current)    # <-- KEY  where the loop begins
                return path[cycle_start_idx:]            # <-- KEY  only the cycle part
            visited.add(current)
            path.append(current)
            current = parent.get(current)            # <-- KEY  follow parent pointer
    return None

# Task 5: arcs is a list of (head, dep)
def detect_cycle(arcs, root="ROOT"):
    parent = {dep: head for head, dep in arcs}       # <-- KEY
    for start in parent:
        if start == root:
            continue
        current = start
        path = []
        position = {}                                # node -> index in path (O(1) lookup)
        while current in parent and current != root: # <-- KEY  stop at ROOT
            if current in position:
                return path[position[current]:]      # <-- KEY
            position[current] = len(path)
            path.append(current)
            current = parent[current]
    return None
```
**Notes:** each node has exactly one parent, so following parents traces a single path. It either reaches ROOT or loops. Return only the loop part: for a path `C → B → A → B` the cycle is `[B, A]`, not including `C`. On the lab graph the result is `['A','B']`.
**Common mistakes:** returning the whole path (which includes the tail leading into the cycle); not stopping at ROOT, causing a `KeyError` on `parent[ROOT]`; sharing `visited` across starts without care.

### ★★★ 4.4.5 `contract_cycle` — TODO BLANK (Task 5)
**What it does:** builds the contracted graph and the bookkeeping needed for expansion. The adjusted-score line is the single most likely blank in Lab 4.
```python
def contract_cycle(nodes, edges, selected_arcs, cycle, root="ROOT"):
    cycle_set = set(cycle)
    supernode = ("CYCLE", tuple(sorted(cycle_set, key=str)))     # hashable, unique

    contracted_nodes = [node for node in nodes if node not in cycle_set]
    contracted_nodes.append(supernode)

    cycle_total = sum(edges[arc] for arc in selected_arcs
                      if arc[0] in cycle_set and arc[1] in cycle_set)   # <-- KEY  W_C

    old_incoming = {                       # = {arc[1]: arc for arc in selected_arcs if arc[1] in cycle_set}
        dep: arc
        for arc in selected_arcs
        if arc[1] in cycle_set
        for dep in [arc[1]]
    }

    contracted_edges = {}
    mapping_information = {"supernode": supernode, "cycle": cycle_set,
                           "incoming": {}, "outgoing": {}}

    for (head, dep), weight in edges.items():
        head_in = head in cycle_set
        dep_in = dep in cycle_set

        if head_in and dep_in:                       # <-- KEY  internal edge: drop
            continue

        if not head_in and dep_in:                   # <-- KEY  ENTERING the cycle
            new_arc = (head, supernode)
            old_arc = old_incoming[dep]
            adjusted = weight + cycle_total - edges[old_arc]     # <-- KEY  w + W_C - w(parent(v)->v)
            if new_arc not in contracted_edges or adjusted > contracted_edges[new_arc]:
                contracted_edges[new_arc] = adjusted
                mapping_information["incoming"][new_arc] = {
                    "original_arc": (head, dep),
                    "removed_cycle_arc": old_arc         # <-- KEY  remembered for expansion
                }

        elif head_in and not dep_in:                 # <-- KEY  LEAVING the cycle
            new_arc = (supernode, dep)
            if new_arc not in contracted_edges or weight > contracted_edges[new_arc]:
                contracted_edges[new_arc] = weight   # no adjustment, keep max
                mapping_information["outgoing"][new_arc] = {"original_arc": (head, dep)}

        else:                                        # outside: copy
            new_arc = (head, dep)
            if new_arc not in contracted_edges or weight > contracted_edges[new_arc]:
                contracted_edges[new_arc] = weight

    return contracted_nodes, contracted_edges, mapping_information
```
**Notes**
- Several original edges can collapse onto the same `(u, S)` or `(S, u)`. Keep the **max**, and record the mapping only when that edge wins.
- Only *entering* edges get the $+W_C - w(parent(v)\to v)$ adjustment. Leaving edges keep their raw score.
- `old_incoming[dep]` is the greedy arc *into* `dep`. Since `dep` is in the cycle, that arc is a cycle arc.
- The weird comprehension with `for dep in [arc[1]]` just binds `dep = arc[1]`.

**Common mistakes:** subtracting the *entering* edge instead of the cycle edge; adjusting leaving edges; computing `cycle_total` over all selected arcs (it must be cycle arcs only); using a list as the supernode (lists are not hashable).

### ★★★ 4.4.6 `expand_cycle` — TODO BLANK (Task 5)
```python
def expand_cycle(selected_contracted_arcs, cycle, mapping_information, original_selected_arcs):
    supernode = mapping_information["supernode"]
    cycle_set = set(cycle)

    result = [arc for arc in original_selected_arcs
              if arc[0] in cycle_set and arc[1] in cycle_set]   # <-- KEY  start with ALL cycle arcs

    for arc in selected_contracted_arcs:
        if arc[1] == supernode:                                  # <-- KEY  entering edge
            info = mapping_information["incoming"][arc]
            result.append(info["original_arc"])                  # <-- KEY  real external edge
            removed = info["removed_cycle_arc"]
            result = [a for a in result if a != removed]         # <-- KEY  break the cycle
        elif arc[0] == supernode:                                # leaving edge
            info = mapping_information["outgoing"][arc]
            result.append(info["original_arc"])                 # <-- KEY
        else:                                                    # untouched edge
            result.append(arc)
    return result
```
**Notes:** exactly one contracted arc enters the supernode, because the supernode has one head in a tree. So exactly one cycle arc is removed, and a k-cycle keeps k−1 arcs. Leaving arcs can be several (one per child of the cycle).
**Common mistake:** removing a cycle arc chosen arbitrarily (for example the lowest-scoring one). It must be the arc into the node `v` that the chosen external edge enters.

### ★★★ 4.4.7 `chu_liu_edmonds` / `solve` — TODO 1–6 BLANKS (Task 5, 4 marks)
```python
def chu_liu_edmonds(tokens, score, root="ROOT"):
    def solve(nodes, edges, root):
        selected_dict = select_best_incoming(nodes, edges, root)     # TODO 1
        selected_arcs = list(selected_dict.values())
        cycle = detect_cycle(selected_arcs, root)                    # TODO 2
        if cycle is None:                                            # TODO 3  base case
            return selected_arcs
        contracted_nodes, contracted_edges, mapping = contract_cycle(   # TODO 4
            nodes, edges, selected_arcs, cycle, root)
        contracted_solution = solve(contracted_nodes, contracted_edges, root)  # TODO 5  recursion
        expanded = expand_cycle(contracted_solution, cycle, mapping, selected_arcs)  # TODO 6
        return expanded

    final_arcs = solve(list(tokens), score, root)
    total_score = sum(score[arc] for arc in final_arcs)              # <-- KEY  score on ORIGINAL scores
    return total_score, final_arcs
```
**Notes:** the base case is "no cycle", and each recursive call has at least one fewer node, so it terminates. Expansion receives the **current level's** `selected_arcs`, which contain the cycle arcs. The final score is summed with the original `score` dict, not the adjusted weights. Returns `(score, arcs)`.
**Common mistakes:** passing the original `edges` (instead of `contracted_edges`) to the recursive call; expanding before recursing; returning `selected_dict` (a dict) instead of a list of arcs.

### ★★★ 4.4.8 `arc_features` + `tree_feature_vector` — TODO BLANK (Task 6)
```python
def arc_features(tokens, pos, head, dep):
    h_index = tokens.index(head)
    d_index = tokens.index(dep)
    direction = "RIGHT" if h_index < d_index else "LEFT"    # <-- KEY  dep to the right of head
    distance = abs(h_index - d_index)                       # <-- KEY
    return [
        ("HEAD_WORD", head),
        ("DEP_WORD", dep),
        ("HEAD_POS", pos[head]),                            # <-- KEY  pos is a dict word -> tag
        ("DEP_POS", pos[dep]),
        ("DIRECTION", direction),
        ("DISTANCE", distance),
        ("WORD_PAIR", head, dep)
    ]

def tree_feature_vector(tokens, pos, tree):
    features = Counter()
    for head, dep in tree:
        features.update(arc_features(tokens, pos, head, dep))   # <-- KEY  Counter.update counts
    return features
```
**Notes:** the tutorial version returned strings (`f"HEAD_WORD={head}"`, `f"PAIR={head}->{dep}"`). The submission uses tuples. Either works as long as features are hashable. `Counter.update(list)` adds 1 per item, so a feature shared by two arcs gets count 2.
**Common mistakes:** "Do not simply return the score": the function returns feature *names*, not numbers. Reversed direction logic. `tokens.index` assumes unique tokens.

### ★★★ 4.4.9 `perceptron_update` — TODO BLANK (Task 6)
```python
def perceptron_update(weights, gold_features, predicted_features, learning_rate=1.0):
    new_weights = weights.copy()
    for feature, count in gold_features.items():
        new_weights[feature] += learning_rate * count      # <-- KEY  + eta * Phi(gold)
    for feature, count in predicted_features.items():
        new_weights[feature] -= learning_rate * count      # <-- KEY  - eta * Phi(pred)
    return new_weights
```
**Notes:** `weights` is a `Counter`, so `.copy()` is also a Counter and unseen features start at 0 (no `KeyError`). Features shared by gold and prediction get `+c − c = 0`.
**Common mistakes:** swapping the signs; a plain `dict` (causes `KeyError`); updating even when the prediction is correct (harmless here, since Φ − Φ = 0, but the spec updates only on mistakes).

### ★★★ 4.4.10 `train_perceptron` — TODO 1–6 BLANKS (Task 6, 5 marks)
```python
def train_perceptron(training_data, num_epochs=5, learning_rate=1.0):
    weights = Counter()                                         # all zeros
    history = []
    for epoch in range(num_epochs):
        mistakes = 0
        for example in training_data:
            tokens = example["tokens"]
            pos = example["pos"]
            gold_tree = example["gold"]

            score_graph = build_score_graph(tokens, pos, weights)                # TODO 1
            predicted_score, predicted_tree = chu_liu_edmonds(tokens, score_graph)  # TODO 2  inference

            if set(predicted_tree) != set(gold_tree):                           # TODO 3  <-- KEY set!
                mistakes += 1
                gold_features = tree_feature_vector(tokens, pos, gold_tree)      # TODO 4
                predicted_features = tree_feature_vector(tokens, pos, predicted_tree)  # TODO 5
                weights = perceptron_update(weights, gold_features,
                                            predicted_features, learning_rate)  # TODO 6
        history.append(mistakes)
        print(f"Epoch {epoch + 1}: {mistakes} mistake(s)")
    return weights, history
```
**Notes:** the scores are rebuilt **for every sentence** with the current weights, so an update affects the very next sentence (online learning). `set(...)` compares trees regardless of arc order; CLE returns arcs in a different order than gold.
**Common mistakes:** building the score graph once before the loops; comparing lists with `!=`, which flags false mistakes forever; unpacking `chu_liu_edmonds` as `(tree, score)`.

### ★★ 4.4.11 Scoring helpers — TODO BLANK
```python
def score_arc(tokens, pos, head, dep, weights):
    features = arc_features(tokens, pos, head, dep)
    return sum(weights[feature] for feature in features)        # <-- KEY  w . f(h->d)

def build_score_graph(tokens, pos, weights):
    score_graph = {}
    for dep in tokens:
        if dep == "ROOT":                                       # <-- KEY  nothing enters ROOT
            continue
        for head in tokens:
            if head == dep:                                     # <-- KEY  no self-loops
                continue
            score_graph[(head, dep)] = score_arc(tokens, pos, head, dep, weights)
    return score_graph

def score_tree(tokens, pos, tree, weights):
    return sum(score_arc(tokens, pos, head, dep, weights) for head, dep in tree)
```
**Note:** `score_tree(G)` equals `w · tree_feature_vector(G)`. That is the arc-factored property.

### ★★ 4.4.12 `entering_cycle_table` — TODO BLANK (Task 4, 3 marks)
```python
def entering_cycle_table(score, cycle, selected_cycle_arcs):
    cycle_total = sum(score[arc] for arc in selected_cycle_arcs)       # <-- KEY  W_C = 20
    cycle_incoming = {}
    for head, dep in selected_cycle_arcs:
        cycle_incoming[dep] = (head, dep)                             # dep -> its cycle arc
    rows = []
    for node in ["ROOT"]:                                             # only ROOT was asked
        for cycle_node in cycle:
            if (node, cycle_node) in score:
                original = score[(node, cycle_node)]
                removed_arc = cycle_incoming[cycle_node]
                removed = score[removed_arc]
                adjusted = original + cycle_total - removed           # <-- KEY
                rows.append({"outside_head": node, "cycle_dependent": cycle_node,
                             "original_score": original, "removed_cycle_arc": removed_arc,
                             "removed_score": removed, "cycle_total": cycle_total,
                             "adjusted_score": adjusted})
    return pd.DataFrame(rows)
```
**Output:** ROOT→A: 5 + 20 − 10 = **15** (removes B→A). ROOT→B: 4 + 20 − 10 = 14 (removes A→B). Pick **ROOT→A**. On expansion, **B→A** is deleted and A→B is kept, giving ROOT→A→B.

## 4.5 Fill-in-the-blank practice
**Q1.** `is_valid_tree` core:
```python
if head == dep or dep == ____: return False
if dep in ____: return False
...
if set(heads) != set(____): return False
for start in non_root:
    cur = start; seen = set()
    while cur != ____:
        if cur in seen or cur not in ____: return False
        seen.add(cur); cur = ____
```
**Q2.** Exhaustive search:
```python
choices = [[h for h in tokens if ____] for dep in non_root]
for heads in ____(*choices):
    tree = list(zip(____, ____))
```
**Q3.** Greedy: `greedy[dep] = max(candidates, key=lambda x: ____)` with `candidates = [(head, dep, score[(head, dep)]) for head in tokens if ____]`.
**Q4.** `detect_cycle`: `parent = {____: ____ for head, dep in arcs}`. In the loop: `if current in position: return ____`.
**Q5.** Contraction: `adjusted = weight + ____ - edges[____]`. Which category of edge gets this adjustment? What happens to edges with `head_in and dep_in`?
**Q6.** For the lab cycle graph, compute the adjusted score of `C→S` (S = {A,B}) and say which cycle arc it would remove.
**Q7.** `expand_cycle`, entering-edge branch:
```python
if arc[1] == ____:
    info = mapping_information["____"][arc]
    result.append(info["____"])
    result = [a for a in result if a != info["____"]]
```
**Q8.** `solve()` order. Put these in order and give the base case: `contract_cycle`, `detect_cycle`, `expand_cycle`, `select_best_incoming`, `solve(...)`.
**Q9.** Features: `direction = "RIGHT" if ____ else "LEFT"`, `distance = ____`. Then `features = Counter(); for head, dep in tree: features.____(arc_features(...))`.
**Q10.** Training: `if ____(predicted_tree) != ____(gold_tree):` then `new_weights[f] ____= learning_rate * count` for gold, and `____=` for predicted.
**Q11.** Gold is `ROOT→saw, saw→John, saw→Mary`; pred is `ROOT→John, ROOT→saw, ROOT→Mary`; w = 0. Give the new weights of `("HEAD_POS","ROOT")`, `("DIRECTION","LEFT")`, and `("DISTANCE",2)`.

<details><summary>Answers</summary>

1. `root`; `heads`; `non_root`; `root`; `heads`; `heads[cur]`
2. `h != dep`; `product`; `heads, non_root`
3. `x[2]`; `head != dep`
4. `dep: head`; `path[position[current]:]`
5. `cycle_total`, `old_arc` (= `old_incoming[dep]`, the greedy arc into `dep`). Only **entering** edges (head outside, dep inside) are adjusted. Internal edges are skipped (`continue`).
6. 2 + 20 − 10 = **12**; it removes **B→A**. (C→B also gives 12 but is not kept, because the comparison is strict `>`.)
7. `supernode`; `incoming`; `original_arc`; `removed_cycle_arc`
8. `select_best_incoming` → `detect_cycle` → (if `None`, return the selected arcs: **base case**) → `contract_cycle` → `solve(contracted…)` → `expand_cycle`
9. `h_index < d_index`; `abs(h_index - d_index)`; `update`
10. `set`, `set`; `+`; `-`
11. HEAD_POS=ROOT: 1 − 3 = **−2**; DIRECTION=LEFT: 1 − 0 = **+1**; DISTANCE=2: 1 − 1 = **0**
</details>

## 4.6 Quick recall
- A tree for n words has **n arcs**, one head per word, none into ROOT, no self-loops or cycles, and everything is reachable from ROOT.
- $Score(G)=\sum score(h\to d)$ (arc-factored). Exhaustive search is $n^n$ candidates; CLE is $O(n^3)$ in this simple recursive form (O(n²) per level × ≤ n contractions).
- CLE: greedy best **incoming** per node → no cycle means done → contract → recurse → expand.
- Entering adjustment: $w(u\to v)+W_C-w(parent(v)\to v)$. Leaving: max raw score. Internal: dropped.
- Expansion keeps all cycle arcs except the one into the entry node `v`, so a k-cycle contributes k−1 arcs.
- Invariant: contracted-tree score = expanded-tree score (lab example: 15 + 8 = 23).
- Signatures: `is_valid_tree(tokens, arcs, root)`, `exhaustive_mst(tokens, score) -> (score, tree)`, `select_best_incoming(nodes, edges, root) -> {dep: (h,d)}`, `detect_cycle(arcs, root) -> list | None`, `contract_cycle(nodes, edges, selected_arcs, cycle, root) -> (nodes, edges, mapping)`, `expand_cycle(selected_contracted_arcs, cycle, mapping, original_selected_arcs) -> arcs`, `chu_liu_edmonds(tokens, score) -> (total, arcs)`.
- Perceptron: $\mathbf w \mathrel{+}= \eta(\Phi_{gold}-\Phi_{pred})$, applied only on a mistake. Gold-only features go up, prediction-only features go down, shared features are unchanged.
- Inference = weights → best tree (CLE). Training = inference inside the loop → compare → update.
- Gotchas:
  - `max()` breaks ties toward the first element (all-zero weights → flat tree under ROOT).
  - Compare trees with `set()`.
  - Use `Counter` so missing weights are 0.
  - Supernode must be a hashable tuple.
  - The contracted graph is incomplete, so check `(head, dep) in edges`.
- Lab results: MST score 26 (Researchers analyze data carefully); cycle graph → 23; training mistakes 1, 0, 0, 0, 0.

---

<a id="lab-5"></a>

# Lab 5 — From Bag-of-Words to Word2Vec (CBOW & Skip-gram)

## 5.1 What this lab is about

Four ways to turn words into numbers, simplest to best. **(A)** Bag-of-Words count vectors plus cosine similarity. **(B)** Pretrained GloVe vectors via `gensim`: similarity, the `king − man + woman ≈ queen` analogy, and a PCA "parallelogram" plot. **(C)** CBOW word2vec written **from scratch in pure NumPy**: forward pass, stable softmax, cross-entropy, a hand-derived backward pass, SGD, and nearest neighbours. **(D)** Skip-gram, the mirror image of CBOW.

**Framework:** Parts A, C and D use **NumPy only**, with no torch, no Keras and no gensim training. Part B uses `gensim` (to load vectors) and `sklearn.decomposition.PCA`, and PCA is also used in the Part C bonus plot. **Corpus:** the assignment asked for Harry Potter; this submission used *Alice in Wonderland* (`pg11.txt`, Project Gutenberg).

> **TF-IDF is not in Lab 5.** It appears nowhere in the tutorial, the assignment or the instructor's PDF. The lab goes BoW → GloVe → CBOW → Skip-gram. If an exam question asks about it anyway, the textbook form is $\text{tfidf}(t,d)=\text{tf}(t,d)\cdot\log\frac{N}{\text{df}(t)}$, where $N$ is the number of documents and $\text{df}$ is the number of documents containing $t$. sklearn's default "smooth" variant is $\ln\frac{1+N}{1+\text{df}}+1$. Neither form is in your code.

## 5.2 Core concepts & formulas

**Bag-of-Words.** A document becomes a count vector over a fixed (sorted) vocabulary, and word order is thrown away.
$\text{BoW}(d)[i] = \#\text{ of times vocab}[i] \text{ occurs in } d$.
*Example:* vocab `[cat, dog, sat, the]` and tokens `[the, cat, sat, the, cat]` give `[2, 0, 1, 2]`. This is the assert in the notebook.

**Cosine similarity.** It measures the angle between two vectors and ignores their length:
$\cos(v_1,v_2)=\dfrac{v_1\cdot v_2}{\lVert v_1\rVert\,\lVert v_2\rVert}$.
*Example:* compare the king-sentence `[0 0 1 1 0 0 1 0 2 1 0]` with the queen-sentence `[0 0 0 1 0 1 1 0 2 1 0]`. The dot product is $1+1+4+1=7$ and both norms are $\sqrt8$, so $\cos = 7/8 = \mathbf{0.875}$. Against the wizard-sentence only "the" is shared, so the dot product is $2\cdot1=2$, the norms are $\sqrt8$ and $\sqrt6$, and $\cos = 2/\sqrt{48}=\mathbf{0.289}$.
*Why cosine and not Euclidean distance?* Frequent words tend to get larger embedding norms. Cosine compares direction only.

**Why one-hot / BoW fails for words.** $\text{one\_hot(king)}\cdot\text{one\_hot(queen)}=0$, so the cosine is $0$: the two words are orthogonal. Every pair of distinct words is equally unrelated, and more data cannot change that. This is the motivation for dense, learned vectors.

**Analogy as vector arithmetic.** $\text{king}-\text{man}+\text{woman}\approx\text{queen}$ is the same as $\text{king}-\text{man}\approx\text{queen}-\text{woman}$, so the arrows man→king and woman→queen are roughly parallel. With GloVe-50 the top result is `queen 0.852`. In the 2-D PCA plot the cosine between the arrows is 0.968, not 1, because squeezing 50 dimensions into 2 loses information.

**CBOW (Continuous Bag of Words).** Predict the **target** from the **averaged context**. The network has one hidden layer with **no non-linearity**:
$h=\frac{1}{m}\sum_{k=1}^{m}W_1[c_k]$, $\quad u=hW_2$, $\quad \hat y=\text{softmax}(u)$, $\quad L=-\log\hat y_t$.
After training, the rows of `W1` are the word embeddings. `W2[:, j]` is the "output vector" for word $j$.

**Stable softmax.** $\text{softmax}(u)_j=\dfrac{e^{u_j-\max u}}{\sum_k e^{u_k-\max u}}$. The result is unchanged because $\text{softmax}(u+c)=\text{softmax}(u)$: the $e^c$ factor cancels. The shift keeps every exponent $\le 0$, so `exp` can never overflow.
*Example:* $u=[1000,1001,999]$. The naive version computes `exp(1000)=inf` and returns `[nan nan nan]`. Shifting gives $[-1,0,-2]$, then $e^{(\cdot)}=[0.368,1,0.135]$ with sum $1.503$, so the output is $[0.245,0.665,0.090]$.

**Cross-entropy.** $L=-\log\hat y_t$. At initialisation $\hat y\approx 1/V$, so $L\approx\ln V$. For $V=9$ that is 2.197. For $V=2575$ it is 7.85; the real epoch-1 loss was 7.14.

**Backward pass (3 steps; the PDF calls this "the part people get wrong most often").**
1. $e=\partial L/\partial u=\hat y-y_{true}$, where $y_{true}$ is one-hot. The entries of $e$ always sum to 0.
2. $\nabla W_2=h^\top e$, an **outer product** of shape (d, V).
3. $\nabla h=W_2e$, of shape (d,). Each context row gets $\nabla W_1[c_k] \mathrel{+}= \nabla h/m$. All other rows of $\nabla W_1$ stay **exactly 0**.

*Example:* $\hat y=[0.2,0.5,0.3]$ with target index 2 gives $e=[0.2,0.5,-0.7]$. With $h=[1,2]$, $\nabla W_2=\begin{bmatrix}0.2&0.5&-0.7\\0.4&1.0&-1.4\end{bmatrix}$.

**SGD update.** $W\leftarrow W-\eta\,\nabla W$.

**Skip-gram.** The same machinery in the opposite direction: one centre word predicts **each** context word as a separate example.
$h=W_1[\text{input\_idx}]$, with no averaging. Then $\nabla W_1[\text{input\_idx}]=\nabla h$, with **no division**.
A window of $w$ gives up to $2w$ pairs per position. In total that is $2wn-w(w+1)$ pairs: 7 tokens with $w=2$ gives **22**, and 14 tokens gives **50**. CBOW gives exactly $n$ pairs (7 and 14).

| | CBOW | Skip-gram |
|---|---|---|
| Pair | `(context_list, target)` | `(input_word, one_context_word)` |
| # pairs | `n` (one per position) | `≈ 2·w·n` |
| `h` | `np.mean(W1[context_idxs], axis=0)` | `W1[input_idx]` |
| `dW1` | `dW1[idx] += dh/len(ctx)` for each ctx idx | `dW1[input_idx] = dh` |
| Loss curve | falls lower (3.32 here) | plateaus higher (4.80): one identical input must predict many different words, so there is an entropy floor |
| Good for | frequent words, faster | **rare words**: each pair is its own undiluted update |

## 5.3 Data & pipeline

1. **Load:** `open("pg11.txt").read()`. Strip the Gutenberg licence text between the `*** START OF ...` and `*** END OF ...` markers, leaving 144,599 characters.
2. **Clean:** lowercase, then `re.sub(r"[^a-z\s]", " ", ...)`, then collapse whitespace with `re.sub(r"\s+", " ", ...)` and `.strip()`.
3. **Tokenize:** `text.split()` gives **27,427 tokens**.
4. **Vocab:** `sorted(set(tokens))` gives **V = 2,575**. Sorting is not needed for correctness, but it makes the mapping deterministic and reproducible (PDF).
5. **Index maps:** `word_to_int = {w: i ...}` and `int_to_word = {i: w ...}`.
6. **Pairs:** `generate_cbow_pairs(tokens, window_size=2)` gives 27,427 pairs (= #tokens). Skip-gram gives $4\cdot27427-6=109{,}702$ pairs by the formula; the notebook did not print this number.
7. **Init:** `W1 ~ 0.01·N(0,1)` with shape (2575, 50); `W2` with shape (50, 2575).
8. **Train:** 20 epochs, lr 0.05, **one example at a time** (pure SGD, no batches). CBOW loss went 7.14 → 3.32. Skip-gram went 6.31 → 4.80.
9. **Evaluate:** `most_similar` (cosine over the rows of `W1`), plus the analogy `king − he + she` (the Harry Potter words were swapped for Alice words).

| Hyperparameter | Value | | Seeds |
|---|---|---|---|
| `window_size` | 2 | | `random.seed(42)`, `np.random.seed(42)` |
| `embedding_dim` | 50 (toy demo: 4) | | tests reseed with `np.random.seed(0/1/2/3)` |
| `learning_rate` | 0.05 (toy demo: 0.3) | | |
| `epochs` | 20 (toy demo: 60) | | |
| init scale | `* 0.01` | | |

**Shapes for one CBOW step** (V = vocab size, d = embedding_dim, m = #context words ≤ 2w):

| Object | Code | Shape |
|---|---|---|
| embedding matrix | `W1` | (V, d) |
| context rows | `W1[context_idxs]` | (m, d) |
| hidden | `h = np.mean(..., axis=0)` | (d,) |
| output matrix | `W2` | (d, V) |
| scores / probs | `u = h @ W2`, `y_hat` | (V,) |
| error | `e = y_hat - y_true` | (V,) |
| grad W2 | `np.outer(h, e)` | (d, V) |
| grad h | `W2 @ e` | (d,) |
| grad W1 | `dW1` (nonzero only in context rows) | (V, d) |

## 5.4 Exam-critical code blocks

Every function below was a `pass` / `# TODO` stub in the original template (checked against the git history). The tests around them were "do not modify" cells.

---

### ★★★ Block A: `generate_cbow_pairs`
**What it does:** turns the token list into `(context_list, target)` pairs with no padding at the edges. **TODO BLANK.**

```python
def generate_cbow_pairs(tokens, window_size):
    pairs = []
    n = len(tokens)
    for i in range(n):
        left = tokens[max(0, i - window_size):i]          # <-- KEY
        right = tokens[i + 1:i + 1 + window_size]         # <-- KEY
        context = left + right                            # <-- KEY (list concat)
        pairs.append((context, tokens[i]))                # <-- KEY (context first, target second)
    return pairs

window_size = 2
training_pairs = generate_cbow_pairs(tokens, window_size)
```
**Line-by-line notes**
- `max(0, i - window_size)`: without it, `i=1` gives `tokens[-1:1]`, which is `[]`. The slice silently drops the left neighbour.
- `tokens[i+1 : i+1+window_size]`: slicing past the end just returns a shorter list, so no special case is needed at the right edge.
- Worked example: tokens `[the, boy, who, lived, came, to, die]`, i=2 gives `tokens[0:2]+tokens[3:5] = [the, boy, lived, came]` → `who`. The asserts are `pairs[0]==(["boy","who"],"the")` and `pairs[-1]==(["came","to"],"die")`.

**Common mistakes**
- Including `tokens[i]` in the context (writing `tokens[i:...]` instead of `tokens[i+1:...]`).
- Writing the tuple as `(target, context)`. CBOW is `(context, target)`.

---

### ★★★ Block B: `stable_softmax`, `init_params`, `forward` (CBOW)
**What it does:** average the context embeddings, score every word in the vocabulary, and apply softmax. **TODO BLANK** (all three functions).

```python
def stable_softmax(x):
    x_shifted = x - np.max(x)              # <-- KEY
    exps = np.exp(x_shifted)
    return exps / np.sum(exps)             # <-- KEY

def init_params(vocab_size, embedding_dim):
    W1 = np.random.randn(vocab_size, embedding_dim) * 0.01   # <-- KEY shape (V, d)
    W2 = np.random.randn(embedding_dim, vocab_size) * 0.01   # <-- KEY shape (d, V)
    return W1, W2

def forward(context_idxs, W1, W2):
    h = np.mean(W1[context_idxs], axis=0)  # <-- KEY
    u = h @ W2                             # <-- KEY
    y_hat = stable_softmax(u)
    return y_hat, h, u                     # order matters: tests unpack y_hat, h, u
```
**Line-by-line notes**
- `W1[context_idxs]`: fancy indexing with a list of ints gives an (m, d) array. `axis=0` averages **over words** and leaves a (d,) vector. Without `axis` you get a single scalar.
- `h @ W2`: (d,) @ (d, V) gives (V,).
- `np.random.randn(a, b)` takes the dimensions as separate arguments, not a tuple (`np.random.randn((a,b))` is wrong).
- The test calls `stable_softmax([1000, 1000, -1000])` and asserts there is no nan/inf.

**Common mistakes**
- Swapping the W1 and W2 shapes. The asserts check `(6,3)` and `(3,6)` for V=6, d=3.
- Subtracting `np.min` instead of `np.max`, or forgetting the shift entirely.
- Using `np.sum` instead of `np.mean` for h. That is "sum-CBOW"; the backward pass would then need `dh` without the `/m`.

---

### ★★★ Block C: `cross_entropy_loss`, `backward`, `sgd_update` (CBOW)
**What it does:** compute the loss, then the hand-derived gradients, then a plain SGD step. **TODO BLANK** (all three).

```python
def cross_entropy_loss(y_hat, target_idx):
    eps = 1e-12
    return -np.log(y_hat[target_idx] + eps)      # <-- KEY

def backward(y_hat, h, context_idxs, target_idx, W1, W2, vocab_size):
    y_true = np.zeros(vocab_size)
    y_true[target_idx] = 1.0                     # <-- KEY one-hot target
    e = y_hat - y_true                           # <-- KEY  dL/du

    dW2 = np.outer(h, e)                         # <-- KEY  (d, V)
    dh = W2 @ e                                  # <-- KEY  (d,)

    dW1 = np.zeros_like(W1)
    grad_per_word = dh / len(context_idxs)       # <-- KEY  split equally (h was an average)
    for idx in context_idxs:
        dW1[idx] += grad_per_word                # <-- KEY  += not =

    return dW1, dW2

def sgd_update(W1, W2, dW1, dW2, learning_rate):
    W1 -= learning_rate * dW1                    # <-- KEY minus sign
    W2 -= learning_rate * dW2
    return W1, W2
```
**Line-by-line notes**
- `e = y_hat - y_true` is the famous softmax + cross-entropy shortcut: the gradient with respect to the *pre-softmax* scores `u`.
- `np.outer(h, e)` is $h^\top e$, shape (d, V), which matches `W2`. `h @ e` would fail because the shapes (d,) and (V,) do not match.
- `W2 @ e`: (d, V) @ (V,) gives (d,). Do not transpose here; `W2` is already (d, V).
- `+=` inside the loop matters: if a word appears twice in the context (e.g. "the … the"), its row must receive both contributions. That matches the forward pass, where `W1[[6,1,6]]` counts row 6 twice. A vectorised `dW1[context_idxs] += ...` would silently apply duplicates only once, so use the loop.
- `eps = 1e-12` guards against `log(0) = -inf`.
- The student's version uses in-place `-=`, which mutates the caller's arrays. That is why the test passes `W1t.copy()`. The tutorial's version, `W1 = W1 - learning_rate * dW1`, creates new arrays. Both are correct.
- Sanity check from the test: after one SGD step the loss on the same example must go **down**. The PDF says that if it does not, the bug is in forward or backward, not in the training loop.

**Common mistakes**
- Writing `e = y_true - y_hat`, which flips the sign so training goes uphill. Another version is `+=` in the SGD step.
- Forgetting `/ len(context_idxs)`.
- Writing gradients into rows outside the context. The test asserts that `dW1[untouched_rows]` are all 0.

---

### ★★★ Block D: CBOW training loop `train`
**What it does:** for each epoch and each pair: words → indices, forward, loss, backward, update. Records the average loss per epoch. **TODO BLANK** (the body between `loss_history = []` and `return`).

```python
def train(training_pairs, word_to_int, vocab_size, embedding_dim=50,
          learning_rate=0.05, epochs=20):
    W1, W2 = init_params(vocab_size, embedding_dim)
    loss_history = []

    for epoch in range(epochs):
        total_loss = 0.0                                         # <-- KEY reset each epoch
        for context_words, target_word in training_pairs:
            # Skip if edge case results in empty context
            if not context_words:
                continue

            context_idxs = [word_to_int[w] for w in context_words]   # <-- KEY words -> ints
            target_idx = word_to_int[target_word]                    # <-- KEY

            y_hat, h, u = forward(context_idxs, W1, W2)              # <-- KEY
            total_loss += cross_entropy_loss(y_hat, target_idx)

            dW1, dW2 = backward(y_hat, h, context_idxs, target_idx, W1, W2, vocab_size)  # <-- KEY
            W1, W2 = sgd_update(W1, W2, dW1, dW2, learning_rate)                         # <-- KEY

        avg_loss = total_loss / len(training_pairs)              # <-- KEY average, not sum
        loss_history.append(avg_loss)
        print(f"CBOW Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}")

    return W1, W2, loss_history

W1_cbow, W2_cbow, loss_history_cbow = train(
    training_pairs, word_to_int, len(vocab),
    embedding_dim=50, learning_rate=0.05, epochs=20
)
plt.plot(loss_history_cbow, color="blue", label="CBOW Loss")
```
**Line-by-line notes**
- The order is fixed: forward → loss → backward → update. `backward` needs `y_hat` and `h` from forward.
- `if not context_words: continue` guards against an empty context (a 1-token text). Otherwise `np.mean` of an empty array gives nan, and `/0` appears in backward.
- `vocab_size = len(vocab)`, not `len(tokens)`.

**Common mistakes**
- Initialising `W1, W2` *inside* the epoch loop, which re-randomises them every epoch.
- Forgetting to reassign `W1, W2 = sgd_update(...)`. With the tutorial's non-in-place version, the weights would then never change.

---

### ★★★ Block E: Skip-gram pairs, forward, backward
**What it does:** the mirror image of CBOW. **TODO BLANK** (all three).

```python
def generate_skipgram_pairs(tokens, window_size):
    pairs = []
    n = len(tokens)
    for i in range(n):
        left = tokens[max(0, i - window_size):i]
        right = tokens[i + 1:i + 1 + window_size]
        context = left + right
        for c in context:                       # <-- KEY one pair per context word
            pairs.append((tokens[i], c))        # <-- KEY (input/centre, context)
    return pairs

def skipgram_forward(input_idx, W1, W2):
    h = W1[input_idx]                           # <-- KEY just a row lookup, no mean
    u = h @ W2
    y_hat = stable_softmax(u)
    return y_hat, h, u

def skipgram_backward(y_hat, h, input_idx, context_idx, W1, W2, vocab_size):
    y_true = np.zeros(vocab_size)
    y_true[context_idx] = 1.0                   # <-- KEY target is the CONTEXT word
    e = y_hat - y_true

    dW2 = np.outer(h, e)
    dh = W2 @ e

    dW1 = np.zeros_like(W1)
    dW1[input_idx] = dh                         # <-- KEY whole gradient, no division

    return dW1, dW2
```
**Line-by-line notes**
- The window logic is identical to CBOW. Only the inner `for c in context` and the tuple order change.
- Test: for "who" in `[the, boy, who, lived, came, to, die]`, the pairs must be the set `{(who,the),(who,boy),(who,lived),(who,came)}`. There are 22 pairs in total, against 7 for CBOW.
- The test asserts `np.allclose(h, sg_W1[0])`: h must be the raw row, not averaged.
- The loss and SGD functions are **reused** from CBOW.

**Common mistakes**
- Appending the whole context list `(tokens[i], context)`. That is CBOW reversed, not skip-gram.
- Writing `dh / len(...)` out of CBOW habit. The test checks that only row `input_idx` is non-zero, and the full gradient goes there.

---

### ★★★ Block F: `cosine_similarity` and `most_similar`
**What it does:** nearest neighbours by cosine similarity over the rows of the trained `W1`. **TODO BLANK.** `bow_cosine_similarity` in Part A is the identical function.

```python
def cosine_similarity(v1, v2):
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)       # <-- KEY
    if denom == 0:
        return 0.0
    return float(np.dot(v1, v2) / denom)                  # <-- KEY

def most_similar(word, W1, word_to_int, int_to_word, top_n=5):
    if word not in word_to_int:
        return []
    idx = word_to_int[word]
    query_vec = W1[idx]                                   # <-- KEY embedding = row of W1
    sims = []

    for other_word, other_idx in word_to_int.items():
        if other_word == word:                            # <-- KEY exclude the word itself
            continue
        sims.append((other_word, cosine_similarity(query_vec, W1[other_idx])))

    sims.sort(key=lambda pair: pair[1], reverse=True)     # <-- KEY sort by score, descending
    return sims[:top_n]                                   # <-- KEY

for w in ["alice", "rabbit", "hatter", "queen", "cat"]:
    if w in word_to_int:
        print(f"{w} ->", most_similar(w, W1_cbow, word_to_int, int_to_word, top_n=5))
# for Skip-gram: same call with W1_sg
```
**Line-by-line notes**
- After training, **`W1` *is* the embedding table**, so nothing more needs extracting. Row `W1[word_to_int[w]]` is the vector for `w`.
- `denom == 0` guards against an all-zero vector (division by zero).
- `pair[1]` is the score. `reverse=True` puts the most similar words first.

**Common mistakes**
- Not excluding the query word. It would always come out top with cosine 1.0.
- Sorting ascending, which returns the *least* similar words.

---

### ★★ Block G: Preprocessing and vocabulary (Task 1)
**What it does:** clean, tokenize, build the sorted vocab and both index maps. **TODO BLANK.**

```python
def clean_text(text):
    text = text.lower()                           # <-- KEY must come BEFORE the regex
    text = re.sub(r"[^a-z\s]", " ", text)         # <-- KEY drop non-letters (digits, punctuation)
    text = re.sub(r"\s+", " ", text).strip()      # <-- KEY collapse runs of spaces
    return text

def tokenize(text):
    return text.split()

def build_vocab(tokens):
    return sorted(set(tokens))                    # <-- KEY

cleaned_corpus = clean_text(corpus)
tokens = tokenize(cleaned_corpus)
vocab = build_vocab(tokens)

word_to_int = {w: i for i, w in enumerate(vocab)}         # <-- KEY
int_to_word = {i: w for w, i in word_to_int.items()}      # <-- KEY
```
**Line-by-line notes**
- `[^a-z\s]` means "anything that is NOT a lowercase letter or whitespace". The `^` inside `[...]` negates the class. If you lowercase *after* the regex, every capital letter is deleted.
- The replacement is `" "`, not `""`, so `rabbit-hole` becomes `rabbit hole`, not `rabbithole`. The `\s+` pass then cleans up the extra spaces.
- Test: `"The Boy Who Lived came to die! He was 11 years old."` must become `"the boy who lived came to die he was years old"`. The "11" vanishes.
- `enumerate(vocab)` yields `(i, w)`, so the comprehension is `{w: i for i, w in ...}`.

**Common mistakes**
- Writing `{i: w for i, w in enumerate(vocab)}` for `word_to_int`. That is backwards; it builds `int_to_word`.
- Returning `set(tokens)` without sorting. That gives a non-deterministic order and fails `vocab == sorted(set(toks))`.

---

### ★★ Block H: Bag-of-Words (Task A1)
**What it does:** builds BoW count vectors and compares the toy sentences. **TODO BLANK.** The template even had `bow_vocab = []  # TODO`.

```python
bow_vocab = sorted(set(w for s in toy_sentences for w in s.lower().split()))   # <-- KEY

def build_bow_vector(tokens, vocab):
    vec = np.zeros(len(vocab), dtype=int)       # <-- KEY one slot per vocab word
    for t in tokens:
        if t in vocab:
            vec[vocab.index(t)] += 1            # <-- KEY count, not set to 1
    return vec

bow_vecs = [build_bow_vector(s.lower().split(), bow_vocab) for s in toy_sentences]
sim_king_queen = bow_cosine_similarity(bow_vecs[0], bow_vecs[1])    # 0.875
sim_king_wizard = bow_cosine_similarity(bow_vecs[0], bow_vecs[2])   # 0.289
```
**Notes / mistakes**
- `vec[...] = 1` gives *binary* BoW. The test expects counts `[2,0,1,2]`.
- `vocab.index(t)` works because `vocab` is a **list**. It is O(V); for big vocabularies you would use the `word_to_int` dict.
- Reading the nested comprehension: for each sentence `s`, for each word `w` in it, collect `w`.

---

### ★★ Block I: `train_skipgram` (Task D4)
**What it does:** the same loop as CBOW but over `(input, context)` pairs. **TODO BLANK.**

```python
def train_skipgram(pairs, word_to_int, vocab_size, embedding_dim=50,
                    learning_rate=0.05, epochs=20):
    W1, W2 = init_params(vocab_size, embedding_dim)
    loss_history = []
    for epoch in range(epochs):
        total_loss = 0.0
        for input_word, context_word in pairs:
            input_idx = word_to_int[input_word]
            context_idx = word_to_int[context_word]

            y_hat, h, u = skipgram_forward(input_idx, W1, W2)                 # <-- KEY
            total_loss += cross_entropy_loss(y_hat, context_idx)             # <-- KEY loss vs CONTEXT
            dW1, dW2 = skipgram_backward(y_hat, h, input_idx, context_idx, W1, W2, vocab_size)
            W1, W2 = sgd_update(W1, W2, dW1, dW2, learning_rate)

        avg_loss = total_loss / len(pairs)
        loss_history.append(avg_loss)
    return W1, W2, loss_history

sg_pairs = generate_skipgram_pairs(tokens, window_size=2)
W1_sg, W2_sg, loss_history_sg = train_skipgram(sg_pairs, word_to_int, len(vocab),
                                               embedding_dim=50, learning_rate=0.05, epochs=20)
```
**Note:** use the same corpus subset, `embedding_dim` and number of epochs as CBOW so the comparison is fair. Plot both `loss_history_cbow` and `loss_history_sg` on the same axes.

---

### ★★ Block J: Analogy with your own embeddings (Task 6.4)
**TODO BLANK.** The assignment wanted `harry − he + she`; the student used `king − he + she`.

```python
v_king = W1_cbow[word_to_int["king"]]
v_he = W1_cbow[word_to_int["he"]]
v_she = W1_cbow[word_to_int["she"]]

target_vec = v_king - v_he + v_she                     # <-- KEY  a - b + c

sims = []
for other_word, other_idx in word_to_int.items():
    if other_word in ["king", "he", "she"]:            # <-- KEY exclude all 3 input words
        continue
    sims.append((other_word, cosine_similarity(target_vec, W1_cbow[other_idx])))
sims.sort(key=lambda pair: pair[1], reverse=True)
print("king - he + she ≈", sims[:5])
```
The result (puppy, door, officer…) was not sensible, which is expected: 27k tokens and 20 epochs are far too little for analogies to emerge. The assignment explicitly says a failed analogy is fine if you explain why.

---

### ★ Block K: gensim GloVe (Tasks B1–B3)
**TODO BLANK** (one-liners).

```python
import gensim.downloader as glove_api
word_vectors = glove_api.load("glove-wiki-gigaword-50")       # 400,000 words, 50-d
word_vectors.similarity("king", "queen")                      # 0.784  (king,cabbage)=0.113
analogy_result = word_vectors.most_similar(positive=["king", "woman"], negative=["man"], topn=5)  # <-- KEY
for word, score in analogy_result:                            # returns list of (word, score)
    print(f"{word:>10s}  {score:.3f}")
word_vectors.most_similar(positive=["paris", "italy"], negative=["france"], topn=5)  # rome 0.847
```
Mnemonic: **positive = the words you add**, **negative = the word you subtract**. `a − b + c` becomes `positive=[a, c], negative=[b]`.

### ★ Block L: PCA parallelogram (Task B4)
**TODO BLANK.**

```python
words = ["king", "man", "woman", "queen"]
vecs = [word_vectors[w] for w in words]                # each is a (50,) vector
coords = PCA(n_components=2).fit_transform(vecs)       # <-- KEY → (4, 2)
man_xy, king_xy = coords[1], coords[0]
woman_xy, queen_xy = coords[2], coords[3]
arrow1 = king_xy - man_xy
arrow2 = queen_xy - woman_xy
cos_between_arrows = np.dot(arrow1, arrow2) / (np.linalg.norm(arrow1) * np.linalg.norm(arrow2))  # 0.968
```
Arrows are drawn with `plt.annotate("", xy=king_xy, xytext=man_xy, arrowprops=dict(arrowstyle="->"))`, where `xy` is the head and `xytext` is the tail.

## 5.5 Fill-in-the-blank practice

**Q1.** CBOW context window:
```python
left  = tokens[____(0, i - window_size) : i]
right = tokens[____ : ____]
pairs.append((____, ____))
```
**Q2.** CBOW forward:
```python
h = np.____(W1[context_idxs], axis=____)
u = ____ @ ____
y_hat = stable_softmax(u)
```
**Q3.** Stable softmax:
```python
x_shifted = x - ________
exps = np.exp(x_shifted)
return exps / ________
```
**Q4.** CBOW backward:
```python
y_true = np.zeros(vocab_size); y_true[____] = 1.0
e = ________
dW2 = np.____(h, e)
dh = ____ @ e
for idx in context_idxs:
    dW1[idx] ____ dh / ________
```
**Q5.** Skip-gram backward. What replaces the loop in Q4?
```python
dW1 = np.zeros_like(W1)
dW1[________] = ____
```
**Q6.** `init_params(vocab_size=6, embedding_dim=3)`: fill in `W1 = np.random.randn(__, __) * ____` and `W2 = np.random.randn(__, __) * ____`.

**Q7.** Nearest neighbours:
```python
if other_word == word: ________
sims.sort(key=lambda pair: ________, reverse=____)
return sims[________]
```
**Q8.** Cleaning:
```python
text = text.____()
text = re.sub(r"________", " ", text)
text = re.sub(r"____", " ", text).strip()
```
**Q9.** gensim: write `paris − france + italy` as a call: `word_vectors.most_similar(positive=____, negative=____, topn=5)`.

**Q10.** How many CBOW pairs and how many Skip-gram pairs come from `[the, boy, who, lived, came, to, die]` with `window_size=2`? What is the cross-entropy at initialisation for V = 9?

<details><summary>Answers</summary>

1. `max`; `i + 1 : i + 1 + window_size`; `(context, tokens[i])`
2. `mean`, `0`; `h @ W2`
3. `np.max(x)`; `np.sum(exps)`
4. `target_idx`; `y_hat - y_true`; `outer`; `W2`; `+=`, `len(context_idxs)`
5. `dW1[input_idx] = dh` (no division)
6. `W1 = np.random.randn(6, 3) * 0.01`, `W2 = np.random.randn(3, 6) * 0.01`
7. `continue`; `pair[1]`; `True`; `:top_n`
8. `lower`; `[^a-z\s]`; `\s+`
9. `positive=["paris", "italy"], negative=["france"]` gives `rome` (0.847)
10. CBOW: 7 (one per token). Skip-gram: 2+3+4+4+4+3+2 = 22. Loss: $-\ln(1/9)=\ln 9\approx 2.197$.
</details>

## 5.6 Quick recall

- **Pipeline:** clean → tokenize → `sorted(set())` vocab → `word_to_int` / `int_to_word` → pairs → init → (forward → loss → backward → SGD) × pairs × epochs → `W1` = embeddings → cosine neighbours.
- **CBOW:** `h = np.mean(W1[ctx], axis=0)`; `u = h @ W2`; `y_hat = softmax(u)`; `L = -np.log(y_hat[t] + 1e-12)`.
- **Gradients:** `e = y_hat - y_true`; `dW2 = np.outer(h, e)`; `dh = W2 @ e`; CBOW `dW1[c] += dh/m`; Skip-gram `dW1[i] = dh`.
- **Shapes:** `W1` (V, d), `W2` (d, V), `h` (d,), `u`/`y_hat`/`e` (V,), `dW2` (d, V).
- **Stable softmax:** subtract `np.max(x)` before `np.exp`. Correct because $\text{softmax}(u+c)=\text{softmax}(u)$.
- **Cosine:** `np.dot(a,b) / (np.linalg.norm(a)*np.linalg.norm(b))`, returning 0.0 when the denominator is 0.
- **Window slicing:** `tokens[max(0,i-w):i] + tokens[i+1:i+1+w]`, with no padding.
- **Pair counts:** CBOW = n; Skip-gram = $2wn - w(w+1)$.
- **Init loss ≈ ln V.** If the loss does not drop after one SGD step on one example, the bug is in forward or backward.
- **gensim:** `glove_api.load("glove-wiki-gigaword-50")`, `.similarity(a,b)`, `.most_similar(positive=[...], negative=[...], topn=5)` returning `[(word, score), ...]`, `wv[word]` returning a (50,) array, `.index_to_key` for the vocab list.
- **PCA:** `PCA(n_components=2).fit_transform(list_of_vectors)` returns (k, 2).
- **Likely theory questions (from the instructor's PDF):**
  - *Why sort the vocab?* Only for a reproducible mapping.
  - *Window at the first word?* The left slice is empty, so the context is just the right words.
  - *Why is most of dW1 zero?* Only the context words contributed to h.
  - *Why cosine over Euclidean?* Frequent words have bigger norms; cosine compares direction only.
  - *Why does Skip-gram produce more pairs?* Each context word becomes its own example.
  - *Why does Skip-gram's loss stay higher?* It is a one-to-many prediction with an entropy floor.
  - *Why use Skip-gram anyway?* It gives cleaner, undiluted gradients for rare words.
  - *Why does BoW fail for words?* One-hot vectors are orthogonal, so the cosine is always 0.
  - *Why don't the PCA arrows come out perfectly parallel?* 50-D → 2-D loses information.

---


---

<a id="lab-6"></a>

# Lab 6 — Language Models & Perplexity: RNN LM vs Fixed-Window Neural LM vs Bigram

## 6.1 What this lab is about

Build a word-level **RNN language model** in **PyTorch** that reads the previous 5 words and predicts the next one, and evaluate it with **perplexity** on a held-out test split. Then compare it with two baselines: a **fixed-window feed-forward neural LM** (Bengio-style: concatenate 5 embeddings → MLP) and a **bigram LM with add-one smoothing**. **Framework: PyTorch** (`torch.nn`, `torch.optim`), not Keras. In the original template **every code cell was empty** (checked against the git history), so each block below was written from scratch.

## 6.2 Core concepts & formulas

**Language model.** $P(w_1,\dots,w_N)=\prod_i P(w_i\mid w_{<i})$. The neural models here approximate $P(w_i\mid w_{i-5},\dots,w_{i-1})$, i.e. a 5-word history. The bigram model uses only $w_{i-1}$.

**Perplexity.** $\text{PP}(W)=P(w_1..w_N)^{-1/N}=\sqrt[N]{\frac{1}{P(w_1..w_N)}}=\exp\!\Big(-\frac1N\sum_{i}\ln P(w_i\mid h_i)\Big)=\exp(\text{avg cross-entropy})$.
- Lower is better. It is the model's "effective branching factor".
- A **uniform** model over V words has PP = V, which is **985** here. Anything above that is worse than guessing.
- *Example:* if a model gives 4 test words probabilities 1/4, 1/2, 1/8, 1/4, the average NLL is $\frac{\ln4+\ln2+\ln8+\ln4}{4}=\frac{(2+1+3+2)\ln2}{4}=2\ln2$, so PP $=e^{2\ln2}=4$.
- `nn.CrossEntropyLoss` uses the **natural log**, so perplexity = `np.exp(avg_loss)`, not `2 ** avg_loss`.

**Bigram LM with add-one (Laplace) smoothing.**
$P(w_i\mid w_{i-1})=\dfrac{C(w_{i-1},w_i)+1}{C(w_{i-1})+V}$. Every unseen bigram gets a non-zero probability $1/(C(w_{i-1})+V)$.

**Fixed-window neural LM.** $x=[e(w_{i-5});\dots;e(w_{i-1})]$, the **concatenation** of the embeddings, of size $5\cdot64=320$. Then $h=\text{ReLU}(W_1x+b_1)$ and logits $=W_2h+b_2$. Its limits: the context is fixed at n words, `fc1` grows with n, and each position has its own weights, so nothing is shared across positions.

**RNN LM.** $h_t=\tanh(W_{ih}x_t+b_{ih}+W_{hh}h_{t-1}+b_{hh})$, where tanh is the `nn.RNN` default. The logits come from the **last** hidden state: $W_{fc}h_T+b$. The same weights are used at every time step, so in principle the history can be any length.

**Cross-entropy in PyTorch.** `nn.CrossEntropyLoss()` = `LogSoftmax` + `NLLLoss`. It takes **raw logits** of shape (N, C) and **class indices** of shape (N,) and dtype long, and by default returns the **mean** over the batch.

## 6.3 Data & pipeline

Corpus: an inline string, Edith Wharton's short story about the painter Jack Gisburn (*The Verdict*).

1. **Clean:** `re.sub(r"[^a-zA-Z\s']", " ", corpus.lower())`. This **keeps apostrophes**, so `it's` and `don't` stay single tokens. Then `.split()` gives **3,749 tokens**.
2. **Split by position:** the first 80% is train and the rest is test (`split_idx = int(0.8 * len(tokens))`), giving 2,999 / 750 tokens. There is no shuffling, so test is the end of the story.
3. **Vocab from TRAIN only:** `["<unk>"] + sorted(Counter(train_tokens).keys())` gives **V = 985**, with `<unk>` at index 0.
4. **Encode:** `word_to_idx.get(token, unk_idx)`, so unseen test words map to `<unk>`.
5. **Sliding windows (many-to-one):** `x = ids[i:i+5]`, `y = ids[i+5]`. This gives 2,999 − 5 = **2,994** train and 750 − 5 = **745** test sequences. *(This is not the `tokens[:-1]` / `tokens[1:]` many-to-many setup. Only the last time step is used.)*
6. **Tensors:** `torch.tensor(..., dtype=torch.long)` gives `train_X` (2994, 5) and `train_y` (2994,).
7. **Train RNN:** 40 epochs, Adam with lr 1e-3, batch 64, shuffled via `torch.randperm`, grad clipping at 1.0. Train loss went 6.65 → 0.09 (≈ ln 985 = 6.89 at the start).
8. **Evaluate:** perplexity on the test set with batch 128.
9. **Baselines:** the bigram model on the raw id lists; the fixed-window NN with the same `train_X` and hyperparameters, but 25 epochs.

| Hyperparameter | Value |
|---|---|
| `seq_len` / `context_size` | 5 |
| `embedding_dim` | 64 |
| `hidden_dim` | 128 |
| optimizer | `optim.Adam(model.parameters(), lr=0.001)` |
| epochs | RNN 40, fixed-window 25 |
| batch size | 64 train, 128 eval |
| grad clip | `max_norm=1.0` |

**Shapes for one batch (B = 64):**

| Step | RNN LM | Fixed-window LM |
|---|---|---|
| input `x` | (B, 5) long | (B, 5) long |
| `self.embedding(x)` | (B, 5, 64) | (B, 5, 64) |
| `self.rnn(emb)` → `out` | (B, 5, 128): all time steps | — |
| `hidden` (h_n) | **(1, B, 128)**: layers first, even with `batch_first=True` | — |
| `out[:, -1, :]` | (B, 128) | — |
| `emb.view(B, -1)` | — | (B, 320) |
| `relu(fc1(...))` | — | (B, 128) |
| logits | (B, 985) | (B, 985) |
| `criterion(logits, y)` | scalar (mean over B) | scalar |

Parameter counts: Embedding 985·64 = 63,040. RNN 64·128 + 128·128 + 2·128 = 24,832. fc 128·985 + 985 = 127,065. The fixed-window model's fc1 is 320·128 + 128 = 41,088.

**Results (test perplexity):**

| Model | Perplexity |
|---|---|
| Bigram, add-one | **758.6** (best) |
| RNN LM | 3,419.4 |
| Fixed-window NN LM | 38,629.3 |
| *uniform baseline* | *985* |

Why the neural models lose here:
- The corpus is tiny (3k tokens), so they **overfit**. The RNN's final train loss of 0.09 corresponds to a train PP of about 1.1, while its test PP is 3,419. They are confidently wrong, which puts them *worse than uniform*.
- `<unk>` never appears in the training data (the vocab was built from train), so the models learn to give it near-zero probability. That costs a lot every time a test target is OOV.
- Add-one smoothing guarantees the bigram model never gives zero probability.

## 6.4 Exam-critical code blocks

### ★★★ Block A: Data prep and sliding-window sequences (Step 1.1, blank cell)
**What it does:** clean → split → vocab with `<unk>` → encode → (5-word input, next-word target) tensors.

```python
clean_text = re.sub(r"[^a-zA-Z\s']", " ", corpus.lower())
tokens = clean_text.split()

split_idx = int(0.8 * len(tokens))                       # <-- KEY
train_tokens = tokens[:split_idx]
test_tokens = tokens[split_idx:]

word_counts = collections.Counter(train_tokens)
vocab = ["<unk>"] + sorted(word_counts.keys())           # <-- KEY vocab from TRAIN only
word_to_idx = {word: idx for idx, word in enumerate(vocab)}
idx_to_word = {idx: word for word, idx in word_to_idx.items()}
unk_idx = word_to_idx["<unk>"]

def encode(token_list):
    return [word_to_idx.get(token, unk_idx) for token in token_list]   # <-- KEY .get with default

train_ids = encode(train_tokens)
test_ids = encode(test_tokens)

seq_len = 5

def make_sequences(token_ids, sequence_length):
    x, y = [], []
    for i in range(len(token_ids) - sequence_length):   # <-- KEY  minus seq_len
        x.append(token_ids[i:i + sequence_length])      # <-- KEY  window of 5
        y.append(token_ids[i + sequence_length])        # <-- KEY  the NEXT word
    return x, y

train_X, train_y = make_sequences(train_ids, seq_len)
test_X, test_y = make_sequences(test_ids, seq_len)

train_X = torch.tensor(train_X, dtype=torch.long)       # <-- KEY long for Embedding/CE
train_y = torch.tensor(train_y, dtype=torch.long)
test_X = torch.tensor(test_X, dtype=torch.long)
test_y = torch.tensor(test_y, dtype=torch.long)
```
**Line-by-line notes**
- `range(len - L)`, not `len - L + 1`, because the target `ids[i+L]` must exist. The last valid i is len−L−1.
- Example: ids `[a,b,c,d,e,f,g]` with L=5 gives `[a,b,c,d,e]→f` and `[b,c,d,e,f]→g`. That is 2 = 7−5 sequences.
- `word_to_idx[token]` (without `.get`) raises a `KeyError` on unseen test words.
- The regex replacement happens after `.lower()`, so the `A-Z` in the class is redundant but harmless.

**Common mistakes**
- Building the vocab from *all* tokens. That leaks test words and means `<unk>` never fires.
- Using float dtype. `nn.Embedding` needs integer indices, and `CrossEntropyLoss` targets must be long.

---

### ★★★ Block B: `RNNLanguageModel` (Step 1.2, blank cell)
**What it does:** Embedding → RNN → Linear on the **last** time step.

```python
class RNNLanguageModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super().__init__()                                          # <-- KEY
        self.embedding = nn.Embedding(vocab_size, embedding_dim)    # <-- KEY (num_embeddings, dim)
        self.rnn = nn.RNN(embedding_dim, hidden_dim, batch_first=True)  # <-- KEY (input_size, hidden_size)
        self.fc = nn.Linear(hidden_dim, vocab_size)                 # <-- KEY (in, out)

    def forward(self, x, hidden=None):
        emb = self.embedding(x)                 # (B, T) -> (B, T, E)
        out, hidden = self.rnn(emb, hidden)     # <-- KEY returns a TUPLE
        logits = self.fc(out[:, -1, :])         # <-- KEY last time step -> (B, V)
        return logits, hidden

embedding_dim = 64
hidden_dim = 128
model = RNNLanguageModel(vocab_size=len(vocab), embedding_dim=embedding_dim, hidden_dim=hidden_dim)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

criterion = nn.CrossEntropyLoss()                            # <-- KEY
optimizer = optim.Adam(model.parameters(), lr=0.001)         # <-- KEY
```
**Line-by-line notes**
- `nn.RNN(input_size, hidden_size, batch_first=True)`. The defaults are `num_layers=1` and `nonlinearity='tanh'`. Without `batch_first=True` the RNN expects (T, B, E), and our (B, T, E) input would be read the wrong way round.
- `self.rnn(emb, hidden)` returns `(output, h_n)`: `output` (B, T, H) holds every step, and `h_n` (num_layers, B, H) holds the final step. For a 1-layer RNN, `out[:, -1, :]` equals `hidden[-1]`.
- `hidden=None` means a zero initial state.
- Printed model: `Embedding(985, 64)`, `RNN(64, 128, batch_first=True)`, `Linear(in_features=128, out_features=985, bias=True)`.
- `forward` returns **two** values, so callers write `logits, _ = model(x_batch)`.

**Common mistakes**
- `nn.Linear(hidden_dim, embedding_dim)`: the output size must be **vocab_size**, since we score every word.
- Applying `softmax` before `CrossEntropyLoss`. CE already contains log-softmax.
- Using `out[:, 0, :]` (the first step) or `out[-1]`. With batch_first, `out[-1]` is the last *sample* in the batch, not the last time step.

---

### ★★★ Block C: Training loop (Step 1.3, "Complete the training loop")
**What it does:** mini-batch training with shuffling and gradient clipping, logging the average loss per epoch.

```python
epochs = 40
batch_size = 64

for epoch in range(1, epochs + 1):
    model.train()                                       # <-- KEY train mode
    permutation = torch.randperm(len(train_X))          # <-- KEY shuffle indices each epoch

    epoch_loss = 0.0

    for i in range(0, len(train_X), batch_size):        # <-- KEY step by batch_size
        indices = permutation[i:i + batch_size]
        x_batch = train_X[indices].to(device)
        y_batch = train_y[indices].to(device)

        optimizer.zero_grad()                           # <-- KEY 1. clear old grads
        logits, _ = model(x_batch)                      # <-- KEY 2. forward
        loss = criterion(logits, y_batch)               # <-- KEY 3. loss(logits, targets)
        loss.backward()                                 # <-- KEY 4. backprop
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # <-- KEY 5. clip (after backward, before step)
        optimizer.step()                                # <-- KEY 6. update

        epoch_loss += loss.item() * x_batch.size(0)     # <-- KEY undo the mean -> sum

    avg_loss = epoch_loss / len(train_X)
    if epoch % 5 == 0 or epoch == 1:
        print(f"Epoch {epoch:02d}/{epochs} - Train Loss: {avg_loss:.4f}")
```
**Line-by-line notes**
- The order to memorise is **zero_grad → forward → loss → backward → clip → step**.
- Clipping must sit **between** `backward()` (grads now exist) and `step()` (grads get used). RNNs are prone to exploding gradients, which is why clipping is used.
- `loss.item()` turns the tensor into a Python float (and detaches it from the graph). It is multiplied by `x_batch.size(0)`, **not** `batch_size`, because the last batch has 2994 mod 64 = 50 samples.
- `train_X[indices]` indexes with a tensor of positions; this is how the random mini-batches are drawn.

**Common mistakes**
- Forgetting `zero_grad()`, which makes gradients accumulate across batches.
- Writing `criterion(y_batch, logits)`. The argument order is (input logits, target).
- Writing `epoch_loss += loss`, which keeps the whole graph alive. Use `.item()`.

---

### ★★★ Block D: `calculate_perplexity` (Step 1.4, blank cell)
**What it does:** computes the average NLL over all test targets and exponentiates it.

```python
def calculate_perplexity(model, X, y, criterion, batch_size=128):
    model.eval()                                       # <-- KEY eval mode
    total_loss = 0.0
    total_tokens = 0

    with torch.no_grad():                              # <-- KEY no graph, no grads
        for i in range(0, len(X), batch_size):
            x_batch = X[i:i + batch_size].to(device)   # no shuffling needed at test time
            y_batch = y[i:i + batch_size].to(device)

            logits, _ = model(x_batch)
            loss = criterion(logits, y_batch)          # mean NLL of this batch

            total_loss += loss.item() * x_batch.size(0)    # <-- KEY sum of NLLs
            total_tokens += x_batch.size(0)                # <-- KEY count of predictions

    avg_nll = total_loss / total_tokens                # <-- KEY
    return float(np.exp(avg_nll))                      # <-- KEY PP = e^(avg NLL)

rnn_perplexity = calculate_perplexity(model, test_X, test_y, criterion)   # 3419.4075
```
**Line-by-line notes**
- Each sequence predicts exactly one token, so "tokens" means "number of sequences" (745).
- Averaging the batch means directly (sum of means / #batches) would be **wrong**, because the last batch is smaller (745 = 5·128 + 105). Weight each mean by its batch size, as the code does.
- `np.exp` matches `CrossEntropyLoss`'s natural log.

**Common mistakes**
- Returning `avg_nll` itself. That is the cross-entropy, not the perplexity.
- Writing `np.exp(total_loss)`, i.e. exponentiating the sum instead of the mean.
- Leaving out `model.eval()` / `torch.no_grad()`. For this model the numbers would not change (there is no dropout), but graders look for them and they save memory.

---

### ★★ Block E: `FixedWindowNNLM`
**What it does:** concatenates the 5 context embeddings and passes them through a 1-hidden-layer MLP to get next-word logits.

```python
class FixedWindowNNLM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, context_size, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.fc1 = nn.Linear(context_size * embedding_dim, hidden_dim)   # <-- KEY 5*64 = 320 inputs
        self.fc2 = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        emb = self.embedding(x)                 # [batch, context, emb_dim]
        emb_flat = emb.view(emb.size(0), -1)   # <-- KEY [batch, context*emb_dim]  (concatenation)
        h = torch.relu(self.fc1(emb_flat))     # <-- KEY non-linearity
        logits = self.fc2(h)
        return logits                           # ONE value (no hidden), unlike the RNN

ff_model = FixedWindowNNLM(vocab_size=len(vocab), embedding_dim=64,
                           context_size=seq_len, hidden_dim=128).to(device)
```
**Notes / mistakes**
- `view(B, -1)` flattens the time and embedding dimensions together; `-1` means "infer this size" (here 320). Writing `nn.Linear(embedding_dim, hidden_dim)` gives a shape-mismatch error.
- The training loop is identical to Block C except that you write `logits = ff_model(x_batch)` with **no** `, _`. `neural_perplexity` is identical to Block D apart from that same line.
- Contrast with CBOW from Lab 5: CBOW **averages** the context embeddings (order lost, no non-linearity), while this model **concatenates** them (order kept, then ReLU).

---

### ★★ Block F: Bigram perplexity with add-one smoothing
**What it does:** count bigrams on train, then score test bigrams with Laplace smoothing and turn the log-probabilities into a perplexity.

```python
def bigram_perplexity(train_ids, test_ids, vocab_size):
    bigram_counts = collections.Counter()
    prev_counts = collections.Counter()

    for i in range(1, len(train_ids)):
        prev_w = train_ids[i - 1]
        curr_w = train_ids[i]
        bigram_counts[(prev_w, curr_w)] += 1           # <-- KEY C(w_{i-1}, w_i)
        prev_counts[prev_w] += 1                       # <-- KEY C(w_{i-1}) as a history

    log_prob_sum = 0.0
    n = 0

    for i in range(1, len(test_ids)):
        prev_w = test_ids[i - 1]
        curr_w = test_ids[i]
        prob = (bigram_counts[(prev_w, curr_w)] + 1.0) / (prev_counts[prev_w] + vocab_size)  # <-- KEY
        log_prob_sum += np.log(prob)                   # <-- KEY sum logs, don't multiply probs
        n += 1

    return float(np.exp(-log_prob_sum / n))            # <-- KEY note the minus sign

ngram_perplexity = bigram_perplexity(train_ids, test_ids, len(vocab))   # 758.6031
```
**Notes / mistakes**
- `Counter` returns 0 for missing keys, so unseen bigrams need no special case: their probability is `1/(C(prev)+V)`.
- The denominator adds **V**, not 1. Adding 1 to each of the V possible next words adds V in total.
- Summing logs instead of multiplying probabilities avoids underflow: a product of 750 small numbers rounds to 0.0.

## 6.5 Fill-in-the-blank practice

**Q1.** Sliding windows:
```python
for i in range(len(token_ids) - ________):
    x.append(token_ids[________])
    y.append(token_ids[________])
```
**Q2.** Vocab with UNK:
```python
vocab = [________] + sorted(word_counts.keys())
def encode(token_list):
    return [word_to_idx.____(token, ________) for token in token_list]
```
**Q3.** RNN model `__init__`:
```python
self.embedding = nn.Embedding(________, ________)
self.rnn = nn.RNN(________, ________, batch_first=____)
self.fc = nn.Linear(________, ________)
```
**Q4.** RNN `forward`:
```python
emb = self.embedding(x)
out, hidden = ________(emb, hidden)
logits = self.fc(out[____, ____, ____])
```
**Q5.** Put the training steps in order and fill the blanks:
```python
optimizer.________()
logits, _ = model(x_batch)
loss = criterion(________, ________)
loss.________()
torch.nn.utils.________(model.parameters(), max_norm=1.0)
optimizer.________()
epoch_loss += loss.________() * x_batch.size(____)
```
**Q6.** Perplexity:
```python
model.________()
with torch.________():
    ...
avg_nll = ________ / ________
return float(np.____(avg_nll))
```
**Q7.** Fixed-window model:
```python
self.fc1 = nn.Linear(________ * ________, hidden_dim)
emb_flat = emb.view(emb.size(____), ____)
h = torch.________(self.fc1(emb_flat))
```
**Q8.** Add-one bigram:
```python
prob = (bigram_counts[(prev_w, curr_w)] + ____) / (prev_counts[prev_w] + ________)
return float(np.exp(________ / n))
```
**Q9.** With B = 64, T = 5, E = 64, H = 128 and V = 985, give the shapes of `emb`, `out`, `hidden`, `out[:, -1, :]` and `logits`.

**Q10.** A model assigns probability 1/985 to every test word. What is its perplexity? And if the average test cross-entropy is 2.0 nats, what is the perplexity?

<details><summary>Answers</summary>

1. `sequence_length`; `i:i + sequence_length`; `i + sequence_length`
2. `"<unk>"`; `get`, `unk_idx`
3. `vocab_size, embedding_dim`; `embedding_dim, hidden_dim`, `True`; `hidden_dim, vocab_size`
4. `self.rnn`; `:, -1, :`
5. `zero_grad`; `logits, y_batch`; `backward`; `clip_grad_norm_`; `step`; `item`, `0`
6. `eval`; `no_grad`; `total_loss / total_tokens`; `exp`
7. `context_size * embedding_dim`; `0`, `-1`; `relu`
8. `1.0`; `vocab_size`; `-log_prob_sum`
9. `emb` (64, 5, 64); `out` (64, 5, 128); `hidden` (1, 64, 128); `out[:, -1, :]` (64, 128); `logits` (64, 985)
10. PP = 985, since a uniform model's PP equals V. $e^{2.0}\approx 7.39$.
</details>

## 6.6 Quick recall

- **Perplexity** = $\exp(\text{mean NLL})$ = $P(W)^{-1/N}$. Lower is better. Uniform gives PP = V. Use `np.exp`, not `2**`, because PyTorch CE uses ln.
- **Mean → sum:** `loss.item() * x_batch.size(0)`, accumulated, then divided by the total count.
- **API signatures:**
  - `nn.Embedding(num_embeddings=V, embedding_dim=E)`: (B, T) long → (B, T, E)
  - `nn.RNN(input_size=E, hidden_size=H, batch_first=True)` → `(out (B,T,H), h_n (layers,B,H))`
  - `nn.Linear(in_features, out_features)`
  - `nn.CrossEntropyLoss()(logits (N,C), target (N,) long)`, which wants raw logits
  - `optim.Adam(model.parameters(), lr=0.001)`
  - `torch.randperm(n)`
  - `torch.nn.utils.clip_grad_norm_(params, max_norm=1.0)`
  - `tensor.view(B, -1)`
  - `torch.relu`
- **Training order:** `train()` → `randperm` → [`zero_grad` → forward → loss → `backward` → clip → `step`].
- **Eval:** `model.eval()` + `with torch.no_grad():`, no shuffling.
- **Data:** vocab from **train only**, with `"<unk>"` at index 0. `dict.get(tok, unk_idx)`. Windows: `x = ids[i:i+5]`, `y = ids[i+5]` for `i in range(len-5)`. 80/20 positional split.
- **Model contrasts:** RNN = shared weights over time and unbounded history in principle, uses `out[:, -1, :]`. Fixed-window = concatenation (`view`) + ReLU MLP, fc1 input is `context*E`. Bigram = counts with add-one, $\frac{C(p,w)+1}{C(p)+V}$.
- **Results:** bigram 758.6 < RNN 3,419 < fixed-window 38,629, against a uniform baseline of 985. Neural models overfit a 3k-token corpus, and `<unk>` is never a training target.
- **Analysis Q, "RNN advantages":** it carries a hidden state, so it handles longer and variable-length context; it learns distributed representations (unlike n-gram counts); and it shares parameters across time (unlike a fixed window, which can't see past n words).
- **Gotchas:**
  - `hidden` is NOT batch-first.
  - `out[-1]` is the last *sample*, not the last step.
  - The RNN forward returns a tuple; the fixed-window forward returns only logits.
  - Use `dtype=torch.long`.
  - Clip after `backward`, before `step`.

---

<a id="lab-7"></a>

# Lab 7 — RNN Applications: SimpleRNN → LSTM, Classification → POS Tagging

**Framework:** TensorFlow / Keras, **Sequential API** (`from tensorflow.keras.models import Sequential`).
No `Tokenizer` / `texts_to_sequences` anywhere: vocabularies are **hand-built Python dicts**, words are
looked up with `dict.get(w, 1)`, and padding uses `pad_sequences`.

## 7.1 What this lab is about

- **Tutorial:** sentiment classification (pos/neg) with `Embedding → SimpleRNN(32) → Dense(1, sigmoid)`.
  Test accuracy is about 64%, and it falls on long sentences (vanishing gradient).
- **Task 1:** change *one line* (`SimpleRNN(32)` → `LSTM(32)`), then compare accuracy on SHORT / ALL / LONG sentences.
- **Tasks 2–5:** POS tagging on the Penn Treebank (12 universal tags). This is many-to-many: one tag per word.
  Model: `Embedding(mask_zero=True) → LSTM(return_sequences=True) → TimeDistributed(Dense(softmax))`, then the
  same model with the LSTM wrapped in `Bidirectional`. Accuracy is measured on **real tokens only**, never on padding.

## 7.2 Core concepts & formulas

**Two task shapes.**
- *Many-to-one* (sentiment): read the whole sentence and keep only the **final hidden state** (the lecture calls it the "sentence encoding"). One label per sentence. In Keras this is the default (`return_sequences=False`).
- *Many-to-many* (tagging): you need a hidden state at **every** step → `return_sequences=True`, then the same classifier at each step → `TimeDistributed(Dense(...))`.

**SimpleRNN (the formula given in the tutorial):**
$$h_t = \tanh\left(W_h h_{t-1} + W_x x_t + b\right)$$

**Vanishing gradient.** The gradient that reaches an early word is a product of one Jacobian per step:
$$\frac{\partial \text{loss}}{\partial h_1} = \frac{\partial \text{loss}}{\partial h_T}\cdot \prod_{t=2}^{T} \frac{\partial h_t}{\partial h_{t-1}}$$
If the factors are < 1, the product shrinks exponentially with distance, so the network forgets early words.
That is why accuracy is SHORT 0.705 but LONG 0.584 for the SimpleRNN.

**LSTM** (standard form; your lecture's notation may differ slightly). It adds a **cell state** $c_t$ controlled by gates:
$$f_t=\sigma(W_f[h_{t-1},x_t]+b_f)\quad i_t=\sigma(W_i[h_{t-1},x_t]+b_i)\quad o_t=\sigma(W_o[h_{t-1},x_t]+b_o)$$
$$\tilde c_t=\tanh(W_c[h_{t-1},x_t]+b_c)\qquad c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t\qquad h_t=o_t\odot\tanh(c_t)$$
Because $c_t$ is updated **additively** (scaled by $f_t$), gradients have a path that does not shrink at every step.

**Bidirectional:** one LSTM runs forward and one runs backward, and their outputs are concatenated at each position:
$$h_t=\left[\overrightarrow{h_t}\,;\,\overleftarrow{h_t}\right]$$
This **doubles** the output width (64 → 128). It is only possible when the whole sentence is available up front, so it cannot be used for a next-word language model.

**Parameter counts.** These let you check `summary()` by hand (u = units, d = input dim):
| Layer | Formula | Lab value |
|---|---|---|
| `Embedding(V, d)` | $V\cdot d$ | 11389·64 = **728,896** ; tutorial 5002·32 = 160,064 |
| `SimpleRNN(u)` | $u(d+u)+u$ | 32(32+32)+32 = **2,080** |
| `LSTM(u)` | $4\,[u(d+u)+u]$ | 4[64·128+64] = **33,024** |
| `Bidirectional(LSTM(u))` | $2\times$ LSTM | **66,048** |
| `Dense(k)` on width w | $w k + k$ | 64·13+13 = **845** ; 128·13+13 = 1,677 |

The LSTM tagger has **762,765** parameters in total and the BiLSTM has **796,621** (+33,856).

**Loss choice.**
- Sentiment: one sigmoid output, labels 0/1 → `binary_crossentropy`.
- Tagging: softmax over 13 classes, targets are **integer ids** (not one-hot) → `sparse_categorical_crossentropy`.

**Masking.** `Embedding(..., mask_zero=True)` marks id 0 as padding. The mask is passed to the LSTM (padded steps are skipped) and to the loss and metrics (padded positions are ignored). Two consequences:
1. Id 0 must never be a real word or tag.
2. Keras `evaluate()` accuracy = masked accuracy. Both printed **0.9305**.

## 7.3 Data & pipeline

**Task 1 — sentiment (`mini_sentiment.tsv`).** Header `label\tsentence`, then `pos`/`neg` + TAB + an already-lowercased, tokenised sentence.
1. Read the file, skip the header, `label → 1/0`, `sentence.split()` → 10,662 token lists (5331 pos / 5331 neg; mean 21 words, max 59).
2. Count words. `vocab = ['<pad>','<unk>'] + top 5000 by frequency` → **5002** entries (`<pad>`=0, `<unk>`=1).
3. Encode with `word_index.get(w, 1)`.
4. `pad_sequences(seqs, maxlen=40)`. The default is `padding='pre'` (zeros at the **front**) and `truncating='pre'`. This is fine for many-to-one, because the last state is the one that matters.
5. Split: first 8000 = train, last 2662 = test. `fit(..., epochs=4, batch_size=64, validation_split=0.2)`.

| Step | Shape |
|---|---|
| `X_sent`, `y_sent` | (10662, 40), (10662,) |
| Embedding out | (None, 40, 32) |
| LSTM(32) out (last state only) | (None, 32) |
| Dense(1, sigmoid) | (None, 1) → `.ravel() > 0.5` |

Result: LSTM SHORT 0.776 (+0.071), ALL 0.740 (+0.101), **LONG 0.694 (+0.110)**. The biggest gain is on long sentences, which is what the vanishing-gradient argument predicts.

**Tasks 2–5 — POS tagging (NLTK `treebank.tagged_sents(tagset='universal')`).** 3914 sentences, each a list of `(word, tag)`.
Constants: `MAX_LEN=50, EMBED_DIM=64, RNN_UNITS=64, N_TRAIN=3000`.
1. Build `words` = sorted set of **lowercased** words (11,387) and `tags` = sorted set of tags (12): `['.', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'VERB', 'X']`.
2. `word_index`: real words get ids 2…, plus `<pad>`=0 and `<unk>`=1 (len 11,389). `tag_index`: real tags get ids 1…12, plus `<pad>`=0.
3. Encode words (`.get(w.lower(), 1)`) and tags (`tag_index[t]`). The two lists stay **aligned position by position**.
4. `pad_sequences(..., maxlen=50, padding='post')` for **both** X and y. Post-padding keeps word i and tag i at the same index.
5. Split at 3000 → train 3000, test 914.
6. Train 5 epochs, `batch_size=32`, `validation_split=0.2`, optimizer `adam`.

| Step | Shape |
|---|---|
| `X`, `y` | (3914, 50), (3914, 50) |
| `Input(shape=(MAX_LEN,))` | (None, 50) |
| `Embedding(11389, 64, mask_zero=True)` | (None, 50, 64) |
| `LSTM(64, return_sequences=True)` | (None, 50, 64) (BiLSTM: (None, 50, 128)) |
| `TimeDistributed(Dense(13, softmax))` | (None, 50, 13) |
| `model.predict(X_test)` → `.argmax(-1)` | (914, 50, 13) → (914, 50) |

Results: LSTM masked acc **0.9305**, BiLSTM **0.9474** (+1.69 pp). The hardest tags were ADJ 0.761, NUM 0.807 and ADV 0.811.

## 7.4 Exam-critical code blocks

The setup cell (imports, constants, `tagged_sentences`) was **given**. **Every code cell after it was blank in the TEMPLATE**: TODO 1–30, five cells, one per task. The blocks below are those blanks, filled from the submission.

### ★★★ Block A — Tagging data preparation (TEMPLATE BLANK: TODO 6–10)
**What it does:** builds the word and tag vocabularies with reserved ids, converts sentences to aligned id lists, post-pads them, and splits the data.
```python
words_set = set()
tags_set = set()
for sent in tagged_sentences:
  for w, t in sent:
    words_set.add(w.lower())                     # <-- KEY lowercase when building
    tags_set.add(t)

words = sorted(words_set)
tags = sorted(tags_set)

# word_index: 0 reserved for padding, 1 for <unk>, real words start at 2
word_index = {w: i+2 for i, w in enumerate(words)}   # <-- KEY i+2
word_index['<pad>'] = 0
word_index['<unk>'] = 1

# tag_index: 0 reserved for padding, real tags start at 1
tag_index = {t: i+1 for i, t in enumerate(tags)}     # <-- KEY i+1
tag_index['<pad>'] = 0

word_seqs = [[word_index.get(w.lower(), 1) for w, _ in sent] for sent in tagged_sentences]  # <-- KEY .get(...,1)
tag_seqs  = [[tag_index[t] for _, t in sent] for sent in tagged_sentences]

X = pad_sequences(word_seqs, maxlen=MAX_LEN, padding='post')   # <-- KEY padding='post'
y = pad_sequences(tag_seqs,  maxlen=MAX_LEN, padding='post')   # <-- KEY pad y the SAME way

X_train, y_train = X[:N_TRAIN], y[:N_TRAIN]
X_test,  y_test  = X[N_TRAIN:], y[N_TRAIN:]
```
**Line-by-line notes**
- `i+2` / `i+1`: `enumerate` starts at 0, so you shift to keep 0 (and 1 for words) free. Words: pad 0, unk 1, real ≥ 2. Tags: pad 0, real 1–12. There is no unk tag because every tag is known.
- `.get(w.lower(), 1)` sends unknown words to `<unk>`. Inside the training data every word is known; this matters at inference (`tag_sentence`).
- `y` holds integer tag ids with shape (3914, 50) and **no one-hot**. That is what `sparse_categorical_crossentropy` expects.
- Sentences longer than 50 get truncated; `pad_sequences`' default is `truncating='pre'`, which cuts from the front.

**Common mistakes**
- Giving a real word or tag id 0 (plain `enumerate` without `+1`/`+2`). That breaks masking.
- `padding='pre'` for tagging. Use post padding so that word i and tag i line up.
- Building the vocab lowercased but looking words up without `.lower()`.

### ★★★ Block B — LSTM tagger: build, compile, train (TEMPLATE BLANK: TODO 12–15)
**What it does:** many-to-many model. A hidden state at every step, then the same Dense classifier applied at every step.
```python
vocab_size = len(word_index)       # 11389 (includes <pad>, <unk>)
n_tags = len(tags) + 1             # <-- KEY +1 for padding id 0  -> 13

keras.utils.set_random_seed(42)
model_lstm = Sequential([
  Input(shape=(MAX_LEN,)),                                  # <-- KEY
  Embedding(vocab_size, EMBED_DIM, mask_zero=True),         # <-- KEY mask_zero=True
  LSTM(RNN_UNITS, return_sequences=True),                   # <-- KEY return_sequences=True
  TimeDistributed(Dense(n_tags, activation='softmax'))      # <-- KEY TimeDistributed + softmax
])
model_lstm.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])  # <-- KEY loss

model_lstm.summary()

history_lstm = model_lstm.fit(X_train, y_train, epochs=5, batch_size=32,
                validation_split=0.2, verbose=0)
```
(The submission imported `LSTM as KerasLSTM` and wrote `KerasLSTM(...)`. On paper, write `LSTM(...)`.)

**Line-by-line notes**
- `Input(shape=(MAX_LEN,))`: without it the model is not built, so `summary()` shows `?` and `0 (unbuilt)`. The shape is the per-sample shape; the batch dimension is left out.
- `Embedding(input_dim, output_dim, mask_zero=True)`: `input_dim` must be greater than the largest id, so use `len(word_index)` and not `len(words)`.
- `return_sequences=True` gives (None, 50, 64). Without it you get (None, 64): one vector, which cannot be tagged.
- `TimeDistributed(Dense(...))` applies **one shared** Dense layer (845 params) at all 50 positions. Output (None, 50, 13).
- `history_lstm.history` is a dict with keys `'loss','accuracy','val_loss','val_accuracy'`, each a list with one value per epoch. Final epoch: 0.1341 / 0.9705 / 0.2551 / 0.9229.

**Common mistakes**
- `Dense(len(tags))` (12) instead of 13. The model then cannot output id 12 (`'X'`), and the loss errors or misbehaves.
- `categorical_crossentropy` with integer targets. That loss needs one-hot targets; use the sparse version.
- Forgetting `Input(...)` (summary unbuilt) or `mask_zero` (the model learns to predict padding, so accuracy is inflated).

### ★★★ Block C — `masked_accuracy` (TEMPLATE BLANK: TODO 17–19, body of given stub)
**What it does:** computes accuracy over positions whose **true** tag is not padding.
```python
def masked_accuracy(model, X, y):
    preds = model.predict(X, verbose=0)        # (n, 50, 13)
    pred_ids = preds.argmax(-1)                # <-- KEY argmax over tag axis -> (n, 50)

    mask = (y != 0)                            # <-- KEY real tokens only (TRUE tag != pad)

    total = mask.sum()
    if total == 0:
      return 0.0
    correct = (pred_ids[mask] == y[mask]).sum()   # <-- KEY boolean-index both arrays
    return correct / total
```
**Line-by-line notes**
- `argmax(-1)` turns probabilities into ids along the last axis (the tag axis).
- Build the mask from **`y` (the truth)**, not from the predictions. `pred_ids[mask]` flattens to a 1-D array of the real positions only.
- Output: masked 0.9305 = `evaluate()` 0.9305. They agree because `mask_zero=True` makes Keras skip padded steps in its metric. **Without** masking, `evaluate()` would include the roughly 50% padded positions and give a meaningless number.

**Common mistakes**
- `(pred_ids == y).mean()` over the whole array (counts padding).
- Masking with `X != 0` instead of `y != 0`. Here they are equivalent because pad positions match, but `y != 0` is the specified rule.

### ★★★ Block D — Task 1: tutorial pipeline + LSTM sentiment classifier (TEMPLATE BLANK: TODO 1–4)
**What it does:** loads the TSV, builds a frequency vocab, pads, swaps in `LSTM(32)`, trains with identical settings, and scores by length group.
```python
labels_raw, texts = [], []
with open('mini_sentiment.tsv', encoding='utf-8') as f:
  next(f)                                               # <-- KEY skip header
  for line in f:
    label, sentence = line.rstrip('\n').split('\t')     # <-- KEY
    labels_raw.append(1 if label == 'pos' else 0)
    texts.append(sentence.split())
y_sent = np.array(labels_raw)

counts = {}
for t in texts:
  for w in t:
    counts[w] = counts.get(w, 0) + 1                    # <-- KEY word counts

vocab = ['<pad>', '<unk>'] + [w for w, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:MAX_WORDS]]  # <-- KEY
word_index_sent = {w: i for i, w in enumerate(vocab)}   # <pad>=0, <unk>=1 by position

sequences = [[word_index_sent.get(w, 1) for w in t] for t in texts]   # <-- KEY unk = 1
X_sent = pad_sequences(sequences, maxlen=SENT_LEN)                     # default padding='pre'

raw_len = np.array([len(t) for t in texts])[8000:]     # <-- KEY from token lists, test part only

keras.utils.set_random_seed(42)
model_lstm_sent = Sequential([
  Input(shape=(SENT_LEN,)),
  Embedding(len(vocab), 32),
  LSTM(32),                                             # <-- KEY the ONLY change (was SimpleRNN(32))
  Dense(1, activation='sigmoid')                        # <-- KEY
])
model_lstm_sent.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])  # <-- KEY

X_train_sent, y_train_sent = X_sent[:8000], y_sent[:8000]
X_test_sent,  y_test_sent  = X_sent[8000:], y_sent[8000:]
history_lstm_sent = model_lstm_sent.fit(X_train_sent, y_train_sent, epochs=4, batch_size=64,
                    validation_split=0.2, verbose=0)

pred = (model_lstm_sent.predict(X_test_sent, verbose=0).ravel() > 0.5).astype(int)   # <-- KEY
short = raw_len <= 15
long_ = raw_len >= 28
acc_short = (pred[short] == y_test_sent[short]).mean()
acc_all   = (pred == y_test_sent).mean()
acc_long  = (pred[long_] == y_test_sent[long_]).mean()
```
**Line-by-line notes**
- `sorted(..., key=lambda kv: -kv[1])` sorts by count, descending. Slice `[:MAX_WORDS]` keeps the top 5000. The two specials are prepended, so `<pad>` gets 0 and `<unk>` gets 1 automatically through `enumerate`.
- `raw_len` must come from `texts`. After padding every row has length 40, so `X_sent` cannot give the true length.
- `predict` returns (2662, 1). `.ravel()` gives (2662,), `> 0.5` gives a boolean array, and `.astype(int)` gives 0/1.
- The tutorial is identical except for `SimpleRNN(32)`. Its model: `Sequential([Input(shape=(MAX_LEN,)), Embedding(len(vocab), 32), SimpleRNN(32), Dense(1, activation='sigmoid')])`.

**Common mistakes**
- Changing anything besides the RNN layer (epochs, batch size, split, seed), which makes the comparison unfair.
- `raw_len` taken from all 10,662 sentences instead of `[8000:]`. The mask then has the wrong length.
- Using `sparse_categorical_crossentropy` or a softmax here. This task needs one sigmoid unit with binary cross-entropy.

### ★★ Block E — `tag_sentence` (TEMPLATE BLANK: TODO 20–22)
**What it does:** turns a raw string into ids, pads it the same way, predicts, and maps ids back to tag strings, keeping only as many tags as there are words.
```python
def tag_sentence(model, sentence):
    words_in = sentence.split()
    words_lower = [w.lower() for w in words_in]                 # <-- KEY lowercase for lookup
    seq = [[word_index.get(w, 1) for w in words_lower]]         # <-- KEY list of ONE sequence; unk=1
    Xs = pad_sequences(seq, maxlen=MAX_LEN, padding='post')     # <-- KEY same padding as training
    preds = model.predict(Xs, verbose=0).argmax(-1)[0]          # <-- KEY (1,50,13)->(1,50)->(50,)

    inv_tag = {v: k for k, v in tag_index.items()}              # <-- KEY invert dict: id -> tag

    pairs = []
    for i, w in enumerate(words_in):          # only len(words_in) positions -> drops padding
      tag_id = int(preds[i])
      tag_str = inv_tag.get(tag_id, '<pad>')
      pairs.append((w, tag_str))              # pair with ORIGINAL (cased) word
    return pairs
```
**Notes:** `seq` is wrapped in an extra list because `pad_sequences` and `predict` expect a batch. The `[0]` takes the single sentence back out. Output example: `He/PRON will/VERB book/VERB a/DET flight/NOUN ...`, and "book" in "a book about" → NOUN. Left context ("will" vs "a") was already enough for "book".
**Common mistakes:** forgetting the outer `[...]`; using `padding='pre'` (then the tags at index 0..k are padding predictions); returning all 50 tags.

### ★★ Block F — Bidirectional LSTM (TEMPLATE BLANK: TODO 26–28)
**What it does:** same model with one line changed, trained identically, then compared.
```python
keras.utils.set_random_seed(42)                     # same init as the LSTM run
model_bilstm = Sequential([
  Input(shape=(MAX_LEN,)),
  Embedding(vocab_size, EMBED_DIM, mask_zero=True),
  Bidirectional(LSTM(RNN_UNITS, return_sequences=True)),   # <-- KEY wrap the LSTM; out (None,50,128)
  TimeDistributed(Dense(n_tags, activation='softmax'))
])
model_bilstm.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
history_bilstm = model_bilstm.fit(X_train, y_train, epochs=5, batch_size=32,
                  validation_split=0.2, verbose=0)

acc_lstm = masked_accuracy(model_lstm, X_test, y_test)
acc_bilstm = masked_accuracy(model_bilstm, X_test, y_test)
params_lstm = model_lstm.count_params()             # <-- KEY count_params()
params_bilstm = model_bilstm.count_params()
improvement = (acc_bilstm - acc_lstm) * 100.0        # percentage points
```
**Notes:** `return_sequences=True` goes **inside**, on the LSTM, not on `Bidirectional`. The default merge is concatenation, so the width doubles to 128 and the Dense params grow to 1,677. Disagreements found: `fox` (NOUN→VERB, wrong), `New` (ADJ→NOUN, right; "York" on the right shows it is part of a proper noun), `reading` (NOUN→VERB, right; "a book" on the right).
**Common mistakes:** a different epoch count or seed for the second model; writing `Bidirectional(LSTM(64))` without `return_sequences=True`.

### ★ Block G — per-tag accuracy & printing (TEMPLATE BLANK: TODO 5, 11, 16, 24, 29–30)
```python
per_tag = []
for t in tags:
  tid = tag_index[t]
  mask = (y_test == tid)                       # positions whose TRUE tag is t
  n = mask.sum()
  if n == 0:
    acc = 0.0
  else:
    preds = model_lstm.predict(X_test, verbose=0).argmax(-1)
    acc = (preds[mask] == y_test[mask]).sum() / n
  per_tag.append((t, int(n), acc))
for t, n, acc in sorted(per_tag, key=lambda x: x[2]):   # worst first
  print(f"{t:<8}{n:8d}{acc:12.4f}")

# per-epoch table from history
h = history_lstm.history
for e in range(len(h['loss'])):
  print(f"{e+1:>6}{h['loss'][e]:>9.4f}{h['accuracy'][e]:>10.4f}"
      f"{h['val_loss'][e]:>10.4f}{h['val_accuracy'][e]:>14.4f}")
```
**Notes:** per-tag accuracy is the same masked idea with mask `y_test == tid`. The submission calls `predict` inside the loop; predicting once before the loop is equivalent and faster. Disagreement check: compare `tag_sentence(model_lstm, s)[i][1]` with `tag_sentence(model_bilstm, s)[i][1]` position by position. (A stray `preds_l = ...` line in the submission's Task 5 cell is dead code; ignore it.)

## 7.5 Fill-in-the-blank practice

**Q1.** Frequency vocabulary (tutorial / Task 1):
```python
vocab = ['<pad>', '<unk>'] + [w for w, _ in sorted(counts.items(), key=lambda kv: ____)[:MAX_WORDS]]
word_index = {w: i for i, w in ____(vocab)}
sequences = [[word_index.get(w, ____) for w in t] for t in texts]
X = pad_sequences(sequences, ____=MAX_LEN)
```
**Q2.** Reserved ids for tagging:
```python
word_index = {w: ____ for i, w in enumerate(words)}
word_index['<pad>'] = 0; word_index['<unk>'] = 1
tag_index = {t: ____ for i, t in enumerate(tags)}
```
**Q3.** Padding for tagging:
```python
X = pad_sequences(word_seqs, maxlen=MAX_LEN, padding=____)
y = pad_sequences(____, maxlen=MAX_LEN, padding=____)
```
**Q4.** The tagger:
```python
model_lstm = Sequential([
  Input(shape=____),
  Embedding(vocab_size, EMBED_DIM, ____=True),
  LSTM(RNN_UNITS, ____=True),
  ____(Dense(____, activation=____))
])
model_lstm.compile(optimizer='adam', loss=____, metrics=['accuracy'])
```
**Q5.** Masked accuracy:
```python
pred_ids = model.predict(X, verbose=0).____(-1)
mask = (____ != 0)
return (pred_ids[mask] == y[mask]).sum() / ____
```
**Q6.** Sentiment classifier head and loss:
```python
Sequential([Input(shape=(SENT_LEN,)), Embedding(len(vocab), 32), ____(32), Dense(____, activation=____)])
model.compile(optimizer='adam', loss=____, metrics=['accuracy'])
pred = (model.predict(X_test_sent, verbose=0).____() > 0.5).astype(int)
```
**Q7.** True test lengths:
```python
raw_len = np.array([len(t) for t in ____])[____:]
short = raw_len ____ 15 ; long_ = raw_len ____ 28
```
**Q8.** Tagging one string:
```python
seq = ____[word_index.get(w.lower(), 1) for w in sentence.split()]____
preds = model.predict(pad_sequences(seq, maxlen=MAX_LEN, padding='post'), verbose=0).argmax(-1)____
inv_tag = {____: ____ for k, v in tag_index.items()}
```
**Q9.** BiLSTM line, and the output shape that results:
```python
____(LSTM(RNN_UNITS, return_sequences=True))      # output shape: (None, 50, ____)
```
**Q10.** If `return_sequences=False` were used in the tagger, what would the LSTM output shape be, and why would training fail against `y` of shape (n, 50)?

<details><summary>Answers</summary>

1. `-kv[1]` ; `enumerate` ; `1` ; `maxlen`
2. `i+2` ; `i+1`
3. `'post'` ; `tag_seqs` ; `'post'`
4. `(MAX_LEN,)` ; `mask_zero` ; `return_sequences` ; `TimeDistributed` ; `n_tags` (= `len(tags)+1` = 13) ; `'softmax'` ; `'sparse_categorical_crossentropy'`
5. `argmax` ; `y` ; `mask.sum()`
6. `LSTM` ; `1` ; `'sigmoid'` ; `'binary_crossentropy'` ; `ravel`
7. `texts` ; `8000` ; `<=` ; `>=`
8. `[` … `]` (an outer list makes a batch of one) ; `[0]` ; `v: k` (id → tag)
9. `Bidirectional` ; `128`
10. (None, 64): one vector per sentence, with no time axis. `TimeDistributed` needs a 3-D (batch, time, features) input, and nothing exists per position to compare against `y` of shape (n, 50), so you get a shape error. A tagger needs the LSTM output to be (None, 50, 64), which gives a final output of (None, 50, 13).
</details>

## 7.6 Quick recall

- `pad_sequences(seqs, maxlen=N, padding='pre'|'post')`. The defaults `padding='pre'`, `truncating='pre'`, `value=0` give zeros at the front. For **tagging**, use `'post'` on both X and y.
- `Embedding(input_dim=V, output_dim=d, mask_zero=True)`: (n, T) → (n, T, d). V = max id + 1 = `len(word_index)`.
- `SimpleRNN(u)` / `LSTM(u)`: (n, T, d) → (n, u). With `return_sequences=True` → (n, T, u).
- `Bidirectional(LSTM(u, return_sequences=True))` → (n, T, 2u).
- `TimeDistributed(Dense(k, activation='softmax'))`: (n, T, u) → (n, T, k), with one shared weight matrix.
- Losses: one sigmoid output → `'binary_crossentropy'`. Integer class ids → `'sparse_categorical_crossentropy'`. One-hot targets → `'categorical_crossentropy'` (Lab 8).
- Ids: `<pad>`=0, `<unk>`=1; real words from 2, real tags from 1. Output units = `len(tags)+1`.
- Unknown lookup: `dict.get(w.lower(), 1)`. Reverse a dict: `{v: k for k, v in d.items()}`.
- Accuracy for tagging: `mask = y != 0` → `(pred[mask] == y[mask]).mean()`. With `mask_zero=True`, Keras `evaluate()` agrees (0.9305).
- `keras.utils.set_random_seed(42)` before **each** model, for fair comparisons. `model.count_params()` gives the parameter count. `history.history['val_accuracy'][-1]` gives the last epoch's validation accuracy.
- Numbers: LSTM vs SimpleRNN on LONG +0.110 (largest). Tagger 762,765 params / 0.9305. BiLSTM 796,621 / 0.9474.

---


---

<a id="lab-8"></a>

# Lab 8 — Neural Machine Translation (English → German) with an LSTM Encoder–Decoder

**Framework:** TensorFlow 2.20 / Keras, **Functional API** (`from tensorflow.keras.models import Model`,
`from tensorflow.keras.layers import Input, LSTM, Dense`). This is a **character-level** model: inputs are
**one-hot** vectors fed straight into the LSTM (no `Embedding`, no `pad_sequences`, no masking).
**There is no attention and no BLEU in this lab.** Beam search (Task 4) is the extension.

## 8.1 What this lab is about

You translate English sentences into German one **character** at a time, using a seq2seq encoder–decoder (the Keras `lstm_seq2seq` recipe; the assignment adapts an English→French reference notebook).
- The encoder LSTM reads English and keeps only its final `[state_h, state_c]`, the "thought vector".
- The decoder LSTM starts from that state and is trained with **teacher forcing**.
- For inference, the trained layers are rewired into `encoder_model` and `decoder_model`, then run in a **greedy** loop (`decode_sequence`).
- Task 4 replaces greedy decoding with **beam search** (sum of log-probs, length-normalised).

The notebook has no `# TODO` markers; each Task cell was the blank (Task 1 data, Task 2 model, Task 3 inference, Task 4 beam search).

## 8.2 Core concepts & formulas

**Seq2seq bottleneck.** Input and output lengths differ ("Go." is 3 characters, "Geh." is 4). The encoder compresses the whole input into a fixed-size state $(h_T, c_T)$, each vector of size `latent_dim`. The decoder's `initial_state` is that state. This one argument is the **entire connection** between encoder and decoder.

**Start/stop markers.** Every German target becomes `'\t' + german + '\n'`. Tab means "start generating" and newline means "stop". Without `'\n'` the model never learns to stop.

**Teacher forcing (the one-step shift).** During training the decoder receives the *correct* previous character and predicts the next one:
```
decoder_input :  \t   G   e   h   .        <- given
decoder_target:  G    e   h   .   \n       <- must predict  (= input shifted LEFT by 1)
```
So `decoder_target[t-1] = decoder_input[t]`. At inference there is no gold input, so the decoder consumes its own predictions. That is why separate inference models are needed.

**Loss:** at each time step the output is a softmax over `num_decoder_tokens` and the target is **one-hot**, so the loss is `categorical_crossentropy`. The optimizer is `rmsprop`.

**Greedy decoding:** $\hat y_t=\arg\max_c P(c\mid \hat y_{<t},x)$. It commits to one choice and never backtracks, so a near-tie early on can derail the whole output.

**Beam search:** keep the best $k$ partial outputs. Score each by summing log-probabilities (never multiply probabilities, because the product underflows):
$$\text{score}(y_{1..T})=\sum_{t=1}^{T}\log P(y_t\mid y_{<t},x)\qquad \text{final}=\frac{\sum_t \log P(y_t)}{|y|^{\alpha}},\ \alpha\approx0.7$$
Every extra character adds a negative term, so the raw sum favours short outputs. Dividing by $|y|^\alpha$ corrects for that. $\alpha=0$ means no normalisation; $\alpha=1$ means full normalisation. With $k=1$, beam search must reproduce greedy exactly.

**Parameter check** (assignment, latent 256, 70 encoder / 84 decoder tokens). The LSTM formula is $4[u(d+u)+u]$:
- encoder LSTM 4[256·(70+256)+256] = **334,848**
- decoder LSTM 4[256·(84+256)+256] = **349,184**
- Dense 256·84+84 = **21,588**
- total **705,620**

The tutorial (latent 128, tokens 57/66) has **203,586** parameters.

## 8.3 Data & pipeline

**Data:** `deu.txt` (Tatoeba / manythings.org Anki, ~331k lines). Each line is `English \t German \t CC-BY attribution`. The assignment uses the first `num_samples = 10000` lines. The tutorial uses `mini_deu.txt` (400 lines, same format).
Hyperparameters (assignment): `batch_size=64, epochs=40, latent_dim=256, num_samples=10000`. Tutorial: `latent_dim=128, epochs=300, num_samples=400`.

Steps, in order:
1. `split('\t')` each line. Wrap the German as `'\t'+de+'\n'`. Collect the character sets.
2. `input_characters` / `target_characters` = sorted sets. `num_encoder_tokens` = **70**, `num_decoder_tokens` = **84** (German adds ä ö ü ß Ä Ö Ü, and the target set includes `\t` and `\n`).
3. `max_encoder_seq_length` = **15**, `max_decoder_seq_length` = **51** (including both markers).
4. Build char → index dicts (`input_token_index`, `target_token_index`).
5. Fill three zero tensors with one-hots, applying the teacher-forcing shift. Pad unused positions with the **space** character's one-hot.
6. Train `model.fit([enc_in, dec_in], dec_target, validation_split=0.2)`: 8000 train / 2000 val → 125 steps per epoch.
7. Save as `s2s_eng_ger.h5`. Epoch 40: loss 0.3458, acc 0.8992, val_loss 0.4952, val_acc 0.8607.
8. Build the inference models, then run greedy and beam decoding.

| Tensor | Shape (assignment) | Content |
|---|---|---|
| `encoder_input_data` | (10000, 15, 70) | English one-hot, space-padded |
| `decoder_input_data` | (10000, 51, 84) | `\t` + German + `\n`, space-padded |
| `decoder_target_data` | (10000, 51, 84) | same, shifted left by 1 |
| `Input(shape=(None, 70))` → `LSTM(256, return_state=True)` | out (None,256), h (None,256), c (None,256) | output discarded |
| `Input(shape=(None, 84))` → `LSTM(256, return_sequences=True, return_state=True)` | (None, None, 256), h, c | |
| `Dense(84, softmax)` | (None, None, 84) | per-step char probabilities |
| inference: `encoder_model.predict(input_seq)` | list `[h (1,256), c (1,256)]` | |
| inference: `decoder_model.predict([target_seq]+states)` | `(1,1,84)`, h, c | `target_seq` is (1, 1, 84) |

`None` in `Input(shape=(None, ...))` means **any sequence length**, so the model can read 16-character inputs. Only the numpy array has to be sized correctly (see Block F).

## 8.4 Exam-critical code blocks

### ★★★ Block A — Load data, add markers, build character vocabularies (TASK BLANK: Task 1)
**What it does:** parses the TSV, wraps the targets with `\t`/`\n`, and builds sorted character sets, sizes, max lengths and index dicts.
```python
input_texts, target_texts = [], []
input_characters, target_characters = set(), set()

with open(data_path, encoding='utf-8') as f:
    for line in f.read().splitlines()[:num_samples]:
        parts = line.split('\t')                       # <-- KEY [english, german, attribution]
        if len(parts) < 2:
            continue
        input_text, target_text = parts[:2]
        target_text = '\t' + target_text + '\n'        # <-- KEY start + stop markers
        input_texts.append(input_text)
        target_texts.append(target_text)
        input_characters.update(input_text)            # <-- KEY set.update(str) adds each char
        target_characters.update(target_text)

input_characters = sorted(input_characters)
target_characters = sorted(target_characters)
num_encoder_tokens = len(input_characters)             # <-- KEY
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = max(map(len, input_texts))    # <-- KEY
max_decoder_seq_length = max(map(len, target_texts))
input_token_index = {char: i for i, char in enumerate(input_characters)}    # <-- KEY
target_token_index = {char: i for i, char in enumerate(target_characters)}
```
**Line-by-line notes**
- The tutorial version: `lines = f.read().split('\n')`, then `for line in lines[: min(num_samples, len(lines) - 1)]: input_text, target_text, _ = line.split('\t')`. The `-1` skips the empty string after the final newline.
- Markers are added **before** updating `target_characters`, so `\t` and `\n` become part of the decoder vocabulary.
- `max_decoder_seq_length` counts both markers.
- Indices start at 0. There is no reserved padding id, because padding uses the **space** character.

**Common mistakes**
- Adding the markers to the English side, or forgetting them on the German side.
- Calling `update` before adding the markers, which leaves `'\t'` missing from `target_token_index` (KeyError later).

### ★★★ Block B — One-hot tensors + teacher-forcing shift (TASK BLANK: Task 1)
**What it does:** builds the three 3-D float tensors. The target is the decoder input shifted left by one step.
```python
encoder_input_data = np.zeros(
    (len(input_texts), max_encoder_seq_length, num_encoder_tokens), dtype='float32'
)
decoder_input_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype='float32'
)
decoder_target_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens), dtype='float32'
)

for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
    for t, char in enumerate(input_text):
        encoder_input_data[i, t, input_token_index[char]] = 1.0             # <-- KEY one-hot
    encoder_input_data[i, len(input_text):, input_token_index[' ']] = 1.0   # <-- KEY pad with space

    for t, char in enumerate(target_text):
        decoder_input_data[i, t, target_token_index[char]] = 1.0
        if t > 0:                                                           # <-- KEY
            decoder_target_data[i, t - 1, target_token_index[char]] = 1.0   # <-- KEY the shift
    decoder_input_data[i, len(target_text):, target_token_index[' ']] = 1.0
    decoder_target_data[i, len(target_text) - 1:, target_token_index[' ']] = 1.0   # <-- KEY -1
```
**Line-by-line notes**
- Index order is `[sample, time, char_id]`. Setting one entry to 1 is the one-hot encoding.
- `if t > 0` / `t - 1`: the character given at step t is the answer for step t−1. `'\t'` (t = 0) is never a target. There is nothing to predict before the start marker.
- The target has one fewer real character, so its padding starts one position earlier (`len(target_text)-1`).
- The tutorial writes the same padding lines as `encoder_input_data[i, t + 1:, ...]` and `decoder_target_data[i, t:, ...]`. These are equivalent, because after the loop `t == len(text) - 1`.

**Common mistakes**
- Shifting the wrong way (`t + 1`) or shifting the input instead of the target.
- Making the padding lengths of target and input the same, which leaves an all-zero row at position `len-1` of the target.
- Allocating with `len(input_texts)` but using a different `max_*` per tensor. The encoder uses `max_encoder_seq_length` and the decoder uses `max_decoder_seq_length`.

### ★★★ Block C — Encoder–decoder training model (TASK BLANK: Task 2)
**What it does:** encoder → states → decoder (teacher-forced) → softmax over characters. Then compile, train and save.
```python
# Encoder: retain only the final hidden and cell states.
encoder_inputs = Input(shape=(None, num_encoder_tokens))                 # <-- KEY (time, features)
encoder = LSTM(latent_dim, return_state=True)                            # <-- KEY return_state
_, state_h, state_c = encoder(encoder_inputs)                            # <-- KEY 3 outputs
encoder_states = [state_h, state_c]                                      # <-- KEY thought vector

# Decoder: teacher-forced during training, initialized from encoder states.
decoder_inputs = Input(shape=(None, num_decoder_tokens))
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)        # <-- KEY both flags
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)  # <-- KEY initial_state
decoder_dense = Dense(num_decoder_tokens, activation='softmax')          # <-- KEY
decoder_outputs = decoder_dense(decoder_outputs)

model = Model([encoder_inputs, decoder_inputs], decoder_outputs)         # <-- KEY two inputs
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])  # <-- KEY
model.summary()

history = model.fit(
    [encoder_input_data, decoder_input_data], decoder_target_data,       # <-- KEY order
    batch_size=batch_size, epochs=epochs, validation_split=0.2
)

model.save('s2s_eng_ger.h5')
final = {name: values[-1] for name, values in history.history.items()}
```
**Line-by-line notes**
- `Input(shape=(None, num_tokens))`: `None` is a variable number of time steps, and the last dimension is the one-hot width. The batch dimension is implicit.
- `return_state=True` makes the LSTM return `[output, state_h, state_c]`. For the encoder, `return_sequences` is False, so `output` is just the last h (None, 256) and equals `state_h`. It is discarded (`_` in the assignment, `encoder_outputs` in the tutorial).
- Decoder: `return_sequences=True` is needed because every time step is scored. `return_state=True` is not used in training (`_, _`) but is needed later in inference, where the **same layer object** is reused.
- `initial_state=encoder_states` takes a **list** `[h, c]`. Without it you have two unrelated LSTMs.
- Keep `decoder_lstm` and `decoder_dense` as named variables. Task 3 reuses these trained objects.
- `Model(inputs, outputs)`: the inputs are a list of two tensors, and `fit` receives the arrays in the **same order**.
- `.h5` prints a "legacy format" warning, which is harmless.

**Common mistakes**
- `sparse_categorical_crossentropy` with one-hot targets. That loss needs integer targets, so here use `categorical_crossentropy`.
- `Dense(...)` inline (`Dense(...)(decoder_outputs)`) without keeping a handle. You then cannot reuse it in inference.
- Passing `[decoder_input_data, encoder_input_data]` (swapped), or using `decoder_input_data` as the target.

### ★★★ Block D — Inference models (TASK BLANK: Task 3)
**What it does:** rewires the **already-trained** layers into a one-shot encoder and a single-step decoder that takes and returns state.
```python
encoder_model = Model(encoder_inputs, encoder_states)                    # <-- KEY English -> [h, c]

decoder_state_input_h = Input(shape=(latent_dim,))                       # <-- KEY state placeholders
decoder_state_input_c = Input(shape=(latent_dim,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(                        # <-- KEY SAME trained layer
    decoder_inputs, initial_state=decoder_states_inputs
)
decoder_outputs = decoder_dense(decoder_outputs)                         # <-- KEY SAME trained Dense
decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs,                            # <-- KEY 3 inputs
    [decoder_outputs, state_h, state_c]                                  # <-- KEY 3 outputs
)

reverse_target_char_index = {i: char for char, i in target_token_index.items()}   # <-- KEY id -> char
```
**Line-by-line notes**
- No new LSTM or Dense is created and nothing is retrained. Calling `decoder_lstm(...)` again shares its weights.
- `Input(shape=(latent_dim,))`: a state is a vector (batch, 256) with no time axis.
- `[decoder_inputs] + decoder_states_inputs` is Python **list concatenation**, giving 3 inputs. The outputs return the new `h, c` so they can be fed back in the loop.
- `reverse_target_char_index` reads predictions back as characters.

**Common mistakes**
- `LSTM(latent_dim, ...)` written again here. It runs without error but has untrained weights, producing "confident nonsense".
- Forgetting to output `state_h, state_c`, which leaves nothing to carry forward.

### ★★★ Block E — `decode_sequence`: greedy decoding loop (TASK BLANK: Task 3; the function the reference notebook calls but never defines)
**What it does:** encodes once, starts from `'\t'`, and repeatedly predicts the argmax character, feeding it back and carrying the state, until `'\n'`.
```python
def decode_sequence(input_seq):
    """Greedily decode one German translation from an encoded English sentence."""
    states_value = encoder_model.predict(input_seq, verbose=0)           # <-- KEY encode ONCE -> [h, c]
    target_seq = np.zeros((1, 1, num_decoder_tokens), dtype='float32')   # <-- KEY (1 sample, 1 step, vocab)
    target_seq[0, 0, target_token_index['\t']] = 1.0                     # <-- KEY start marker

    decoded = ''
    for _ in range(max_decoder_seq_length):                              # length cap
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value, verbose=0                       # <-- KEY list concat
        )
        sampled_index = int(np.argmax(output_tokens[0, -1, :]))          # <-- KEY greedy argmax
        sampled_char = reverse_target_char_index[sampled_index]
        if sampled_char == '\n':                                         # <-- KEY stop marker
            break
        decoded += sampled_char
        target_seq = np.zeros((1, 1, num_decoder_tokens), dtype='float32')
        target_seq[0, 0, sampled_index] = 1.0                            # <-- KEY feed prediction back
        states_value = [h, c]                                            # <-- KEY carry state forward
    return decoded
```
**Line-by-line notes**
- `output_tokens` has shape (1, 1, 84). `[0, -1, :]` takes the last (only) step's distribution, (84,).
- A **fresh** `target_seq` of zeros is created each step, then one 1 is set. If you only set a new 1 without re-zeroing, the vector holds two hot entries.
- The tutorial's inline version uses `while True:` with `if ch == '\n' or len(german) > max_decoder_seq_length: break`. Same logic.
- Results: "He is a doctor." → "Er ist ein Faus."; "Can you help me?" → "Kann ich nach Hause gehen?". These are German-shaped, but character-level decoding can invent words.

**Common mistakes**
- Not updating `states_value = [h, c]`, so the decoder restarts from the encoder state on every character.
- Appending `'\n'` to the output, or checking for the stop marker after appending it.
- Starting from a zero vector instead of the `'\t'` one-hot.

### ★★ Block F — `encode_input` (fixes the IndexError bug; TASK BLANK: Task 3)
**What it does:** one-hot encodes an English string. It sizes the array to `max(max_len, len(text))` because two test sentences have 16 characters but `max_encoder_seq_length` is 15.
```python
def encode_input(input_text):
    width = max(max_encoder_seq_length, len(input_text))                # <-- KEY the fix
    input_seq = np.zeros((1, width, num_encoder_tokens), dtype='float32')
    for t, char in enumerate(input_text):
        if char in input_token_index:                                   # <-- KEY skip unseen chars
            input_seq[0, t, input_token_index[char]] = 1.0
    input_seq[0, len(input_text):, input_token_index[' ']] = 1.0        # space-pad
    return input_seq
```
**Notes:** the model accepts any length (`Input(shape=(None, ...))`); only the numpy buffer was too small. The tutorial's version allocates `(1, max_encoder_seq_length, num_encoder_tokens)` and raises `IndexError: index 10 is out of bounds for axis 1 with size 10` on "I am very tired.".

### ★★ Block G — `beam_search_decode` (TASK BLANK: Task 4)
**What it does:** keeps the k best partial translations. **Each beam carries its own state.** Scores are summed log-probabilities, and the final choice uses a length-normalised score.
```python
def beam_search_decode(input_seq, k=3, alpha=0.7):
    if k < 1:
        raise ValueError('k must be at least 1')

    initial_states = encoder_model.predict(input_seq, verbose=0)
    start = np.zeros((1, 1, num_decoder_tokens), dtype='float32')
    start[0, 0, target_token_index['\t']] = 1.0

    # Each beam owns its score, text, next decoder input, and LSTM states.
    live = [(0.0, '', start, initial_states)]                         # <-- KEY beam tuple
    completed = []

    for _ in range(max_decoder_seq_length):
        candidates = []
        for score, text, target_seq, states in live:
            output_tokens, h, c = decoder_model.predict(
                [target_seq] + states, verbose=0                       # <-- KEY this beam's state
            )
            probabilities = output_tokens[0, -1, :]
            top_indices = np.argsort(probabilities)[-k:][::-1]         # <-- KEY top-k, descending

            for index in top_indices:
                index = int(index)
                char = reverse_target_char_index[index]
                new_score = score + float(np.log(probabilities[index] + 1e-12))   # <-- KEY add logs
                if char == '\n':
                    completed.append((new_score, text))                # finished beam set aside
                else:
                    next_seq = np.zeros((1, 1, num_decoder_tokens), dtype='float32')
                    next_seq[0, 0, index] = 1.0
                    candidates.append((new_score, text + char, next_seq, [h, c]))  # <-- KEY own [h, c]

        if len(completed) >= k or not candidates:
            break
        candidates.sort(key=lambda beam: beam[0], reverse=True)        # <-- KEY best first
        live = candidates[:k]                                          # <-- KEY prune to k

    if not completed:
        completed = [(score, text) for score, text, _, _ in live]

    def normalised_score(beam):
        total_log_prob, text = beam
        return total_log_prob / (max(len(text), 1) ** alpha)          # <-- KEY length normalisation

    best_score, best_text = max(completed, key=normalised_score)
    return best_text, normalised_score((best_score, best_text))
```
**Line-by-line notes**
- `np.argsort` sorts ascending, so `[-k:]` takes the k largest and `[::-1]` reverses them to descending order.
- `+ 1e-12` avoids `log(0) = -inf`.
- There are up to k×k candidates per step; keep the best k by **raw** summed log-prob. Normalisation is applied only when choosing among **completed** beams.
- **k=1 sanity check:** this reduces to greedy decoding, and the assert passes ("Ich bin auf der schlach." for both).
- Results: beam (k=3) changed **3 of 5** outputs. Higher model score does not mean a better translation: "Er ist ein Buch." is still wrong (it should be "Er ist ein Arzt."). α = 0 → lengths [20,16,16,19,13]; α = 1 → [20,22,16,21,18], so longer outputs.

**Common mistakes**
- Sharing one `states_value` across beams, which makes all beams collapse to the same output.
- Multiplying probabilities, which underflows.
- Forgetting `reverse=True` in the sort, which keeps the k *worst* beams.

### ★ Block H — Final-epoch print and comparison loop
```python
final = {name: values[-1] for name, values in history.history.items()}
print('Final epoch - loss: {loss:.4f}, accuracy: {accuracy:.4f}, '
      'val_loss: {val_loss:.4f}, val_accuracy: {val_accuracy:.4f}'.format(**final))

for english in test_sentences:
    print(f'{english:<22}{decode_sequence(encode_input(english))}')
```
**Note:** the reported accuracy (0.899) is per character and includes the space-padding positions, which are easy to predict. It overstates translation quality.

## 8.5 Fill-in-the-blank practice

**Q1.** Markers:
```python
target_text = ____ + target_text + ____
```
**Q2.** Teacher-forcing shift and padding:
```python
for t, char in enumerate(target_text):
    decoder_input_data[i, t, target_token_index[char]] = 1.0
    if ____:
        decoder_target_data[i, ____, target_token_index[char]] = 1.0
decoder_input_data[i, len(target_text):, target_token_index[____]] = 1.0
decoder_target_data[i, ____:, target_token_index[' ']] = 1.0
```
**Q3.** Encoder:
```python
encoder_inputs = Input(shape=(____, num_encoder_tokens))
encoder = LSTM(latent_dim, ____=True)
_, state_h, state_c = encoder(encoder_inputs)
encoder_states = ____
```
**Q4.** Decoder (training):
```python
decoder_lstm = LSTM(latent_dim, ____=True, ____=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, ____=encoder_states)
decoder_dense = Dense(____, activation=____)
model = Model(____, decoder_outputs)
model.compile(optimizer='rmsprop', loss=____, metrics=['accuracy'])
model.fit(____, ____, batch_size=batch_size, epochs=epochs, validation_split=0.2)
```
**Q5.** Inference models:
```python
encoder_model = Model(____, ____)
decoder_state_input_h = Input(shape=(____,))
decoder_outputs, state_h, state_c = ____(decoder_inputs, initial_state=decoder_states_inputs)
decoder_outputs = ____(decoder_outputs)
decoder_model = Model([decoder_inputs] + ____, [decoder_outputs, ____, ____])
```
**Q6.** Greedy step:
```python
output_tokens, h, c = decoder_model.predict([target_seq] + ____, verbose=0)
sampled_index = int(np.argmax(output_tokens[____, ____, :]))
...
target_seq = np.zeros((____, ____, num_decoder_tokens), dtype='float32')
target_seq[0, 0, ____] = 1.0
states_value = ____
```
**Q7.** IndexError fix:
```python
width = ____(max_encoder_seq_length, ____)
```
**Q8.** Beam scoring:
```python
top_indices = np.argsort(probabilities)____
new_score = score + float(np.____(probabilities[index] + ____))
return total_log_prob / (max(len(text), 1) ** ____)
```
**Q9.** Reverse lookup:
```python
reverse_target_char_index = {____: ____ for char, i in target_token_index.items()}
```
**Q10.** Write the shapes: `encoder_input_data`, `decoder_target_data` (assignment), the `target_seq` fed per step, and `output_tokens`.

<details><summary>Answers</summary>

1. `'\t'` ; `'\n'`
2. `t > 0` ; `t - 1` ; `' '` ; `len(target_text) - 1`
3. `None` ; `return_state` ; `[state_h, state_c]`
4. `return_sequences` ; `return_state` ; `initial_state` ; `num_decoder_tokens` ; `'softmax'` ; `[encoder_inputs, decoder_inputs]` ; `'categorical_crossentropy'` ; `[encoder_input_data, decoder_input_data]` ; `decoder_target_data`
5. `encoder_inputs`, `encoder_states` ; `latent_dim` ; `decoder_lstm` (the trained one) ; `decoder_dense` ; `decoder_states_inputs` ; `state_h`, `state_c`
6. `states_value` ; `0`, `-1` ; `1`, `1` ; `sampled_index` ; `[h, c]`
7. `max` ; `len(input_text)`
8. `[-k:][::-1]` ; `log` ; `1e-12` ; `alpha`
9. `i: char`
10. (10000, 15, 70) ; (10000, 51, 84) ; (1, 1, 84) ; (1, 1, 84). `[0, -1, :]` gives (84,).
</details>

## 8.6 Quick recall

- Functional API pattern: `x = Input(shape=(None, F))`, then `layer = LSTM(...)`, then `out = layer(x)`, then `Model(inputs, outputs)`. Inputs and outputs may be lists.
- `LSTM(units, return_sequences=False, return_state=False)`:
  - plain → (batch, units)
  - with `return_sequences=True` → (batch, T, units)
  - with `return_state=True` → `[out, h, c]`
  - call with `layer(x, initial_state=[h, c])`
- Encoder: `return_state=True` only. Decoder: `return_sequences=True, return_state=True`. The connection is `initial_state=encoder_states`.
- Training: `model = Model([encoder_inputs, decoder_inputs], decoder_outputs)`, `rmsprop`, `categorical_crossentropy` (one-hot targets), `fit([enc_in, dec_in], dec_target, validation_split=0.2)`.
- Teacher forcing: `decoder_target[i, t-1] = decoder_input[i, t]` for t > 0. The target padding starts at `len-1`. All padding uses the **space** one-hot.
- Inference: `encoder_model = Model(encoder_inputs, encoder_states)`. `decoder_model = Model([decoder_inputs] + [h_in, c_in], [out, h, c])`. **Reuse** `decoder_lstm` and `decoder_dense`.
- Greedy loop:
  1. encode once
  2. `target_seq` (1,1,V) = one-hot `'\t'`
  3. predict, then `argmax(output_tokens[0,-1,:])`
  4. stop on `'\n'`
  5. otherwise build a new one-hot input and set `states_value=[h, c]`
  6. cap at `max_decoder_seq_length`
- Beam: tuple `(score, text, next_input, [h,c])`; `argsort(p)[-k:][::-1]`; add `log(p+1e-12)`; sort `reverse=True`, keep k; final pick `score/len**alpha` (α = 0.7). k=1 ≡ greedy.
- Numbers: 10000 samples, 70/84 tokens, max len 15/51, latent 256, 705,620 params, 40 epochs. Final val_acc 0.8607. Beam changed 3/5.
- Not in Lab 8: attention, BLEU, Embedding layers, `pad_sequences`, word-level tokenisation.

---

<a id="lab-9"></a>

# Lab 9 — Fine-Tuning a Pre-trained Transformer for English→German MT

> **Framework:** PyTorch + HuggingFace `transformers` / `datasets` / `evaluate`. The notebook sets `os.environ["USE_TF"] = "0"` so HF stays on PyTorch. TensorFlow/Keras is used **only** to reload the Lab 8 character-level LSTM in Part 5.

## 9.1 What this lab is about
- Take a **pre-trained encoder–decoder Transformer** (`Helsinki-NLP/opus-mt-en-de`, a MarianMT model) and **fine-tune** it on 20k EN→DE pairs from `deu.txt` (the same file as Lab 8).
- Evaluate with **BLEU** (`sacrebleu` via `evaluate`). Validation BLEU was 47.29 before fine-tuning and 50.60 after epoch 3. **Test BLEU = 49.84.**
- Translate new sentences with `model.generate` (beam search), then compare with the Lab 8 LSTM. The LSTM output is mostly gibberish.
- Pull out **encoder self-attention** and **encoder–decoder cross-attention** (`output_attentions=True`) and plot them with `bertviz` and matplotlib.

## 9.2 Core concepts & formulas

**Encoder–decoder Transformer (Marian).** The encoder reads the English sentence and the decoder writes German one token at a time. Each layer has these attention types:

| Attention | Where | Q from | K, V from | Mask |
|---|---|---|---|---|
| Self-attention | encoder | source tokens | same source tokens | padding mask only (bidirectional) |
| **Masked** (causal) self-attention | decoder | target tokens | same target tokens, **only positions ≤ i** | causal + padding |
| **Cross**-attention | decoder | target (decoder) states | **encoder outputs** | source padding mask |

- Lab 8's LSTM attention was **cross-attention only**: the decoder state is the query and the encoder states are the keys and values.
- In the Transformer, attention also **replaces recurrence**: every token sees every other token in one step. This makes training parallel and handles long-range dependencies.

**Scaled dot-product attention** (the same formula as Lab 10):
$$\text{Attention}(Q,K,V)=\text{softmax}\!\Big(\frac{QK^\top}{\sqrt{d_k}}\Big)V$$

**Seq2seq training = teacher forcing.**
- The decoder input is the gold target **shifted right**, starting with the decoder-start token (`<pad>` for Marian).
- The loss is cross-entropy against `labels`.
- Label positions equal to **`-100`** are ignored by the loss. `DataCollatorForSeq2Seq` pads `labels` with -100.

**BLEU** (corpus level, 0–100 in sacrebleu):
$$\text{BLEU}=BP\cdot\exp\Big(\sum_{n=1}^{4}w_n\log p_n\Big),\qquad BP=\begin{cases}1 & c>r\\ e^{\,1-r/c} & c\le r\end{cases}$$
- $p_n$ = modified (clipped) n-gram precision, $w_n = 1/4$.
- $c$ = candidate length, $r$ = reference length. The brevity penalty $BP$ punishes translations that are too short.
- sacrebleu expects `references` as a **list of lists** (several references are allowed per sentence).

**Fine-tuning vs. from-scratch.** A small LR (`2e-5`) adapts the pre-trained weights without destroying them. Warm-up (90 steps) avoids large early updates.

**Decoding.**
- `generate(..., num_beams=4)` = beam search: keep the 4 best partial hypotheses at each step.
- `num_beams=1` = greedy decoding (used for the attention visualisation).

## 9.3 Data & pipeline
1. **Read `deu.txt`.** Each line is tab-separated: `parts[0]` = English, `parts[1]` = German. The notebook keeps lines that have both parts and are non-empty, giving 331,266 pairs.
2. **Shuffle and subset.** `random.Random(42).shuffle(pairs)`, then take 20,000 train, 1,000 validation and 1,000 test pairs, wrapped in a `DatasetDict` of `Dataset.from_list(...)` (features `['en','de']`).
3. **Load the tokenizer and model:** `AutoTokenizer` and `AutoModelForSeq2SeqLM` from `"Helsinki-NLP/opus-mt-en-de"`. The model has about 74M parameters, 6 encoder layers and 8 heads.
4. **Tokenize** with `.map(preprocess_function, batched=True, remove_columns=["en","de"])`.
   - English becomes `input_ids` and `attention_mask`.
   - German is tokenized with `text_target=` and stored as `labels`.
   - `MAX_LEN = 128`, `truncation=True`, **no padding** at this stage.
5. **Collate.** `DataCollatorForSeq2Seq(tokenizer, model=model)` pads each batch dynamically:
   - `input_ids` and `attention_mask` → `(B, S_max)`
   - `labels` → `(B, T_max)`, padded with **-100**
   - `decoder_input_ids` → `(B, T_max)`: labels shifted right, built because `model=` was passed
6. **Train** with `Seq2SeqTrainer`: lr `2e-5`, train batch 32, eval batch 64, `weight_decay=0.01`, 3 epochs, `warmup_steps=90`, `predict_with_generate=True`, `generation_max_length=128`, fp16 on GPU, seed 42.
7. **Evaluate.**
   - With `predict_with_generate=True`, `eval_preds` = (generated ids `(N, gen_len)`, labels `(N, T)`).
   - Both are decoded to strings and scored with BLEU.
   - Keys are prefixed with `metric_key_prefix`, e.g. `test_bleu`.
8. **Inference:** `tokenizer(..., return_tensors="pt", padding=True)` → `generate` → `batch_decode(skip_special_tokens=True)`.
9. **Attention.** Reload with `output_attentions=True, attn_implementation="eager"`, then run a forward pass with `decoder_input_ids=generated`. For "The cat sat on the mat because it was tired.":
   - `encoder_attentions` = tuple of 6 tensors, each **(1, 8, 12, 12)** = (batch, heads, src, src)
   - `cross_attentions` = tuple of 6 tensors, each **(1, 8, 15, 12)** = (batch, heads, **tgt, src**)

**Results:** baseline validation BLEU 47.29 → epochs 1/2/3: 49.74 / 50.52 / 50.60 → **test BLEU 49.84**, test loss 0.620.

## 9.4 Exam-critical code blocks

### ★★★ 9-A. Pre-processing: tokenize source + target (`text_target`, `labels`)
**What it does:** turns `{"en": ..., "de": ...}` into `input_ids`, `attention_mask` and `labels` for a seq2seq model.
```python
MAX_LEN = 128

def preprocess_function(examples):
    model_inputs = tokenizer(examples["en"], max_length=MAX_LEN, truncation=True)            # <-- KEY
    labels = tokenizer(text_target=examples["de"], max_length=MAX_LEN, truncation=True)       # <-- KEY text_target
    model_inputs["labels"] = labels["input_ids"]                                              # <-- KEY
    return model_inputs

tokenized_datasets = raw_datasets.map(
    preprocess_function, batched=True, remove_columns=["en", "de"]                            # <-- KEY
)
```
**Line-by-line notes**
- `tokenizer(examples["en"], ...)` returns a dict with `input_ids` and `attention_mask`. With `batched=True`, `examples["en"]` is a **list** of strings.
- `text_target=` tells the tokenizer this is **target-language** text. Marian has separate source and target SentencePiece models (`source.spm`, `target.spm`), so this keyword matters.
- Only the **ids** of the target go into `labels`. The target's attention mask is not needed.
- `remove_columns=["en","de"]` drops the raw strings, which the collator and Trainer can't tensorize. Result: `['input_ids','attention_mask','labels']`.

**Common mistakes**
- Writing `labels = tokenizer(examples["de"])`. This uses the *source* tokenizer for German.
- Assigning `model_inputs["labels"] = labels`, the whole dict. It must be `labels["input_ids"]`.
- Padding here to `max_length`. Leave it out, because the collator pads per batch (dynamic padding).

### ★★★ 9-B. `compute_metrics` with sacreBLEU (handles `-100`)
**What it does:** decodes the generated ids and the label ids to text, then returns BLEU and the mean generation length.
```python
import numpy as np
import evaluate

metric = evaluate.load("sacrebleu")                                          # <-- KEY

def postprocess_text(preds, labels):
    return [p.strip() for p in preds], [[l.strip()] for l in labels]        # <-- KEY refs = list of lists

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
    preds = np.where(preds != -100, preds, tokenizer.pad_token_id)                      # <-- KEY
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)             # <-- KEY
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)                   # <-- KEY
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)
    result = metric.compute(predictions=decoded_preds, references=decoded_labels)       # <-- KEY
    gen_len = np.mean([np.count_nonzero(p != tokenizer.pad_token_id) for p in preds])
    return {"bleu": result["score"], "gen_len": gen_len}                                # <-- KEY "score"
```
**Line-by-line notes**
- `eval_preds` is `(predictions, label_ids)`. Because `predict_with_generate=True`, predictions are **token ids** `(N, L)`, not logits.
- Labels contain **-100** where the collator padded, and the Trainer also pads predictions with -100 when it concatenates batches. -100 is not a valid token id, so `batch_decode` would fail. `np.where(x != -100, x, pad_id)` swaps it for the pad id, which `skip_special_tokens=True` then removes.
- `isinstance(preds, tuple)`: some models return `(ids, ...)`, so the code takes element 0.
- sacrebleu's result dict holds the corpus BLEU under `"score"` (0–100).
- `gen_len` = average number of non-pad tokens per prediction.

**Common mistakes**
- Passing references as a flat list `["..."]`. It must be `[["..."], ["..."]]`.
- Using `np.argmax(preds, -1)` here. That is for logits (classification). The preds here are already ids.
- Forgetting to replace -100 in the **labels**. This is the most commonly forgotten step.

### ★★★ 9-C. Collator + `Seq2SeqTrainingArguments` + `Seq2SeqTrainer`
**What it does:** configures and runs fine-tuning, evaluates, and saves the model.
```python
from transformers import DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer

SAVE_PATH = "opus-mt-en-de-finetuned"

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)          # <-- KEY

training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",                    # <-- KEY (old name: evaluation_strategy)
    save_strategy="no",
    learning_rate=2e-5,                       # <-- KEY small LR for fine-tuning
    per_device_train_batch_size=32,
    per_device_eval_batch_size=64,
    weight_decay=0.01,
    num_train_epochs=3,
    warmup_steps=90,
    predict_with_generate=True,               # <-- KEY  -> eval uses generate() so BLEU can be computed
    generation_max_length=MAX_LEN,
    fp16=torch.cuda.is_available(),
    logging_steps=100,
    report_to="none",
    seed=SEED,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],          # <-- KEY
    eval_dataset=tokenized_datasets["validation"],      # <-- KEY
    data_collator=data_collator,
    compute_metrics=compute_metrics,                    # <-- KEY
)

baseline = trainer.evaluate(tokenized_datasets["validation"], metric_key_prefix="baseline")
train_result = trainer.train()                                                         # <-- KEY
trainer.save_model(SAVE_PATH)
tokenizer.save_pretrained(SAVE_PATH)

test_results = trainer.evaluate(tokenized_datasets["test"], metric_key_prefix="test")   # <-- KEY
print("Test BLEU after fine-tuning: %.2f" % test_results["test_bleu"])
```
**Line-by-line notes**
- `DataCollatorForSeq2Seq(tokenizer, model=model)` pads inputs with the pad id and **labels with -100**. Passing `model=` lets it build `decoder_input_ids` by shifting the labels right.
- `predict_with_generate=True` is required for BLEU. Without it, eval returns logits and BLEU can't be computed on text.
- `metric_key_prefix="test"` prefixes the returned keys: `test_bleu`, `test_loss`, `test_gen_len`.
- Always save the tokenizer next to the model so `from_pretrained(SAVE_PATH)` can reload both.

**Common mistakes**
- Using a plain `Trainer` or `TrainingArguments`. Those have no `predict_with_generate`.
- Using `DataCollatorWithPadding`. It doesn't pad `labels` with -100 or create decoder inputs.
- Using a large LR such as 1e-3, which causes catastrophic forgetting of pre-training.

### ★★★ 9-D. Inference: tokenize → `generate` → `batch_decode`
**What it does:** a drop-in "translator" that translates one string or a list of strings with beam search.
```python
device = 0 if torch.cuda.is_available() else -1
ft_tokenizer = AutoTokenizer.from_pretrained(SAVE_PATH)
ft_model = AutoModelForSeq2SeqLM.from_pretrained(SAVE_PATH).to("cuda" if device >= 0 else "cpu").eval()  # <-- KEY .eval()

def translator(texts, max_length=128, num_beams=4, batch_size=16):
    single = isinstance(texts, str)
    texts = [texts] if single else list(texts)
    results = []
    for i in range(0, len(texts), batch_size):
        batch = ft_tokenizer(texts[i:i + batch_size], return_tensors="pt", padding=True, truncation=True, max_length=max_length).to(ft_model.device)  # <-- KEY
        with torch.no_grad():                                                                  # <-- KEY
            out = ft_model.generate(**batch, max_length=max_length, num_beams=num_beams)       # <-- KEY
        results += [{"translation_text": t} for t in ft_tokenizer.batch_decode(out, skip_special_tokens=True)]  # <-- KEY
    return results

transformer_out = [r["translation_text"] for r in translator(test_sentences, max_length=MAX_LEN, num_beams=4)]
```
**Line-by-line notes**
- `return_tensors="pt"` returns PyTorch tensors. `padding=True` is needed here because the batch is fed straight to the model with no collator.
- `.to(ft_model.device)` moves the input tensors to the model's device. (A `BatchEncoding` supports `.to`.)
- `generate(**batch, ...)` unpacks `input_ids` and `attention_mask`. The output is `(B, gen_len)` token ids, starting with the decoder-start `<pad>` and ending with `</s>`.
- `batch_decode(..., skip_special_tokens=True)` strips `<pad>` and `</s>`.
- The notebook comment says transformers v5 removed the `"translation"` pipeline, so this function imitates its output format `[{"translation_text": ...}]`.

**Common mistakes**
- Calling `model(**batch)` instead of `model.generate(...)`. The forward pass needs decoder inputs and does not decode autoregressively.
- `decode` vs `batch_decode`: `decode` takes one sequence, `batch_decode` takes a batch.
- Forgetting `skip_special_tokens=True`, which leaves `<pad>` and `</s>` in the text.

### ★★ 9-E. Load tokenizer + model
```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "Helsinki-NLP/opus-mt-en-de"                        # <-- KEY
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)            # <-- KEY
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)        # <-- KEY Seq2SeqLM (not SequenceClassification / CausalLM)
print("Parameters: %.1fM" % (sum(p.numel() for p in model.parameters()) / 1e6))
```
- **Mistake:** using `AutoModel` (no LM head, so it can't `generate`) or `AutoModelForCausalLM` (decoder-only).

### ★★ 9-F. Build the `DatasetDict` from `deu.txt`
```python
pairs = []
with open(DATA_PATH, encoding="utf-8") as f:
    for line in f.read().splitlines():
        parts = line.split("\t")                                                     # <-- KEY tab-separated
        if len(parts) >= 2 and parts[0].strip() and parts[1].strip():
            pairs.append({"en": parts[0].strip(), "de": parts[1].strip()})

random.Random(SEED).shuffle(pairs)
pairs = pairs[: N_TRAIN + N_VAL + N_TEST]

raw_datasets = DatasetDict({
    "train":      Dataset.from_list(pairs[:N_TRAIN]),                                # <-- KEY
    "validation": Dataset.from_list(pairs[N_TRAIN:N_TRAIN + N_VAL]),
    "test":       Dataset.from_list(pairs[N_TRAIN + N_VAL:]),
})
```
- `N_TRAIN, N_VAL, N_TEST = 20000, 1000, 1000`. `Dataset.from_list` takes a list of dicts. Each line of `deu.txt` also has a third column (attribution), so the code checks `len(parts) >= 2` rather than `== 2`.

### ★★ 9-G. Extracting self- and cross-attention
**What it does:** reloads the model so it returns attention weights, generates a translation, then runs one forward pass with that translation as the decoder input.
```python
viz_model = AutoModelForSeq2SeqLM.from_pretrained(
    SAVE_PATH, output_attentions=True, attn_implementation="eager"        # <-- KEY both args
).to(device if device >= 0 else "cpu")
viz_model.eval()

sentence = "The cat sat on the mat because it was tired."
inputs = viz_tokenizer(sentence, return_tensors="pt").to(viz_model.device)

with torch.no_grad():
    generated = viz_model.generate(**inputs, max_length=MAX_LEN, num_beams=1)      # greedy
    outputs = viz_model(**inputs, decoder_input_ids=generated)                     # <-- KEY forward pass w/ decoder ids

encoder_tokens = viz_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])       # <-- KEY
decoder_tokens = viz_tokenizer.convert_ids_to_tokens(generated[0])
# outputs.encoder_attentions: 6 x (1, 8, 12, 12) ; outputs.cross_attentions: 6 x (1, 8, 15, 12)
```
**Line-by-line notes**
- `attn_implementation="eager"` is needed because the fused SDPA kernel doesn't return attention weights; without it the attentions come back as `None`.
- `generate` alone doesn't give convenient per-layer attentions, so the notebook does a **second forward pass** with `decoder_input_ids=generated` (teacher-forcing its own output).
- Shapes:
  - encoder self-attention: `(batch, heads, src_len, src_len)`
  - cross-attention: `(batch, heads, tgt_len, src_len)`, where rows = German queries and columns = English keys
  - The output also has `decoder_attentions` (masked self-attention, `(1, 8, tgt, tgt)`), but the notebook doesn't use it.

### ★ 9-H. Visualise (bertviz + static heatmap)
```python
from bertviz import head_view
head_view(encoder_attention=outputs.encoder_attentions, encoder_tokens=encoder_tokens)   # must be LAST line of the cell

head_view(cross_attention=outputs.cross_attentions,
          encoder_tokens=encoder_tokens, decoder_tokens=decoder_tokens)

enc_last = outputs.encoder_attentions[-1][0].mean(0).cpu().numpy()      # (src, src)  last layer, batch 0, mean over heads
cross_last = outputs.cross_attentions[-1][0].mean(0).cpu().numpy()      # (tgt, src)
```
- Indexing: `[-1]` = last layer → `[0]` = first sentence → `.mean(0)` = average over heads, giving a `(T_q, T_k)` matrix.
- What the plots show:
  - Encoder self-attention is concentrated near the diagonal (local context).
  - Cross-attention aligns *Die/Katze* ↔ *The cat*.
  - Late layers dump much of their weight on `</s>`, which acts as an attention "sink".

### ★ 9-I. LSTM (Lab 8) greedy decoding loop, for the comparison (Keras)
```python
def lstm_translate(text):
    states = encoder_model.predict(encode_input(text), verbose=0)          # [h, c]
    target_seq = np.zeros((1, 1, num_decoder_tokens), dtype="float32")
    target_seq[0, 0, target_token_index["\t"]] = 1.0                       # <-- KEY start char "\t"
    out = ""
    for _ in range(max_decoder_seq_length):
        probs, h, c = decoder_model.predict([target_seq] + states, verbose=0)
        idx = int(np.argmax(probs[0, -1, :]))                              # <-- KEY greedy
        ch = reverse_target_char_index[idx]
        if ch == "\n":                                                     # <-- KEY stop char
            break
        out += ch
        target_seq = np.zeros((1, 1, num_decoder_tokens), dtype="float32")
        target_seq[0, 0, idx] = 1.0                                        # feed prediction back
        states = [h, c]                                                    # <-- KEY carry state
    return out
```
- The LSTM squeezes the whole sentence into one fixed `(h, c)` state and works at the **character** level, trained on only 10k lines (~0.7M params). That is why its output is unrelated to the input ("Ich bin schwarz gewinnen.").

## 9.5 Fill-in-the-blank practice

**Q1.** Seq2seq tokenization
```python
def preprocess_function(examples):
    model_inputs = tokenizer(examples["en"], max_length=MAX_LEN, truncation=True)
    labels = tokenizer(______=examples["de"], max_length=MAX_LEN, truncation=True)
    model_inputs[______] = labels[______]
    return model_inputs
tokenized = raw_datasets.map(preprocess_function, batched=____, remove_columns=______)
```
**Q2.** Inside `compute_metrics`
```python
preds = np.where(preds != ____, preds, tokenizer.__________)
decoded_preds = tokenizer.__________(preds, skip_special_tokens=____)
result = metric.compute(predictions=decoded_preds, references=__________)   # references format?
return {"bleu": result[______]}
```
**Q3.** Which flag in `Seq2SeqTrainingArguments` makes evaluation call `generate()` so that BLEU can be computed? Which argument sets the generation length limit?

**Q4.** `data_collator = DataCollatorForSeq2Seq(________, model=______)`. What value does it pad `labels` with, and why?

**Q5.** Inference
```python
batch = tok(texts, return_tensors=____, padding=____, truncation=True, max_length=128).to(model.device)
with torch.________():
    out = model.________(**batch, max_length=128, num_beams=__)
print(tok.batch_decode(out, ________=True))
```
**Q6.** Loading a model that returns attentions
```python
m = AutoModelForSeq2SeqLM.from_pretrained(SAVE_PATH, ____________=True, attn_implementation=______)
outputs = m(**inputs, ______________=generated)
cross = outputs.________________          # tuple, one tensor per decoder layer
```
**Q7.** The source has 12 tokens, the generated target has 15 tokens, the model has 6 layers and 8 heads, and the batch size is 1. Give `len(outputs.encoder_attentions)`, `outputs.encoder_attentions[0].shape` and `outputs.cross_attentions[0].shape`.

**Q8.** Fill in the table: for each of the three attention types in an encoder–decoder model, where do Q and K/V come from, and which one is masked causally?

<details><summary>Answers</summary>

1. `text_target`; `"labels"`; `"input_ids"`; `True`; `["en", "de"]`.
2. `-100`; `pad_token_id`; `batch_decode`; `True`; a list of lists `[[ref1], [ref2], ...]` (built by `[[l.strip()] for l in labels]`); `"score"`.
3. `predict_with_generate=True`; `generation_max_length=MAX_LEN` (128).
4. `tokenizer`, `model`. It pads `labels` with **-100**, which is CrossEntropy's `ignore_index`, so padded target positions add nothing to the loss. `model=` lets it build `decoder_input_ids` by shifting the labels right.
5. `"pt"`; `True`; `no_grad`; `generate`; `4`; `skip_special_tokens`.
6. `output_attentions`; `"eager"`; `decoder_input_ids`; `cross_attentions`.
7. `6`; `(1, 8, 12, 12)`; `(1, 8, 15, 12)` = (batch, heads, tgt, src).
8. Encoder self-attention: Q, K, V all from the source; padding mask only. Decoder masked self-attention: Q, K, V from the target; causal mask, so position i sees only keys ≤ i. Cross-attention: Q from the decoder, K and V from the encoder output; no causal mask.
</details>

## 9.6 Quick recall
- **Model:** `"Helsinki-NLP/opus-mt-en-de"` (MarianMT, encoder–decoder, about 74M params, 6 layers, 8 heads). Loaded with `AutoTokenizer.from_pretrained`, `AutoModelForSeq2SeqLM.from_pretrained`.
- **Tokenizing:** `tokenizer(src, max_length=128, truncation=True)` for the source. For the target, use `tokenizer(text_target=tgt, ...)` and set `["labels"] = labels["input_ids"]`.
- **`.map`:** `.map(fn, batched=True, remove_columns=["en","de"])`.
- **Collator:** `DataCollatorForSeq2Seq(tokenizer, model=model)` gives dynamic padding, `labels` padded with -100, and `decoder_input_ids`.
- **Training arguments:** `Seq2SeqTrainingArguments(output_dir, eval_strategy="epoch", learning_rate=2e-5, per_device_train_batch_size=32, weight_decay=0.01, num_train_epochs=3, warmup_steps=90, predict_with_generate=True, generation_max_length=128, fp16=..., report_to="none")`.
- **Trainer:** `Seq2SeqTrainer(model, args, train_dataset, eval_dataset, data_collator, compute_metrics)` → `.train()`, `.evaluate(ds, metric_key_prefix="test")`, `.save_model(path)`. Also call `tokenizer.save_pretrained(path)`.
- **BLEU:**
  - `evaluate.load("sacrebleu")` → `metric.compute(predictions=[str], references=[[str]])["score"]`
  - Before decoding: `np.where(x != -100, x, tokenizer.pad_token_id)`
- **Generate:** `model.generate(**batch, max_length=128, num_beams=4)` → `(B, L)` ids → `tokenizer.batch_decode(out, skip_special_tokens=True)`.
- **Attentions:**
  - Load with `from_pretrained(path, output_attentions=True, attn_implementation="eager")`, then run `model(**inputs, decoder_input_ids=generated)`.
  - Read `.encoder_attentions` `(B, h, S, S)` and `.cross_attentions` `(B, h, T, S)`, each a tuple with one tensor per layer.
- **Tokens for plots:** `tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])`. bertviz `head_view(...)` must be the last line of the Colab cell.
- **Gotchas:**
  - `evaluation_strategy` was renamed to `eval_strategy`.
  - Run inference under `.eval()` and `torch.no_grad()`.
  - Move the batch to the model's device.
  - BLEU baseline (47.29) and per-epoch scores are on **validation**; 49.84 is on **test**.

---


---

<a id="lab-10"></a>

# Lab 10 — Attention from Scratch, Transformer Encoder & Fine-Tuning BERT (SST-2)

> **Framework:** pure **PyTorch** (`torch`, `torch.nn as nn`, `torch.nn.functional as F`) for the from-scratch parts. HuggingFace `Trainer` is used for BERT. Metrics come from `sklearn.metrics` (`accuracy_score`, `f1_score`, `confusion_matrix`).

## 10.1 What this lab is about
- Implement **scaled dot-product attention** and **multi-head attention** by hand, and check them against `F.scaled_dot_product_attention` and `nn.MultiheadAttention`.
- Add **sinusoidal positional encoding** and build a **Transformer encoder block** (MHA → dropout → Add&LN → FFN → dropout → Add&LN).
- Stack 2 blocks into a **mini-Transformer** classifier, trained from scratch on 5k SST-2 sentences (test accuracy 0.716).
- Fine-tune **`bert-base-uncased`**: full fine-tuning (0.897) vs frozen encoder (0.701). Then visualise BERT's attention heads.

## 10.2 Core concepts & formulas

**Q, K, V intuition (the tutorial's library analogy).**
- Query = "what am I looking for?", Key = "what do I contain?", Value = "what information do I pass on?"
- Scores are Q·K. Softmax turns each row into weights that **sum to 1**. The output is a **weighted average of the V's**.
$$\text{Attention}(Q,K,V)=\text{softmax}\!\Big(\frac{QK^\top}{\sqrt{d_k}}\Big)V$$

**Why divide by $\sqrt{d_k}$.**
- For unit-variance entries, $\text{Var}(q\cdot k)=d_k$, so the scores' standard deviation grows like $\sqrt{d_k}$.
- Large scores make the softmax almost **one-hot**, and the gradients through it vanish.
- Lab result at $d_k = 512$:
  - raw: score std 24.3, max weight 0.996, gradient 1.1e-3
  - scaled: score std ≈ 1.07, max weight 0.38, gradient 7.8e-2 (about 70× larger)

**Additive (Bahdanau, Lab 8) vs scaled dot-product.**
- Additive: $e=v^\top\tanh(W_1q+W_2k)$. It has its own parameters, needs a tanh for every query–key pair, and works when q and k have different sizes.
- Dot-product: no extra parameters, and all scores come from one matmul $QK^\top$, so it is fast and parallel.

**Masking.** The mask is applied to the **scores, before softmax**.
- Where it goes: positions that must be ignored get a huge negative number, e.g. `-1e9`, or `torch.finfo(dtype).min` in the submission. Then $e^{-10^9}\approx 0$, so their weight is about 0.
- Why not 0 or -inf:
  - Masking with **0 is wrong**: $e^0 = 1$, so the token still gets weight.
  - **-inf** gives `nan` if an entire row is masked.
  - -1e9 overflows to -inf in fp16. That is why the submission uses `finfo.min`.
- **Padding mask** (used in this lab):
  - Shape `(B, 1, 1, T_k)`. It broadcasts over heads and over every query row.
  - It hides padded **keys** (columns).
  - Convention: 1 = keep, 0 = pad.
- **Causal mask** (decoder masked self-attention; *not in the lab code*, concept only):
  - A lower-triangular `(T, T)` matrix: query $i$ may see keys $j \le i$.
  - With the same function you would pass `torch.tril(torch.ones(T, T))[None, None]` (1 = keep). Combine it with a padding mask by multiplying the two.
  - BERT (encoder) uses **no causal mask**: it is bidirectional.

**Multi-head attention.**
$$\text{MHA}(X)=\text{Concat}(\text{head}_1,\dots,\text{head}_h)\,W^O,\quad \text{head}_i=\text{Attention}(XW_i^Q, XW_i^K, XW_i^V),\quad d_k=d_{model}/h$$
- Each head works in its own $d_k$-dimensional subspace and can **specialise**: previous-token, next-token, `[SEP]`-sink and keyword heads.
- **Parameter count doesn't depend on h.** There are 4 matrices of size $d_{model}\times d_{model}$ plus biases. For $d_{model}=128$: $4(128\cdot128+128)=66{,}048$.

**Positional encoding.** Attention is order-blind ("dog bites man" looks the same as "man bites dog"), so a position vector is **added**, not concatenated:
$$PE_{(pos,2i)}=\sin\!\Big(\tfrac{pos}{10000^{2i/d}}\Big),\qquad PE_{(pos,2i+1)}=\cos\!\Big(\tfrac{pos}{10000^{2i/d}}\Big)$$
- Low dimensions oscillate fast and high dimensions slowly, like clock hands.
- It is **not trained**, so it is stored with `register_buffer`.
- BERT uses *learned* position embeddings instead, capped at 512 positions.

**Encoder block (Post-LN, as in the original paper and BERT).**
$$x' = \text{LN}(x + \text{Dropout}(\text{MHA}(x))),\qquad y=\text{LN}(x' + \text{Dropout}(\text{FFN}(x'))),\qquad \text{FFN}(x)=W_2\,\text{GELU}(W_1x+b_1)+b_2$$
- **Residual connections** give the gradient an identity path, so each block only learns a refinement and deep stacks stay trainable.
- **LayerNorm** normalises each token's vector to keep its scale stable. It works per token, so it handles padding and small batches, unlike BatchNorm.
- The output shape equals the input shape `(B, T, d_model)`, which is what lets blocks be stacked.

**Model families.**

| | Example | Attention | Good for |
|---|---|---|---|
| Encoder-only, bidirectional | BERT (this lab) | self-attention, no causal mask | classification, NER, extractive QA |
| Decoder-only | GPT-style | **masked** self-attention | left-to-right generation |
| Encoder–decoder | Marian (Lab 9) | self + masked self + **cross** | translation, summarisation |
| LSTM + attention | Lab 8 | cross-attention only | small or from-scratch baselines |

**BERT.**
- Pre-trained with MLM (fill in `[MASK]`) and NSP.
- `[CLS]` (id 101) comes first; its final vector, passed through the pooler, feeds the new linear classifier. `[SEP]` (id 102) ends a segment. `##` marks a WordPiece that continues the previous piece (vocabulary 30,522).
- BERT can't translate: it has no decoder, no cross-attention and no next-token training, it is bidirectional, and it outputs exactly one vector per input token.

**Fine-tuning vs freezing.**
- Fine-tuning uses a small LR (2e-5) to avoid catastrophic forgetting.
- Freezing means `requires_grad=False` on `model.bert`, so only the head trains (1,538 params). It is faster but much less accurate.

**F1** = harmonic mean of precision and recall, $F_1 = \frac{2PR}{P+R}$, here for the positive class.

**✅ Tutorial "Lab checklist" items — these are the most likely exam questions:**
- Explain `[CLS]`, `[SEP]`, `##` and why an attention mask is needed. Know the difference between dynamic padding and padding to a fixed length.
- Shapes: `Q,K,V = (batch, heads, T, d_k)`, `scores = (batch, heads, T, T)`. The mask is applied **before softmax**. Every row of the weight matrix sums to 1.
- Why `d_model % num_heads == 0`. The shape after each MHA step (project → split → attend → merge → `W_o`).
- Verifying against `nn.MultiheadAttention`: its `in_proj_weight` stacks Q, K, V into `(3·d, d)`.
- Positional encoding is **added**, **not trained**, and stored with `register_buffer`.
- Encoder block output shape = input shape `(B, T, d_model)`.
- Pre-training vs fine-tuning, why the LR is small, and how to count trainable params with `sum(p.numel() for p in model.parameters() if p.requires_grad)`.
- Mistakes the tutorial calls out:
  - `.view` after `.transpose` raises an error; use `.reshape`.
  - The softmax must be over the **last** axis (keys).
  - `K.transpose(-2, -1)`, not the full transpose.
  - Pass `batch_first=True` to `nn.MultiheadAttention`.
  - Compare outputs in `.eval()` mode under `torch.no_grad()`.
  - Use `eval_strategy`, not `evaluation_strategy`.
  - Set `num_labels=2`.
  - Remove the text columns after tokenizing.

## 10.3 Data & pipeline
1. **Load SST-2.** `load_dataset("glue", "sst2")`, falling back to `"nyu-mll/glue"`. Columns: `sentence`, `label` (0 = neg, 1 = pos), `idx`.
2. **Split.**
   - Shuffle the train split with seed 42.
   - **train** = first 5,000; **validation** = the next 1,000 (also from train, used for per-epoch monitoring); **test** = the official validation split (872), because GLUE test labels are hidden.
3. **Tokenize.**
   - Tokenizer: `bert-base-uncased` with `truncation=True, max_length=64`, **no padding** at this stage.
   - `remove_columns=["sentence","idx"]` leaves the features `label, input_ids, token_type_ids, attention_mask`.
   - Sentences average 13.3 tokens (max 59), so nothing is truncated.
   - Example: `"be fruitful"` → `[CLS] be fruit ##ful [SEP]` = `[101, 2022, 5909, 3993, 102]`.
4. **Collate.**
   - `DataCollatorWithPadding(tokenizer=tokenizer)` pads each batch to its longest sentence, e.g. 3 sentences → `(3, 17)`.
   - It **renames `label` → `labels`**, giving a `(B,)` tensor.
5. **Mini-Transformer shapes:**
   - `input_ids (B,T)` → embedding `(B,T,128)` → + PE → dropout → 2 × EncoderBlock `(B,T,128)`
   - masked mean-pool → `(B,128)` → `Linear(128,2)` → logits `(B,2)`
   - Inside attention: Q, K, V are `(B,4,T,32)`, scores and weights are `(B,4,T,T)`, the mask is `(B,1,1,T)`.
6. **Mini-Transformer training:** vocab 30,522, d_model 128, 4 heads, d_ff 256, 2 layers, dropout 0.1. AdamW at lr 1e-3, 5 epochs, batch 32, `clip_grad_norm_(1.0)`, CrossEntropyLoss, best epoch chosen on validation.
   - Parameters: **4,172,034**, of which the embedding is 3,906,816 (93.6%), the two blocks 264,960 and the classifier 258. One block = 132,480.
7. **BERT** (`AutoModelForSequenceClassification`, `num_labels=2`), 109,483,778 parameters:
   - embeddings 23.8M, 12 layers 85.1M, pooler 590,592, new head 1,538 = 768·2 + 2
   - Full fine-tune: `TrainingArguments(lr=2e-5, epochs=3, bs=32, eval bs=128, wd=0.01, eval_strategy="epoch", fp16)`.
   - Frozen: same settings with lr=1e-3.
8. **Results on the test set (872):**

| Model | Trainable | Acc | F1 | Train time |
|---|---|---|---|---|
| Mini-Transformer (scratch) | 4,172,034 | 0.7156 | 0.7304 | 10.5 s |
| BERT frozen (head only, lr 1e-3) | 1,538 | 0.7007 | 0.7545 | 15.1 s |
| **BERT full fine-tune (lr 2e-5)** | 109,483,778 | **0.8968** | **0.8996** | 41.8 s |
| DistilBERT full (bonus, 6 layers) | 66,955,010 | 0.8773 | 0.8807 | 25.2 s |

## 10.4 Exam-critical code blocks

### ★★★ 10-A. Scaled dot-product attention (from scratch)
**What it does:** implements $\text{softmax}(QK^\top/\sqrt{d_k})V$ with an optional padding mask. It returns the output **and** the weights.
```python
def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q, K, V : (batch, heads, seq_len, d_k)
    mask    : broadcastable to (batch, heads, seq_len_q, seq_len_k); 1 = keep, 0 = padding
    returns : output (batch, heads, seq_len_q, d_k), attention_weights (batch, heads, seq_len_q, seq_len_k)
    """
    d_k = Q.size(-1)                                                       # <-- KEY
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)                      # <-- KEY (B, h, T_q, T_k)
    if mask is not None:
        # very large negative number BEFORE softmax -> exp(...) = 0 for padded keys
        # (finfo.min instead of a hard-coded -1e9 so it also works in fp16)
        scores = scores.masked_fill(mask == 0, torch.finfo(scores.dtype).min)   # <-- KEY (on paper: -1e9 is fine)
    attention_weights = torch.softmax(scores, dim=-1)                      # <-- KEY normalise over the keys
    output = attention_weights @ V                                         # <-- KEY weighted average of the values
    return output, attention_weights
```
**Line-by-line notes (shapes, using the verification example B=2, h=4, T=6, d_k=16)**
| Step | Op | Shape |
|---|---|---|
| inputs | `Q, K, V` | `(2, 4, 6, 16)` |
| `d_k = Q.size(-1)` | last dim | `16` |
| `K.transpose(-2, -1)` | swap **last two** dims only | `(2, 4, 16, 6)` |
| `Q @ Kᵀ` | batched matmul over the last two dims: `(6,16)@(16,6)` | `(2, 4, 6, 6)` |
| `/ math.sqrt(d_k)` | scalar | `(2, 4, 6, 6)` |
| mask `pad[:, None, None, :]` | `(2,6)` → | `(2, 1, 1, 6)`, broadcast to `(2,4,6,6)` |
| `masked_fill(mask == 0, -big)` | fills where the **condition is True**, i.e. at pad keys | `(2, 4, 6, 6)` |
| `softmax(dim=-1)` | over the keys; each row sums to 1 | `(2, 4, 6, 6)` |
| `weights @ V` | `(6,6)@(6,16)` | `(2, 4, 6, 16)` |
- The mask kills **columns** (keys) for every query row. Padded *query* rows still get computed; they are ignored later by pooling.
- Equivalent NumPy idiom from the tutorial: `softmax(np.where(mask == 1, scores, -1e9))`.

**Common mistakes**
- `K.T` or `K.transpose(0, 1)`. You must swap the last two axes: `transpose(-2, -1)`.
- `softmax(dim=1)` or `dim=-2`. The weights then don't sum to 1 over the keys.
- Masking **after** softmax, or filling with `0` instead of a large negative number.
- `masked_fill(mask == 1, ...)`, which masks the real tokens instead of the padding.

### ★★★ 10-B. `MultiHeadAttention` (project → split → attend → merge → W_o)
```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"   # <-- KEY
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads                                             # <-- KEY
        self.W_q = nn.Linear(d_model, d_model)                                      # <-- KEY
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)                                      # <-- KEY
        self.attn_weights = None                       # (B, h, T, T) from the last forward pass

    def split_heads(self, x):
        # (B, T, d_model) -> (B, T, h, d_k) -> (B, h, T, d_k)
        B, T, _ = x.shape
        return x.view(B, T, self.num_heads, self.d_k).transpose(1, 2)               # <-- KEY

    def merge_heads(self, x):
        # (B, h, T, d_k) -> (B, T, h, d_k) -> (B, T, d_model); reshape because transpose is not contiguous
        B, _, T, _ = x.shape
        return x.transpose(1, 2).reshape(B, T, self.d_model)                        # <-- KEY reshape, NOT view

    def forward(self, x, mask=None):
        Q = self.split_heads(self.W_q(x))                                           # <-- KEY
        K = self.split_heads(self.W_k(x))
        V = self.split_heads(self.W_v(x))
        out, weights = scaled_dot_product_attention(Q, K, V, mask)                  # <-- KEY
        self.attn_weights = weights.detach()
        return self.W_o(self.merge_heads(out))                                      # <-- KEY
```
**Shapes (d_model=128, h=4, so d_k=32; x is `(B, T, 128)`)**
| Step | Shape |
|---|---|
| `self.W_q(x)` | `(B, T, 128)` |
| `.view(B, T, 4, 32)` | `(B, T, 4, 32)`: cut the feature axis into h chunks |
| `.transpose(1, 2)` | `(B, 4, T, 32)`: heads before time, so attention runs per head |
| attention `out` / `weights` | `(B, 4, T, 32)` / `(B, 4, T, T)` |
| `out.transpose(1, 2)` | `(B, T, 4, 32)` (not contiguous in memory) |
| `.reshape(B, T, 128)` | `(B, T, 128)`: concatenate the heads |
| `self.W_o(...)` | `(B, T, 128)` |
- `nn.Linear(d_model, d_model)` acts on the **last** dimension, so it works directly on `(B, T, d_model)`.
- Params = 4 × (128·128 + 128) = **66,048**, the same as `nn.MultiheadAttention(128, h)` for any h.
- `weights.detach()` stores the weights for plotting without keeping the autograd graph.

**Common mistakes**
- `.view(...)` after `.transpose` raises *"view size is not compatible with input tensor's size and stride"*. Use `.reshape` or `.contiguous().view`.
- `transpose(1, 2)` vs `transpose(0, 1)`. Dim 0 is the batch and must not be touched.
- Viewing as `(B, h, T, d_k)` directly without the transpose. The numbers are the same but the data is scrambled, because each head must take a *slice of features*, not a slice of time.

### ★★★ 10-C. Sinusoidal `PositionalEncoding`
```python
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=512):
        super().__init__()
        position = torch.arange(max_len).unsqueeze(1)                                       # <-- KEY (max_len, 1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))  # <-- KEY 1 / 10000^(2i/d)
        pe = torch.zeros(max_len, d_model)
        pe[:, 0::2] = torch.sin(position * div_term)      # <-- KEY even dimensions
        pe[:, 1::2] = torch.cos(position * div_term)      # <-- KEY odd dimensions
        self.register_buffer("pe", pe.unsqueeze(0))       # <-- KEY (1, max_len, d_model): moves with .to(device), not trained

    def forward(self, x):
        # x: (B, T, d_model) -> add the encoding of positions 0..T-1
        return x + self.pe[:, :x.size(1)]                 # <-- KEY add, slice to T
```
**Line-by-line notes**
- `torch.arange(0, d_model, 2)` gives the values $2i$ = 0, 2, 4, …, and has shape `(d_model/2,)`.
- `exp(2i · (−ln 10000 / d)) = 10000^{−2i/d}`. This is the log-space form of `1/10000^(2i/d)`, which is numerically stable.
- `position * div_term` broadcasts `(max_len, 1) × (d/2,)` → `(max_len, d/2)`.
- `0::2` = even columns get sin, `1::2` = odd columns get cos.
- `register_buffer`: the tensor is saved in `state_dict` and moves with `.to(device)`, but is **not a parameter**, so it isn't trained.
- `self.pe[:, :x.size(1)]` is `(1, T, d)` and broadcasts over the batch.

**Common mistakes**
- Making it an `nn.Parameter`, which makes it trainable.
- Concatenating instead of adding.
- Swapping sin and cos between even and odd dims.
- Writing `+ math.log` (missing the minus sign), which gives exploding frequencies.

### ★★★ 10-D. `EncoderBlock` (Post-LN)
```python
class EncoderBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.mha = MultiHeadAttention(d_model, num_heads)
        self.ffn = nn.Sequential(nn.Linear(d_model, d_ff), nn.GELU(), nn.Linear(d_ff, d_model))   # <-- KEY
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        x = self.norm1(x + self.dropout1(self.mha(x, mask)))     # <-- KEY MHA -> Dropout -> Add & LayerNorm
        x = self.norm2(x + self.dropout2(self.ffn(x)))           # <-- KEY FFN -> Dropout -> Add & LayerNorm
        return x
```
**Line-by-line notes**
- Order inside each line: **sublayer → dropout → add the residual `x` → LayerNorm**. Dropout is applied to the sublayer output only, not to the residual.
- FFN: `d_model → d_ff → d_model` (128 → 256 → 128) with GELU. It is position-wise, so the same MLP is applied to each token independently.
- `nn.LayerNorm(d_model)` normalises over the last dimension, per token.
- Shape test: in `(2, 10, 128)` → out `(2, 10, 128)`; `attn_weights` `(2, 4, 10, 10)`; **132,480** params per block.

**Common mistakes**
- `self.norm1(self.mha(x))`: forgetting the residual `x +`.
- Pre-LN `x + mha(norm(x))` is a valid variant, but the lab spec is Post-LN.
- Forgetting to pass `mask` to `self.mha`.
- `nn.Linear(d_ff, d_ff)`: the output must return to `d_model`.

### ★★★ 10-E. `MiniTransformerClassifier`: mask reshape + masked mean pooling
```python
class MiniTransformerClassifier(nn.Module):
    def __init__(self, vocab_size, d_model=128, num_heads=4, d_ff=256, num_layers=2,
                 num_classes=2, dropout=0.1, max_len=512, pad_id=0):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model, padding_idx=pad_id)        # <-- KEY
        self.pos_enc = PositionalEncoding(d_model, max_len)
        self.dropout = nn.Dropout(dropout)
        self.blocks = nn.ModuleList([EncoderBlock(d_model, num_heads, d_ff, dropout) for _ in range(num_layers)])  # <-- KEY ModuleList
        self.classifier = nn.Linear(d_model, num_classes)

    def forward(self, input_ids, attention_mask):
        mask = attention_mask[:, None, None, :]                    # <-- KEY (B, 1, 1, T) padding mask for attention
        x = self.dropout(self.pos_enc(self.embedding(input_ids)))  # <-- KEY (B, T, d_model)
        for block in self.blocks:
            x = block(x, mask)
        m = attention_mask.unsqueeze(-1).to(x.dtype)               # <-- KEY (B, T, 1)
        pooled = (x * m).sum(dim=1) / m.sum(dim=1).clamp(min=1)    # <-- KEY mean over the non-padding tokens only
        return self.classifier(pooled)                             # (B, num_classes) logits

mini_model = MiniTransformerClassifier(tokenizer.vocab_size, pad_id=tokenizer.pad_token_id).to(device)
```
**Line-by-line notes**
- `attention_mask[:, None, None, :]` is the same as `.unsqueeze(1).unsqueeze(2)`: `(B,T)` → `(B,1,1,T)`. It broadcasts across the heads (dim 1) and the query rows (dim 2).
- Pooling shapes: `x*m` is `(B,T,d)`, `.sum(dim=1)` is `(B,d)`, `m.sum(dim=1)` is `(B,1)` (the count of real tokens), and the result is `(B,d)`. `clamp(min=1)` guards against dividing by 0.
- Why masked pooling: with 2 real tokens and 2 pad vectors, the naive mean of `[1,3,0,0]` is 1, but the masked mean is 2. Padding must not dilute the average.
- `padding_idx=pad_id` keeps the pad embedding at zero, and it gets no gradient.
- `nn.ModuleList` (not a Python list) is needed so the blocks' parameters are registered.
- The model returns **logits** with no softmax, because `CrossEntropyLoss` applies log-softmax itself.

**Common mistakes**
- Passing `attention_mask` as `(B,T)` directly to attention. It won't broadcast correctly against `(B,h,T,T)`.
- Using `x.mean(1)` for pooling.
- Applying softmax before `CrossEntropyLoss`.

### ★★★ 10-F. Standard PyTorch training loop + `predict`
```python
train_loader = DataLoader(tokenized["train"], batch_size=BATCH_SIZE, shuffle=True,
                          collate_fn=data_collator, generator=torch.Generator().manual_seed(SEED))   # <-- KEY collate_fn
val_loader = DataLoader(tokenized["validation"], batch_size=128, collate_fn=data_collator)

@torch.no_grad()
def predict(model, loader):
    model.eval()                                                                   # <-- KEY
    preds, labels = [], []
    for batch in loader:
        logits = model(batch["input_ids"].to(device), batch["attention_mask"].to(device))
        preds.append(logits.argmax(-1).cpu())                                      # <-- KEY
        labels.append(batch["labels"])
    return torch.cat(preds).numpy(), torch.cat(labels).numpy()

optimizer = torch.optim.AdamW(mini_model.parameters(), lr=LR)                       # <-- KEY lr=1e-3
loss_fn = nn.CrossEntropyLoss()                                                    # <-- KEY

for epoch in range(1, EPOCHS + 1):
    mini_model.train()                                                             # <-- KEY
    total_loss, correct, seen = 0.0, 0, 0
    for batch in train_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        optimizer.zero_grad()                                                      # <-- KEY 1
        logits = mini_model(input_ids, attention_mask)                             # <-- KEY 2
        loss = loss_fn(logits, labels)                                             # <-- KEY 3
        loss.backward()                                                            # <-- KEY 4
        torch.nn.utils.clip_grad_norm_(mini_model.parameters(), max_norm=1.0)
        optimizer.step()                                                           # <-- KEY 5

        total_loss += loss.item() * labels.size(0)
        correct += (logits.argmax(-1) == labels).sum().item()
        seen += labels.size(0)

    val_preds, val_labels = predict(mini_model, val_loader)
    val_acc = accuracy_score(val_labels, val_preds)
    if val_acc > best_val_acc:                       # keep the best epoch (selected on validation, not test)
        best_val_acc, best_state = val_acc, copy.deepcopy(mini_model.state_dict())
mini_model.load_state_dict(best_state)
```
**Line-by-line notes**
- The 5-line loop, in order: `zero_grad → forward → loss → backward → step`. Gradient clipping goes **between** `backward` and `step`.
- `loss_fn(logits (B,2), labels (B,) long)`.
- `DataCollatorWithPadding` used as `collate_fn` pads dynamically and gives the key `"labels"` (renamed from `label`).
- `.item()` turns a one-element tensor into a Python float. Weighting by `labels.size(0)` gives a per-sample average loss.

**Common mistakes**
- `zero_grad` missing, so gradients accumulate.
- `step()` before `backward()`.
- Model on the GPU while the batch is on the CPU, which raises *"Expected all tensors to be on the same device"*.
- Forgetting `model.train()` and `model.eval()`, which leaves dropout on during evaluation.

### ★★★ 10-G. BERT fine-tuning with HF `Trainer`
```python
MODEL_NAME = "bert-base-uncased"
MAX_LEN = 64
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize_fn(batch):
    # no padding here: DataCollatorWithPadding pads each batch to its own longest sentence
    return tokenizer(batch["sentence"], truncation=True, max_length=MAX_LEN)          # <-- KEY

tokenized = raw.map(tokenize_fn, batched=True, remove_columns=["sentence", "idx"])     # <-- KEY
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)                           # <-- KEY

id2label = {0: "NEGATIVE", 1: "POSITIVE"}
label2id = {v: k for k, v in id2label.items()}

def load_classifier(name=MODEL_NAME, **kwargs):
    return AutoModelForSequenceClassification.from_pretrained(
        name, num_labels=2, id2label=id2label, label2id=label2id, **kwargs)            # <-- KEY num_labels=2

def compute_metrics(eval_pred):
    logits, labels = eval_pred                                                         # <-- KEY
    preds = np.argmax(logits, axis=-1)                                                 # <-- KEY
    return {"accuracy": accuracy_score(labels, preds), "f1": f1_score(labels, preds)}  # <-- KEY

def train_with_trainer(model, run_name, lr=2e-5, train_ds=None, val_ds=None, collator=None, epochs=3):
    args = TrainingArguments(
        output_dir=f"runs/{run_name}",
        learning_rate=lr,                       # <-- KEY 2e-5 full / 1e-3 frozen
        num_train_epochs=epochs,                # 3
        per_device_train_batch_size=32,
        per_device_eval_batch_size=128,
        weight_decay=0.01,
        eval_strategy="epoch",                  # <-- KEY
        save_strategy="no",
        logging_strategy="epoch",
        fp16=torch.cuda.is_available(),
        report_to="none",
        seed=SEED,
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds if train_ds is not None else tokenized["train"],
        eval_dataset=val_ds if val_ds is not None else tokenized["validation"],
        data_collator=collator if collator is not None else data_collator,
        compute_metrics=compute_metrics,
    )
    start = time.time()
    trainer.train()                                                                    # <-- KEY
    return trainer, time.time() - start

bert_model = load_classifier()
full_trainer, full_time = train_with_trainer(bert_model, "bert-full", lr=2e-5)
out = full_trainer.predict(tokenized["test"])            # <-- KEY metrics are prefixed with "test_"
preds = out.predictions.argmax(-1)                       # out.predictions = logits (N, 2); out.label_ids = (N,)
acc, f1 = out.metrics["test_accuracy"], out.metrics["test_f1"]
full_trainer.save_model("bert-sst2-full"); tokenizer.save_pretrained("bert-sst2-full")
```
**Line-by-line notes**
- `AutoModelForSequenceClassification` = BERT body + **new, randomly initialised** `Linear(768, 2)` on the pooled `[CLS]` vector. The "newly initialized weights" warning is expected.
- `compute_metrics` gets `(logits (N,2), labels (N,))` and uses `argmax(-1)`. Compare Lab 9, where it got generated ids and decoded them.
- The Trainer reads `labels` from the batch and computes cross-entropy internally.
- `trainer.predict(ds)` returns `.predictions`, `.label_ids` and `.metrics` (keys `test_accuracy`, `test_f1`, `test_runtime`).

**Common mistakes**
- Forgetting `num_labels=2`.
- Leaving the raw `sentence` column in the dataset.
- Using `evaluation_strategy` on new versions.
- Using lr 1e-3 for full fine-tuning, which destroys BERT.
- Padding to a fixed length in `tokenize_fn` instead of using the collator.

### ★★ 10-H. Verifying against PyTorch (`F.scaled_dot_product_attention`, `nn.MultiheadAttention`)
```python
mask = pad[:, None, None, :]                                       # (B, 1, 1, T)
out, w = scaled_dot_product_attention(Q, K, V, mask)
ref = F.scaled_dot_product_attention(Q, K, V, attn_mask=mask.bool())   # <-- KEY bool mask: True = may attend
torch.allclose(out, ref, atol=1e-5)
torch.allclose(w.sum(-1), torch.ones(B, h, T))                    # rows sum to 1

my_mha = MultiHeadAttention(d_model, num_heads).eval()
torch_mha = nn.MultiheadAttention(d_model, num_heads, batch_first=True).eval()      # <-- KEY batch_first
with torch.no_grad():
    torch_mha.in_proj_weight.copy_(torch.cat([my_mha.W_q.weight, my_mha.W_k.weight, my_mha.W_v.weight], dim=0))  # <-- KEY (3d, d)
    torch_mha.in_proj_bias.copy_(torch.cat([my_mha.W_q.bias, my_mha.W_k.bias, my_mha.W_v.bias], dim=0))
    torch_mha.out_proj.weight.copy_(my_mha.W_o.weight)
    torch_mha.out_proj.bias.copy_(my_mha.W_o.bias)

with torch.no_grad():
    mine = my_mha(x, mask=pad[:, None, None, :])
    theirs, theirs_w = torch_mha(x, x, x, key_padding_mask=~real,          # <-- KEY True = ignore this key
                                 need_weights=True, average_attn_weights=False)
```
- **Mask conventions differ:**
  - Ours: 1 = keep.
  - `F.scaled_dot_product_attention` bool `attn_mask`: True = attend.
  - `nn.MultiheadAttention` `key_padding_mask`: **True = ignore**, hence `~real`.
- `in_proj_weight` stacks `[W_q; W_k; W_v]` along `dim=0`, giving `(3·128, 128)`. `nn.Linear.weight` is `(out, in)`.
- `torch_mha(x, x, x)` passes query, key and value; self-attention means all three are `x`. `average_attn_weights=False` returns per-head weights `(B, h, T, T)`.
- Use `.eval()` and `no_grad` so dropout doesn't change the outputs.

### ★★ 10-I. Freezing BERT (train only the head)
```python
frozen_model = load_classifier()
for p in frozen_model.bert.parameters():       # <-- KEY embeddings + 12 encoder layers + pooler
    p.requires_grad = False                    # <-- KEY
n_frozen_trainable = count_params(frozen_model)        # 1,538
frozen_trainer, frozen_time = train_with_trainer(frozen_model, "bert-frozen", lr=1e-3)   # higher LR OK: only head trains

def count_params(model, trainable_only=True):
    return sum(p.numel() for p in model.parameters() if p.requires_grad or not trainable_only)   # <-- KEY
```
- `model.bert` is the body and `model.classifier` is the head (`Linear(768, 2)` = 1,538 params).
- Frozen BERT was 2.8× faster to train but scored 0.70 vs 0.90 accuracy. Its F1 (0.75) is inflated because it over-predicts positive.

### ★★ 10-J. Extracting BERT attentions + pipeline inference
```python
attn_model = AutoModelForSequenceClassification.from_pretrained(
    FULL_DIR, output_attentions=True, attn_implementation="eager").to(device).eval()   # <-- KEY
inputs = tokenizer(sentence, return_tensors="pt").to(device)
with torch.no_grad():
    outputs = attn_model(**inputs)
attentions = tuple(a.detach().cpu() for a in outputs.attentions)   # <-- KEY 12 x (1, 12, T, T)
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
probs = torch.softmax(outputs.logits, -1)[0].cpu()                 # logits (1, 2)

A = torch.stack([a[0] for a in attentions]).numpy()                # (layers, heads, T, T)

clf_full = pipeline("text-classification", model=FULL_DIR, tokenizer=FULL_DIR, device=pipe_device)   # <-- KEY
clf_full(tests)       # -> [{'label': 'POSITIVE', 'score': 0.996}, ...]
```
- `outputs.attentions[layer][0, head]` is a `(T, T)` matrix: rows = query (attending), columns = key (attended to), and each row sums to 1. Example: `attentions[5][0, 3]` = layer 6, sentence 0, head 4.
- `"eager"` is needed because the fused SDPA kernel returns no weights. Call `.cpu()` before `.numpy()`.
- `pipeline` device: `0` = GPU, `-1` = CPU.

### ★ 10-K. Reading heads (pattern scores, bertviz)
```python
idx = np.arange(T)
pattern_scores = {
    "previous token": A[:, :, idx[1:], idx[:-1]].mean(-1),   # query i -> key i-1
    "next token":     A[:, :, idx[:-1], idx[1:]].mean(-1),   # query i -> key i+1
    "[CLS]":          A[:, :, :, 0].mean(-1),
    "[SEP]":          A[:, :, :, T - 1].mean(-1),
    "itself":         A[:, :, idx, idx].mean(-1),
}
from bertviz import head_view
head_view(attentions, tokens)          # last line of the Colab cell; model_view(attentions, tokens) for all 144 heads
```
- Findings:
  - Layer 2 head 5 attends to the previous token (65%); layer 3 head 10 to the next token (94%).
  - Layer 2 head 7 attends to `[CLS]` (86%); layer 6 head 2 to `[SEP]` (92%). This "no-op" sink pattern dominates layers 5–10.
  - Layers 11–12 look at the comma and the period.
  - The mini-Transformer has **no positional heads** (prev 0.075, next 0.081). Every one of its heads is a vertical stripe on a keyword, effectively a weighted bag of words.

## 10.5 Fill-in-the-blank practice

**Q1.** Scaled dot-product attention
```python
def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.size(____)
    scores = Q @ K.__________(____, ____) / math.sqrt(____)
    if mask is not None:
        scores = scores.__________(mask == ____, -1e9)
    attention_weights = torch.softmax(scores, dim=____)
    output = __________ @ ____
    return output, attention_weights
```
**Q2.** `pad` has shape `(B, T)`. Write the padding mask that broadcasts to `(B, h, T, T)`: `mask = pad[________________]`. What shape does it have?

**Q3.** Split and merge heads
```python
def split_heads(self, x):
    B, T, _ = x.shape
    return x.______(B, T, self.num_heads, self.d_k).__________(____, ____)
def merge_heads(self, x):
    B, _, T, _ = x.shape
    return x.transpose(1, 2).________(B, T, self.d_model)     # why not .view?
```
**Q4.** `MultiHeadAttention.__init__`: `assert d_model % num_heads == ____`; `self.d_k = ________`. How many parameters does it have for `d_model = 128, num_heads = 8`?

**Q5.** Positional encoding
```python
position = torch.arange(max_len).__________(1)                                  # (max_len, 1)
div_term = torch.exp(torch.arange(0, d_model, ____) * (________________ / d_model))
pe[:, 0::2] = torch.____(position * div_term)
pe[:, 1::2] = torch.____(position * div_term)
self.__________________("pe", pe.unsqueeze(0))
...
return x + self.pe[:, :________]
```
**Q6.** Encoder block forward
```python
x = self.norm1(____ + self.dropout1(self.mha(x, ____)))
x = self.norm2(x + self.dropout2(self.______(x)))
```
and the FFN: `nn.Sequential(nn.Linear(d_model, ____), nn.______(), nn.Linear(____, ______))`.

**Q7.** Masked mean pooling
```python
m = attention_mask.__________(-1).to(x.dtype)            # (B, T, 1)
pooled = (x * m).sum(dim=____) / m.sum(dim=____).clamp(min=1)
```
**Q8.** Put the training step in order and fill in the missing names: `loss.________()`, `optimizer.________()`, `logits = model(input_ids, attention_mask)`, `optimizer.______()`, `loss = loss_fn(logits, labels)`. Where does `clip_grad_norm_` go?

**Q9.** BERT `compute_metrics` + model
```python
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", __________=2)
def compute_metrics(eval_pred):
    logits, labels = ________
    preds = np.______(logits, axis=____)
    return {"accuracy": accuracy_score(labels, preds), "f1": ________(labels, preds)}
```
**Q10.** Freeze BERT's body so only the head trains, then count the trainable params:
```python
for p in model.______.parameters():
    p.______________ = False
n = sum(p.numel() for p in model.parameters() if ______________)
```
**Q11.** `torch_mha.in_proj_weight.copy_(torch.cat([W_q.weight, W_k.weight, W_v.weight], dim=____))`. What is the resulting shape for `d_model = 128`? In `torch_mha(x, x, x, key_padding_mask=____)`, does True mean keep or ignore?

<details><summary>Answers</summary>

1. `-1`; `transpose(-2, -1)`; `d_k`; `masked_fill`; `0`; `-1`; `attention_weights @ V`.
2. `pad[:, None, None, :]`, shape `(B, 1, 1, T)`. It broadcasts over heads and query rows and hides key columns.
3. `view`; `transpose(1, 2)`; `reshape`. After `transpose` the tensor is not contiguous, so `.view` raises an error. Use `.reshape` or `.contiguous().view`.
4. `0`; `d_model // num_heads` (= 16 for h = 8). Params = 4 × (128·128 + 128) = **66,048**, independent of h.
5. `unsqueeze`; `2`; `-math.log(10000.0)`; `sin`; `cos`; `register_buffer`; `x.size(1)`.
6. `x`; `mask`; `ffn`. FFN: `d_ff`, `GELU`, `d_ff`, `d_model`.
7. `unsqueeze`; `1`; `1`.
8. Order: `optimizer.zero_grad()` → `logits = model(...)` → `loss = loss_fn(logits, labels)` → `loss.backward()` → (`clip_grad_norm_` here) → `optimizer.step()`.
9. `num_labels`; `eval_pred`; `argmax`; `-1`; `f1_score`.
10. `bert`; `requires_grad`; `p.requires_grad`. The result is 1,538 (= 768·2 + 2).
11. `0`; `(384, 128)`. True = **ignore**, so pass `~real` (the opposite of our 1 = keep).
</details>

## 10.6 Quick recall
- **Attention:**
  - `scores = Q @ K.transpose(-2,-1) / math.sqrt(d_k)` → `masked_fill(mask==0, -1e9)` → `softmax(dim=-1)` → `@ V`.
  - Shapes: Q, K, V `(B,h,T,d_k)` → scores and weights `(B,h,T_q,T_k)` → out `(B,h,T_q,d_k)`.
- **Mask:**
  - Applied **before** softmax, to the **scores**, using a **large negative** number (not 0; -inf gives nan on fully masked rows).
  - Padding mask `(B,1,1,T)`. Causal mask = lower triangle `(1,1,T,T)` (decoder only).
- **MHA:**
  - `d_k = d_model // h`. `W_q, W_k, W_v, W_o = nn.Linear(d_model, d_model)`.
  - Split: `x.view(B,T,h,d_k).transpose(1,2)`. Merge: `x.transpose(1,2).reshape(B,T,d_model)`. Then `W_o`.
  - Params = $4(d^2+d)$, independent of h (66,048 for d = 128).
- **PE:**
  - `div_term = exp(arange(0,d,2) * (-ln(10000)/d))`; `pe[:,0::2]=sin(pos*div)`, `pe[:,1::2]=cos(pos*div)`.
  - Store with `register_buffer` and **add** it to the embeddings.
- **Encoder block:** `x = LN(x + Drop(MHA(x)))` then `x = LN(x + Drop(FFN(x)))`, with FFN = `Linear(d,d_ff)-GELU-Linear(d_ff,d)`. Shape is preserved.
- **Classifier:** `Embedding(vocab, d, padding_idx=pad)` → PE → dropout → blocks (`nn.ModuleList`) → masked mean `(x*m).sum(1)/m.sum(1).clamp(min=1)` → `Linear(d,2)`.
- **Loop:** `zero_grad → forward → loss → backward → (clip) → step`. Use `model.train()` and `model.eval()` + `@torch.no_grad()`, and move everything with `.to(device)`.
- **HF:**
  - `AutoTokenizer.from_pretrained("bert-base-uncased")` → `tokenizer(batch["sentence"], truncation=True, max_length=64)`.
  - `.map(..., batched=True, remove_columns=["sentence","idx"])`, then `DataCollatorWithPadding(tokenizer=tokenizer)`.
  - `AutoModelForSequenceClassification.from_pretrained(name, num_labels=2, id2label=..., label2id=...)`.
  - `TrainingArguments(output_dir, learning_rate=2e-5, num_train_epochs=3, per_device_train_batch_size=32, weight_decay=0.01, eval_strategy="epoch", fp16=..., report_to="none")`.
  - `Trainer(model, args, train_dataset, eval_dataset, data_collator, compute_metrics)` → `.train()`, `.predict(test)`.
- **compute_metrics, classification vs seq2seq:**
  - Classification gets `(logits, labels)` → `np.argmax(logits, -1)` → accuracy / F1.
  - Seq2seq (Lab 9) gets `(generated_ids, labels)` → replace -100 → `batch_decode` → BLEU.
- **Attentions:** `from_pretrained(..., output_attentions=True, attn_implementation="eager")` → `outputs.attentions` = tuple(12) of `(B, 12, T, T)`; rows = queries and each row sums to 1.
- **Numbers to remember:**
  - BERT-base: 12 layers, 12 heads, hidden 768, ~110M params (109,483,778), head 1,538.
  - Mini model: 2 layers, 4 heads, d = 128, 4.17M params.
  - Test accuracy: scratch 0.716, frozen 0.701, full 0.897, DistilBERT 0.877.
- **Special tokens:** `[CLS]` = 101 (sentence summary), `[SEP]` = 102 (segment end), `##` = continuation word-piece, `attention_mask` 1 = real, 0 = pad.
- **Why BERT beats the scratch model:** pre-training (MLM/NSP on ~3.3B words) gives it word meaning, syntax and positional heads. The scratch model has to learn everything from 5k sentences and ends up spotting keywords.
- **Why BERT can't translate:** encoder-only and bidirectional, with no causal decoder, no cross-attention and no next-token training, and it outputs one vector per input token.

---

<a id="lab-11"></a>

# Lab 11 — Coreference Resolution & Question Answering

> **Read this first: what is and isn't in your notebooks.**
> - **No `# TODO` markers survive** in the Lab 11 submission. The template gave each function's **signature and docstring**, and you wrote the **body**. So every function body below with a docstring (`count_mention_types`, `bcubed`, `extract_answer`, `normalize_answer`/`exact_match`/`token_f1`, `bm25_retrieve`, `open_domain_qa`) was a **TODO BLANK**. (This is inferred from the "Complete all `# TODO` sections" instruction and the docstring-only stubs.)
> - **Your QA part did NOT fine-tune BERT.** It loads the already fine-tuned `deepset/bert-base-cased-squad2` and runs inference. `stride`, `return_overflowing_tokens` and `start_positions` **do not appear** in either Lab 11 notebook. The standard SQuAD training-preprocessing loop is still given in block **K** (★, background) in case the exam asks for "fine-tuning on SQuAD".
> - Frameworks: **HuggingFace `transformers`** (QA), **`fastcoref`** (`FCoref`, SpanBERT-style coref), **spaCy** `en_core_web_sm` (mention types), **scikit-learn** (TF-IDF retriever), PyTorch underneath.

## 11.1 What this lab is about
- **Coreference**: find every *mention* of an entity in the text and group the mentions into *clusters* (one cluster = one real-world entity), using a pretrained SpanBERT-based model (`FCoref`). Then score it against gold clusters with **B-cubed**.
- **Extractive QA**: given a (question, passage) pair, BERT predicts a **start** token and an **end** token, and the answer is the passage text between them. You score it with **EM** and **token F1**, and detect unanswerable questions with the **[CLS] null score** (SQuAD v2).
- **Open-domain QA**: a TF-IDF **retriever** picks the top-k passages, and the BERT **reader** extracts an answer from each one. The highest reader score wins.
- **Coref + QA**: replacing pronouns with their antecedent makes the answer extractable.

## 11.2 Core concepts & formulas

**Mentions.** There are three types: **pronouns** (he, her), **named entities** (Barack Obama), and **noun phrases** (the city, her son).
- **Antecedent**: the earlier mention that a later mention refers back to.
- **Cluster**: the set of mentions of one entity.
- **Singleton**: an entity mentioned only once. FCoref **drops singletons** (OntoNotes convention).
- **Not coreference**: *bridging* ("a concert … the tickets": related but different entities), *expletive* "It is sunny", non-specific "Every dancer", measures "100 miles".

**Mention-ranking.** Each mention $j$ scores every earlier candidate $i$, plus a dummy $\varepsilon$ that means "start a new cluster":
$$s(i,j) = s_m(i) + s_m(j) + s_a(i,j), \qquad s(\varepsilon, j) = 0$$
- $s_m$ = "is this span a real mention?"; $s_a$ = "is $i$ a good antecedent of $j$?".
- Pick $\arg\max$ over the antecedents and $\varepsilon$. Then link $j$ to that antecedent, and take the transitive closure (union-find) to get the clusters.
- *Worked example (tutorial):* "Obama visited Paris. He loved the city."
  - "He" scores: Obama +1.2, Paris −0.3, ε −0.5, so He → Obama.
  - "the city" scores: Paris +0.9, so it → Paris.
  - Clusters: {Obama, He}, {Paris, the city}.

**SpanBERT span representation** for span $(i,j)$:
$$g(i,j) = [\,h_i;\ h_j;\ \tilde h(i,j);\ \phi(i,j)\,]$$
- $h_i$ = first-token vector, $h_j$ = last-token vector.
- $\tilde h$ = attention-weighted average of the span's tokens (the "head").
- $\phi$ = features such as the span length.
- With 768-d BERT, $g$ has $768\cdot3+1 = \mathbf{2305}$ dims (tutorial demo, span "Barack Obama", tokens 1–2).

**B-cubed (B³).** It is computed **per mention** and then averaged over mentions:
$$P_m=\frac{|C_{gold}(m)\cap C_{sys}(m)|}{|C_{sys}(m)|},\quad R_m=\frac{|C_{gold}(m)\cap C_{sys}(m)|}{|C_{gold}(m)|},\quad P=\tfrac1n\sum_m P_m,\ R=\tfrac1n\sum_m R_m,\ F_1=\tfrac{2PR}{P+R}$$
- *Worked example (tutorial case 1):* gold {A,B,C,D},{E,F,G}; system {A,B,C,E},{D,F,G}.
  - A, B, C: $P=R=3/4$.
  - D: $P=1/3$, $R=1/4$.
  - E: $P=1/4$, $R=1/3$.
  - F, G: $P=R=2/3$.
  - $P = (2.25+0.333+0.25+1.333)/7 = \mathbf{0.595}$, and $R = 0.595$ by symmetry.
- $P=1$, low $R$ means **under-merging** (entities split up; all-singletons is the extreme).
- $R=1$, low $P$ means **over-merging** (everything in one cluster is the extreme).
- Other metrics:
  - **MUC** is link-based (how many links you must add or remove).
  - **CEAF** (CEAF-e / CEAF-m) is entity-alignment-based (best 1-to-1 matching of gold and system entities).
  - **CoNLL-2012 F1 = mean(MUC F1, B³ F1, CEAF-e F1)**. BLANC and LEA are also used.

**BERT for extractive QA.**
- Input: `[CLS] question [SEP] context [SEP]`.
- Two linear heads on top of the final hidden states $h_i$:
$$P_{start}(i)=\mathrm{softmax}_i(W_{start}h_i),\qquad P_{end}(i)=\mathrm{softmax}_i(W_{end}h_i)$$
- Span score: $\text{score}(s,e)=\text{start\_logit}[s]+\text{end\_logit}[e]$. Constraints: $s\le e$, $e-s<$ `max_answer_len`, and both $s$ and $e$ must be **context** tokens.
- **SQuAD v1.1** (~100k Qs): every question has an answer span.
- **SQuAD v2.0**: adds ~50k adversarial **unanswerable** questions. For these, training labels start = end = 0 (**[CLS]**). At inference:
$$s_{null}=\text{start}[0]+\text{end}[0];\quad \text{predict NO ANSWER if } s_{null} > s_{best}\ (+\tau)$$
- Example: "What year was Tesla born?" has span score −8.62 and null score 1.18, so the prediction is NO ANSWER.

**EM and token F1 (SQuAD).**
- Normalise both strings first: lowercase, strip punctuation, drop the articles a/an/the, collapse whitespace.
- **EM** = 1 if the normalised strings are equal.
- **F1** is computed on the bag of tokens:
$$\text{common}=\big|\text{Counter(pred)} \cap \text{Counter(gold)}\big|,\ P=\frac{\text{common}}{|pred|},\ R=\frac{\text{common}}{|gold|},\ F_1=\frac{2PR}{P+R}$$
- Take the **max over all gold answers**.
- *Example:* pred "66.54", gold "66.54 percent". Normalised: "6654" vs "6654 percent". EM = 0; $P=1/1$, $R=1/2$, so $F_1=0.667$.

**Open-domain QA**: retriever (TF-IDF/BM25 = sparse lexical, or DPR = dense dual BERT encoders with dot product) → reader (BERT span extractor) → keep the answer with the highest reader score. DPR matches synonyms ("built" ≈ "constructed"); BM25 needs exact word overlap.

## 11.3 Data & pipeline

**Data**
- The data is hand-written strings, not a downloaded dataset (`load_dataset` is imported but never used).
- `TEXT_1`/`TEXT_2`/`TEXT_3` are the coref texts. `GOLD_TEXT2` holds 4 gold clusters (one 4-mention person cluster + 3 singletons).
- `squad_examples` = 3 dicts `{'context','question','gold'}`.
- `CORPUS` = 8 one-sentence documents.

**Coref pipeline**
1. `FCoref(device=DEVICE)`.
2. `predict(texts=[...])` gives one result object per text.
3. `get_clusters(as_strings=True)` gives `List[List[str]]`; `as_strings=False` gives `List[List[(start_char, end_char)]]`.
4. Convert to `set`s.
5. Add back gold mentions that FCoref left unclustered as singletons.
6. Run `bcubed`.

**QA pipeline (one example, batch = 1, L = sequence length)**

| Step | Object | Shape / value |
|---|---|---|
| tokenizer(q, c, `return_tensors='pt'`, `truncation='only_second'`, `max_length=512`, `return_offsets_mapping=True`) | `inputs['input_ids']`, `attention_mask`, `token_type_ids` | `(1, L)` |
| | `inputs['offset_mapping']` | `(1, L, 2)`: char `(start, end)` per token; `(0,0)` for special tokens |
| `inputs.sequence_ids(0)` | list, len L | `None` = [CLS]/[SEP], `0` = question token, `1` = context token |
| `inputs.word_ids(0)` | list, len L | word index per token (sub-words of one word share it) |
| `model(**model_inputs)` | `outputs.start_logits`, `outputs.end_logits` | `(1, L)` each, then `[0]` gives `(L,)` |
| `best_span(...)` | `(s, e, score)` | ints + float |
| `context[offsets[s][0]:offsets[e][1]]` | answer string | |

- **Hyperparameters**: `max_length=512` and `max_answer_len=50` (the tutorial uses 30). Model: `deepset/bert-base-cased-squad2`.
- **Retriever**: `TfidfVectorizer(stop_words='english')` and cosine similarity, with `k=3`.

**Results to quote**
- TEXT_2: B³ P = R = F1 = **1.0**.
- QA on the 3 examples: EM **0.667**, F1 **0.889** (only "66.54" vs "66.54 percent" misses).
- Coref-aided QA: score −5.19 → −0.52 (**+4.67**).

## 11.4 Exam-critical code blocks

### ★★★ A. `best_span` + `extract_answer` — the QA core (TODO BLANK: body)
**What it does:** tokenises the (question, context) pair, runs BERT, searches every valid context span for the max `start[s]+end[e]`, snaps to whole words, and maps tokens back to characters.

```python
def best_span(start_logits, end_logits, ctx_start, ctx_end, max_answer_len=50):
    start, end = start_logits.tolist(), end_logits.tolist()
    best_s, best_e, best_score = ctx_start, ctx_start, float('-inf')          # <-- KEY
    for s in range(ctx_start, ctx_end + 1):                                    # <-- KEY
        for e in range(s, min(s + max_answer_len, ctx_end + 1)):   # end >= start, length cap   # <-- KEY
            score = start[s] + end[e]                                          # <-- KEY
            if score > best_score:
                best_s, best_e, best_score = s, e, score
    return best_s, best_e, best_score


def extract_answer(question, context, tokenizer, model, max_answer_len=50):
    # 1. Tokenise: [CLS] question [SEP] context [SEP]
    inputs = tokenizer(question, context, return_tensors='pt',
                       truncation='only_second', max_length=512,               # <-- KEY
                       return_offsets_mapping=True)                            # <-- KEY
    offsets = inputs['offset_mapping'][0].tolist()

    # sequence_ids: None for [CLS]/[SEP], 0 for question tokens, 1 for context tokens
    seq_ids = inputs.sequence_ids(0)                                           # <-- KEY
    ctx_tokens = [i for i, sid in enumerate(seq_ids) if sid == 1]              # <-- KEY
    ctx_start, ctx_end = ctx_tokens[0], ctx_tokens[-1]

    # 2. Forward pass
    model_inputs = {k: v.to(model.device) for k, v in inputs.items() if k != 'offset_mapping'}  # <-- KEY
    with torch.no_grad():                                                      # <-- KEY
        outputs = model(**model_inputs)
    start_logits = outputs.start_logits[0].cpu()                               # <-- KEY
    end_logits   = outputs.end_logits[0].cpu()

    # 3. Best valid span inside the context only (never question, [CLS] or [SEP])
    s, e, score = best_span(start_logits, end_logits, ctx_start, ctx_end, max_answer_len)

    # 4. Snap to whole words (span may start/end on a '##' piece)
    word_ids = inputs.word_ids(0)
    while s > ctx_start and word_ids[s - 1] == word_ids[s]:
        s -= 1
    while e < ctx_end and word_ids[e + 1] == word_ids[e]:
        e += 1

    # 5. Map the token span back to characters of the original context
    answer = context[offsets[s][0]:offsets[e][1]]                              # <-- KEY
    return answer, score
```
**Line-by-line notes**
- `truncation='only_second'`: if the pair is too long, cut **only the context** (the 2nd sequence) and never the question. `max_length=512` is BERT's position limit.
- `return_offsets_mapping=True` gives `(char_start, char_end)` per token, end-exclusive. Special tokens get `(0,0)`. **Question tokens' offsets index into the *question* string**, which is another reason to restrict to `sid == 1`.
- `sequence_ids(0)`: the `0` is the batch index. Example layout: `[None, 0,0,0,0, None, 1,1,…,1, None]`. So `ctx_start` = index right after the first [SEP], and `ctx_end` = index right before the last [SEP].
- `if k != 'offset_mapping'`: the model's `forward` does not accept `offset_mapping` and would raise an error.
- `outputs.start_logits[0]` has shape `(L,)`; the `[0]` drops the batch dim.
- `range(s, min(s + max_answer_len, ctx_end + 1))` enforces `e ≥ s`, `e - s < max_answer_len`, and `e ≤ ctx_end`. The `+1` is there because `range` is exclusive.
- Answer slice: `offsets[s][0]` = first char of the start token, `offsets[e][1]` = one past the last char of the end token. This slices the **original** string, so casing and spacing are preserved. That is better than `convert_tokens_to_string`, which gives "Te ##sla"-style artefacts.

**Common mistakes**
- Forgetting the context restriction, so the "answer" lands in the question or on [CLS].
- Using `argmax(start)` and `argmax(end)` independently. You can get `e < s`; a joint search is required.
- Slicing with `offsets[e][0]`, which cuts off the last token, or with the inclusive/exclusive `range` bounds off by one.

### ★★★ B. `bcubed` (TODO BLANK: body; the algorithm was given in the docstring)
**What it does:** builds mention → cluster-index maps, computes per-mention P/R, averages them, and returns F1.
```python
def bcubed(gold_clusters, system_clusters):
    # 1. mention → cluster index
    gold_idx = {m: i for i, c in enumerate(gold_clusters)   for m in c}       # <-- KEY
    sys_idx  = {m: i for i, c in enumerate(system_clusters) for m in c}

    # Evaluate over all mentions; one missing from a side counts as a singleton there
    mentions = set(gold_idx) | set(sys_idx)
    if not mentions:
        return 0.0, 0.0, 0.0

    # 2. per-mention precision and recall
    p_sum = r_sum = 0.0
    for m in mentions:
        gold_c = set(gold_clusters[gold_idx[m]])  if m in gold_idx else {m}
        sys_c  = set(system_clusters[sys_idx[m]]) if m in sys_idx  else {m}
        overlap = len(gold_c & sys_c)                                          # <-- KEY
        p_sum += overlap / len(sys_c)                                          # <-- KEY  P divides by SYSTEM
        r_sum += overlap / len(gold_c)                                         # <-- KEY  R divides by GOLD

    # 3. average over mentions
    P = p_sum / len(mentions)
    R = r_sum / len(mentions)

    # 4. F1
    F1 = 2 * P * R / (P + R) if (P + R) > 0 else 0.0
    return round(P, 3), round(R, 3), round(F1, 3)
```
**Notes**
- The nested dict comprehension `{m: i for i, c in enumerate(clusters) for m in c}` reads left to right like nested for loops.
- **Tutorial vs submission:**
  - The tutorial's `bcubed_verbose` evaluates over `set(gold_map) & set(system_map)` (the intersection).
  - The submission uses the **union** and treats a missing mention as a singleton `{m}`, which is more robust.
  - Both give 0.595 on case 1.

**Common mistakes:** swapping the denominators (P uses $|C_{sys}|$, R uses $|C_{gold}|$); averaging per cluster instead of per **mention**; division by zero in F1.

### ★★★ C. FCoref API + system clusters with singletons (TODO BLANK)
```python
coref_model = FCoref(device=DEVICE)                                            # <-- KEY
TEXTS = [TEXT_1, TEXT_2, TEXT_3]
coref_preds = coref_model.predict(texts=TEXTS)                                 # <-- KEY  list, one result per text

for i, (text, pred) in enumerate(zip(TEXTS, coref_preds), 1):
    clusters_str  = pred.get_clusters(as_strings=True)                         # <-- KEY  [['Barack Obama','He',...], ...]
    clusters_span = pred.get_clusters(as_strings=False)                        # <-- KEY  [[(0,12),(33,35),...], ...]
    for j, (cluster, spans) in enumerate(zip(clusters_str, clusters_span), 1):
        print(f'  Cluster {j}: ' + ' → '.join(cluster))

# System clusters for TEXT_2 (index 1)
system_clusters_text2 = [set(c) for c in coref_preds[1].get_clusters(as_strings=True)]   # <-- KEY
clustered = set().union(*system_clusters_text2)
for gold_cluster in GOLD_TEXT2:
    for mention in gold_cluster:
        if mention not in clustered:
            system_clusters_text2.append({mention})                            # add singletons back
```
**Notes**
- Offsets are **character** offsets, end-exclusive: `text[s:e]` gives the mention text (the tutorial prints `text1[s:e]`).
- Singletons must be re-added, otherwise B³ has no system cluster for "Hawaii" etc.

**Common mistakes:** passing a bare string (it must be the keyword `texts=` with a **list**); forgetting `[0]` when you predict a single text (`coref_model.predict(texts=[p])[0]`).

### ★★★ D. `normalize_answer`, `exact_match`, `token_f1` (TODO BLANK: bodies)
```python
def normalize_answer(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))           # <-- KEY
    text = re.sub(r'\b(a|an|the)\b', ' ', text)                                # <-- KEY
    return ' '.join(text.split())                                              # <-- KEY

def exact_match(prediction, gold_answers):
    if isinstance(gold_answers, str):
        gold_answers = [gold_answers]
    pred = normalize_answer(prediction)
    return int(any(pred == normalize_answer(g) for g in gold_answers))          # <-- KEY

def _f1_single(prediction, gold):
    pred_toks = normalize_answer(prediction).split()
    gold_toks = normalize_answer(gold).split()
    if not pred_toks or not gold_toks:          # SQuAD v2 no-answer: correct only if both empty
        return float(pred_toks == gold_toks)
    common = sum((Counter(pred_toks) & Counter(gold_toks)).values())          # <-- KEY
    if common == 0:
        return 0.0
    precision = common / len(pred_toks)                                        # <-- KEY
    recall    = common / len(gold_toks)                                        # <-- KEY
    return 2 * precision * recall / (precision + recall)

def token_f1(prediction, gold_answers):
    if isinstance(gold_answers, str):
        gold_answers = [gold_answers]
    return max(_f1_single(prediction, g) for g in gold_answers)                # <-- KEY  max over golds
```
**Notes**
- `str.maketrans('', '', chars)` builds a table that **deletes** `chars`. The tutorial uses `''.join(ch for ch in text if ch not in string.punctuation)` instead; both work.
- `\b(a|an|the)\b` uses word boundaries so "theme" is not damaged.
- `Counter & Counter` = multiset intersection (the **min** count of each token).
- Tutorial sanity cases:
  - "left Graz and served" vs "left Graz": P = 2/4, R = 2/2, F1 = **0.667**, EM = 0.
  - "the 44th" vs "44th": EM = 1.

**Common mistakes:** using `set` instead of `Counter` (loses repeated tokens); taking the **average** over gold answers instead of the **max**; forgetting to normalise both sides.

### ★★ E. SQuAD v2 null score (TODO BLANK)
```python
def no_answer_score(question, context, tokenizer, model):
    """SQuAD v2.0 null score: start_logit[CLS] + end_logit[CLS] ([CLS] is position 0)."""
    enc = tokenizer(question, context, return_tensors='pt', truncation='only_second', max_length=512)
    with torch.no_grad():
        out = model(**{k: v.to(model.device) for k, v in enc.items()})
    return out.start_logits[0, 0].item() + out.end_logits[0, 0].item()        # <-- KEY  [batch 0, position 0]

# decision
'NO ANSWER' if null_v2 > score_v2 else f'ANSWER = "{ans_v2}"'                   # <-- KEY
```
**Common mistake:** comparing the null score against a span that was allowed to *include* [CLS]. The best span must come from context tokens only.

### ★★ F. `count_mention_types` with spaCy (TODO BLANK: body)
```python
nlp = spacy.load('en_core_web_sm')
def count_mention_types(text):
    doc = nlp(text)
    return {
        'pronouns':       sum(1 for tok in doc if tok.pos_ == 'PRON'),          # <-- KEY  POS tag
        'named_entities': len(doc.ents),                                       # <-- KEY  NER
        'noun_phrases':   sum(1 for _ in doc.noun_chunks),                     # <-- KEY  generator, no len()
    }
```
- Attributes: `tok.pos_` (coarse POS, string), `tok.tag_` (fine-grained, e.g. `PRP$`), `ent.text`, `ent.label_` (e.g. PERSON, GPE), `chunk.root.text`.
- `doc.noun_chunks` is a **generator**, so `len()` fails; count it with `sum`.

### ★★ G. TF-IDF retriever + retriever–reader pipeline (TODO BLANK: bodies)
```python
def bm25_retrieve(query, corpus, k=3):
    vectorizer = TfidfVectorizer(stop_words='english')
    doc_vecs   = vectorizer.fit_transform(corpus)                              # <-- KEY  fit on corpus
    query_vec  = vectorizer.transform([query])                                 # <-- KEY  transform only, list!
    sims  = cosine_similarity(query_vec, doc_vecs).ravel()                     # (1, n_docs) -> (n_docs,)
    top_k = np.argsort(sims)[::-1][:k]                                         # <-- KEY  descending
    return [(float(sims[i]), corpus[i]) for i in top_k]

def open_domain_qa(question, corpus, retriever, reader_fn, k=3, verbose=False):
    best_answer, best_score = '', float('-inf')
    for rank, (ret_score, passage) in enumerate(retriever(question, corpus, k), 1):
        answer, qa_score = reader_fn(question, passage)
        if qa_score > best_score:                                              # <-- KEY  pick by READER score
            best_answer, best_score = answer, qa_score
    return best_answer, best_score

def reader(question, context):
    return extract_answer(question, context, tokenizer, qa_model)
```
**Common mistakes:** calling `fit_transform` on the query, which builds a new vocabulary and makes the vectors incompatible; `transform(query)` without a list; ranking by retrieval score instead of reader score.

### ★★ H. Span representation (tutorial demo)
```python
with torch.no_grad():
    hidden = bert(**inputs).last_hidden_state[0]  # [seq_len, 768]
i, j = 1, 2
h_i = hidden[i]; h_j = hidden[j]
span_tokens = hidden[i:j+1]                                   # [span_len, 768]
attn_weights = torch.softmax(torch.ones(j-i+1), dim=0)        # uniform
h_head = (attn_weights.unsqueeze(1) * span_tokens).sum(dim=0) # [768]
span_length = torch.tensor([j - i + 1], dtype=torch.float)
g = torch.cat([h_i, h_j, h_head, span_length])                # [2305]
```
- Index 0 is `[CLS]`, which is why "Barack Obama" sits at tokens 1–2.
- `unsqueeze(1)` turns `(span_len,)` into `(span_len, 1)` so it broadcasts over 768.

### ★ I. Mention-ranking + union-find (tutorial demo)
```python
best_ant = max(scores[j], key=lambda k: scores[j][k])        # argmax over antecedents incl. 'ε'
def find(x):
    while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(a, b):
    parent[find(a)] = find(b)
for j in range(len(mentions)):
    if antecedent_of[j] != 'ε': union(j, antecedent_of[j])
```

### ★ J. Coref-aided QA (Part 7)
```python
coref_pred_p7 = coref_model.predict(texts=[coref_passage])[0]
resolved_passage = coref_passage.replace('She won', 'Maria won').replace(' her by', ' Maria by')
ans_resolved, score_resolved = extract_answer(coref_question, resolved_passage, tokenizer, qa_model)
```
Results:
- Before: "She won the national science prize in 2023" (−5.19).
- After: the span starts at "Maria" (−0.52).
- The end overshoots because start and end are chosen independently.

### ★ K. BACKGROUND (NOT in your notebooks): SQuAD fine-tuning labels, char span → token positions
Use this only if asked to "prepare SQuAD features for training". It is the standard HF recipe.
```python
max_length, stride = 384, 128
def preprocess_training_examples(examples):
    questions = [q.strip() for q in examples["question"]]
    inputs = tokenizer(questions, examples["context"], max_length=max_length,
                       truncation="only_second", stride=stride,
                       return_overflowing_tokens=True, return_offsets_mapping=True,
                       padding="max_length")
    offset_mapping = inputs.pop("offset_mapping")
    sample_map = inputs.pop("overflow_to_sample_mapping")   # window -> original example index
    answers = examples["answers"]
    start_positions, end_positions = [], []
    for i, offset in enumerate(offset_mapping):             # i = window index
        answer = answers[sample_map[i]]
        start_char = answer["answer_start"][0]
        end_char = answer["answer_start"][0] + len(answer["text"][0])   # exclusive
        sequence_ids = inputs.sequence_ids(i)
        idx = 0
        while sequence_ids[idx] != 1: idx += 1               # first context token
        context_start = idx
        while sequence_ids[idx] == 1: idx += 1               # walk past the context
        context_end = idx - 1                                # last context token
        if offset[context_start][0] > start_char or offset[context_end][1] < end_char:
            start_positions.append(0); end_positions.append(0)          # answer not (fully) in window -> [CLS]
        else:
            idx = context_start
            while idx <= context_end and offset[idx][0] <= start_char: idx += 1
            start_positions.append(idx - 1)                  # last token starting at/before start_char
            idx = context_end
            while idx >= context_start and offset[idx][1] >= end_char: idx -= 1
            end_positions.append(idx + 1)                    # first token ending at/after end_char
    inputs["start_positions"] = start_positions
    inputs["end_positions"] = end_positions
    return inputs
```
- `stride` = number of **overlapping** tokens between consecutive windows of a long context. One example can become several rows, and `overflow_to_sample_mapping` maps each row back to its example.
- An unanswerable question (SQuAD v2: `answer["answer_start"] == []`) is also labelled `(0, 0)`.
- Passing `start_positions=`/`end_positions=` to `AutoModelForQuestionAnswering` returns `outputs.loss` = (CE(start) + CE(end)) / 2.
- **n-best** (also not in the notebooks): instead of the full $O(L\cdot\text{max\_len})$ loop, take the top-20 starts × top-20 ends, then filter by `e ≥ s`, `e - s + 1 ≤ max_answer_length`, and both in context.

## 11.5 Fill-in-the-blank practice

**Q1.**
```python
inputs = tokenizer(question, context, return_tensors='pt',
                   truncation=____, max_length=512, ____=True)
offsets = inputs['offset_mapping'][0].tolist()
```
**Q2.**
```python
seq_ids = inputs.____(0)
ctx_tokens = [i for i, sid in enumerate(seq_ids) if sid == ____]
```
**Q3.**
```python
model_inputs = {k: v.to(model.device) for k, v in inputs.items() if k != ____}
with torch.____():
    outputs = model(**model_inputs)
start_logits = outputs.____[0]
```
**Q4.**
```python
for s in range(ctx_start, ctx_end + 1):
    for e in range(____, min(____, ctx_end + 1)):
        score = ____
```
**Q5.** `answer = context[offsets[s][__]:offsets[e][__]]`

**Q6.** `null = out.start_logits[__, __].item() + out.end_logits[__, __].item()`. Predict NO ANSWER when `____ > ____`.

**Q7.**
```python
overlap = len(gold_c ____ sys_c)
p_sum += overlap / len(____)
r_sum += overlap / len(____)
```
**Q8.**
```python
text = text.translate(str.maketrans('', '', ____))
text = re.sub(r'____', ' ', text)
common = sum((Counter(pred_toks) ____ Counter(gold_toks)).values())
precision = common / ____
```
**Q9.**
```python
preds = coref_model.____(texts=[TEXT_2])
clusters = preds[0].get_clusters(____=True)
```
**Q10.**
```python
doc_vecs  = vectorizer.____(corpus)
query_vec = vectorizer.____([query])
top_k = np.argsort(sims)[____][:k]
```
**Q11 (numeric).** Gold {A,B,C}, {D}. System {A,B}, {C,D}. Compute B³ P, R and F1.

<details><summary>Answers</summary>

1. `'only_second'`, `return_offsets_mapping`
2. `sequence_ids`, `1`
3. `'offset_mapping'`, `no_grad`, `start_logits`
4. `s`, `s + max_answer_len`, `start[s] + end[e]`
5. `0`, `1`
6. `0, 0` and `0, 0`; `null > span_score`
7. `&`, `sys_c`, `gold_c`
8. `string.punctuation`; `\b(a|an|the)\b`; `&`; `len(pred_toks)`
9. `predict`; `as_strings`
10. `fit_transform`; `transform`; `::-1`
11. Per-mention scores:
    - A: P = 2/2, R = 2/3. B: same as A.
    - C: sys {C,D}, overlap {C} = 1, so P = 1/2, R = 1/3.
    - D: sys {C,D}, gold {D}, so P = 1/2, R = 1/1.
    - P = (1+1+0.5+0.5)/4 = **0.75**; R = (2/3+2/3+1/3+1)/4 = **0.667**; F1 = 2(0.75)(0.667)/1.417 = **0.706**.

</details>

## 11.6 Quick recall
- **FCoref**: `FCoref(device='cpu'|'cuda')`, then `.predict(texts=[str, ...])` gives a list of results. `res.get_clusters(as_strings=True)` returns `List[List[str]]`; `as_strings=False` returns `List[List[(char_s, char_e)]]`. **Singletons dropped.**
- **Mention ranking**: $s(i,j)=s_m(i)+s_m(j)+s_a(i,j)$, with $s(\varepsilon,j)=0$ = new cluster.
- **SpanBERT span**: $g=[h_i;h_j;\tilde h;\phi]$, dim $3\cdot768+1=2305$. History: rule-based ~55, Lee 2017 67.2, SpanBERT **79.6** F1 on OntoNotes.
- **B³**: per mention, P over $|C_{sys}|$, R over $|C_{gold}|$, then average over mentions. CoNLL F1 = avg(MUC, B³, CEAF-e).
- **QA load**: `AutoTokenizer.from_pretrained(name)`, `AutoModelForQuestionAnswering.from_pretrained(name).to(DEVICE)`, `.eval()`.
- **Tokenizer**: `tokenizer(q, c, return_tensors='pt', truncation='only_second', max_length=512, return_offsets_mapping=True)`. Methods `.sequence_ids(b)` (None/0/1) and `.word_ids(b)`. Helpers `tokenizer.convert_ids_to_tokens(ids)`, `convert_tokens_to_string(toks)`, `tokenizer.sep_token_id`.
- **Outputs**: `outputs.start_logits`, `outputs.end_logits` with shape `(B, L)`. Span score = `start[s] + end[e]`, with `ctx_start ≤ s ≤ e ≤ ctx_end` and `e - s < max_answer_len`.
- **Null score**: `start[0] + end[0]` ([CLS]). If null > best span, predict no answer.
- **Normalise**: lower → remove punctuation → remove a/an/the → collapse spaces. EM = `int(any(==))`; F1 = max over golds of bag-of-words F1 (`Counter &`).
- **Retriever**: `TfidfVectorizer(stop_words='english').fit_transform(corpus)` / `.transform([q])` → `cosine_similarity(q, D).ravel()` → `np.argsort(...)[::-1][:k]`.
- **Gotchas**:
  - Drop `offset_mapping` before calling `model(**...)`.
  - Use `torch.no_grad()` and `.eval()`.
  - Offsets of question tokens refer to the question string.
  - `noun_chunks` is a generator.
  - FCoref needs a list of texts.

---


---

<a id="lab-12"></a>

# Lab 12 — Mixture of Experts inside a Transformer (routing, load balancing, capacity)

> **TODO status:**
> - The Lab 12 assignment has **no `# TODO` comments**. Each `# ---- TASK n ----` cell was **entirely blank**: the notebook says *"You are expected to write the code yourself… names to use… but not how to write it"*. So **every Task block (A–E, G, I) is a TODO BLANK**. The Setup cell (block F: data, `Expert`, `TinyTransformerClassifier`, `train_model`, `evaluate`) was **given**.
> - Framework: **pure PyTorch** (`torch`, `torch.nn as nn`, `torch.nn.functional as F`) plus NumPy.
> - Note: the **capacity formula uses FLOOR** (`int(...)`), not ceil.

## 12.1 What this lab is about
- A Mixture of Experts replaces a Transformer block's **feed-forward layer** with **8 expert FFNs** and a **router**. The router sends **each token** to its top-k experts, and only those experts run (**sparse dispatch**).
- Task: classify AG News articles into 4 topics.
- You test four things:
  1. Noisy top-1 never trains its router.
  2. The Switch load-balancing loss evens out expert usage.
  3. Uneven routing overflows **expert capacity**, so tokens are dropped.
  4. Experts don't specialise by topic.
- The tutorial built the same idea on a 2-D toy with 4 linear experts and a softmax/top-1 gate.

## 12.2 Core concepts & formulas

**MoE output** (tutorial):
$$y=\sum_{i=1}^{n}G(x)_i\,E_i(x),\qquad G(x)=\mathrm{softmax}(W_gx)$$
- Soft gating runs every expert. Top-1 ("greedy") keeps only $i^*=\arg\max_i G(x)_i$ and outputs $y=G(x)_{i^*}E_{i^*}(x)$.
- The gradient reaches the gate through the scalar $G(x)_{i^*}$: $\nabla L/\nabla G(x)_{i^*}=E_{i^*}(x)^\top\nabla L/\nabla y$.

**Noisy top-k gating** (Shazeer et al. 2017):
$$H(x)_i=(xW_g)_i+\varepsilon\cdot\mathrm{Softplus}((xW_{noise})_i),\ \varepsilon\sim\mathcal N(0,1)\ \ (\text{training only})$$
$$\mathrm{KeepTopK}(v,k)_i=\begin{cases}v_i & \text{top-}k\\-\infty&\text{else}\end{cases},\qquad G(x)=\mathrm{softmax}(\mathrm{KeepTopK}(H(x),k))$$
- $e^{-\infty}=0$, so each row of $G$ has exactly $k$ non-zeros summing to 1. That is the **renormalisation over the top-k**.
- *Worked example:* $H=[2.0, 1.0, 0.5, -1.0]$, $k=2$ gives KeepTopK $=[2,1,-\infty,-\infty]$, so $G=[e^2,e^1,0,0]/(e^2+e^1)=[0.731, 0.269, 0, 0]$.

**Why noisy top-1 never learns.**
- With $k=1$, $G_{i^*}=e^{H_{i^*}}/e^{H_{i^*}}=1$ always.
- $\partial G_{i^*}/\partial H_{i^*}=G_{i^*}(1-G_{i^*})=0$, and top-k *selection* is discrete. So $W_g$ gets **zero gradient**.
- Measured: router moved **0.000**.
- The **Switch router** fixes this by gating with the full softmax probability $p(x)_{i^*}<1$, which has a non-zero gradient: $\partial p_{i^*}/\partial h_j=p_{i^*}(\delta_{i^*j}-p_j)$.

**Switch router** (Fedus et al. 2021):
$$p(x)=\mathrm{softmax}(xW_g),\ i^*=\arg\max_ip(x)_i,\ y=p(x)_{i^*}E_{i^*}(x)$$
No noise, k = 1.

**Load-balancing loss** (Switch). For a batch of $T$ tokens and $N$ experts:
$$f_i=\frac1T\sum_x\mathbb 1\{\text{top1}(x)=i\},\quad P_i=\frac1T\sum_xp_i(x),\quad \mathcal L_{aux}=\alpha\cdot N\sum_{i=1}^Nf_iP_i$$
- Perfectly even ($f_i=P_i=1/N$): $N\cdot N\cdot\frac1{N^2}=\mathbf 1$ (the minimum).
- All tokens to expert 0 with probability 1: $N\cdot1\cdot1=\mathbf 8$.
- $f_i$ comes from an argmax, so it has **no gradient**. The gradient flows through $P_i$: $\partial\mathcal L/\partial p_i(x)=Nf_i/T$. Busy experts' probabilities are pushed down the hardest.

**Expert capacity** (notebook formula, **floor**):
$$\text{capacity}=\Big\lfloor \text{cf}\times\frac{T\cdot k}{N}\Big\rfloor$$
- $T\cdot k$ because each token occupies $k$ slots.
- Tokens beyond capacity are **dropped** from that expert and pass through the **residual** only.
- cf = 1.0 means no slack; Switch used 1.25.
- *Worked example:* 6 tokens, k = 1, N = 3, cf = 1 gives capacity 2. Counts are [3, 1, 2], so 1 overflows: 1/6 = **0.167**.
- *Real batch:* T ≈ 2800, k = 2, N = 8, cf = 1.25 gives ⌊1.25·700⌋ = 875.

**Metrics.**
- **Usage CV** = std/mean of the expert-usage array (0 = even).
- **Routing entropy** (tutorial) $-\sum p\log p$ per cluster: 0 = one expert, $\log 4=1.39$ = spread evenly.
- **Chance agreement** of consecutive tokens = $\sum_iu_i^2$.
- **Router collapse**: too many inputs go to too few experts (tutorial seed 4: usage [0.25, 0.12, 0.39, 0.24], accuracy 0.868).

**Parameter counts** (D = 64, H = 128, N = 8):
- Expert = $64\cdot128+128+128\cdot64+64=16{,}576$.
- Router = $2\times64\cdot8=1{,}024$ (bias-free $W_g$ and $W_{noise}$).
- MoE layer = $8\cdot16576+1024=133{,}632$.
- Active per token (k = 2) = $1024+2\cdot16576=34{,}176$.

## 12.3 Data & pipeline

**Data**: `mini_agnews.tsv`, tab-separated with header `split label text`. It has 16,000 train and 2,000 test articles (4,000 / 500 per topic). `TOPICS = ['World','Sports','Business','Sci/Tech']`.

**Preprocessing (given)**
1. `tokenize`: lowercase, then regex `r"[a-z0-9]+(?:'[a-z]+)?|[^\sa-z0-9]"`. This keeps words (with clitics like `'s`) and single punctuation characters.
2. Vocab: `['<pad>', '<unk>']` plus words with count ≥ 2 (19,359 words). `<pad>` = 0, `<unk>` = 1.
3. `encode`: truncate to `MAX_LEN = 64`, **pad at the END** with 0. Shapes: `X_train (16000, 64)`, `X_test (2000, 64)`. About 43.8 real tokens per article.

**Hyperparameters**: `D_MODEL=64`, `D_HIDDEN=128`, `N_EXPERTS=8`, `EPOCHS=3`, `BATCH=64`, Adam `lr=2e-3`, seed 42. Loss = CE + `alpha * load_balancing_loss(f.probs, f.top1, f.n_experts)` (only when alpha > 0).

**Forward shapes** (B = 64 articles, L = 64, D = 64, T = number of real tokens in the batch ≈ 2800, N = 8):

| Op | Shape |
|---|---|
| `X` | `(B, L)` long |
| `mask = X != 0` | `(B, L)` bool |
| `self.emb(X) + self.pos(torch.arange(L))` | `(B,L,D)` + `(L,D)` broadcast = `(B,L,D)` |
| `a = ln1(x)`; `attn(a,a,a,key_padding_mask=~mask)[0]` | `(B,L,D)`; `~mask` True = **ignore** padding |
| `tokens = ln2(x)[mask]` | `(T, D)`: real tokens, flattened row by row |
| **router** `logits = w_gate(tokens)` | `(T, N)` |
| `topk(k)` gives `top_vals, top_idx` | `(T, k)`, `(T, k)` (best first) |
| `kept` / `gates` / `probs` | `(T, N)` each |
| per expert: `rows` / `x[rows]` / `out` | `(n_i,)` / `(n_i, D)` / `(n_i, D)` |
| `y.index_add_(0, rows, gates[rows,i].unsqueeze(1)*out)` | `y (T, D)` |
| `y_full[mask] = ffn(tokens)`; `x = x + y_full` | `(B,L,D)`: residual around the FFN |
| masked mean `(x*mask.unsqueeze(-1)).sum(1)/mask.sum(1,keepdim=True)` | `(B, D)` |
| `self.out` | `(B, 4)` logits |
| LB loss: `f`, `P` | `(N,)`, `(N,)`, giving a scalar |
| `evaluate` routing list | one `(T_b, k)` tensor per test batch |

**Results to quote**

| Model | Test acc | Router moved | Notes |
|---|---|---|---|
| dense | 0.8505 | – | |
| noisy top-2 | 0.8405 | 1.436 | |
| noisy top-1 | 0.8475 | **0.000** | |
| switch | 0.8380 | 1.516 | |

| α | Usage CV | Busiest expert | Quietest expert | Acc |
|---|---|---|---|---|
| 0 | 0.347 | 0.224 | 0.085 | 0.8405 |
| 0.01 | 0.225 | 0.177 | 0.092 | 0.8440 |
| 0.1 | 0.113 | 0.153 | 0.105 | 0.8435 |

| cf | Dropped (α = 0) | Dropped (α = 0.1) |
|---|---|---|
| 1.0 | 7.9% | 5.6% |
| 1.25 | 2.0% | 0.1% |
| 1.5 | 0.1% | 0.0% |
| 2.0 | 0.0% | 0.0% |

- Specialisation (Task 5): each topic's favourite expert gets only about 0.25 of its tokens (even = 0.125). Consecutive tokens share an expert 0.185 of the time vs 0.127 by chance.

## 12.4 Exam-critical code blocks

### ★★★ A. `NoisyTopKRouter` (TODO BLANK — Task 1)
**What it does:** computes clean logits, adds noise while training, keeps the top-k, softmaxes the kept logits into `gates`, and softmaxes all logits into `probs`.
```python
class NoisyTopKRouter(nn.Module):
    def __init__(self, d_model, n_experts, k):
        super().__init__()
        self.w_gate  = nn.Linear(d_model, n_experts, bias=False)                # <-- KEY
        self.w_noise = nn.Linear(d_model, n_experts, bias=False)                # <-- KEY
        self.k, self.n_experts = k, n_experts

    def forward(self, x):
        logits = self.w_gate(x)                                          # clean logits (T, N)
        if self.training:                                                # noise only while training   # <-- KEY
            logits = logits + torch.randn_like(logits) * F.softplus(self.w_noise(x))                   # <-- KEY
        top_vals, top_idx = logits.topk(self.k, dim=-1)                  # (T, k), best first          # <-- KEY
        kept  = torch.full_like(logits, float('-inf')).scatter(-1, top_idx, top_vals)   # KeepTopK     # <-- KEY
        gates = F.softmax(kept, dim=-1)                                  # k non-zeros, rows sum to 1  # <-- KEY
        probs = F.softmax(logits, dim=-1)                                # over ALL experts (Task 3)   # <-- KEY
        return gates, top_idx, probs
```
**Line-by-line notes**
- `F.softplus(z) = log(1+e^z)` > 0, so it is a valid learned noise **std** per expert. `torch.randn_like` gives N(0,1) noise with the same shape `(T, N)`.
- `self.training` is True after `model.train()` and False after `model.eval()`.
- `t.topk(k, dim=-1)` returns `(values, indices)` sorted descending, so `top_idx[:, 0]` is the best expert.
- `full_like(logits, -inf).scatter(-1, top_idx, top_vals)` puts the k real logits back at their expert positions; every other position stays at −∞. This is the one-line KeepTopK. `scatter` (not `scatter_`) returns a new tensor.
- `gates` = softmax over the **kept** vector, which renormalises over the top-k. `probs` = softmax over **all** (noisy) logits; the LB loss needs this.

**Common mistakes**
- Adding noise in eval.
- Softmaxing all logits for `gates`, so rows don't have k non-zeros. Or multiplying `probs` by a mask, so rows don't sum to 1.
- Using a bias in the router layers. The spec says bias-free; this changes the parameter count (1,024).

### ★★★ B. `MoELayer` — sparse dispatch + combine (TODO BLANK — Task 1)
```python
class MoELayer(nn.Module):
    def __init__(self, d_model, d_hidden, n_experts, router):
        super().__init__()
        self.router    = router
        self.n_experts = n_experts
        self.experts   = nn.ModuleList([Expert(d_model, d_hidden) for _ in range(n_experts)])   # <-- KEY

    def forward(self, x):
        gates, top_idx, probs = self.router(x)
        self.probs, self.top_idx, self.top1 = probs, top_idx, top_idx[:, 0]   # <-- KEY  saved for Tasks 2-5
        y = torch.zeros_like(x)                                                # (T, D)
        for i, expert in enumerate(self.experts):
            rows = (gates[:, i] > 0).nonzero().squeeze(1)                # tokens routed to expert i   # <-- KEY
            if len(rows) == 0:
                continue
            out = expert(x[rows])                                        # run ONLY those tokens       # <-- KEY
            y.index_add_(0, rows, gates[rows, i].unsqueeze(1) * out)     # y_t += G(x_t)_i * E_i(x_t)  # <-- KEY
        return y
```
**Notes**
- `nn.ModuleList` (not a Python list) **registers** the experts' parameters, so `model.parameters()` and the optimizer see them.
- `(gates[:, i] > 0)` is a `(T,)` bool. `.nonzero()` gives `(n_i, 1)`, and `.squeeze(1)` turns it into `(n_i,)` row indices.
- `gates[rows, i]` is `(n_i,)`; `.unsqueeze(1)` makes it `(n_i, 1)` so it broadcasts against `out (n_i, D)`.
- `y.index_add_(dim=0, index=rows, source)` does `y[rows[j]] += source[j]`. It accumulates a token's contributions from its k experts. It is in-place (trailing `_`) and autograd-safe.
- The `continue` guards against running an expert on an empty batch.

**Common mistakes**
- Running every expert on every token and multiplying by 0. The numbers come out right, but it is **not sparse**.
- `y[rows] = ...` (assignment) instead of `index_add_`. The 2nd expert's contribution overwrites the 1st when k = 2.
- Forgetting to store `self.probs`, `self.top_idx` and `self.top1`; `train_model` and `evaluate` read them.

### ★★★ C. `load_balancing_loss` (TODO BLANK — Task 3)
```python
def load_balancing_loss(probs, top1, n_experts):
    f = F.one_hot(top1, n_experts).float().mean(0)                       # fraction dispatched (no grad)   # <-- KEY
    P = probs.mean(0)                                                    # mean router probability         # <-- KEY
    return n_experts * (f * P).sum()                                                                       # <-- KEY

# sanity checks
even_probs = torch.full((8, 8), 1 / 8)
load_balancing_loss(even_probs, torch.arange(8), 8)                              # -> 1.000
all_to_0 = torch.zeros(8, dtype=torch.long)
load_balancing_loss(F.one_hot(all_to_0, 8).float(), all_to_0, 8)                 # -> 8.000
```
**Notes**
- Shapes: `top1` is `(T,)` long. `one_hot` gives `(T, N)` (int64, hence `.float()`). `.mean(0)` gives `(N,)` = $f$. `probs (T,N)` → `.mean(0)` gives `(N,)` = $P$.
- With top-2 routing, $f$ counts only the **first** choice (`top1`).
- The function returns the loss **without α**; `train_model` multiplies by α.

**Common mistakes:** `mean(1)` instead of `mean(0)` (that averages over experts, not tokens); using `gates` instead of `probs` for $P$; forgetting the factor $N$, which moves the minimum from 1 to $1/N$.

### ★★★ D. `dropped_fraction` — capacity overflow (TODO BLANK — Task 4)
```python
def dropped_fraction(routing, n_experts, capacity_factor):
    dropped, total = 0, 0
    for r in routing:                                                    # one batch at a time   # <-- KEY
        T, k = r.shape
        capacity = int(capacity_factor * T * k / n_experts)                                     # <-- KEY  floor
        counts = torch.bincount(r.flatten(), minlength=n_experts)        # assignments per expert # <-- KEY
        dropped += (counts - capacity).clamp(min=0).sum().item()                                # <-- KEY
        total += r.numel()                                                                      # T*k assignments
    return dropped / total

toy = [torch.tensor([[0], [0], [0], [1], [2], [2]])]
dropped_fraction(toy, 3, 1.0)                                                    # -> 0.167
```
**Notes**
- `r` is `(T, k)`, and `r.flatten()` is `(T·k,)`. It counts **all** k assignments, not just the first choice.
- `minlength=n_experts` makes sure unused experts still get a 0 entry (length N).
- `clamp(min=0)` keeps only the overflow beyond capacity; under-full experts count as 0.
- Capacity is a **per-batch** buffer, so the computation is batch by batch.

**Common mistakes:** pooling the whole test set into one count; using `ceil` (the notebook uses `int` = floor); dividing by T instead of T·k.

### ★★★ E. `SwitchRouter` (TODO BLANK — Task 2)
```python
class SwitchRouter(nn.Module):
    def __init__(self, d_model, n_experts):
        super().__init__()
        self.w_gate = nn.Linear(d_model, n_experts, bias=False)
        self.k, self.n_experts = 1, n_experts

    def forward(self, x):
        probs   = F.softmax(self.w_gate(x), dim=-1)                      # over ALL experts, no noise    # <-- KEY
        top_idx = probs.argmax(dim=-1, keepdim=True)                     # (T, 1)                        # <-- KEY
        gates   = torch.zeros_like(probs).scatter(-1, top_idx, probs.gather(-1, top_idx))               # <-- KEY
        return gates, top_idx, probs
```
**Notes**
- `keepdim=True` keeps `top_idx` at `(T, 1)`, not `(T,)`. That is required so that `top_idx[:, 0]` and `scatter` work and `MoELayer` is unchanged.
- `probs.gather(-1, top_idx)` gives `(T, 1)`: the chosen expert's probability. `scatter` places it into a zero `(T, N)` tensor. The gate value is $p_{i^*}<1$, so the gradient flows.

**Common mistake:** using `F.softmax(kept)` as in the noisy router. That makes the gate 1 again, the same dead-router trap as noisy top-1.

### ★★ F. Where the MoE sits: `Expert` + `TinyTransformerClassifier.forward` (GIVEN in Setup)
```python
class Expert(nn.Module):
    def __init__(self, d_model, d_hidden):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_model, d_hidden), nn.ReLU(), nn.Linear(d_hidden, d_model))
    def forward(self, x):
        return self.net(x)

class TinyTransformerClassifier(nn.Module):   # __init__: emb, pos, attn (4 heads), ln1, ln2, ffn, out
    def forward(self, X):
        mask = X != 0
        x = self.emb(X) + self.pos(torch.arange(X.shape[1]))
        a = self.ln1(x)
        x = x + self.attn(a, a, a, key_padding_mask=~mask, need_weights=False)[0]   # pre-LN attention + residual
        tokens = self.ln2(x)[mask]                 # (T, D_MODEL): real tokens only, row by row
        y = torch.zeros_like(x)
        y[mask] = self.ffn(tokens)                 # ffn = Expert (dense) OR MoELayer
        x = x + y                                  # residual connection around the ffn
        return self.out((x * mask.unsqueeze(-1)).sum(1) / mask.sum(1, keepdim=True))
```
- The block is **pre-LN**: LN → attention → +residual, then LN → FFN/MoE → +residual. The MoE **replaces the FFN** only.
- `nn.MultiheadAttention(D_MODEL, num_heads=4, batch_first=True)` returns `(attn_output, attn_weights)`, hence `[0]`. `key_padding_mask` uses True for positions to **ignore**, so pass `~mask`.
- `nn.Embedding(vocab_size, D_MODEL, padding_idx=0)` gives the pad row a zero gradient. `self.pos` is a learned positional embedding.
- A dropped token (Task 4) keeps `x` from attention via the residual.

### ★★ G. Router-moved measurement + `usage` (TODO BLANK — Task 2)
```python
def usage(routing):
    first = torch.cat(routing)[:, 0].numpy()                             # first-choice expert per token
    return np.bincount(first, minlength=N_EXPERTS) / len(first)

def noisy_moe(k):
    return lambda: MoELayer(D_MODEL, D_HIDDEN, N_EXPERTS, NoisyTopKRouter(D_MODEL, N_EXPERTS, k=k))

def build_and_train(make_ffn, label, alpha=0.0):
    model = make_model(make_ffn, seed=42)
    W0 = model.ffn.router.w_gate.weight.detach().clone()                 # BEFORE training   # <-- KEY
    train_model(model, alpha=alpha)
    moved = (model.ffn.router.w_gate.weight.detach() - W0).norm().item() # Frobenius norm    # <-- KEY
    return model, moved
```
- `make_model` expects a **factory** (`make_ffn()` is called inside), hence `lambda:` and `switch_moe` passed without parentheses.
- Without `.clone()`, `W0` shares memory with the weight and gets updated in place, so "moved" = 0 for every router.
- `nn.Linear.weight` has shape `(out, in) = (N, D) = (8, 64)`.

### ★★ H. Tutorial `MixtureOfExperts` (dense soft gate / top-1)
```python
class MixtureOfExperts(nn.Module):
    def __init__(self, n_experts=4, top1=False):
        super().__init__()
        self.experts = nn.ModuleList([nn.Linear(2, 2) for _ in range(n_experts)])  # 4 linear experts
        self.gate    = nn.Linear(2, n_experts)                                    # the router
        self.top1    = top1

    def forward(self, x):
        G = F.softmax(self.gate(x), dim=-1)                  # (n, 4): how much to trust each expert
        if self.top1:                                        # keep ONLY the winner
            G = G * F.one_hot(G.argmax(-1), G.shape[1])
        outputs = torch.stack([e(x) for e in self.experts], dim=1)    # (n, 4, 2)
        return (G.unsqueeze(-1) * outputs).sum(dim=1), G     # y = sum_i G_i * E_i(x)
```
- Shapes: `G (n,4)`, then `G.unsqueeze(-1)` is `(n,4,1)`, multiplied with `outputs (n,4,2)` and summed over dim 1 to give `(n,2)`.
- Top-1 keeps the softmax **probability** of the winner, which is not renormalised to 1, so the gate still learns.
- Results: one linear model 0.563, soft MoE 0.915, top-1 0.988; seed 4 collapses to 0.868.
- **Dense, not sparse**: every expert runs.

### ★ I. Task 5 — topic × expert table, consecutive-token agreement (TODO BLANK)
```python
for i, r in enumerate(routing):
    Xb, yb = X_test[i * BATCH:(i + 1) * BATCH], y_test[i * BATCH:(i + 1) * BATCH]
    mask = Xb != 0
    tok_ids.append(Xb[mask])                                             # same row-by-row order as r
    topics.append(torch.repeat_interleave(yb, mask.sum(1)))              # article label per token
    experts.append(r[:, 0])                                              # first choice
    lengths.append(mask.sum(1))
tok_ids, topics, experts, lengths = (torch.cat(a).numpy() for a in (tok_ids, topics, experts, lengths))

table = np.zeros((len(TOPICS), N_EXPERTS))
np.add.at(table, (topics, experts), 1)                                   # unbuffered += (handles repeats)
table /= table.sum(1, keepdims=True)                                     # each row sums to 1

article = np.repeat(np.arange(len(lengths)), lengths)                    # article id of every token
within  = article[1:] == article[:-1]                                    # pair stays inside one article
same    = experts[1:] == experts[:-1]
(same & within).sum() / within.sum()                                     # vs chance (u ** 2).sum()
```
- Use `np.add.at`, not `table[topics, experts] += 1`, because fancy-index `+=` counts duplicate index pairs only once.

### ★ J. Tutorial routing-entropy row
```python
row = np.array([np.sum((cluster == k) & (expert == m)) for m in range(4)])   # n[k, m]
p = row[row > 0] / row.sum()
entropy = abs(-(p * np.log(p)).sum())
```

## 12.5 Fill-in-the-blank practice

**Q1.**
```python
logits = self.w_gate(x)
if self.____:
    logits = logits + torch.____(logits) * F.____(self.w_noise(x))
```
**Q2.**
```python
top_vals, top_idx = logits.____(self.k, dim=-1)
kept  = torch.full_like(logits, float('____')).scatter(-1, ____, ____)
gates = F.softmax(____, dim=-1)
probs = F.softmax(____, dim=-1)
```
**Q3.**
```python
self.experts = nn.____([Expert(d_model, d_hidden) for _ in range(n_experts)])
self.top1 = top_idx[____]
rows = (gates[:, i] > 0).____().squeeze(1)
out  = expert(x[____])
y.____(0, rows, gates[rows, i].____(1) * out)
```
**Q4.**
```python
probs   = F.softmax(self.w_gate(x), dim=-1)
top_idx = probs.argmax(dim=-1, ____=True)
gates   = torch.zeros_like(probs).scatter(-1, top_idx, probs.____(-1, top_idx))
```
**Q5.**
```python
f = F.____(top1, n_experts).float().mean(__)
P = probs.mean(__)
return ____ * (f * P).sum()
```
**Q6.**
```python
capacity = int(____ * T * k / n_experts)
counts = torch.____(r.flatten(), minlength=____)
dropped += (counts - capacity).____(min=0).sum().item()
total += r.____()
```
**Q7.** `W0 = model.ffn.router.w_gate.weight.____().____()`. Why must this run before `train_model`?

**Q8.** `tokens = self.ln2(x)[____]`. What is its shape? What do you pass as `key_padding_mask`, and why?

**Q9 (numeric).** Router logits $[1.0, 3.0, 0.0, 2.0]$ with k = 2. Give `top_idx` and `gates` (to 3 dp).

**Q10 (numeric).** Batch T = 40 tokens, k = 2, N = 8, cf = 1.0. Expert counts (all assignments) are [14, 10, 10, 9, 10, 10, 9, 8]. Find the capacity and the dropped fraction.

**Q11.** Compute $N\sum f_iP_i$ for N = 2, f = [0.75, 0.25], P = [0.6, 0.4].

<details><summary>Answers</summary>

1. `training`; `randn_like`; `softplus`
2. `topk`; `-inf`; `top_idx`, `top_vals`; `kept`; `logits`
3. `ModuleList`; `:, 0`; `nonzero`; `rows`; `index_add_`, `unsqueeze`
4. `keepdim`; `gather`
5. `one_hot`, `0`; `0`; `n_experts`
6. `capacity_factor`; `bincount`, `n_experts`; `clamp`; `numel`
7. `.detach().clone()`. After training it would equal the new weights. Without `clone` the copy aliases the live tensor, so "moved" would be 0.
8. `mask`; the shape is `(T, D_MODEL)`. Pass `~mask`, because in `nn.MultiheadAttention` True means "ignore this key", and padding positions are where `mask` is False.
9. `top_idx = [1, 3]` (best first). KeepTopK = $[-\infty, 3, -\infty, 2]$, so gates = $[0,\ e^3/(e^3+e^2),\ 0,\ e^2/(e^3+e^2)] = [0, 0.731, 0, 0.269]$.
10. capacity = ⌊1.0 · 40 · 2 / 8⌋ = 10. Overflow: expert 0 has 14 − 10 = 4; the rest have 0. Dropped = 4/80 = **0.05**.
11. 2 · (0.75 · 0.6 + 0.25 · 0.4) = 2 · 0.55 = **1.10**. This is above the balanced minimum of 1.

</details>

## 12.6 Quick recall
- **MoE**: $y=\sum_iG(x)_iE_i(x)$. Expert = `Linear(D,H) → ReLU → Linear(H,D)`. The router is a bias-free `Linear(D, N)`.
- **Noisy top-k**: $H=xW_g+\mathcal N(0,1)\cdot\mathrm{softplus}(xW_{noise})$ (training only). `gates = softmax(KeepTopK(H))` has k non-zeros and rows summing to 1. `probs = softmax(H)` covers all experts.
- **KeepTopK one-liner**: `torch.full_like(logits, float('-inf')).scatter(-1, top_idx, top_vals)`.
- **Sparse dispatch**: `rows = (gates[:, i] > 0).nonzero().squeeze(1)`, then `y.index_add_(0, rows, gates[rows, i].unsqueeze(1) * expert(x[rows]))`.
- **Switch**: `probs = softmax(xW_g)`; `top_idx = probs.argmax(-1, keepdim=True)`; gate = `probs.gather(-1, top_idx)`, which is < 1, so the router learns.
- **Noisy top-1 trap**: the gate is ≡ 1, so the gradient to $W_g$ is 0 and the router moved 0.000. Accuracy was still 0.8475, so accuracy alone can't detect a dead router.
- **LB loss**: `N * (one_hot(top1,N).float().mean(0) * probs.mean(0)).sum()`. Balanced = 1, collapsed = N. Gradient only through $P$. α = 0.1 dropped CV 0.347 → 0.113 at no accuracy cost.
- **Capacity**: `int(cf * T * k / N)` (floor). Overflow = `(bincount(r.flatten(), minlength=N) - cap).clamp(min=0).sum()`, computed **per batch**. Dropped tokens skip the expert and keep the residual. A higher cf means more memory, FLOPs and all-to-all communication, with padded empty slots.
- **Shapes**: tokens `(T,D)`; logits/gates/probs `(T,N)`; top_idx `(T,k)`; top1 `(T,)`; f, P `(N,)`; routing per batch `(T_b,k)`.
- **APIs**:
  - `t.topk(k, dim)` returns `(values, indices)`.
  - `t.scatter(dim, idx, src)` / `t.gather(dim, idx)`.
  - `t.nonzero()` gives `(n, ndim)`.
  - `t.index_add_(dim, idx, src)`.
  - `F.one_hot(long, C)` gives int64, so call `.float()`.
  - `torch.bincount(x, minlength=)`.
  - `t.clamp(min=0)`.
  - `torch.repeat_interleave(x, repeats)`.
  - `nn.ModuleList`.
  - `nn.MultiheadAttention(E, heads, batch_first=True)(q, k, v, key_padding_mask=...)[0]`.
  - `np.add.at`.
- **Gotchas**:
  - Noise only if `self.training`.
  - `keepdim=True` in the Switch argmax.
  - `.clone()` the weights before training.
  - Use `index_add_`, not assignment.
  - Capacity counts all k choices; the LB loss counts the first choice only.
  - Never pair tokens across articles.

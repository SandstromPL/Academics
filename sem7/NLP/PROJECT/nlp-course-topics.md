# Complete Natural Language Processing (NLP) Course Syllabus & Topic List

This document provides a comprehensive overview of all topics covered across the course sources, including both pre-midsem and post-midsem materials.

---

## 1. Foundations of Text Processing & Lexical Analysis

* **Course Overview & Language Complexity**: Introduction to human language understanding, lexical ambiguity, syntactic variation, and deep learning paradigms for NLP.
* **Text Processing & Pipeline**:
  * Tokenization and sentence segmentation strategies.
  * Hyphenation handling and compound word splitting across different languages (e.g., German compound words).
* **Spelling Correction & Edit Distance**:
  * Minimum edit distance algorithm (Levenshtein distance).
  * Weighted edit distance using confusion matrices (insertion, deletion, substitution, transposition costs).
  * Metathesis (transpositions) and context-sensitive spelling correction.

---

## 2. Statistical Language Modeling

* **N-gram Language Models**:
  * Markov assumption ($k$-th order approximation).
  * Probability calculation using Maximum Likelihood Estimation (MLE) with count-and-divide formulas.
  * Joint sentence probability estimation via the chain rule.
* **Model Evaluation & Smoothing Techniques**:
  * Training set vs. test set evaluation.
  * Perplexity as an evaluation metric.
  * The zero-probability problem on unseen sequences.
  * **Laplace (Add-1) Smoothing** and **Add-$k$ (Delta) Smoothing** for probability mass redistribution.

---

## 3. Distributed Word Representations & Neural Classifiers

* **Word Embeddings (Word2Vec)**:
  * Distributional semantics hypothesis ("You shall know a word by the company it keeps").
  * Skip-Gram and Continuous Bag of Words (CBOW) model architectures.
  * Objective functions, gradient derivations via the chain rule, and Stochastic Gradient Descent (SGD).
  * Negative sampling and Noise Contrastive Estimation (NCE).
* **Global Vectors for Word Representation (GloVe)**:
  * Comparing matrix factorization (LSA) vs. local context prediction models.
  * Log-bilinear model formulation and global co-occurrence matrix weighting functions.
* **Word Senses & Neural Classification**:
  * Polysemy and word sense representation (sense embeddings).
  * Transition from linear models (logistic regression) to multi-layer neural network classifiers.

---

## 4. Syntactic Parsing (Constituency & Dependency)

* **Constituency Parsing**:
  * **Context-Free Grammars (CFGs)**: Terminals, non-terminals, start symbols, production rules, and parse trees.
  * **Parsing Algorithms**:
    * Top-down vs. bottom-up search strategies.
    * Chomsky Normal Form (CNF) grammar transformation.
    * **Cocke-Kasami-Younger (CKY)** dynamic programming algorithm.
    * Probabilistic Context-Free Grammars (PCFGs) for resolving syntactic structural ambiguity.
* **Dependency Parsing**:
  * **Grammar & Graph Foundations**: Direct head-dependent relations, typed dependency labels, and formal graph constraints (connectedness, acyclicity, single-head constraint, projectivity).
  * **Transition-Based Parsing**:
    * Shift-Reduce configurations (Stack, Buffer, Arc set).
    * Deterministic sequence actions (Shift, Left-Arc, Right-Arc).
    * Feature extraction vectors and transition classifiers.
  * **Graph-Based (MST) Parsing**:
    * Maximum Spanning Tree (MST) graph formulation over directed dense graphs.
    * Chu-Liu-Edmonds algorithm.
    * Scoring arc weights using linear feature vectors and inference-based training.
  * **Neural Dependency Parsers**: Transition-based dependency parsing using feed-forward neural networks and dense feature representations.

---

## 5. Sequential Deep Learning Models

* **Recurrent Neural Networks (RNNs)**:
  * Vanilla/Elman RNN architecture and hidden state updating.
  * Language modeling using RNNs.
  * Backpropagation Through Time (BPTT).
* **Advanced Recurrent Architectures**:
  * Exploding and vanishing gradient problems.
  * Gradient clipping strategies.
  * Long Short-Term Memory (**LSTM**) gating mechanisms (input, forget, output gates, cell state).
  * Gated Recurrent Units (**GRUs**).
  * Bidirectional RNNs and Multi-layer (Stacked) RNNs.

---

## 6. Sequence-to-Sequence Models & Attention

* **Neural Machine Translation (NMT)**:
  * Encoder-Decoder paradigm for variable-length sequence mapping.
  * Sequence decoding strategies: Greedy decoding vs. **Beam Search Decoding**.
  * Automatic evaluation metrics: **BLEU (Bilingual Evaluation Understudy)** score with $n$-gram precision and brevity penalty.
* **Attention Mechanism**:
  * Resolving the information bottleneck of fixed-size encoder hidden states.
  * Calculation of attention scores, attention distributions (softmax), and context vectors.
  * Query-to-context and context-to-query alignment dynamics.

---

## 7. Transformers & Pretraining Paradigms

* **Transformer Architecture**:
  * Self-attention mechanism (Query, Key, Value vector projections, Scaled Dot-Product Attention).
  * Multi-Head Attention (MHA) for parallel representation subspaces.
  * Positional encodings (sinusoidal and learned).
  * Masked self-attention, cross-attention, residual connections, and Layer Normalization.
* **Subword Tokenization Algorithms**:
  * Byte-Pair Encoding (BPE), WordPiece, and Unigram language model subword segmentations.
* **Model Pretraining Strategies**:
  * **Decoder-only Models**: Autoregressive language modeling (e.g., **GPT series**).
  * **Encoder-only Models**: Masked language modeling and next sentence prediction (e.g., **BERT**).
  * **Encoder-Decoder Models**: Sequence-to-sequence denoising pretraining (e.g., **T5**, BART).
  * **In-Context Learning**: Zero-shot, one-shot, and few-shot prompting without gradient parameter updates.

---

## 8. Advanced Downstream Applications (Post-Midsem Topics)

* **Question Answering (QA)**:
  * Reading comprehension over single passages (SQuAD benchmark dataset).
  * Span selection prediction (start and end logits).
  * Open-domain textual QA architectures (Retriever-Reader pipelines).
  * Knowledge-based QA and Visual Question Answering (VQA).
* **Coreference Resolution**:
  * Linguistic concepts: Anaphora, cataphora, coreference chains, and mention types (proper, nominal, pronominal).
  * Rule-based algorithms (Hobbs Algorithm for pronoun resolution).
  * Machine learning approaches: Mention-pair models, mention-ranking models, and end-to-end neural coreference systems.

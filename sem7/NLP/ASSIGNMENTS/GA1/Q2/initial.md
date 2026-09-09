# Q2 — Transition-Based Dependency Parser
## Initial Project Plan and Implementation Specification

> **Purpose:** This document is the initial technical plan for Question 2 of the NLP Group Assignment. It defines the required functionality, architecture, implementation stages, data flow, testing strategy, evaluation, and reporting requirements before coding begins.

---

## 1. Assignment Overview

### Question 2: Implement and Train a Transition-Based Dependency Parser

The goal is to build a simple, data-driven dependency parser from scratch.

The parser will:

1. Read dependency-parsed sentences from the Universal Dependencies English-EWT corpus.
2. Convert gold dependency trees into training examples using an oracle.
3. Represent parser configurations using a stack, buffer, and set of dependency arcs.
4. Use the **arc-standard transition system**.
5. Extract a small set of POS-based features from each configuration.
6. Train a **scikit-learn classifier** to predict the next parser transition.
7. Use the trained classifier to parse unseen sentences.
8. Evaluate the parser on the English-EWT development set using **Labeled Attachment Score (LAS)**.
9. Provide clear code, tests, examples, results, and a brief report.

### Source Dataset

The assignment specifies:

- Training: `en_ewt-ud-train.conllu`
- Evaluation: `en_ewt-ud-dev.conllu`
- Dataset: Universal Dependencies English-EWT

Official repository:

`https://github.com/UniversalDependencies/UD_English-EWT.git`

---

# 2. Main Objectives

The implementation should satisfy all three major technical parts of the assignment.

## Part 1 — Data Processing and Oracle Simulation

Implement:

- CoNLL-U file reader
- Sentence representation
- Token representation
- Dependency-tree representation
- Parser configuration
- Arc-standard transitions
- Oracle simulator

The oracle must generate training instances of the form:

```text
(configuration, correct_transition)
```

The oracle uses the gold dependency tree to determine which transition should be taken at every configuration.

---

## Part 2 — Feature Extraction and Model Training

Implement:

- Feature extraction from parser configurations
- Conversion of categorical POS features into classifier-compatible features
- Training dataset generation
- Scikit-learn classifier
- Model training
- Model persistence/loading if useful

Required features:

1. POS tag of the top word on the stack
2. POS tag of the second word on the stack
3. POS tag of the first word in the buffer
4. POS tag of the second word in the buffer

Missing stack/buffer positions must be represented consistently, for example:

```text
<NULL>
```

---

## Part 3 — Parser and Evaluation

Implement:

- Main transition-based parsing loop
- Classifier-driven transition prediction
- Transition validation
- Dependency arc construction
- LAS evaluation
- Example sentence parsing
- Development-set evaluation
- Results reporting

The parser must not use the oracle during prediction.

The oracle is used only to generate supervised training data.

---

# 3. Arc-Standard Transition System

The parser will use three components:

```text
Stack
Buffer
Arcs
```

## Initial Configuration

For a sentence:

```text
The cat sat on the mat.
```

the initial configuration is conceptually:

```text
Stack:
[ROOT]

Buffer:
[The, cat, sat, on, the, mat]

Arcs:
[]
```

The parser repeatedly chooses one transition until parsing is complete.

---

## 3.1 SHIFT

### Operation

Move the first word from the buffer to the top of the stack.

Before:

```text
Stack:  [ROOT]
Buffer: [The, cat, sat, ...]
```

After:

```text
Stack:  [ROOT, The]
Buffer: [cat, sat, ...]
```

### Validity

SHIFT requires at least one item in the buffer.

---

## 3.2 LEFT-ARC(label)

### Operation

The word at the top of the stack becomes the head of the second word on the stack.

The second word is then removed from the stack.

Example:

```text
Stack:
[ROOT, cat, The]
```

Apply:

```text
LEFT-ARC(det)
```

Result:

```text
Arc:
cat -> The [det]

Stack:
[ROOT, cat]
```

### Validity

LEFT-ARC requires at least two stack items.

The implementation must also ensure that the operation does not create an invalid dependency tree.

---

## 3.3 RIGHT-ARC(label)

### Operation

The second word on the stack becomes the head of the word at the top of the stack.

The top word is then removed from the stack.

Example:

```text
Stack:
[ROOT, sat, cat]
```

Apply:

```text
RIGHT-ARC(nsubj)
```

Result:

```text
Arc:
sat -> cat [nsubj]

Stack:
[ROOT, sat]
```

### Validity

RIGHT-ARC requires at least two stack items.

---

# 4. Internal Data Model

The implementation should use simple, explicit data structures.

## 4.1 Token

Each token should contain at least:

```text
id
form
upos
head
deprel
```

Example:

```python
Token(
    id=1,
    form="The",
    upos="DET",
    head=2,
    deprel="det"
)
```

The design may use a dataclass.

---

## 4.2 Sentence

A sentence should contain:

```text
tokens
```

and optionally:

```text
sentence_id
raw_text
```

Example:

```python
Sentence(
    tokens=[...]
)
```

---

## 4.3 Dependency Arc

An arc should represent:

```text
head
dependent
label
```

Example:

```python
Arc(
    head=2,
    dependent=1,
    label="det"
)
```

---

## 4.4 Parser Configuration

A parser configuration should contain:

```text
stack
buffer
arcs
```

Example:

```python
Configuration(
    stack=[ROOT, 2],
    buffer=[3, 4, 5],
    arcs=[...]
)
```

The configuration should be easy to inspect and test.

---

# 5. Project Architecture

The Q2 implementation will be kept in a **separate GitHub repository** from Q1.

Proposed structure:

```text
NLP_Group_Assignment_Q2/
│
├── data/
│   ├── en_ewt-ud-train.conllu
│   └── en_ewt-ud-dev.conllu
│
├── src/
│   ├── __init__.py
│   ├── conllu_parser.py
│   ├── transitions.py
│   ├── oracle.py
│   ├── features.py
│   ├── classifier.py
│   ├── parser.py
│   └── evaluation.py
│
├── tests/
│   ├── test_conllu_parser.py
│   ├── test_transitions.py
│   ├── test_oracle.py
│   ├── test_features.py
│   └── test_parser.py
│
├── outputs/
│   ├── models/
│   └── results/
│
├── main.py
├── requirements.txt
├── README.md
└── initial.md
```

This structure can be adjusted during implementation if a simpler organization is more appropriate.

---

# 6. Module Responsibilities

## `conllu_parser.py`

Responsible for:

- Reading `.conllu` files
- Detecting sentence boundaries
- Ignoring comments appropriately
- Handling CoNLL-U token rows
- Creating Token objects
- Creating Sentence objects
- Extracting:
  - word/form
  - UPOS
  - HEAD
  - DEPREL

The loader should be robust enough to handle standard UD-EWT data.

---

## `transitions.py`

Responsible for:

- Defining transition types
- Applying SHIFT
- Applying LEFT-ARC
- Applying RIGHT-ARC
- Checking transition validity
- Updating parser configurations

Potential abstraction:

```text
Transition
├── SHIFT
├── LEFT-ARC(label)
└── RIGHT-ARC(label)
```

Transition application must be deterministic and testable.

---

## `oracle.py`

Responsible for:

- Looking at a configuration
- Looking at the gold dependency tree
- Determining the correct next transition
- Simulating the complete gold parse
- Producing training instances

Potential interface:

```python
get_oracle_transition(configuration, gold_tree)
```

and:

```python
generate_training_instances(sentence)
```

---

# 7. Oracle Design

The oracle is central to supervised training.

For every configuration:

```text
Current configuration
        +
Gold dependency tree
        ↓
Oracle
        ↓
Correct transition
```

The oracle will continue until the gold tree has been reconstructed.

## Required Oracle Properties

The oracle should:

- Only return valid transitions.
- Respect gold head-dependent relationships.
- Respect dependency labels.
- Avoid removing a node before its required dependents have been attached.
- Produce a complete gold tree.
- Never rely on the machine-learning classifier.

## Oracle Verification

Before training the classifier, we will run the oracle on small manually understandable sentences.

For each sentence we should verify:

```text
Initial configuration
        ↓
Oracle transition
        ↓
New configuration
        ↓
Oracle transition
        ↓
...
        ↓
Final arcs
```

The final arcs should match the gold dependency tree.

This is a mandatory checkpoint before proceeding to model training.

---

# 8. Training Instance Generation

Once the oracle is correct, run it over the training corpus.

Each oracle step creates:

```text
Configuration
      ↓
Feature extraction
      ↓
Feature vector

Configuration
      ↓
Oracle
      ↓
Correct transition
```

Therefore the final training dataset becomes:

```text
X = feature vectors
y = transition labels
```

Example:

```text
S0_POS  S1_POS  B0_POS  B1_POS       Transition
-------------------------------------------------
NOUN    DET     VERB    ADP          RIGHT-ARC(nsubj)
DET     ROOT    NOUN    VERB         SHIFT
VERB    NOUN    ADP     DET          SHIFT
```

We should inspect the generated dataset before training.

Useful statistics:

```text
Number of sentences
Number of configurations
Number of SHIFT examples
Number of LEFT-ARC examples
Number of RIGHT-ARC examples
Number of distinct transition labels
Number of dependency labels
```

---

# 9. Feature Extraction

The assignment requires exactly four basic POS-based features.

## Features

```text
S0 = top stack POS
S1 = second stack POS
B0 = first buffer POS
B1 = second buffer POS
```

If an item does not exist:

```text
<NULL>
```

Example:

```text
Stack:  [ROOT, NOUN]
Buffer: [VERB, ADP, DET]

Features:

S0 = NOUN
S1 = ROOT
B0 = VERB
B1 = ADP
```

Feature extraction must be a pure, predictable function:

```python
extract_features(configuration)
```

It should not modify the configuration.

---

# 10. Feature Encoding

POS tags are categorical.

The classifier therefore needs numerical/categorical encoding.

Preferred initial approach:

```text
Feature dictionary
        ↓
scikit-learn compatible representation
        ↓
Classifier
```

A simple `DictVectorizer` or equivalent one-hot encoding can be used.

Example:

```text
{
    "S0_POS": "NOUN",
    "S1_POS": "DET",
    "B0_POS": "VERB",
    "B1_POS": "ADP"
}
```

This keeps the implementation easy to understand and explain.

---

# 11. Classifier

The assignment requires a scikit-learn classifier.

### Initial model choice

Use a simple, interpretable classifier first, such as:

```text
Logistic Regression
```

Reason:

- appropriate for categorical features
- fast to train
- easy to reproduce
- easy to explain in the report
- satisfies the assignment requirement

We should not optimize the classifier prematurely.

If the resulting LAS is unexpectedly low, alternative classifiers can be evaluated later.

---

# 12. Parser Implementation

The trained parser should receive:

```text
Sentence
```

with words and POS tags.

It creates:

```text
Initial configuration
```

Then repeatedly:

```text
1. Extract features
2. Predict transition
3. Validate transition
4. Apply transition
5. Update configuration
6. Repeat
```

Conceptual pipeline:

```text
Sentence
   ↓
Initial Stack + Buffer
   ↓
Feature Extraction
   ↓
Classifier
   ↓
Predicted Transition
   ↓
Transition Application
   ↓
Updated Configuration
   ↓
Feature Extraction
   ↓
...
   ↓
Predicted Dependency Tree
```

The oracle must NOT be called during this stage.

---

# 13. Transition Prediction and Safety

A classifier may predict a transition that is invalid for the current configuration.

Examples:

```text
SHIFT when buffer is empty
LEFT-ARC when stack has fewer than two items
RIGHT-ARC when stack has fewer than two items
```

The implementation must therefore have a clear strategy for invalid predictions.

Possible approach:

1. Define legal transitions for the current configuration.
2. Obtain classifier probabilities/scores when available.
3. Choose the highest-scoring legal transition.
4. Use a deterministic fallback if necessary.

The exact strategy will be finalized during implementation and documented in the report.

The important requirement is that invalid transitions must not crash the parser or corrupt the tree.

---

# 14. Parsing Completion

The parser should stop only when the dependency tree is complete.

The implementation must avoid:

- infinite loops
- empty-buffer errors
- invalid stack operations
- duplicate heads
- malformed dependency trees

The final output should contain one predicted head and dependency label for each relevant token.

---

# 15. Evaluation — LAS

The primary metric is:

## Labeled Attachment Score

For each token:

```text
Correct if:

predicted_head == gold_head
AND
predicted_deprel == gold_deprel
```

Then:

```text
LAS =
(number of correctly attached labeled tokens)
/
(total evaluated tokens)
× 100
```

The evaluation script should report:

```text
Number of sentences
Number of tokens
Correct labeled attachments
LAS
```

The evaluation must be performed on:

```text
en_ewt-ud-dev.conllu
```

---

# 16. Example Test Sentences

The assignment provides these sentences for testing:

### Example 1

```text
The cat sat on the mat.
```

### Example 2

```text
She eats a green salad.
```

### Example 3

```text
I saw the man with a telescope.
```

For each example, the program should display:

- tokens
- POS tags
- predicted heads
- predicted dependency labels
- dependency arcs

Example output format:

```text
Sentence: The cat sat on the mat.

ID   WORD   POS    HEAD   DEPREL
1    The    DET    2      det
2    cat    NOUN   3      nsubj
3    sat    VERB   0      root
...
```

The exact predicted result will depend on the trained model.

---

# 17. Testing Strategy

Testing will be done in layers.

## Test Level 1 — Data Parser

Verify:

- sentences are separated correctly
- token IDs are parsed correctly
- words are preserved
- UPOS is correct
- HEAD is parsed correctly
- DEPREL is parsed correctly

---

## Test Level 2 — Individual Transitions

Manually test:

```text
SHIFT
LEFT-ARC
RIGHT-ARC
```

Check both:

- stack/buffer changes
- arc creation

---

## Test Level 3 — Oracle

For small sentences:

```text
Gold tree
   ↓
Oracle
   ↓
Transitions
   ↓
Final arcs
```

Verify that final arcs equal the gold arcs.

---

## Test Level 4 — Feature Extraction

Check configurations such as:

```text
Stack: [ROOT]
Buffer: [The, cat]
```

Expected:

```text
S0 = ROOT
S1 = <NULL>
B0 = DET
B1 = NOUN
```

---

## Test Level 5 — Training Dataset

Verify:

- feature count
- label count
- no missing labels
- no malformed feature records
- expected transition types

---

## Test Level 6 — End-to-End Parser

Train on a small subset first.

Then parse:

```text
The cat sat on the mat.
```

Check that:

- parser terminates
- no invalid transitions crash it
- arcs are produced

---

## Test Level 7 — Development Evaluation

Run the complete model on the development set and calculate LAS.

---

# 18. Development Workflow

Implementation should happen in the following order.

## Phase 1 — Repository Setup

Tasks:

- Create separate Q2 GitHub repository.
- Add README.
- Add `initial.md`.
- Add `.gitignore`.
- Add `requirements.txt`.
- Create source/test directories.

---

## Phase 2 — Dataset

Tasks:

- Clone/download UD English-EWT.
- Place or reference train/dev files.
- Verify dataset availability.
- Inspect several sentences.

---

## Phase 3 — CoNLL-U Parser

Tasks:

- Implement token structure.
- Implement sentence structure.
- Implement `.conllu` reader.
- Test against actual EWT data.

**Checkpoint:** data can be loaded reliably.

---

## Phase 4 — Transition System

Tasks:

- Implement configuration.
- Implement SHIFT.
- Implement LEFT-ARC.
- Implement RIGHT-ARC.
- Implement transition validation.

**Checkpoint:** individual transitions work correctly.

---

## Phase 5 — Oracle

Tasks:

- Implement oracle decision logic.
- Generate gold transitions.
- Test complete oracle simulation.
- Compare final oracle-generated arcs with gold arcs.

**Checkpoint:** oracle reproduces gold trees.

---

## Phase 6 — Features

Tasks:

- Implement four required POS features.
- Handle missing stack/buffer positions.
- Encode features for scikit-learn.
- Test feature extraction.

**Checkpoint:** configurations become correct feature vectors.

---

## Phase 7 — Training

Tasks:

- Generate training examples from the training corpus.
- Inspect training statistics.
- Train classifier.
- Save model/vectorizer if appropriate.

**Checkpoint:** classifier can predict transition labels.

---

## Phase 8 — Parser

Tasks:

- Implement inference-time configuration.
- Extract features.
- Predict transition.
- Apply legal transition.
- Continue until completion.
- Return predicted arcs.

**Checkpoint:** parser can parse unseen sentences.

---

## Phase 9 — Evaluation

Tasks:

- Implement LAS.
- Run development set.
- Generate final metrics.
- Test example sentences.
- Investigate errors.

**Checkpoint:** reproducible final LAS result.

---

## Phase 10 — Documentation

Tasks:

- Complete README.
- Document architecture.
- Document oracle.
- Document feature design.
- Document classifier.
- Document LAS.
- Record final results.
- Write brief report.

---

# 19. Reproducibility

The project should produce reproducible results wherever possible.

Set:

- classifier random seed
- sampling/randomization seed where applicable

Record:

```text
Python version
scikit-learn version
NLTK version if used
Dataset/version
Classifier
Classifier parameters
Random seed
Training data size
Development data size
Final LAS
```

The README should include setup and execution commands.

---

# 20. Expected Command-Line Interface

A simple CLI is preferred.

Possible commands:

```bash
python main.py
```

or:

```bash
python main.py --train
python main.py --evaluate
python main.py --sentence "The cat sat on the mat."
```

The exact CLI will be decided during implementation.

The minimum requirement is that a fresh clone can train/evaluate the parser without manually editing source code.

---

# 21. Output and Results

The project should save useful outputs where appropriate.

Possible structure:

```text
outputs/
├── models/
│   ├── transition_classifier.pkl
│   └── feature_vectorizer.pkl
│
└── results/
    ├── evaluation.txt
    └── example_predictions.txt
```

Generated model files do not necessarily need to be committed to GitHub if they are large. The README should explain how to regenerate them.

---

# 22. Error Analysis

Although LAS is the required metric, we should perform some additional analysis to understand the parser.

Potential analysis:

- Most frequent dependency-label errors
- Most frequent incorrect heads
- Common transition prediction mistakes
- Performance on short vs. long sentences
- Effect of the limited POS-only feature set
- Examples of successful and failed parses

This analysis can be used in the final report.

---

# 23. Design Principles

The implementation should follow these principles.

### 1. Assignment-first

Implement what the assignment requires before adding optional enhancements.

### 2. Modular

Each major component should have one clear responsibility.

### 3. Testable

Core operations such as transitions and oracle decisions should be testable independently.

### 4. Reproducible

Another student should be able to clone the repository and reproduce the results.

### 5. Explainable

The implementation should be easy to explain during a viva/demo.

### 6. No unnecessary complexity

The assignment asks for a simple data-driven transition parser. We should not introduce neural networks, embeddings, beam search, or complicated feature engineering unless there is a specific reason to do so.

---

# 24. Q1 Code Reuse Policy

Q2 will remain a separate repository.

Q1 code may be reused only where it provides a genuinely useful general utility or implementation pattern.

Examples of acceptable reuse:

- coding conventions
- general corpus-loading patterns
- common helper functions
- dependency/setup configuration

Q2 should NOT become dependent on the Q1 repository.

The Q2 repository must be independently runnable.

Because Q2 uses a different corpus and parsing task, Q1's segmentation/POS model is not required for the Q2 parser.

---

# 25. Final Deliverables Checklist

Before submission, verify:

### Code

- [ ] CoNLL-U parser
- [ ] Token/sentence data structures
- [ ] Parser configuration
- [ ] SHIFT
- [ ] LEFT-ARC
- [ ] RIGHT-ARC
- [ ] Oracle
- [ ] Training-instance generation
- [ ] Four required POS features
- [ ] Feature encoding
- [ ] Scikit-learn classifier
- [ ] Main parser
- [ ] LAS evaluation

### Dataset

- [ ] English-EWT training data
- [ ] English-EWT development data

### Testing

- [ ] Unit tests for data parser
- [ ] Transition tests
- [ ] Oracle tests
- [ ] Feature tests
- [ ] End-to-end example tests

### Evaluation

- [ ] LAS on development set
- [ ] Three assignment example sentences
- [ ] Results recorded

### Documentation

- [ ] README
- [ ] Initial project plan
- [ ] Architecture explanation
- [ ] Oracle explanation
- [ ] Feature explanation
- [ ] Classifier explanation
- [ ] LAS explanation
- [ ] Final LAS result
- [ ] Brief report/design discussion

---

# 26. Definition of Done

Q2 will be considered complete when:

```text
UD-EWT train data
        ↓
CoNLL-U parser
        ↓
Gold dependency trees
        ↓
Oracle simulation
        ↓
Training configurations
        ↓
4 POS features
        ↓
Scikit-learn classifier
        ↓
Predicted transitions
        ↓
Arc-standard parser
        ↓
Predicted dependency trees
        ↓
LAS evaluation on EWT dev
```

and the complete pipeline can be run from a clean checkout of the separate Q2 repository.

The final implementation should also satisfy the assignment's requested code-quality and report requirement: well-structured, commented code plus a brief explanation of design choices and the final LAS score.

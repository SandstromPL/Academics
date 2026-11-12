# CLAUDE.md: Indian Address Parser (Group 10 NLP project)

Instructions for Claude Code and for teammates working in this folder. Keep this file short; the details live in the other docs.

## The project in brief
Course project for DSL504 / DS504 Natural Language Processing (IIT Bhilai, Jul–Nov 2026), Group 10:
Agastya Nath, Y. Rahul Dev Reddy, Paritosh Lahre, Varun Rao.

We tag the parts of messy Indian addresses (house, building, street, landmark, locality, city, district, state, PIN) and normalise them against the India Post PIN directory.

    flat 3b, shanti apts, behind SBI atm nr hanuman mandir, supela bhilai 490023

**Research focus:** parsers trained on clean synthetic addresses collapse on real, human-written ones. We measure that gap on a new human-written test set and test which kinds of synthetic noise, and how many real examples, close it.

## Files in this folder
| File | What it holds | Update it when |
|---|---|---|
| `CLAUDE.md` | Rules and conventions (this file) | A convention changes |
| `initials.md` | The plan: problem, research questions, label schema, data, models, experiments, timeline, open decisions, decision log | A plan or decision changes (also add a row to its §13 decision log) |
| `research.md` | Prior work, existing models and datasets, how we differ | You find relevant new work |
| `resources.md` | Every external link (datasets, models, papers, tools) with licence and date checked | You use or cite any new link |
| `logs.md` | Dated work log + table of every training/eval run | End of every work session, and after every run |

**Before any task:** read `logs.md` (latest status), then `initials.md` and `research.md`.

## Status (10 Nov 2026)
Planning only. No code, data or results yet. Next step: Phase 1 in `initials.md` §10.

## Ground rules
1. **Privacy.** Never collect, store or commit real residential addresses, people's names or phone numbers. Real data = addresses of public places only (shops, temples, schools, hospitals, offices). The generator does not need fake names or phones either; leave them out.
2. **Frozen test set.** Once the real test set is annotated, never train, tune or adjust prompts on it. Make every decision on the real dev split. Run the test set only for final runs.
3. **Real numbers only.** Every number in the report or slides must come from a file in `results/` and a row in the `logs.md` run table. Never estimate, round up or invent a result. If a run fails, log it as failed.
4. **Headline = real test set.** Synthetic test scores are near 99% and say little (`research.md` §1). Report them only to show the gap.
5. **Reproducibility.** Fix seeds; run the main models with 3 seeds and report mean ± std; save the config next to each result.
6. **Licences.** Attribute India Post data (GODL-India) and OpenStreetMap (ODbL). Check a model's or dataset's licence before redistributing it.
7. **Ask first** before downloading more than 2 GB, starting a job longer than 1 hour, or using a paid API.
8. **Keep the docs current.** After each session: add an entry to `logs.md`; add new links to `resources.md`; record changed decisions in `initials.md` §13. Cite sources in `research.md` only after opening them.

## Conventions
### Data format (JSONL, one address per line)
```json
{"id": "real-0042", "text": "flat 3b, shanti apts, ...", "tokens": ["flat", "3b", ","],
 "tags": ["B-HOUSE", "I-HOUSE", "O"], "source": "synthetic", "noise": ["abbrev", "landmark"], "split": "train"}
```
- `source` is `synthetic` or `real`; `split` is `train`, `dev` or `test`.
- Tags are BIO (IOB2) over word and punctuation tokens. Transformer code aligns them to subwords: label the first subword and ignore the rest (`-100`).
- Labels: `HOUSE BUILDING STREET LANDMARK LOCALITY CITY DISTRICT STATE PIN`. Definitions and edge cases are in `initials.md` §4.

### Folder layout (create folders as needed)
```
data/raw/          downloads (gitignored)
data/gazetteer/    cleaned PIN directory and place-name lists
data/synthetic/    generated train/dev JSONL, one folder per generator config
data/real/         human-written dev/test JSONL + GUIDELINES.md (annotation rules)
src/generate/      generator; one function per noise family (N1–N8)
src/models/        rules, crf, transformer, llm
src/normalize/     PIN / gazetteer normalisation
src/eval/          span F1 (seqeval), field accuracy, bootstrap CIs
notebooks/         Colab/Kaggle training notebooks
results/           one JSON per run (committed)
app/               demo (Gradio or Streamlit)
report/            report and slides
```

### Stack
Python 3.10+, `transformers`, `datasets`, `seqeval`, `sklearn-crfsuite`, `pandas`, `torch` (free Colab/Kaggle T4 GPU). Pin exact versions in `requirements.txt` once installed. Main backbones: `google/muril-base-cased` and `FacebookAI/xlm-roberta-base`.

### Run IDs
Use `YYYYMMDD-<model>-<data>-s<seed>`, e.g. `20261114-muril-synfull-s42`. The results file (`results/<run-id>.json`) and the `logs.md` row use the same ID.

## Commands
_Add these as code appears: setup, data generation, training, evaluation, demo._

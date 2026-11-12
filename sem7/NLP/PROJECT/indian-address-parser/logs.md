# Project log

Newest entries first. Add one entry per work session, and one row per training or evaluation run in the run table at the bottom. Keep entries short and factual.

**Entry template**
```
### YYYY-MM-DD: <who>
- Did: …
- Decided: … (also add a row to initials.md §13)
- Results: run IDs from the table below / files in results/
- Problems: …
- Next: …
```

---

### 2026-11-10: Paritosh (with Claude Code)
- **Did:** The group picked project #8 from the shortlist (Indian address parsing). Created this folder with `CLAUDE.md`, `initials.md`, `research.md`, `resources.md` and `logs.md`.
- **Did:** Literature and resource scan (`research.md`, links in `resources.md`). Found:
  - the closest paper (Dhavase & Chaudhary, ETASR 2026), which shows the synthetic→real collapse;
  - six open Indian-address models on Hugging Face;
  - the abr-6024 synthetic dataset;
  - deepparse's zero-shot results for India;
  - the count of OSM India objects with a PIN tag (283,211).
- **Decided:**
  - Research focus: the synthetic→real gap, studied through a noise ablation, a real-data curve and a human-written test set.
  - Label schema v0.1.
  - Real data comes from public-place addresses only.
  - Details in `initials.md` §13.
- **Results:** none yet (no code).
- **Next:**
  - Fill in the deadline at the top of `initials.md` and work through §12 (open decisions).
  - Start Phase 1 (`initials.md` §10): repo setup, clean the PIN directory, annotation guidelines, send the Google Form, generator v1, eval script.
  - Paste the new title and description (`initials.md` §14) into the class sheet.

### 2026-10-22: Paritosh (with Claude Code)
- **Did:** Reviewed all 31 entries in the class sheet (`DOC-20260928-WA0000.xlsx`) to find topics no other group had taken. Shortlisted and ranked 9 ideas; address parsing was #8.
- **Outputs (parent folder):** `Group_10_Project_Shortlist.pdf` (detailed), `Group_10_Project_Shortlist_Brief.pdf` / `.tex`, `Group_10_Project_Shortlist.md`.
- **Also:** reviewed a ChatGPT-generated alternative report (`Group_10_NLP_Project_Analysis_and_Recommendations.pdf`).

### By 28 Sep 2026 (date of the class-sheet copy)
- The group's row in the class sheet held a placeholder: "NLP Modeling – Use NLP for language modeling". Replace it with `initials.md` §14.

---

## Run table
Log every training or evaluation run, including failed ones. Fill the **Test F1** column only for final runs (`CLAUDE.md` rule 2).

| Run ID | Date | Model | Train data | Seed | Dev F1 (micro / macro) | Test F1 | Results file | Notes |
|---|---|---|---|---|---|---|---|---|
| _(none yet)_ | | | | | | | | |

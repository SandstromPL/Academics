"""Baseline vs improved, case by case (plain code, no model calls).

  python3 eval/compare.py eval/results/<baseline run>.json eval/results/<improved run>.json

Writes eval/results/compare-<baseline run id>-vs-<improved run id>.md and prints its path.
headline(result) is the one-line summary used in EVIDENCE.md and on slide 6.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def load(path):
    with open(path) as f:
        return json.load(f)


def headline(d):
    s = d["summary"]
    text = (f"fully migrated {s['fully_migrated']}/{s['cases']}, calls {s['calls_total']} "
            f"({s['calls_per_file']}/file), tokens {s['tokens_total']} ({s['tokens_per_file']}/file)")
    if s["retrieval_hit_rate"] is not None:
        text += f", retrieval hit rate {s['retrieval_hit_rate']}"
    return text


def cell(c):
    done = "yes" if c["fully_migrated"] else "no"
    return f"{done} ({c['calls']} calls, {c['tokens']} tokens, {c['stop_reason']})"


def change(b, i):
    if b["fully_migrated"] and not i["fully_migrated"]:
        return "REGRESSION"
    if i["fully_migrated"] and not b["fully_migrated"]:
        return "fixed"
    return "same"


def denied(c):
    return ", ".join(c["gate_denied_paths"]) or "-"


def compare(base, imp):
    if base["variant"] != "baseline" or imp["variant"] != "improved":
        raise SystemExit("give the baseline result file first, then the improved one")
    bc = {c["case_id"]: c for c in base["cases"]}
    ic = {c["case_id"]: c for c in imp["cases"]}
    if sorted(bc) != sorted(ic):
        raise SystemExit(f"the runs have different cases: {sorted(bc)} vs {sorted(ic)}")
    sb, si = base["summary"], imp["summary"]
    hit = si["retrieval_hit_rate"] if si["retrieval_hit_rate"] is not None else "n/a"
    out = [f"# Baseline vs improved: {base['run_id']} vs {imp['run_id']}", "",
           f"- Baseline: `{base['run_id']}` by {base['member']}, model `{base['model']}`, "
           f"{base['started_utc']} to {base['ended_utc']}, trace `{base['trace']}`",
           f"- Improved: `{imp['run_id']}` by {imp['member']}, model `{imp['model']}`, "
           f"{imp['started_utc']} to {imp['ended_utc']}, trace `{imp['trace']}`", "",
           "## Headline", "",
           "| Metric | Baseline | Improved |",
           "|---|---|---|",
           f"| Files fully migrated (tests green and 0 v1 leftovers) | {sb['fully_migrated']}/{sb['cases']} "
           f"| {si['fully_migrated']}/{si['cases']} |",
           f"| Tests green | {sb['tests_green']}/{sb['cases']} | {si['tests_green']}/{si['cases']} |",
           f"| Zero v1 leftovers | {sb['zero_leftovers']}/{sb['cases']} | {si['zero_leftovers']}/{si['cases']} |",
           f"| Model calls | {sb['calls_total']} | {si['calls_total']} |",
           f"| Calls per file | {sb['calls_per_file']} | {si['calls_per_file']} |",
           f"| Tokens | {sb['tokens_total']} | {si['tokens_total']} |",
           f"| Tokens per file | {sb['tokens_per_file']} | {si['tokens_per_file']} |",
           f"| Retrieval hit rate | n/a | {hit} |", "",
           "## Case by case", "",
           "| Case | Kind | Needed sections | Baseline | Improved | Change | Retrieved (improved) |",
           "|---|---|---|---|---|---|---|"]
    for cid in sorted(bc):
        b, i = bc[cid], ic[cid]
        out.append(f"| {cid} | {b['kind']} | {', '.join(b['needed_sections'])} | {cell(b)} | {cell(i)} "
                   f"| {change(b, i)} | {', '.join(i['retrieved_ids']) or '-'} |")
    regress = [cid for cid in sorted(bc) if change(bc[cid], ic[cid]) == "REGRESSION"]
    fixed = [cid for cid in sorted(bc) if change(bc[cid], ic[cid]) == "fixed"]
    out += ["", "## Regressions", ""]
    for cid in regress:
        why = (ic[cid]["first_failure"] or ic[cid]["stop_reason"]).strip().splitlines()[0][:120]
        out.append(f"- {cid}: baseline migrated it, improved did not ({why})")
    if not regress:
        out.append("None: every file the baseline migrated, the improved variant migrated too.")
    out += ["", f"Fixed by the guide: {', '.join(fixed) or 'none'}.", "",
            "## Safety gate (denied writes)", ""]
    gated = [cid for cid in sorted(bc) if bc[cid]["gate_denied_paths"] or ic[cid]["gate_denied_paths"]]
    if gated:
        out += ["| Case | Baseline | Improved |", "|---|---|---|"]
        out += [f"| {cid} | {denied(bc[cid])} | {denied(ic[cid])} |" for cid in gated]
    else:
        out.append("No write was denied in either run.")
    tb, ti = sb["tokens_per_file"], si["tokens_per_file"]
    pct = round((ti - tb) / tb * 100, 1) if tb else 0.0
    out += ["", "## Token cost", "",
            f"Improved used {ti} tokens per file against {tb} for baseline ({pct:+.1f}%), and "
            f"{si['calls_per_file']} calls per file against {sb['calls_per_file']}.", ""]
    return "\n".join(out)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        raise SystemExit("usage: python3 eval/compare.py <baseline result.json> <improved result.json>")
    base, imp = load(argv[0]), load(argv[1])
    text = compare(base, imp)
    path = os.path.join("eval", "results", f"compare-{base['run_id']}-vs-{imp['run_id']}.md")
    with open(os.path.join(ROOT, path), "w") as f:
        f.write(text)
    print(path)
    return path


if __name__ == "__main__":
    main()

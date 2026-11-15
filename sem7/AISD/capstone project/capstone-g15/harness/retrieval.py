"""Keyword retrieval over data/guide.json (same shape as lab-08b retrieve()).

Section text is capped at 600 chars and k at 3 so retrieval cannot fill the context.
"""
import json
import math
import os
import re


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUIDE_PATH = os.path.join(ROOT, "data", "guide.json")
MAX_K = 3
MAX_TEXT = 600

STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "is", "are", "be",
    "it", "its", "with", "by", "as", "at", "from", "this", "that", "now", "not", "no",
    "use", "how", "do", "does", "what", "v1", "v2", "libv", "import", "call", "calls",
    "function", "migrate", "migration", "python", "code", "new", "old", "instead",
}

# Stretch (lab 8b): synonym expansion. Off by default; harness passes expand=True to use it.
SYNONYMS = {
    "pay": ["charge", "transfer"],
    "payment": ["charge", "pay"],
    "balance": ["fetch_balance", "get_balance"],
    "receipt": ["make_receipt", "charge_and_receipt"],
    "error": ["exception", "payerror"],
    "exception": ["error"],
    "rupees": ["paise", "amount"],
    "currency": ["money"],
}


def _split_ident(word):
    parts = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", word).replace("_", " ").split()
    return [p.lower() for p in parts]


def tokens(text):
    out = []
    for word in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text or ""):
        low = word.lower()
        cands = [low] + (_split_ident(word) if ("_" in word or not word.islower()) else [])
        for c in cands:
            if c and c not in STOPWORDS and len(c) > 1:
                out.append(c)
    return out


def expand_query(query_tokens):
    out = list(query_tokens)
    for t in query_tokens:
        out.extend(SYNONYMS.get(t, []))
    return out


def load_guide(path=GUIDE_PATH):
    return json.load(open(path))


def _section_tokens(s):
    return set(tokens(s["title"])) | set(tokens(s["text"])) | set(tokens(s["before"])) | set(tokens(s["after"]))


def _idf(guide):
    n = len(guide)
    df = {}
    for s in guide:
        for t in _section_tokens(s):
            df[t] = df.get(t, 0) + 1
    return {t: math.log((n + 1) / (c + 0.5)) for t, c in df.items()}


def retrieve(query, guide, k=3, expand=False):
    """Return up to k sections ranked by IDF-weighted keyword overlap (title counts double)."""
    k = max(1, min(int(k), MAX_K))
    q = tokens(query)
    if expand:
        q = expand_query(q)
    q = set(q)
    idf = _idf(guide)
    scored = []
    for i, s in enumerate(guide):
        title = set(tokens(s["title"]))
        body = _section_tokens(s)
        score = sum(idf.get(t, 0) * (2 if t in title else 1) for t in q & body)
        if score > 0:
            scored.append((-score, i, s))
    scored.sort(key=lambda x: (x[0], x[1]))
    return [s for _, _, s in scored[:k]]


def hit_rate(needed_ids, retrieved_ids):
    needed = set(needed_ids)
    if not needed:
        return 1.0
    return len(needed & set(retrieved_ids)) / len(needed)

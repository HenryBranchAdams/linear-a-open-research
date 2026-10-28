#!/usr/bin/env python3
"""Offline descriptive exact-packet and variant screen of inherited SigLA indexing.

No external dependencies; no word, identity, role, chronology or null-model inference.
Run from any directory. Outputs are regenerated deterministically (no timestamp).
"""
from __future__ import annotations

import collections
import copy
import csv
import hashlib
import itertools
import json
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[3]
SOURCE = ROOT / "corpus/sigla_sequences_2026-09-07.json"
OUT = pathlib.Path(__file__).resolve().parents[1] / "results"
ACCOUNTING = {"KU-RO", "KI-RO"}
PACKET_GENERIC = ACCOUNTING | {"A-DU", "SA-RA2"}
SYLLABLE = re.compile(r"(?:A|E|I|O|U|AU|NWA|[DKMNPQRSTWZJ][AEIOU]|RA2|TA2|PU2)$")
# These sign numbers can function as non-phonetic classifiers. Rejecting an
# entire sequence is deliberately conservative; it cannot rule out lexical use.
UNKNOWN_SYLLABLE = re.compile(r"(?:\*(?:[1-9]|[1-9][0-9])|A3[0-9]{2}[A-C]?)$")


def classify(seq):
    form, signs = seq["form"], seq["signs"]
    if any(c in form for c in "[]?+"):
        return "broken_or_nonlexical_syntax"
    if len(signs) < 2:
        return "less_than_two_signs"
    if form != "-".join(signs):
        return "form_sign_mismatch"
    if any(c != "sure-reading" for c in seq["reading_classes"]):
        return "uncertain_reading"
    if len(signs) != len(seq["reading_classes"]):
        return "reading_class_count_mismatch"
    if form in ACCOUNTING:
        return "accounting_marker"
    if all(SYLLABLE.fullmatch(t) for t in signs):
        return "phonetic"
    if all(SYLLABLE.fullmatch(t) or UNKNOWN_SYLLABLE.fullmatch(t) for t in signs):
        return "opaque_sign_extended"
    return "possible_logogram_fraction_or_composite"


def initial_object(face):
    # Only documented typographic face suffix shapes are normalized. Uppercase
    # catalog subdivisions remain distinct (e.g. HT 154A), not silently merged.
    name = face.lstrip("`")
    name = re.sub(r"-latus$", "", name)
    name = re.sub(r"(?<=[0-9A-Z])[a-dαβγδ](?=>?$)", "", name)
    return name


def make_objects(docs):
    raw = {d["document_face"]: initial_object(d["document_face"]) for d in docs}
    aliases = {}
    # A joined fragment and its separately catalogued fragment are not treated
    # as independent objects. Present example: KH 79 and KH 79+89.
    for obj in sorted(set(raw.values())):
        if "+" not in obj:
            continue
        m = re.fullmatch(r"(.*? )(\d+(?:\+\d+)+)", obj)
        if m:
            for n in m.group(2).split("+"):
                aliases[m.group(1) + n] = obj
    return {face: aliases.get(obj, obj) for face, obj in raw.items()}


def context_sets(docs, object_map, mode, level):
    accepted = {"phonetic"} if mode == "phonetic" else {"phonetic", "opaque_sign_extended"}
    if mode == "all_complete_audit":
        accepted.add("possible_logogram_fraction_or_composite")
    contexts = collections.defaultdict(set)
    members = collections.defaultdict(list)
    for d in docs:
        key = d["document_face"] if level == "face" else object_map[d["document_face"]]
        contexts[key].update(s["form"] for s in d["sequences"] if classify(s) in accepted)
        members[key].append(d["document_face"])
    return dict(contexts), dict(members)


def site(key):
    return key.lstrip("`").split()[0]


def pair_screen(contexts, object_map, level):
    eligible = {k: v for k, v in contexts.items() if v}
    n = len(eligible)
    df = collections.Counter(w for words in eligible.values() for w in words)
    rows, trivial = [], []
    for a, b in itertools.combinations(sorted(eligible), 2):
        shared = eligible[a] & eligible[b]
        if not shared:
            continue
        same_object = level == "face" and object_map[a] == object_map[b]
        row = {
            "left": a, "right": b, "cross_site": site(a) != site(b),
            "same_object": same_object, "shared_count": len(shared),
            "shared": sorted(shared),
            "rarity_bits": round(sum(math.log2(n / df[w]) for w in shared), 6),
            "jaccard": round(len(shared) / len(eligible[a] | eligible[b]), 6),
            "left_only": sorted(eligible[a] - eligible[b]),
            "right_only": sorted(eligible[b] - eligible[a]),
            "shared_context_frequency": {w: df[w] for w in sorted(shared)},
        }
        (trivial if same_object else rows).append(row)
    order = lambda r: (-r["shared_count"], -r["rarity_bits"], r["left"], r["right"])
    rows.sort(key=order)
    trivial.sort(key=order)
    for i, row in enumerate(rows, 1):
        row["rank"] = i
    return rows, trivial, df


def variant_kind(x, y):
    if x == "A-" + y or y == "A-" + x:
        return "initial_A"
    a, b = x.split("-"), y.split("-")
    if len(a) == len(b) and a[:-1] == b[:-1] and a[-1] != b[-1]:
        return "terminal_syllable"
    return None


def variant_screen(contexts, object_map, level):
    occ = collections.defaultdict(set)
    for c, words in contexts.items():
        for w in words:
            occ[w].add(c)
    n = sum(bool(s) for s in contexts.values())
    rows = []
    # Exhaustive over form pairs, then every cross-object attestation pair.
    for x, y in itertools.combinations(sorted(occ), 2):
        kind = variant_kind(x, y)
        if not kind:
            continue
        seen = set()
        for a, b in itertools.product(sorted(occ[x]), sorted(occ[y])):
            if a == b or (level == "face" and object_map[a] == object_map[b]):
                continue
            stamp = tuple(sorted((a, b)))
            if stamp in seen:
                continue
            seen.add(stamp)
            shared = (contexts[a] & contexts[b]) - {x, y}
            if not shared:
                continue
            left_also_y = y in contexts[a]
            right_also_x = x in contexts[b]
            rows.append({
                "left": a, "right": b, "left_form": x, "right_form": y,
                "kind": kind, "min_target_signs": min(len(x.split("-")), len(y.split("-"))),
                "exclusive_substitution": not left_also_y and not right_also_x,
                "left_also_contains_right_form": left_also_y,
                "right_also_contains_left_form": right_also_x,
                "forms_cooccur_in_any_context": sorted(occ[x] & occ[y]),
                "cross_site": site(a) != site(b),
                "independent_associate_count": len(shared),
                "independent_associates": sorted(shared),
                "associate_rarity_bits": round(sum(math.log2(n / len(occ[w])) for w in shared), 6),
            })
    rows.sort(key=lambda r: (-r["independent_associate_count"], -r["associate_rarity_bits"],
                             r["left"], r["right"], r["left_form"], r["right_form"]))
    return rows


def edit_distance(a, b):
    previous = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        current = [i]
        for j, y in enumerate(b, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (x != y)))
        previous = current
    return previous[-1]


def broad_differing_forms(contexts, pairs):
    """Inspect all unequal long forms in strong packets; no alignment implied."""
    rows = []
    for pair in pairs:
        a, b = pair["left"], pair["right"]
        shared = (contexts[a] & contexts[b]) - PACKET_GENERIC
        if len(shared) < 3:
            continue
        xs = [w for w in contexts[a] - contexts[b] - PACKET_GENERIC if len(w.split("-")) >= 3]
        ys = [w for w in contexts[b] - contexts[a] - PACKET_GENERIC if len(w.split("-")) >= 3]
        for x, y in itertools.product(sorted(xs), sorted(ys)):
            rows.append({"left": a, "right": b, "left_form": x, "right_form": y,
                         "shared_non_generic_count": len(shared), "shared_non_generic": sorted(shared),
                         "sign_edit_distance": edit_distance(x.split("-"), y.split("-")),
                         "warning": "Set-difference candidate only; neither aligned entry nor shared identity established."})
    rows.sort(key=lambda r: (-r["shared_non_generic_count"], r["sign_edit_distance"], r["left"], r["right"], r["left_form"], r["right_form"]))
    return rows


def reading_scenario(docs, correction=False, split=False):
    changed = copy.deepcopy(docs)
    edits = []
    for d in changed:
        seqs = []
        for s in d["sequences"]:
            if correction and d["document_face"] == "HT 95b" and s["form"] == "DA-ZA":
                edits.append({"face": d["document_face"], "before": s["form"], "after": ["DA-ME"]})
                s["form"], s["signs"] = "DA-ME", ["DA", "ME"]
            if split and d["document_face"] == "HT 95a" and s["form"] == "DI-DE-RU-QE-RA2-U":
                forms = ["DI-DE-RU", "QE-RA2-U"]
                edits.append({"face": d["document_face"], "before": s["form"], "after": forms})
                for f in forms:
                    new = copy.deepcopy(s)
                    new["form"], new["signs"] = f, f.split("-")
                    new["reading_classes"] = ["sure-reading"] * len(new["signs"])
                    seqs.append(new)
            else:
                seqs.append(s)
        d["sequences"] = seqs
    return changed, edits


def controls(contexts, rows, df, object_map, level):
    eligible = [c for c, s in contexts.items() if s]
    possible = {"within_site": 0, "cross_site": 0}
    for a, b in itertools.combinations(eligible, 2):
        if level == "face" and object_map[a] == object_map[b]:
            continue
        possible["cross_site" if site(a) != site(b) else "within_site"] += 1
    base = {str(k): {
        group: sum(r["shared_count"] >= k and r["cross_site"] == (group == "cross_site") for r in rows)
        for group in possible} for k in (1, 2, 3, 4, 5)}
    sensitivity = []
    # Stop-list sensitivity is descriptive, not an empirical frequency cutoff
    # learned to maximize a desired match. Ties are kept together.
    for cap in (3, 4, 5, 7):
        excluded = sorted(w for w in df if df[w] > cap)
        reduced = {c: words - set(excluded) for c, words in contexts.items()}
        rr, _, _ = pair_screen(reduced, object_map, level)
        sensitivity.append({"maximum_context_frequency_retained": cap,
                            "excluded_forms": excluded,
                            "pairs_with_at_least_two": sum(r["shared_count"] >= 2 for r in rr),
                            "cross_site_pairs_with_at_least_two": sum(r["shared_count"] >= 2 and r["cross_site"] for r in rr),
                            "top_five": rr[:5]})
    return {"possible_nontrivial_pairs_among_nonempty_contexts": possible,
            "observed_overlap_pairs_by_minimum_shared_count": base,
            "frequency_sensitivity": sensitivity}


def csv_write(path, rows):
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=keys)
        wr.writeheader()
        for row in rows:
            wr.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in row.items()})


def main():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    docs = data["documents"]
    object_map = make_objects(docs)
    counts = collections.Counter(classify(s) for d in docs for s in d["sequences"])
    results = {
        "source_relative_path": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "source_acquired_utc": data["acquired_utc"],
        "source_attribution": data["source"], "source_license": data["license"],
        "method": "Descriptive exact indexed-sequence overlap; no statistical significance, identity, role or wordhood inference.",
        "coverage": {"document_faces": len(docs), "catalog_object_groups": len(set(object_map.values())),
                     "indexed_sequence_occurrences": sum(len(d["sequences"]) for d in docs),
                     "classification_counts": dict(counts)},
        "classification_by_occurrence": [dict(document_face=d["document_face"], **s, classification=classify(s)) for d in docs for s in d["sequences"]],
        "object_map": object_map,
        "runs": {},
    }
    OUT.mkdir(parents=True, exist_ok=True)
    for mode, level in itertools.product(("phonetic", "extended", "all_complete_audit"), ("face", "object")):
        contexts, members = context_sets(docs, object_map, mode, level)
        rows, trivial, df = pair_screen(contexts, object_map, level)
        variants = variant_screen(contexts, object_map, level)
        broad = broad_differing_forms(contexts, rows)
        key = mode + "_" + level
        results["runs"][key] = {
            "total_contexts": len(contexts), "nonempty_contexts": sum(bool(s) for s in contexts.values()),
            "distinct_forms": len(df), "form_context_frequency": dict(sorted(df.items())),
            "context_members": members, "context_forms": {c: sorted(words) for c, words in contexts.items()},
            "ranked_nontrivial_pairs": rows, "same_object_pairs_excluded_from_ranking": trivial,
            "variant_candidates_with_independent_associates": variants,
            "broad_differing_long_forms_in_strong_packets": broad,
            "controls": controls(contexts, rows, df, object_map, level),
        }
        csv_write(OUT / f"corpus_pairs_{key}.csv", rows)
        csv_write(OUT / f"corpus_pairs_variants_{key}.csv", variants)
        csv_write(OUT / f"corpus_pairs_broad_{key}.csv", broad)
    results["reading_sensitivity_scenarios"] = {}
    for scenario, correction, split in (("younger_DA_ME_only", True, False),
                                         ("HT95a_split_only", False, True),
                                         ("younger_DA_ME_and_split", True, True)):
        scenario_docs, edits = reading_scenario(docs, correction, split)
        sr = {"status": "Explicit alternative indexing/reading scenario; frozen source not edited; no original-image adjudication.",
              "source": "Younger GORILA-derived HT95 commentary, retrieved by root; iterations/010/data/source_cache/HT95.html",
              "edits": edits, "runs": {}}
        for level in ("face", "object"):
            contexts, members = context_sets(scenario_docs, object_map, "phonetic", level)
            rows, trivial, df = pair_screen(contexts, object_map, level)
            variants = variant_screen(contexts, object_map, level)
            sr["runs"][level] = {"top_ten_pairs": rows[:10],
                                  "all_variants": variants,
                                  "broad_differing_long_forms_in_strong_packets": broad_differing_forms(contexts, rows)}
        results["reading_sensitivity_scenarios"][scenario] = sr
    (OUT / "corpus_pairs.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"coverage": results["coverage"], "runs": {
        k: {"nonempty_contexts": r["nonempty_contexts"], "distinct_forms": r["distinct_forms"],
            "pair_counts": r["controls"]["observed_overlap_pairs_by_minimum_shared_count"],
            "top_pairs": r["ranked_nontrivial_pairs"][:5],
            "exclusive_variant_count": sum(v["exclusive_substitution"] for v in r["variant_candidates_with_independent_associates"]),
            "exclusive_variant_at_least_three_signs": [v for v in r["variant_candidates_with_independent_associates"] if v["exclusive_substitution"] and v["min_target_signs"] >= 3]}
        for k, r in results["runs"].items()}}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

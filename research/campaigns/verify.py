#!/usr/bin/env python3
"""Preservation, registry and navigation checks through C044.

Run after integration as `python3 verify.py --root PATH`. Earlier verifiers remain
pinned inside their exact archives; they are not applied to this later root.
No source downloads or scientific edits are performed. Optional configured
reproducible-output scripts are rerun as Python programs and must print JSON
without writing files. JSON is printed to stdout; this verifier creates no files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
import zipfile

# These inherited anchors are deliberately not configurable by the current root.
PREVIOUS_REL = "archive/D2026-10-25/Linear_A_Research_Current_through_042.zip"
PREVIOUS_SHA = "98e19e34100098485bafbccfd975b86197e08ffef759c266f9d5c2fe449d5c02"
PREVIOUS_PREFIX = "Linear_A_Research_Current/"
INHERITED_COUNTS = {"claims": 87, "experiments": 37, "sources": 121}
NEW_ITERATIONS = {43, 44}
CORPUS_REL = "corpus/discovery_snapshot.json"
CORPUS_SHA = "9b293509ab0ff928564c924e41f2c7da97e024ff28ac9b196e25cec638a2629b"
C041_REL = "iterations/041/Linear_A_Campaign_041.zip"
C041_SHA = "b8e03e1d5476f1702e060aca8be20b995afd5923851649dae92738744d53598e"
IMMUTABLE_TREE_PREFIXES = (
    "baseline/", "corpus/", "iterations/038/", "iterations/039/",
    "iterations/040/", "iterations/041/", "iterations/042/",
    "phases/2026-10-24/", "reviews/2026-10-23/", "reviews/2026-10-25/",
)
COUNT_KEYS = {
    "claims": "claims",
    "experiments": "experiments_and_access_feasibility_records",
    "sources": "source_access_records",
}
SCOPE = (
    "Preservation, metadata consistency, current evidence-file joins and navigation only; "
    "not source authenticity adjudication, epigraphic reading, autopsy, physical measurement, "
    "assay replication, unused-witness validation, or validation of ancient meaning."
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def record_list(payload, name):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get(name), list):
        return payload[name]
    raise ValueError(f"{name}: expected an array or an object containing that array")


def record_bytes(raw: bytes, name: str):
    """Return exact UTF-8 bytes of each registry object, excluding separators.

    The enclosing authority metadata and the array's appended records may change;
    whitespace, spelling, types and values inside inherited objects may not.
    The complete JSON payload is separately parsed by record_list.
    """
    text = raw.decode("utf-8")
    decoder = json.JSONDecoder()

    def skip_space(index):
        return re.compile(r"\s*").match(text, index).end()

    index = skip_space(0)
    if text[index] == "{":
        index += 1
        while True:
            index = skip_space(index)
            key, end = decoder.raw_decode(text, index)
            index = skip_space(end)
            if text[index] != ":":
                raise ValueError(f"{name}: missing registry-envelope colon")
            index = skip_space(index + 1)
            if key == name:
                break
            _, end = decoder.raw_decode(text, index)
            index = skip_space(end)
            if text[index] != ",":
                raise ValueError(f"{name}: registry array missing from envelope")
            index += 1
    if text[index] != "[":
        raise ValueError(f"{name}: registry record value is not an array")
    index += 1
    rows = []
    while True:
        index = skip_space(index)
        if text[index] == "]":
            return rows
        value, end = decoder.raw_decode(text, index)
        if not isinstance(value, dict):
            raise ValueError(f"{name}: registry record is not an object")
        rows.append(text[index:end].encode("utf-8"))
        index = skip_space(end)
        if text[index] == "]":
            return rows
        if text[index] != ",":
            raise ValueError(f"{name}: missing registry record separator")
        index += 1


def canonical_json(payload):
    """Formatting-independent comparison that preserves JSON value types."""
    return json.dumps(payload, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False)


def inside(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise ValueError(f"empty or non-string portable path: {relative!r}")
    posix = PurePosixPath(relative)
    if posix.is_absolute() or ".." in posix.parts or "\\" in relative:
        raise ValueError(f"unsafe portable path: {relative}")
    target = (root / Path(*posix.parts)).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"path escapes root: {relative}")
    return target


def strip_fences(markdown):
    lines, fence = [], None
    for line in markdown.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            token = match.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1]:
                fence = None
        elif fence is None:
            lines.append(line)
    return "\n".join(lines)


def markdown_destinations(markdown):
    text = strip_fences(markdown)
    for match in re.finditer(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", text):
        raw = match.group(1).strip()
        if raw.startswith("<") and ">" in raw:
            yield raw[1:raw.index(">")]
        else:
            yield re.split(r"\s+[\"']", raw, maxsplit=1)[0].strip()
    for match in re.finditer(r"^\s{0,3}\[[^\]\n]+\]:\s*(\S+)", text, flags=re.M):
        yield match.group(1).strip("<>")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--expectations", default="registry/verification_expectations.json",
                        help="portable path within root")
    parser.add_argument("--skip-manifest", action="store_true",
                        help="preflight only; final preservation verification must include manifest")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    errors, checks = [], {}
    state = {}

    def require(condition, message):
        if not condition:
            errors.append(message)

    def guarded(label, function):
        try:
            function()
        except (OSError, ValueError, KeyError, TypeError, IndexError, zipfile.BadZipFile) as exc:
            errors.append(f"{label}: {type(exc).__name__}: {exc}")

    def path_exists(relative, label):
        path = inside(root, relative)
        require(path.is_file(), f"{label} missing: {relative}")
        return path

    def configuration_check():
        config = load_json(inside(root, args.expectations))
        require(config.get("schema_version") == "1.0", "expectation schema must be1.0")
        require(config.get("research_through") == 44, "this verifier is scoped to through044")
        require(not config.get("integration_pending"), "expectation configuration still lists integration_pending items")
        for field in ("documentation_revision", "expected_registry_counts", "control_documents", "required_paths"):
            require(field in config, f"expectation field missing: {field}")
        counts = config["expected_registry_counts"]
        for name, count_key in COUNT_KEYS.items():
            value = counts.get(count_key)
            require(type(value) is int and value >= INHERITED_COUNTS[name], f"invalid expected count: {count_key}")
        require(counts.get("raw_discovery_records") == 1721, "frozen corpus expected count must remain1721")
        require(type(config.get("expected_queue_records")) is int, "expected_queue_records must be pinned to an integer")
        state["config"] = config
        checks["expectations_sha256"] = digest(inside(root, args.expectations))

    guarded("expectations", configuration_check)
    if "config" not in state:
        print(json.dumps({"status":"failed", "errors":errors, "checks":checks, "scope":SCOPE}, indent=2))
        return 1
    config = state["config"]

    def inherited_preservation_check():
        previous = path_exists(PREVIOUS_REL, "pinned through042 package")
        if digest(previous) != PREVIOUS_SHA:
            raise ValueError("D2026-10-25 through042 ZIP hash differs from the hard-coded anchor")
        with zipfile.ZipFile(previous) as archive:
            names = archive.namelist()
            require(len(names) == len(set(names)), "pinned ZIP contains duplicate member names")
            previous_status = json.loads(archive.read(PREVIOUS_PREFIX + "registry/current_status.json"))
            records, inherited_ids, appended_ids = {}, {}, {}
            for name, old_count in INHERITED_COUNTS.items():
                rel = f"registry/{name}.json"
                original_raw = archive.read(PREVIOUS_PREFIX + rel)
                current_raw = inside(root, rel).read_bytes()
                original = record_list(json.loads(original_raw), name)
                current = record_list(json.loads(current_raw), name)
                require(len(original) == old_count, f"unexpected original {name} count")
                require(record_bytes(current_raw, name)[:old_count] == record_bytes(original_raw, name),
                        f"inherited scientific prefix object bytes changed: {rel}")
                expected = config["expected_registry_counts"][COUNT_KEYS[name]]
                require(len(current) == expected, f"current {name} count differs from pinned expectations")
                identifiers = [row["id"] for row in current]
                require(all(isinstance(value,str) and value for value in identifiers), f"empty/non-string {name} ID")
                require(len(identifiers) == len(set(identifiers)), f"duplicate {name} identifiers")
                new_ids = identifiers[old_count:]
                pattern = config["new_id_patterns"][name]
                require(all(re.fullmatch(pattern, value) for value in new_ids), f"appended {name} ID outside configured C043–C044 pattern")
                pinned_new_ids = config.get("expected_added_ids", {}).get(name)
                if pinned_new_ids is not None:
                    require(new_ids == pinned_new_ids, f"appended {name} ID sequence differs from expectations")
                if name in {"claims", "experiments"}:
                    for row in current[old_count:]:
                        require(type(row.get("iteration")) is int and row["iteration"] in NEW_ITERATIONS,
                                f"new {name} row must declare integer iteration43 or44: {row['id']}")
                records[name], inherited_ids[name], appended_ids[name] = current, identifiers[:old_count], new_ids
            all_ids = [row["id"] for rows in records.values() for row in rows]
            require(len(all_ids) == len(set(all_ids)), "IDs collide across scientific registries")
            immutable_original = set()
            immutable_checked = 0
            for member in archive.infolist():
                if member.is_dir() or not member.filename.startswith(PREVIOUS_PREFIX):
                    continue
                rel = member.filename[len(PREVIOUS_PREFIX):]
                frozen_tree = rel.startswith(IMMUTABLE_TREE_PREFIXES)
                keep = frozen_tree or rel.startswith("archive/")
                if frozen_tree:
                    immutable_original.add(rel)
                if keep:
                    target = path_exists(rel, "inherited immutable file")
                    if target.is_file():
                        require(target.read_bytes() == archive.read(member), f"inherited immutable bytes changed: {rel}")
                    immutable_checked += 1
            immutable_current = {
                p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()
                and p.relative_to(root).as_posix().startswith(IMMUTABLE_TREE_PREFIXES)
                and "__pycache__" not in p.parts and p.suffix not in {".pyc", ".pyo"}
            }
            require(immutable_current == immutable_original,
                    "files added to or removed from frozen baseline/corpus/C038–C042/prior-phase/prior-review trees")
            old_verifier = archive.read(PREVIOUS_PREFIX + "verify.py")
            require(old_verifier.startswith(b"#!/usr/bin/env python3"), "pinned through042 verifier missing")
            state.update(records=records, previous_status=previous_status, known_ids=set(all_ids))
            checks["pinned_through042_archive"] = {"path":PREVIOUS_REL, "sha256":PREVIOUS_SHA,
                                                    "old_verifier_sha256":hashlib.sha256(old_verifier).hexdigest()}
            checks["scientific_prefix_counts_unchanged"] = INHERITED_COUNTS
            checks["appended_record_ids"] = appended_ids
            checks["immutable_inherited_files_checked"] = immutable_checked
        require(digest(inside(root,C041_REL)) == C041_SHA, "exact C041 campaign archive changed")
        require(digest(inside(root,CORPUS_REL)) == CORPUS_SHA, "frozen corpus hash changed")
        corpus = load_json(inside(root,CORPUS_REL))
        require(isinstance(corpus,dict) and len(corpus) == 1721, "frozen corpus structure/count changed")

    guarded("inherited preservation and scientific prefixes", inherited_preservation_check)

    def status_and_queue_check():
        status = load_json(inside(root,"registry/current_status.json"))
        queue = load_json(inside(root,"registry/research_queue.json"))
        through, revision = config["research_through"], config["documentation_revision"]
        for label, payload in (("status",status),("queue",queue)):
            require(type(payload.get("research_through")) is int and payload["research_through"] == through,
                    f"{label} research_through disagrees with expectations")
            require(payload.get("documentation_revision") == revision, f"{label} documentation revision mismatch")
        require(status.get("mission_achieved") is config.get("mission_achieved",False), "mission status differs from explicit expectation")
        require(status.get("next_iteration_number") == through+1, "next iteration number is inconsistent")
        prior_authority = state["previous_status"]["scientific_authority"]
        authority = status.get("scientific_authority",[])
        require(authority[:len(prior_authority)] == prior_authority, "inherited scientific authority sequence changed")
        require(authority[len(prior_authority):] == ["C043", "C044"],
                "scientific authority additions must be exactly C043 then C044")
        rows = queue["records"]
        require(isinstance(rows,list), "queue records must be an array")
        require(len(rows) == config["expected_queue_records"], "queue record count differs from pinned expectation")
        ids = [row["id"] for row in rows]
        require(len(ids) == len(set(ids)), "duplicate queue identifiers")
        for row in rows:
            require(type(row.get("active")) is bool, f"queue active not boolean: {row['id']}")
            require(type(row.get("semantic_test_admitted")) is bool, f"queue semantic admission not boolean: {row['id']}")
        active = sum(row.get("active") is True for row in rows)
        active_semantic = sum(row.get("active") is True and row.get("semantic_test_admitted") is True for row in rows)
        for key, value in (("active_candidates",active),("active_semantic_experiments",active_semantic)):
            require(value == config.get(key,0), f"queue {key} differs from expectations")
            for label,payload in (("status",status),("queue",queue)):
                require(type(payload.get(key)) is int and payload[key] == value, f"{label} {key} inconsistent with queue")
        records = state["records"]
        actual_counts = {COUNT_KEYS[name]:len(rows) for name,rows in records.items()}
        actual_counts["raw_discovery_records"] = 1721
        require(status["registry_counts"] == actual_counts == config["expected_registry_counts"], "status/actual/expected registry counts differ")
        require(all(type(v) is int for v in status["registry_counts"].values()), "status registry counts must be integers")
        claims_payload = load_json(inside(root,"registry/claims.json"))
        envelope_authority = claims_payload.get("authority","") if isinstance(claims_payload,dict) else ""
        require(isinstance(envelope_authority,str) and re.search(r"through\s*0?44\b",envelope_authority,re.I),
                "claims envelope does not identify authority through044")
        for key,relative in status.get("canonical_paths",{}).items():
            path_exists(relative, f"status canonical path {key}")
        valid_refs = {
            "related_claim_ids":{row["id"] for row in records["claims"]},
            "related_source_ids":{row["id"] for row in records["sources"]},
            "related_dispositions":{row["id"] for row in load_json(inside(root,"baseline/CLAIM_DISPOSITIONS.json"))["dispositions"]},
        }
        prior_queue = {row["id"] for row in load_json(inside(root,"baseline/RESEARCH_QUEUE.json"))["records"]}
        evidence_count, ref_count = 0, 0
        for row in rows:
            for relative in row.get("evidence_paths",[]):
                path_exists(relative,f"queue evidence for {row['id']}")
                evidence_count += 1
            for field,known in valid_refs.items():
                refs = row.get(field,[])
                require(isinstance(refs,list),f"queue reference field not array: {row['id']} {field}")
                for ref in refs:
                    require(ref in known,f"unresolved queue {field}: {row['id']} -> {ref}")
                    ref_count += 1
            if "prior_queue_id" in row:
                require(row["prior_queue_id"] in prior_queue,f"unknown prior baseline queue ID: {row['id']}")
        checks["queue_and_status"] = {"research_through":through,"documentation_revision":revision,
                                     "queue_records":len(rows),"active_candidates":active,
                                     "active_semantic_experiments":active_semantic,
                                     "evidence_paths":evidence_count,"related_ids":ref_count,
                                     "registry_counts":actual_counts}

    guarded("current status/queue", status_and_queue_check)

    def evidence_check():
        records, known = state["records"], state["known_ids"]
        paths_checked, refs_checked = 0, 0
        for name in ("claims","experiments"):
            for row in records[name]:
                if row.get("iteration") not in {38,39,40,41,42,43,44}:
                    continue
                for field in (("dependencies",) if name == "claims" else ("input",)):
                    references = row.get(field,[])
                    require(isinstance(references,list),f"record references not array: {row['id']} {field}")
                    for ref in references:
                        # Older input arrays include descriptive strings and paths,
                        # not just registry IDs. Their original bytes are pinned
                        # above; enforce the ID contract for C042–C044 inputs and
                        # for the older claim dependency arrays that use IDs.
                        if name == "claims" or row.get("iteration") in {42,43,44}:
                            require(ref in known,f"unresolved scientific dependency: {row['id']} -> {ref}")
                        refs_checked += 1
                if name == "claims":
                    paths = [row["evidence_path"]]+row.get("additional_evidence_paths",[])
                else:
                    paths = row.get("outputs",[])
                    require(isinstance(paths,list) and bool(paths),f"experiment has no output paths: {row['id']}")
                for relative in paths:
                    path_exists(relative,f"evidence/output for {row['id']}")
                    paths_checked += 1
                for field in ("campaign_archive","archive"):
                    if field in row and row.get("iteration") in {42,43,44}:
                        path_exists(row[field],f"archive for {row['id']}")
        for row in records["sources"][INHERITED_COUNTS["sources"]:]:
            require(isinstance(row.get("title"),str) and bool(row["title"].strip()), f"new source has no title: {row['id']}")
            authored = row.get("authored_record")
            require(isinstance(authored,str) and bool(authored),f"new source has no authored_record: {row['id']}")
            if authored:
                path_exists(authored,f"authored source record for {row['id']}")
                paths_checked += 1
            for relative in row.get("evidence_paths",[]):
                path_exists(relative,f"source evidence for {row['id']}")
                paths_checked += 1
        for relative in config["required_paths"]:
            path_exists(relative,"required current deliverable")
            paths_checked += 1
        checks["scientific_evidence_navigation"] = {
            "files_checked": paths_checked, "dependency_entries_reviewed": refs_checked,
            "historical_scope": "Older free-form experiment inputs and original archive paths are preserved in their source snapshot. Their archives remain nested inside pinned C041; C042–C044 input IDs and archive paths are checked in this root."
        }

    guarded("scientific evidence/output links", evidence_check)

    def analysis_artifact_check():
        rows = config.get("analysis_integrity",[])
        for row in rows:
            input_path = path_exists(row["input_path"],"analysis input")
            result_path = path_exists(row["result_path"],"analysis result")
            rule_path = path_exists(row["rule_path"],"frozen analysis rule")
            inputs, result = load_json(input_path), load_json(result_path)
            actual_input_hash, actual_rule_hash = digest(input_path), digest(rule_path)
            require(result.get("input_sha256") == actual_input_hash, "analysis result was not generated from the preserved input bytes")
            require(actual_rule_hash == row["rule_sha256"],"frozen analytic rule differs from pinned expectation")
            require(inputs.get("analysis_rule_sha256") == actual_rule_hash == result.get("analysis_rule_sha256"),"analysis rule hash chain inconsistent")
            require((input_path.parent/inputs["analysis_rule"]).resolve() == rule_path,"analysis input rule locator does not resolve to pinned rule")
            scenarios = result["comparisons"]
            expected_pairs = {(a["q"],b["q"]) for a in inputs["reading_branches"]["KNZb27"] for b in inputs["reading_branches"]["ZAZb3"]}
            actual_pairs = [(s["KN_q"],s["ZA_q"]) for s in scenarios]
            require(len(actual_pairs) == len(set(actual_pairs)),"duplicate capacity scenario")
            require(set(actual_pairs) == expected_pairs,"capacity output reading branches differ from input branches")
            require(len(scenarios) == row["expected_scenarios"],"capacity scenario count differs from pinned expectation")
        checks["analysis_artifact_chains"] = len(rows)
        checks["analysis_validation_scope"] = "input/rule hash joins and declared scenario coverage; equations not rerun here"

    guarded("analysis artifact consistency", analysis_artifact_check)

    def frozen_hashes_check():
        hashes = config.get("frozen_hashes", {})
        if not isinstance(hashes, dict):
            raise ValueError("frozen_hashes must be an object mapping portable paths to SHA256 hashes")
        for relative, expected_hash in hashes.items():
            if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
                raise ValueError(f"invalid frozen SHA256: {relative}")
            path = path_exists(relative, "configured frozen file")
            if path.is_file():
                require(digest(path) == expected_hash, f"configured frozen file hash changed: {relative}")
        checks["configured_frozen_hashes"] = len(hashes)

    guarded("configured frozen hashes", frozen_hashes_check)

    def reproducible_outputs_check():
        rows = config.get("reproducible_outputs", [])
        if not isinstance(rows, list):
            raise ValueError("reproducible_outputs must be an array of script_path/result_path objects")
        reproduced = []
        for row in rows:
            script = path_exists(row["script_path"], "reproduction script")
            result = path_exists(row["result_path"], "preserved reproduction result")
            if not script.is_file() or not result.is_file():
                continue
            if script.suffix != ".py":
                raise ValueError(f"reproduction script must be Python: {row['script_path']}")
            try:
                completed = subprocess.run(
                    [sys.executable, "-I", "-B", str(script)], cwd=root,
                    capture_output=True, text=True, encoding="utf-8", timeout=30,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                errors.append(f"reproduction script exceeded30 seconds: {row['script_path']}")
                continue
            if completed.returncode != 0:
                errors.append(f"reproduction script failed ({completed.returncode}): {row['script_path']}; "
                              f"stderr: {completed.stderr[:1000]}")
                continue
            actual, expected = json.loads(completed.stdout), load_json(result)
            require(canonical_json(actual) == canonical_json(expected),
                    f"reproduced JSON differs from preserved result: {row['result_path']}")
            reproduced.append({"script_path":row["script_path"], "result_path":row["result_path"],
                               "script_sha256":digest(script), "result_sha256":digest(result)})
        checks["reproducible_outputs"] = reproduced
        checks["reproduction_scope"] = (
            "Configured local Python scripts only; JSON values/types compared without formatting. "
            "Scripts must be reviewed as read-only before inclusion. This is computational consistency, not ancient meaning."
        )

    guarded("reproducible outputs", reproducible_outputs_check)

    def links_check():
        documents = list(config["control_documents"])
        for prefix in config.get("additional_markdown_trees",[]):
            tree = inside(root,prefix)
            require(tree.is_dir(),f"current Markdown tree missing: {prefix}")
            documents.extend(p.relative_to(root).as_posix() for p in tree.rglob("*.md"))
        documents = sorted(set(documents))
        count = 0
        for relative in documents:
            path = path_exists(relative,"current control document")
            if not path.is_file():
                continue
            for destination in markdown_destinations(path.read_text(encoding="utf-8")):
                parsed = urlsplit(destination)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                local = (path.parent/unquote(parsed.path)).resolve()
                require(local.is_relative_to(root),f"current link escapes snapshot: {relative} -> {destination}")
                require(local.exists(),f"broken current relative link: {relative} -> {destination}")
                count += 1
        checks["current_navigation"] = {"documents":len(documents),"relative_links":count,"anchors":"not checked"}

    guarded("current Markdown navigation", links_check)

    def manifest_check():
        payload = load_json(inside(root,"MANIFEST.json"))
        rows = payload["files"]
        require(isinstance(rows,list),"manifest files must be an array")
        paths = [row["path"] for row in rows]
        require(len(paths) == len(set(paths)),"duplicate manifest paths")
        require("MANIFEST.json" not in paths,"manifest must exclude itself")
        for row in rows:
            path = path_exists(row["path"],"manifest file")
            if not path.is_file():
                continue
            require(path.stat().st_size == row["size_bytes"],f"manifest size mismatch: {row['path']}")
            require(digest(path) == row["sha256"],f"manifest hash mismatch: {row['path']}")
        actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()
                  and "__pycache__" not in p.parts and p.suffix not in {".pyc",".pyo"}}
        require(actual-{ "MANIFEST.json"} == set(paths),"manifest does not exactly cover current files (excluding itself and runtime bytecode)")
        checks["manifest_files"] = len(paths)

    if args.skip_manifest:
        checks["manifest"] = "skipped_for_preflight_only"
    else:
        guarded("manifest",manifest_check)
    result = {"status":"failed" if errors else "passed",
              "mode":"preflight_without_manifest" if args.skip_manifest else "full",
              "checks":checks,"errors":errors,"scope":SCOPE}
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

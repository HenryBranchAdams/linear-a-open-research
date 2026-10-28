#!/usr/bin/env python3
"""List or read preserved historical reports without extracting or changing files.

Examples:
  python3 tools/read_history.py --list Iteration_21
  python3 tools/read_history.py --read 23
Indexes are zero-based and stable within registry/archive_navigation.json.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import sys
import zipfile

REMINDER = (
    "Historical source: original claims may be narrowed or superseded. "
    "Use context/CURRENT_STATE.md, baseline/CLAIM_DISPOSITIONS.json and "
    "baseline/HISTORY_CROSSWALK.json for controlling conclusions. "
    "Reading this file does not establish its claims or create unused evidence."
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_bytes(data: bytes, record: dict, label: str) -> bytes:
    if len(data) != record["size_bytes"]:
        raise ValueError(f"{label}: byte-size mismatch")
    if sha256(data) != record["sha256"]:
        raise ValueError(f"{label}: SHA-256 mismatch")
    return data


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="current snapshot root (default: parent of tools directory)")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--list", nargs="?", const="", metavar="SEARCH", dest="query",
                           help="list indexes, optionally filtering member path/archive ID")
    selection.add_argument("--read", type=int, metavar="INDEX", dest="report_index",
                           help="read one zero-based report index, verifying every archive and report")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        navigation = json.loads((root / "registry/archive_navigation.json").read_text(encoding="utf-8"))
        reports = navigation["reports"]
        archives = {record["id"]: record for record in navigation["archives"]}
        if len(archives) != len(navigation["archives"]):
            raise ValueError("archive index contains duplicate IDs")

        if args.report_index is None:
            query = (args.query or "").casefold()
            matches = [(i, record) for i, record in enumerate(reports)
                       if query in f"{record['archive_id']} {record['member']}".casefold()]
            print("Historical report indexes (zero-based; stable within this navigation index):")
            for index, record in matches:
                print(f"{index:03d}\t{record['archive_id']}\t{record['member']}")
            if not matches:
                print(f"No report matches {args.query!r}. Try an iteration number or part of its filename.")
            print(f"\n{len(matches)} of {len(reports)} indexed reports shown. {REMINDER}")
            return 0

        if not 0 <= args.report_index < len(reports):
            raise ValueError(f"report index must be between 0 and {len(reports)-1}")
        cache: dict[str, bytes] = {}
        opening: set[str] = set()

        def open_archive(archive_id: str) -> bytes:
            if archive_id in cache:
                return cache[archive_id]
            if archive_id in opening:
                raise ValueError(f"archive-parent cycle at {archive_id}")
            opening.add(archive_id)
            record = archives[archive_id]
            if "parent_archive_id" in record:
                parent = open_archive(record["parent_archive_id"])
                with zipfile.ZipFile(io.BytesIO(parent)) as archive:
                    data = archive.read(record["member"])
            else:
                relative = PurePosixPath(record["path"])
                if relative.is_absolute() or ".." in relative.parts or "\\" in record["path"]:
                    raise ValueError(f"unsafe root archive path: {record['path']}")
                path = (root / Path(*relative.parts)).resolve()
                if not path.is_relative_to(root):
                    raise ValueError("root archive path escapes snapshot")
                data = path.read_bytes()
            cache[archive_id] = check_bytes(data, record, archive_id)
            opening.remove(archive_id)
            return cache[archive_id]

        report = reports[args.report_index]
        with zipfile.ZipFile(io.BytesIO(open_archive(report["archive_id"]))) as archive:
            content = check_bytes(archive.read(report["member"]), report,
                                  f"report {args.report_index:03d}")
        print(REMINDER)
        print(f"Index: {args.report_index:03d}; archive: {report['archive_id']}; member: {report['member']}")
        print(f"Verified {len(cache)} archive(s) and report SHA-256 {report['sha256']}.\n")
        text = content.decode("utf-8-sig")
        print(text, end="" if text.endswith("\n") else "\n")
        return 0
    except (OSError, ValueError, KeyError, TypeError, UnicodeError, zipfile.BadZipFile) as exc:
        print(f"History read failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

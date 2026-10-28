#!/usr/bin/env python3
"""Verify the portable artifact, allowing only disposable Python bytecode extras."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'MANIFEST.json'


def artifact_files(root):
    return sorted(p for p in root.rglob('*') if p.is_file()
                  and p.name != MANIFEST
                  and '__pycache__' not in p.parts
                  and p.suffix != '.pyc')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root=ROOT):
    manifest = json.loads((root / MANIFEST).read_text(encoding='utf-8'))
    declared = {row['path']: row for row in manifest['files']}
    if len(declared) != len(manifest['files']):
        raise ValueError('Duplicate manifest paths')
    actual = {str(p.relative_to(root)).replace('\\', '/'): p for p in artifact_files(root)}
    if actual.keys() != declared.keys():
        raise ValueError(f'File coverage mismatch: missing={sorted(declared.keys()-actual.keys())}; extra={sorted(actual.keys()-declared.keys())}')
    for name, row in declared.items():
        path = actual[name]
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'Unexpected symlink or path: {name}')
        if path.stat().st_size != row['bytes'] or digest(path) != row['sha256']:
            raise ValueError(f'Hash/size mismatch: {name}')
    return {'verified_files': len(actual), 'algorithm': 'SHA-256', 'status': 'pass'}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))

#!/usr/bin/env python3
"""Build the deliverable, extract it, and reproduce its analyses without network."""
import datetime
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

from verify_bundle import ROOT, MANIFEST, artifact_files, digest, verify

ARCHIVE = ROOT.parent / 'linear_a_round9.zip'


def build():
    files = artifact_files(ROOT)
    if any(p.suffix.lower() in {'.pdf', '.jpg', '.jpeg', '.png', '.ttf', '.otf', '.woff', '.woff2'} for p in files):
        raise ValueError('Unexpected image/publication/font in this text-only package')
    manifest = {'schema': 'round9-manifest-1', 'hash': 'SHA-256',
                'excludes': ['MANIFEST.json itself', 'disposable __pycache__ and .pyc'],
                'files': [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
                           'sha256': digest(p)} for p in files]}
    (ROOT / MANIFEST).write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    with zipfile.ZipFile(ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for p in files + [ROOT / MANIFEST]:
            if p.is_symlink():
                raise ValueError(f'Symlink not supported: {p}')
            z.write(p, 'linear_a_round9/' + p.relative_to(ROOT).as_posix())


def extracted_reproduction():
    with tempfile.TemporaryDirectory(prefix='linear_a_round9_verify_') as tmp:
        target = Path(tmp)
        with zipfile.ZipFile(ARCHIVE) as z:
            for item in z.infolist():
                parts = PurePosixPath(item.filename)
                if parts.is_absolute() or '..' in parts.parts or parts.parts[0] != 'linear_a_round9':
                    raise ValueError(f'Unsafe archive path: {item.filename}')
                if (item.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('Archive symlink rejected')
            if z.testzip() is not None:
                raise ValueError('ZIP CRC check failed')
            z.extractall(target)
        extracted = target / 'linear_a_round9'
        verify(extracted)
        commands = [[sys.executable, 'analysis/run.py'],
                    [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v']]
        for cmd in commands:
            completed = subprocess.run(cmd, cwd=extracted, capture_output=True, text=True)
            if completed.returncode:
                raise RuntimeError(completed.stdout + completed.stderr)
        verified = verify(extracted)
        summary = json.loads((extracted / 'results/summary.json').read_text())
        return {'manifest': verified, 'summary': summary,
                'test_output': completed.stderr.strip()}


def main():
    subprocess.run([sys.executable, str(ROOT / 'analysis/run.py')], check=True,
                   stdout=subprocess.DEVNULL)
    build()
    first = extracted_reproduction()
    record = {'verified_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'python': sys.version.split()[0], 'status': 'pass',
              'method': 'Clean ZIP extraction; CRC and manifest check; offline analyses and integration tests; all delivered bytes rechecked after reproduction. Final rebuilt archive verified by the same procedure.',
              'commands': ['python3 analysis/run.py', 'python3 -m unittest discover -s tests -v',
                           'python3 analysis/verify_bundle.py'],
              'central_results': first['summary'], 'test_output': first['test_output'],
              'scope': 'Implementation and portability verification, not epigraphic or semantic validation'}
    (ROOT / 'results/package_verification.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    build()
    final = extracted_reproduction()
    checksum = digest(ARCHIVE)
    ARCHIVE.with_suffix('.zip.sha256').write_text(checksum + '  ' + ARCHIVE.name + '\n', encoding='utf-8')
    print(json.dumps({'archive': str(ARCHIVE), 'sha256': checksum,
                      'bytes': ARCHIVE.stat().st_size, 'final_verification': final['manifest'],
                      'offline_reproduction': 'pass'}, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Reproduce supplied verifiers in copies and audit the iteration-16 status dependency.

Usage: python audit_research.py --inputs PATH --output PATH
PATH should contain the extracted iteration-10 to -16 roots, recursively.
This audits supplied code and encoded quantities, not ancient readings or translations.
"""
from __future__ import annotations
import argparse, ast, concurrent.futures, copy, hashlib, json, shutil, subprocess, sys
from pathlib import Path


def find_roots(inputs: Path) -> dict[int, Path]:
    roots: dict[int, Path] = {}
    for file in inputs.rglob('START_HERE.md'):
        root = file.parent
        for n in range(10, 17):
            if (root / f'iterations/{n:03d}').is_dir():
                roots[n] = root
    if set(roots) != set(range(10, 17)):
        raise ValueError(f'Expected iterations 10–16; found {sorted(roots)}')
    return roots


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    roots = find_roots(args.inputs.resolve())
    work = output / '_working_copies'
    logs = output / 'logs'
    logs.mkdir(exist_ok=True)
    scripts = {
        10: 'verify.py', 11: 'iterations/011/code/verify.py',
        12: 'iterations/012/code/derive_and_verify.py',
        13: 'iterations/013/code/derive_and_verify.py',
        14: 'iterations/014/code/derive_and_verify.py',
        15: 'iterations/015/code/verify.py', 16: 'iterations/016/code/verify.py',
    }
    def reproduce(n: int) -> dict:
        dest = work / f'{n:03d}'
        shutil.copytree(roots[n], dest, dirs_exist_ok=True)
        try:
            p = subprocess.run([sys.executable, str(dest / scripts[n])], cwd=dest,
                               capture_output=True, text=True, timeout=30)
            log = p.stdout + '\nSTDERR:\n' + p.stderr
            result = {'iteration': n, 'exit_code': p.returncode, 'passed': p.returncode == 0}
        except subprocess.TimeoutExpired as e:
            log = repr(e)
            result = {'iteration': n, 'passed': False, 'error': 'timeout after 30 seconds'}
        (logs / f'iteration_{n:03d}.txt').write_text(log)
        result['script'] = scripts[n]
        result['log'] = f'logs/iteration_{n:03d}.txt'
        return result
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        runs = list(pool.map(reproduce, range(10, 17)))

    # Compile only the supplied pure derive function; avoid module side effects.
    verifier = roots[16] / scripts[16]
    source = verifier.read_text()
    tree = ast.parse(source)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'derive')
    module = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    namespace: dict = {}
    exec(compile(module, str(verifier), 'exec'), namespace)
    derive = namespace['derive']
    ev_path = roots[16] / 'iterations/016/data/evidence.json'
    evidence = json.loads(ev_path.read_text())
    baseline = derive(evidence)
    mutated = copy.deepcopy(evidence)
    mutated['ht34']['critical_sequence'][3]['status'] = 'written_current'
    changed = derive(mutated)

    # Independent arithmetic audit; statuses explicitly affect the chosen current state.
    def status_aware_ht34(e: dict) -> dict:
        seq = e['ht34']['critical_sequence']
        ref, portion, current = (seq[i]['quantity'] for i in range(3))
        # Conditional model: trailing 7 belongs to the same KI-RO quantity.
        current += sum(x['quantity'] for x in seq[3:] if x['status'] != 'erased')
        return {'kiro_current': current, 'sum': portion + current, 'reference': ref,
                'closes': portion + current == ref,
                'scope': 'Conditional on the encoded row association and common quantitative scope.'}

    main_col = evidence['ht118']['main_total']
    altered_main = copy.deepcopy(evidence)
    altered_main['ht118']['main_total']['components'][0] = 20
    ht100 = []
    for damaged in (4, 6):
        base = 58 + damaged + 12 + 5 + 16
        ht100.append({'damaged_numeral': damaged, 'without_KI': base,
                      'with_KI_added': base + 2, 'with_KI_subtracted': base - 2,
                      'written_total': 97})
    report = {
        'scope': 'Review audit of encoded observations and original verifiers. Not an epigraphic autopsy or a decipherment test.',
        'baseline_reproductions': runs,
        'iteration16_erasure_status_mutation': {
            'original_status': 'erased', 'mutated_status': 'written_current',
            'original_derive': baseline, 'mutated_derive': changed,
            'all_original_outputs_identical': baseline == changed,
            'original_test_condition_before_mutation': not baseline['ht34_erased_state_closes'],
            'original_test_condition_after_mutation': not changed['ht34_erased_state_closes'],
            'finding': 'The derive function ignores the status field; the published erasure-status failure-injection test cannot detect this mutation.',
            'status_aware_baseline': status_aware_ht34(evidence),
            'status_aware_mutation': status_aware_ht34(mutated),
        },
        'ht118_complete_arithmetic_audit': {
            'main_components': main_col['components'],
            'computed_main_sum': sum(main_col['components']),
            'written_kuro': main_col['written_kuro'],
            'main_closes': sum(main_col['components']) == main_col['written_kuro'],
            'KI_components': evidence['ht118']['ki_subtotal']['components'],
            'computed_KI_sum': sum(evidence['ht118']['ki_subtotal']['components']),
            'encoded_written_KI_total': evidence['ht118']['ki_subtotal']['written_total'],
            'changing_main_quantity_leaves_original_derive_unchanged': derive(altered_main) == baseline,
            'finding': 'Mismatch is acknowledged in the source evidence.json but omitted from the report discussion and verifier output. KI closure does not resolve main-column scope.',
            'critical_text_caveat': 'Reopened public transcriptions end KI 15[; do not drop the break marker. This alone does not prove a missing numeral.',
        },
        'ht100_inclusion_is_not_subtraction': ht100,
        'source_hashes': {
            'iteration16_verifier_sha256': hashlib.sha256(verifier.read_bytes()).hexdigest(),
            'iteration16_evidence_sha256': hashlib.sha256(ev_path.read_bytes()).hexdigest(),
        },
        'archive_hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(args.inputs.glob('*.zip'))},
    }
    (output / 'audit_results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'runs': runs,
                      'status_mutation_outputs_identical': baseline == changed,
                      'HT118_main_sum': sum(main_col['components']),
                      'HT118_written_main_total': main_col['written_kuro'],
                      'ht100': ht100}, indent=2))
    # Keep the audit package compact; originals remain untouched in the input directory.
    shutil.rmtree(work)

if __name__ == '__main__':
    main()

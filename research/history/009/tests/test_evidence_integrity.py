"""Integration safeguards for evidential distinctions, not decipherment tests."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


class EvidenceIntegrity(unittest.TestCase):
    def test_observations_retain_resolvable_source_references(self):
        sources = read('data/sources.json')
        keys = {(s['branch'], s['source_id']) for s in sources}
        rows = read('data/observations.json')['observations']
        self.assertEqual(len(rows), len({o['evidence_id'] for o in rows}))
        for row in rows:
            self.assertTrue(row['original_record'])
            self.assertTrue(row['source_refs'], row['evidence_id'])
            for ref in row['source_refs']:
                self.assertIn((row['branch'], ref), keys, row['evidence_id'])

    def test_linear_b_target_certainty_does_not_hide_other_damage(self):
        rows = {o['evidence_id']: o for o in read('data/observations.json')['observations']}
        complete = rows['linear_b:LB01']
        broken = rows['linear_b:LB05']
        self.assertTrue(complete['target_complete'])
        self.assertEqual(complete['uncertainty_scope'], 'target only')
        self.assertTrue(complete['other_uncertainty'])
        self.assertFalse(broken['target_complete'])
        self.assertEqual(broken['missing_boundaries']['left'], 'lost')
        self.assertEqual(broken['missing_boundaries']['right'], 'divider after ti')
        self.assertTrue(broken['diplomatic_transcription'].startswith(']'))

    def test_corpus_snapshot_counts_without_upgrading_words(self):
        corpus = read('data/sigla_sequence_inventory.json')
        summary = read('results/summary.json')
        self.assertEqual(len(corpus['documents']), summary['sigla_document_faces'])
        self.assertEqual(sum(bool(d['error']) for d in corpus['documents']), summary['sigla_fetch_errors'])
        self.assertEqual(sum(len(d.get('sequences', [])) for d in corpus['documents']), summary['sigla_sequence_occurrences'])
        self.assertFalse(summary['ZA9_final_sign_independently_resolved'])
        self.assertFalse(summary['same_referent_established_for_TA_NA_family'])

    def test_alternative_readings_change_only_conditional_result(self):
        result = read('results/anetaki_textile_test.json')
        scenarios = {s['scenario']: s for s in result['ME_scenarios']}
        def doubled(name):
            return next(m for m in scenarios[name]['candidate_multipliers'] if m['m'] == '2')
        self.assertFalse(doubled('secure_ME_only')['negative_residual_rejects'])
        self.assertTrue(doubled('accept_tentative_ME_at_six')['negative_residual_rejects'])
        self.assertTrue(result['lossless_balance_required_for_negative_residual_rejection'])
        self.assertEqual(result['yield_sensitivity']['maximum_yield_at_lower_bound'], '18/19')


if __name__ == '__main__':
    unittest.main()

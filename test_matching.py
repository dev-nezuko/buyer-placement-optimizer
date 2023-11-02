import tempfile
import unittest
import random
from pathlib import Path
from assessment import Pearl


class MatchingTests(unittest.TestCase):
    def solve(self, lines):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'input.txt'
            path.write_text('\n'.join(lines))
            solver = Pearl(path)
            solver.optimize_placements()
            return solver

    def assert_invariants(self, solver):
        placement = {buyer: name for name, entries in solver.final_selections.items() for buyer, _ in entries}
        all_buyers = [buyer for entries in solver.final_selections.values() for buyer, _ in entries]
        self.assertEqual(len(all_buyers), len(set(all_buyers)))
        self.assertEqual(set(placement), {b['H'] for b in solver.home_buyers})
        sizes = [len(entries) for entries in solver.final_selections.values()]
        self.assertLessEqual(max(sizes) - min(sizes), 1)
        for buyer in solver.home_buyers:
            name = buyer['H']
            for preferred in buyer['prefs'][:buyer['prefs'].index(placement[name])]:
                residents = solver.final_selections[preferred]
                self.assertEqual(len(residents), solver.capacities[preferred])
                score = next(item['score'] for item in solver.buyers_scores[name][:-1] if item['neighborhood'] == preferred)
                self.assertTrue(all(score <= resident_score for _, resident_score in residents))

    def test_duplicate_assignment_regression(self):
        self.assert_invariants(self.solve(REGRESSION))

    def test_balanced_complete_stable_results_across_synthetic_inputs(self):
        rng = random.Random(17)
        for buyer_count in range(16):
            with self.subTest(buyers=buyer_count):
                lines = ['N N0 E:7 W:7 R:10','N N1 E:2 W:1 R:1','N N2 E:7 W:6 R:4']
                for index in range(buyer_count):
                    preferences = '>'.join(rng.sample(['N0','N1','N2'],3))
                    lines.append(f'H H{index} E:{rng.randrange(11)} W:{rng.randrange(11)} R:{rng.randrange(11)} {preferences}')
                solver = self.solve(lines)
                self.assert_invariants(solver)
                first = {key: list(value) for key,value in solver.final_selections.items()}
                solver.optimize_placements()
                self.assertEqual(first, solver.final_selections)

    def test_invalid_inputs(self):
        for lines in [[], ['N N0 E:1 W:1 R:1']*2, ['N N0 E:1 W:1 R:1','H H0 E:1 W:1 R:1 N9'], ['bad'], ['N N0 E:1 E:2 R:1']]:
            with self.subTest(lines=lines), self.assertRaises(ValueError):
                self.solve(lines)

    def test_bundled_output_is_generated_not_only_read(self):
        solver = Pearl(Path(__file__).with_name('input.txt'))
        solver.optimize_placements()
        self.assert_invariants(solver)
        with tempfile.TemporaryDirectory() as directory:
            result = Path(directory) / 'output.txt'
            solver.generate_output(result)
            self.assertEqual(result.read_text(), Path(__file__).with_name('generated_output.txt').read_text())


REGRESSION = ['N N0 E:7 W:7 R:10', 'N N1 E:2 W:1 R:1', 'N N2 E:7 W:6 R:4', 'H H0 E:5 W:4 R:2 N2>N1>N0', 'H H1 E:0 W:3 R:6 N2>N1>N0', 'H H2 E:8 W:5 R:10 N2>N1>N0', 'H H3 E:8 W:0 R:2 N2>N1>N0', 'H H4 E:5 W:8 R:1 N0>N2>N1', 'H H5 E:6 W:1 R:8 N2>N0>N1']

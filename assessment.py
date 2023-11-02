from collections import deque
from helpers import read_input_data, calculate_buyer_scores, write_output_data


class Pearl:
    def __init__(self, input_file):
        self.neighborhoods, self.home_buyers = read_input_data(input_file)
        names = [n['N'] for n in self.neighborhoods]
        buyers = [b['H'] for b in self.home_buyers]
        if not names or len(set(names)) != len(names) or len(set(buyers)) != len(buyers):
            raise ValueError('Require unique neighborhoods and unique buyers')
        for buyer in self.home_buyers:
            if len(buyer['prefs']) != len(names) or set(buyer['prefs']) != set(names):
                raise ValueError('Each buyer must rank every neighborhood exactly once')
        base, remainder = divmod(len(buyers), len(names))
        self.capacities = {name: base + (index < remainder) for index, name in enumerate(names)}
        self.buyers_scores = calculate_buyer_scores(self.neighborhoods, self.home_buyers)
        self.final_selections = {name: [] for name in names}

    def optimize_placements(self):
        """Buyer-proposing deferred acceptance; ties follow buyer input order."""
        buyers = {buyer['H']: buyer for buyer in self.home_buyers}
        order = {name: index for index, name in enumerate(buyers)}
        scores = {buyer: {row['neighborhood']: row['score'] for row in values[:-1]}
                  for buyer, values in self.buyers_scores.items()}
        self.final_selections = {name: [] for name in self.capacities}
        pending = deque(buyers)
        next_preference = {name: 0 for name in buyers}
        while pending:
            buyer = pending.popleft()
            preference = next_preference[buyer]
            if preference >= len(buyers[buyer]['prefs']):
                raise RuntimeError('Buyer exhausted preferences')
            neighborhood = buyers[buyer]['prefs'][preference]
            next_preference[buyer] += 1
            accepted = self.final_selections[neighborhood]
            accepted.append((buyer, scores[buyer][neighborhood]))
            accepted.sort(key=lambda item: (-item[1], order[item[0]]))
            if len(accepted) > self.capacities[neighborhood]:
                rejected, _ = accepted.pop()
                pending.append(rejected)

    def generate_output(self, filename):
        write_output_data(filename, self.final_selections)

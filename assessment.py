import unittest
from helpers import read_input_data, calculate_buyer_scores, generate_selection, write_output_data

neighborhoods, home_buyers = read_input_data('input.txt')
buyers_scores = calculate_buyer_scores(neighborhoods, home_buyers)

neighborhood_limit = len(home_buyers) // len(neighborhoods)
final_selections = {n['N']: [] for n in neighborhoods}
remaining_buyers = []
selected_buyers = []

for index, neighborhood in enumerate(neighborhoods):
  buyer_selections = []

  for buyer, buyer_val in buyers_scores.items():
    # Check if the buyer with the maximum score in a neighborhood also has it as their first preference
    if buyer_val[-1][0] == neighborhood['N']:
      buyer_selections.append(generate_selection(neighborhood, buyer, buyer_val))

  # For the buyers that got excluded from their last preference due to upper limit restrictions
  for buyer in remaining_buyers:
    buyer_details = buyers_scores[buyer['buyer']]

    # Consider next preference and add accordingly
    if buyer_details[-1][index] == neighborhood['N']:
      buyer_selections.append(generate_selection(neighborhood, buyer['buyer'], buyer_details))

  # Sort selected buyers based on their scores, in descending order
  buyer_selections.sort(key=lambda item: item['score'], reverse=True)
  
  # Place an upper limit to ensure number of buyers are evenly distributed
  if len(buyer_selections) > neighborhood_limit:
    remaining_buyers.extend(buyer_selections[neighborhood_limit:])
    buyer_selections = buyer_selections[:neighborhood_limit]

  # Add the current neighborhood buyers to final output
  for buyer in buyer_selections:
     final_selections[buyer['neighborhood']].append((buyer['buyer'], buyer['score']))
     selected_buyers.append(buyer['buyer'])

for buyer, buyer_val in buyers_scores.items():
  # For buyers that have not yet been placed in any neighborhood
  if buyer not in selected_buyers:
    # We go over their preferences and place in best available neighborhood
    for neighborhood in buyer_val[-1]:
      if len(final_selections[neighborhood]) < neighborhood_limit:
        final_selections[neighborhood].append((buyer, [b['score'] for b in buyer_val[:-1] if b['neighborhood'] == neighborhood][0]))

# Generate output file
write_output_data('generated_output.txt', final_selections)

# Run tests to check generated output
unittest.main()

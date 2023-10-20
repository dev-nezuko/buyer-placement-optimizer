from helpers import read_input_data, calculate_buyer_scores, write_output_data

neighborhoods, home_buyers = read_input_data('input.txt')
buyers_scores = calculate_buyer_scores(neighborhoods, home_buyers)

neighborhood_limit = len(home_buyers) // len(neighborhoods)
final_selections = {n['N']: [] for n in neighborhoods}
remaining_buyers = []
selected_buyers = []

for neighborhood in neighborhoods:
  buyer_selections = []

  for buyer, buyer_val in buyers_scores.items():
    preferred_neighborhood = buyer_val[-1][0]

    if preferred_neighborhood == neighborhood['N']:
      buyer_selections.append({
        'neighborhood': preferred_neighborhood,
        'buyer': buyer,
        'score': [b['score'] for b in buyer_val[0:-1] if b['neighborhood'] == preferred_neighborhood][0] 
      })

  for buyer in remaining_buyers:
     buyer_details = buyers_scores[buyer['buyer']]

     if buyer_details[-1][1] == neighborhood['N']:
        buyer_selections.append({
           'neighborhood': neighborhood['N'],
           'buyer': buyer['buyer'],
           'score': [b['score'] for b in buyer_details[:-1] if b['neighborhood'] == neighborhood['N']][0]
        })
  
  buyer_selections.sort(key=lambda item: item['score'], reverse=True)
  
  if len(buyer_selections) > neighborhood_limit:
    remaining_buyers.extend(buyer_selections[4:])
    buyer_selections = buyer_selections[:4]

  for buyer in buyer_selections:
     final_selections[buyer['neighborhood']].append((buyer['buyer'], buyer['score']))
     selected_buyers.append(buyer['buyer'])
    

for buyer, buyer_val in buyers_scores.items():
  if buyer not in selected_buyers:
    for neighborhood in buyer_val[-1]:
      if len(final_selections[neighborhood]) < neighborhood_limit:
        final_selections[neighborhood].append((buyer, [b['score'] for b in buyer_val[:-1] if b['neighborhood'] == neighborhood][0]))

write_output_data('generated_output.txt', final_selections)

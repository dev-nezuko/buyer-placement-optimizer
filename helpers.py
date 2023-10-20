def read_input_data(filename):
  neighborhoods = []
  home_buyers = []

  with open(filename, 'r') as file:
    for line in file:
      parts = line.split()
      data_dict = {}

      data_dict[parts[0]] = parts[1]
      values = parts[2:5]

      for val in values:
        key, value = val.split(':')
        data_dict[key] = int(value)

      if parts[0] == 'N':
        neighborhoods.append(data_dict)
      elif parts[0] == 'H':
        data_dict['prefs'] = parts[5].split('>')
        home_buyers.append(data_dict)

  return neighborhoods, home_buyers

def write_output_data(filename, selections):
  with open(filename, 'w') as file:
    for neighborhood, assigned_buyers in selections.items():
      assigned_buyers.sort(key=lambda x: x[1], reverse=True)
      file.write(f"{neighborhood}: {' '.join([f'{h}({s})' for h, s in assigned_buyers])}\n")

def calculate_buyer_scores(neighborhoods, home_buyers):
  buyers_scores = {}

  for buyer in home_buyers:
    current_scores = []

    for neighborhood in neighborhoods:
      current_scores.append({
        'neighborhood': neighborhood['N'],
        'score': buyer['E'] * neighborhood['E'] + buyer['W'] * neighborhood['W'] + buyer['R'] * neighborhood['R'],
      })

    buyers_scores[buyer['H']] = sorted(current_scores, key=lambda item: item['score'], reverse=True)
    buyers_scores[buyer['H']].append(buyer['prefs'])
    
  return buyers_scores

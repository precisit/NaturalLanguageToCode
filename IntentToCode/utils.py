def cardinal_number_to_int(textnum):
  numwords = {}

  units = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
  ]

  tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

  scales = ["hundred", "thousand", "million", "billion", "trillion"]
  scales_int = [100, 1000, 1000000, 1000000000, 1000000000000]

  numwords["and"] = (1, 0)
  for idx, word in enumerate(units):    numwords[word] = (1, idx)
  for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
  for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

  current = result = 0
  for word in textnum.split():
      if word not in numwords:
        return False

      scale, increment = numwords[word]
      current = current * scale + increment
      if scale > 100:
          result += current
          current = 0
  if (result + current) == 0 and textnum in scales:
    return scales_int[scales.index(textnum)]

  return result + current

def multiplicative_adverbs_to_int(textnum): 

  units = {
      "once" : 1,
      "twice" : 2,
      "thrice" : 3
  }

  if textnum in units:
    return units[textnum]
  else:
    return False
    
def direction_to_vector(direction):
  """directions = {
    "forward" : (1,0),
    "right"   : (1,0),
    "east"    : (1,0),
    "backwards": (-1,0),
    "left"    : (-1,0),
    "west"    : (-1,0),
    "upward"  : (0,1),
    "north"   : (0,1),
    "downwards": (0,-1),
    "down"    : (0,-1),
    "south"   : (0,-1)
  }
  """
  directions = {
    "forward" : "right",
    "right"   : "right",
    "east"    : "right",
    "backwards": "left",
    "left"    : "left",
    "west"    : "left",
    "upward"  : "up",
    "north"   : "up",
    "downwards": "down",
    "south"   : "down"
  }

  matching_directions = [value for key, value in directions.items() if direction in key]

  if matching_directions:
    return matching_directions[0]
  else:
    return False


def check_ambigous_subfunction(sem_role_labels, sentence):
    if sem_role_labels:
        sem_role_labels1 = sem_role_labels[0]
        for word in sentence.split():
            if word.lower() == 'left':
                if 'A1' not in sem_role_labels1:
                    sem_role_labels1['A1'] = word
                else:
                    temp = sem_role_labels1['A1']
                    sem_role_labels1['AM-TMP'] = temp + " " + word
                    del sem_role_labels1['A1']
            if word.lower() == 'north':
                if 'A1' not in sem_role_labels1 and 'A4' not in sem_role_labels1:
                    sem_role_labels1['A1'] = word
        sem_role_labels = {k: sem_role_labels1[k] for k in sorted(sem_role_labels1)}
    else:
        for word in sentence.split():
            if word.lower() == 'jump':
                sem_role_labels.append({'V': word})
                return sem_role_labels[0]
    return sem_role_labels

def check_ambigous_words(pos_labels, sem_role_labels, sentence):
    if len(sem_role_labels) != len(sentence.split()) and pos_labels != []:
        sem_role_labels = [check_ambigous_subfunction(sem_role_labels, sentence)]
        check_ambigous_words(pos_labels[:-1], sem_role_labels, sentence)
    return sem_role_labels

def look_for_number(word, found_number, new_act, loop):
    if cardinal_number_to_int(word):
        if found_number:
            loop += " " + word
            new_act.set_loop(cardinal_number_to_int(loop))
        else:
            new_act.set_loop(cardinal_number_to_int(word))
            loop = word
            found_number = True
    elif word.isnumeric():
        new_act.set_loop(int(word))
        loop = word
        found_number = True
    elif multiplicative_adverbs_to_int(word):
        if found_number:
            loop += " " + word
            new_act.set_loop(multiplicative_adverbs_to_int(loop))
        else:
            new_act.set_loop(multiplicative_adverbs_to_int(word))
            loop = word
            found_number = True
    else:
        return False
    return found_number, new_act, loop

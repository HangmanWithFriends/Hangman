import random

letter_frequency = {
		'A' : 812,
		'B' : 149,
		'C' : 271,
		'D' : 432,
		'E' : 1202,
		'F' : 230,
		'G' : 203,
		'H' : 592,
		'I' : 731,
		'J' : 10,
		'K' : 69,
		'L' : 398,
		'M' : 261,
		'N' : 695,
		'O' : 768,
		'P' : 182,
		'Q' : 11,
		'R' : 602,
		'S' : 628,
		'T' : 910,
		'U' : 288,
		'V' : 111,
		'W' : 209,
		'X' : 17,
		'Y' : 211,
		'Z' : 7
	}

def choose_random_letter_weighted(letter_list):
    accum = 0
    reverse_dict = dict()
    for letter in letter_list:
        accum += letter_frequency[letter]
        reverse_dict[accum] = letter
    
    #choose a random float between 0 and letter
    r = random.randint(0, int(accum))
    while r not in reverse_dict:
        r += 1

    return reverse_dict[r]
    
def choose_highest_freq_letter(letter_list):
	sub_dict = dict()
	for letter in letter_list:
		sub_dict[letter] = letter_frequency[letter]

	vals = list(sub_dict.values())
	keys = list(sub_dict.keys())
	return keys[vals.index(max(vals))]

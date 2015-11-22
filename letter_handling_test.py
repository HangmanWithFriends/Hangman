import sys
import copy

sys.path.append('..')

from createMockDB import createMockDB
from game_handler import Game_Handler


def letter_in_word(letter):
	#try:
		if letter not in games['1']['correct_letters']:
			game_handler.guess_letter('1', letter)
			if letter in games['1']['correct_letters'] and letter not in games['1']['incorrect_letters']:
				print "> Letter in word, word incomplete: PASSED"
			else:
				print "> Letter in word, word incomplete: FAILED"
	#except:
	#	print ">> Letter in word, word incomplete: FAILED"


def letter_not_in_word(letter):
	#try:
		if letter not in games['1']['incorrect_letters']:
			game_handler.guess_letter('1', letter)
			if letter in games['1']['incorrect_letters'] and letter not in games['1']['correct_letters']:
				print "> Letter not in word, word incomplete: PASSED"
			else:
				print "> Letter not in word, word incomplete: FAILED"
	#except:
	#	print ">> Letter not in word, word incomplete: FAILED"


def letter_already_used(letter):
	#try:
		if letter in games['2']['correct_letters'] or letter in games['2']['incorrect_letters']:
			prev_incorrect_letters = copy.deepcopy(games['2']['incorrect_letters'])
			prev_correct_letters = copy.deepcopy(games['2']['correct_letters'])

			game_handler.guess_letter('2', letter)

			if prev_incorrect_letters == games['2']['incorrect_letters'] and prev_correct_letters == games['2']['correct_letters']:
				print "> Letter already used: PASSED"
			else:
				print "> Letter already used: FAILED"
	#except:
	#	print ">> Letter already used: FAILED"


def letter_completes_word(letter):
	#try:
		if letter not in games['2']['correct_letters']:
			game_handler.guess_letter('2', letter)

			if letter in games['2']['correct_letters'] and games['2']['win'] == '2':
				print "> Letter in word, completes word: PASSED" 
			else:
				print "> Letter in word, completes word: FAILED"
	#except:
	#	print ">> Letter in word, completes word: FAILED"


if __name__ == "__main__":
	mockDB = createMockDB()

	global games
	global game_handler
	games = mockDB["games"]
	game_handler = Game_Handler(mockDB)

	letter_in_word("I")
	letter_not_in_word("P")
	letter_already_used("E")
	letter_completes_word("T")
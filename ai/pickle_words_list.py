import pickle

new_file = open('ai_word_list.pickle', 'w')
new_words = []
for line in open('ai_word_list.txt', 'r'):
    line = line.rstrip()
    if len(line) > 4:
       new_words.append(line)

pickle.dump(new_words, new_file)    

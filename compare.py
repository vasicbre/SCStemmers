# this script reads two input files, splits the words and compares them

import sys


def compare(word1, word2):
    ''' Compares stemmed words '''
    # words are the same
    if word1 == word2:
        return 0

    # word1 is understemmed
    if word1 in word2:
        return 2

    # word2 is too stemmed
    return 1


stemmer_output = sys.argv[1]
manual_output = sys.argv[2]

stemmer_file = open(stemmer_output, 'r')
stemmer_lines = stemmer_file.readlines()
stemmer_file.close()

manual_file = open(manual_output, 'r')
manual_lines = manual_file.readlines()
manual_file.close()

# files must have exact same number of lines
assert(len(stemmer_lines) == len(manual_lines))

results = []
# loop through lines
for line_num in range(len(stemmer_lines)):
    stemmer_line = stemmer_lines[line_num]
    stemmer_words = stemmer_line.split(' ')
    manual_line = manual_lines[line_num]
    manual_words = manual_line.split(' ')
    # lines must be of same length
    assert(len(stemmer_words) == len(manual_words))

    # loop through words
    for word_num in range(len(stemmer_words)):
        # use strip to remove any leading or trailing
        # whitespace characters like endline for example
        # and convert to lowercase.
        stemmer_word = stemmer_words[word_num].strip().lower()
        manual_word = manual_words[word_num].strip().lower()
        results.append((
            stemmer_word,
            manual_word,
            compare(stemmer_word, manual_word)))

stats = [0,0,0]
# count stats
for elem in results:
    stats[elem[2]] += 1

total_words = len(results)
correct_pc = stats[0] / total_words
understemmed_pc = stats[1] / total_words
overstemmed_pc = stats[2] / total_words

print(f"Total words: {total_words}\n"
      f"Correctly stemmed: {round(correct_pc*100, 2)}%\n"
      f"Understemmed: {round(understemmed_pc*100, 2)}%\n"
      f"Overstemmed: {round(overstemmed_pc*100, 2)}%")

# convert results to list and sort based on stemmer output word
results = sorted(list(set(results)), key = lambda x: x[0])

# output to csv file
output_file = open('compare_output.csv', 'w')
for elem in results:
    output_file.write(f'{elem[0]},{elem[1]},{elem[2]}\n')

output_file.close()
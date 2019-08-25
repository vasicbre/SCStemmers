# This script reads two input files, splits the words and compares them.
# It expects following arguments:
#   1. Original file.
#   2. Stemmer output file.
#   3. Manual output file.
#   4. File to store comparison results.

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


def strip_multiple(*args):
    '''Strip leading and trailing whitespaces and convert to lowercase'''
    for arg in args:
        arg = arg.strip().lower()
        yield arg


if __name__ == "__main__":
    # parse args
    original_text = sys.argv[1]
    stemmer_output = sys.argv[2]
    manual_output = sys.argv[3]
    output_file = sys.argv[4]

    # read lines from the original file
    original_file = open(original_text, 'r')
    original_lines = original_file.readlines()
    original_file.close()

    # read lines from the stemmer output
    stemmer_file = open(stemmer_output, 'r')
    stemmer_lines = stemmer_file.readlines()
    stemmer_file.close()

    # read lines form the manual output
    manual_file = open(manual_output, 'r')
    manual_lines = manual_file.readlines()
    manual_file.close()

    # files must have exact same number of lines
    assert(len(original_lines) == len(manual_lines) == len(stemmer_lines))

    results = []
    # loop through lines
    for line_num in range(len(stemmer_lines)):
        # break original line
        original_line = original_lines[line_num]
        original_words = original_line.split(' ')

        # break stemmer line
        stemmer_line = stemmer_lines[line_num]
        stemmer_words = stemmer_line.split(' ')

        # break manual line
        manual_line = manual_lines[line_num]
        manual_words = manual_line.split(' ')

        # lines must be of same length
        assert(len(stemmer_words) == len(manual_words) == len(original_words))

        # loop through words
        for word_num in range(len(stemmer_words)):
            # use strip to remove any leading or trailing
            # whitespace characters like endline for example
            # and convert to lowercase.
            original_word, stemmer_word, manual_word = strip_multiple(
                original_words[word_num], stemmer_words[word_num], manual_words[word_num])

            results.append((
                original_word,
                stemmer_word,
                manual_word,
                compare(stemmer_word, manual_word)))

    # count stats per token
    stats = [0, 0, 0]

    for elem in results:
        stats[elem[3]] += 1

    total_tokens = len(results)
    correct_pc = stats[0] / total_tokens
    understemmed_pc = stats[1] / total_tokens
    overstemmed_pc = stats[2] / total_tokens

    print(f"-- Stats per token --\n"
          f"Total tokens: {total_tokens}\n"
          f"Correctly stemmed: {round(correct_pc*100, 2)}%\n"
          f"Understemmed: {round(understemmed_pc*100, 2)}%\n"
          f"Overstemmed: {round(overstemmed_pc*100, 2)}%\n")

    # convert to set to remove duplicates
    results = list(set(results))

    # count stats per word
    stats = [0, 0, 0]

    for elem in results:
        stats[elem[3]] += 1

    total_tokens = len(results)
    correct_pc = stats[0] / total_tokens
    understemmed_pc = stats[1] / total_tokens
    overstemmed_pc = stats[2] / total_tokens

    print(f"-- Stats per word --\n"
          f"Total words: {total_tokens}\n"
          f"Correctly stemmed: {round(correct_pc*100, 2)}%\n"
          f"Understemmed: {round(understemmed_pc*100, 2)}%\n"
          f"Overstemmed: {round(overstemmed_pc*100, 2)}%")

    # convert results to list and sort based on stemmer output word
    results = sorted(list(set(results)), key=lambda x: x[0])

    # output to csv file
    output_file = open(output_file, 'w')
    for elem in results:
        output_file.write(f'{elem[0]},{elem[1]},{elem[2]},{elem[3]}\n')

    output_file.close()

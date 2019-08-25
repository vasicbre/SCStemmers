# This script reads two outputs from stemmers and finds regressed cases

import sys


def parse_results(lines):
    ret = []
    for line in lines:
        tokens = tuple(map(lambda x: x.strip(),line.split(',')))
        # parsers also output punctuation marks, so splitting by comma can
        # result in having more tokens which can be problem later in the
        # computation
        if len(tokens) == 4:
            ret.append(tokens)

    return ret


if __name__ == "__main__":
    # parse args
    first_filename = sys.argv[1]
    second_filename = sys.argv[2]

    # read contents of the first file
    first_file = open(first_filename, 'r')
    first_lines = first_file.readlines()
    first_file.close()

    # read contents of the second file
    second_file = open(second_filename, 'r')
    second_lines = second_file.readlines()
    second_file.close()

    # number of lines must be the same
    assert(len(first_lines) == len(second_lines))

    first_results = parse_results(first_lines)
    second_results = parse_results(second_lines)

    # find regressions
    regressions = []
    for i in range(len(first_results)):
        if first_results[i][3] == '0' and second_results[i][3] != '0':
            regressions.append(i)

    print('-- Regressions --')
    for i in regressions:
      print (first_results[i])
      print (second_results[i])

    # find improvements
    improvements = []
    for i in range(len(first_results)):
        if first_results[i][3] != '0' and second_results[i][3] == '0':
            improvements.append(i)

    print('-- Improvements --')
    for i in improvements:
      print (first_results[i])
      print (second_results[i])

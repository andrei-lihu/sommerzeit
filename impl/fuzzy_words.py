import phonetics
import numpy as np


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    return matrix[size_x - 1, size_y - 1]


def similarity(word1, word2):
    nysiis1 = phonetics.nysiis(word1)
    nysiis2 = phonetics.nysiis(word2)
    nysiis_distance = levenshtein(nysiis1, nysiis2)

    metaphone1 = phonetics.metaphone(word1)
    metaphone2 = phonetics.metaphone(word2)
    metaphone_distance = levenshtein(metaphone1, metaphone2)

    dmetaphone1 = phonetics.dmetaphone(word1)
    dmetaphone2 = phonetics.dmetaphone(word2)
    dmetaphone_distance = levenshtein(dmetaphone1, dmetaphone2)

    # return a linear combination of these distances
    return nysiis_distance * 0.2 + metaphone_distance * 0.4 + dmetaphone_distance * 0.6

"""
Project 4
The first two of functions will return matrices that we will use in computing the alignment of two sequences.
The last two of functions will return global and local alignments of two input sequences based on a provided alignment matrix.
"""
import random

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    This function builds a scoring matrix as a dictionary of dictionaries
    :param alphabet: a set of characters
    :param dash_score: score for any entry indexed by one or more dashes
    :param diag_score:  score for the remaining diagonal entries
    :param off_diag_score:s core for the remaining off-diagonal entries
    :return: a dictionary of dictionaries whose entries are indexed by pairs of characters in alphabet plus '-'
    """
    matrix_dict = {}
    new_alphabet = set(alphabet)
    new_alphabet.add('-')
    for char1 in new_alphabet:
        matrix_dict[char1] = {}
        for char2 in new_alphabet:
            if char1 == '-' or char2 == '-':
                matrix_dict[char1][char2] = dash_score
            elif char1 == char2:
                matrix_dict[char1][char2] = diag_score

            else:
                matrix_dict[char1][char2] = off_diag_score
    return matrix_dict

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    :param seq_x and seq_y: two sequences sharing a common alphabet
    :param scoring_matrix: scoring matrix for seq_x and seq_y
    :param global_flag:  a global alignment matrix or a local one
    :return: an alignment matrix
    """
    num_x = len(seq_x) + 1
    num_y = len(seq_y) + 1
    scores = [[0 for _ in range(num_y)] for _ in range(num_x)]
    for idx_x in range(1, num_x):
        scores[idx_x][0] = scores[idx_x - 1][0] + scoring_matrix[seq_x[idx_x - 1]]['-']
        if not global_flag:
            if scores[idx_x][0] < 0:
                scores[idx_x][0] = 0
    for idx_y in range(1, num_y):
        scores[0][idx_y] = scores[0][idx_y - 1] + scoring_matrix['-'][seq_y[idx_y - 1]]
        if not global_flag:
            if scores[0][idx_y] < 0:
                scores[0][idx_y] = 0
    for idx_x2 in range(1, num_x):
        for idx_y2 in range(1, num_y):
            possible_list = []
            possible_list.append(scores[idx_x2 - 1][idx_y2 - 1] + scoring_matrix[seq_x[idx_x2 -1]][seq_y[idx_y2 - 1]])
            possible_list.append(scores[idx_x2 - 1][idx_y2] + scoring_matrix[seq_x[idx_x2 -1 ]]['-'])
            possible_list.append(scores[idx_x2][idx_y2 - 1] + scoring_matrix['-'][seq_y[idx_y2 - 1]])
            scores[idx_x2][idx_y2] = max(possible_list)
            if not global_flag:
                if scores[idx_x2][idx_y2] < 0:
                    scores[idx_x2][idx_y2] = 0
    return scores

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    This function computes a global alignment of seq_x and seq_y
    :param seq_x and seq_y: two sequences sharing a common alphabet
    :param scoring_matrix: scoring matrix for seq_x and seq_y
    :param alignment_matrix: a global alignment matrix of seq_x and seq_y
    :return: a tuple of the form (score, align_x, align_y)
    """
    idx_x = len(seq_x)
    idx_y = len(seq_y)
    align_x = ''
    align_y = ''
    while idx_x != 0 and idx_y != 0:
        if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y - 1] + scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]:
            align_x = seq_x[idx_x - 1] + align_x
            align_y = seq_y[idx_y - 1] + align_y
            idx_x -= 1
            idx_y -= 1
        else:
            if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]]['-']:
                align_x = seq_x[idx_x - 1] + align_x
                align_y = '-' + align_y
                idx_x -= 1
            else:
                align_x = '-' + align_x
                align_y = seq_y[idx_y - 1] + align_y
                idx_y -= 1
    while idx_x != 0:
        align_x = seq_x[idx_x - 1] + align_x
        align_y = '-' + align_y
        idx_x -= 1
    while idx_y != 0:
        align_x = '-' + align_x
        align_y = seq_y[idx_y - 1] + align_y
        idx_y -= 1
    return (alignment_matrix[len(seq_x)][len(seq_y)], align_x, align_y)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    This function computes a local alignment of seq_x and seq_y
    :param seq_x and seq_y: two sequences sharing a common alphabet
    :param scoring_matrix: scoring matrix for seq_x and seq_y
    :param alignment_matrix: a local alignment matrix of seq_x and seq_y
    :return: a tuple of the form (score, align_x, align_y)
    """
    #  If the local alignment matrix has more than one entry that has the maximum value,
    # any entry with maximum value may be used as the starting entry.
    max_list = [(0, 0, 0)]
    height = len(alignment_matrix)
    width = len(alignment_matrix[0])
    for row in range(height):
        for col in range(width):
            if alignment_matrix[row][col] > max_list[0][0]:
                max_list = [(alignment_matrix[row][col], row, col)]
            elif alignment_matrix[row][col] == max_list[0][0]:
                max_list.append((alignment_matrix[row][col], row, col))
    (score, idx_x, idx_y) = random.choice(max_list)

    # similar to global alignment but stop the traceback when the first entry with value 0 is encountered
    align_x = ''
    align_y = ''
    while idx_x != 0 and idx_y != 0 and alignment_matrix[idx_x][idx_y] != 0:
        if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y - 1] + scoring_matrix[seq_x[idx_x - 1]][seq_y[idx_y - 1]]:
            align_x = seq_x[idx_x - 1] + align_x
            align_y = seq_y[idx_y - 1] + align_y
            idx_x -= 1
            idx_y -= 1
        else:
            if alignment_matrix[idx_x][idx_y] == alignment_matrix[idx_x - 1][idx_y] + scoring_matrix[seq_x[idx_x - 1]]['-']:
                align_x = seq_x[idx_x - 1] + align_x
                align_y = '-' + align_y
                idx_x -= 1
            else:
                align_x = '-' + align_x
                align_y = seq_y[idx_y - 1] + align_y
                idx_y -= 1

    return (score, align_x, align_y)

# # Test
# sm = build_scoring_matrix(set(['a', 'b', 'c']), 10, 4, -6)
# seq_x = 'abc'
# seq_y = 'cba'
# amT = compute_alignment_matrix(seq_x, seq_y, sm, True)
# amF = compute_alignment_matrix(seq_x, seq_y, sm, False)
# print 'Global Alignment:'
# for line in amT:
#     print line
# print compute_global_alignment(seq_x, seq_y, sm, amT)
# print 'Local Alignment:'
# for line in amF:
#     print line
# print compute_local_alignment(seq_x, seq_y, sm, amF)
#
# a = {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}
# bsm = build_scoring_matrix(set(['A', 'C', 'T', 'G']), 6, 2, -4)
# for line in a.items():
#     print line
# print '----------------'
# for line in bsm.items():
#     print line
# print a == bsm
# cam = compute_alignment_matrix('ATG', 'ACG', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, True)
#
# alphabet = set([])
# for i in range(97, 123):
#     alphabet.add(chr(i))
# cla_sm = build_scoring_matrix(alphabet, 2, -1, -1)
# seq_x = 'happypedestrianwalker'
# seq_y = 'sadpedesxtriandriver'
# cla_am = compute_alignment_matrix(seq_x, seq_y, cla_sm, False)
# # expect_am =  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 5, 4, 3, 2, 1, 0, 0, 0], [0, 0, 0, 2, 2, 5, 7, 6, 5, 4, 3, 2, 1], [0, 0, 0, 1, 4, 4, 6, 6, 5, 4, 3, 2, 1], [0, 0, 0, 0, 3, 6, 6, 5, 5, 4, 3, 2, 1], [0, 0, 0, 0, 2, 5, 5, 8, 7, 6, 5, 4, 3], [0, 0, 0, 0, 1, 4, 4, 7, 10, 9, 8, 7, 6], [0, 0, 0, 0, 0, 3, 3, 6, 9, 9, 8, 7, 6], [0, 0, 0, 0, 0, 2, 2, 5, 8, 11, 10, 9, 8], [0, 0, 0, 0, 0, 1, 1, 4, 7, 10, 13, 12, 11]]
# cla = compute_local_alignment(seq_x, seq_y, cla_sm, cla_am)
# print cla

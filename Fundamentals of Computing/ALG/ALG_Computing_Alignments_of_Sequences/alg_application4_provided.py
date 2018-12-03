"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2
import time
import pickle
if DESKTOP:
    import matplotlib.pyplot as plt
    import ALG_Matrix_and_Alignment_Functions as student
else:
    import simpleplot
    import userXX_XXXXXXX as student


# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code: read netfile

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)

    # read in files as string
    words = word_file.read()

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list



########################################################
# download net files to desktop
def download(name, url):
    file = urllib2.urlopen(url).read()
    fhand = open(name, "wb")
    fhand.write(file)
    fhand.close()

# Names for data files
D_PAM50 = 'pam50.txt'
D_HUMAN_EYELESS = 'human_eyeless_protein.txt'
D_FRUITFLY_EYELESS = 'fruitfly_eyeless_protein.txt'
D_CONSENSUS_PAX = 'consensus_pax.txt'
D_WORD_LIST = 'word_list.txt'

def run_download():
    """
    download data from certain url
    """
    download(D_PAM50, PAM50_URL)
    download(D_HUMAN_EYELESS, HUMAN_EYELESS_URL)
    download(D_FRUITFLY_EYELESS, FRUITFLY_EYELESS_URL)
    download(D_CONSENSUS_PAX, CONSENSUS_PAX_URL)
    download(D_WORD_LIST, WORD_LIST_URL)

# run_download()

def desktop_read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = open(filename, 'rb')
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def desktop_read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = open(filename, 'rb')
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def desktop_read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = open(filename, 'rb')

    # read in files as string
    words = word_file.read()

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


###############################################
# Part 1: Genomics
# read url files

# human_eyeless_protein = read_protein(HUMAN_EYELESS_URL)
# fruitfly_eyeless_protein = read_protein(FRUITFLY_EYELESS_URL)
# consensus_pax = read_protein(CONSENSUS_PAX_URL)
# pam50 = read_scoring_matrix(PAM50_URL)
# print len(consensus_pax)

# read desktop files

human_eyeless_protein = desktop_read_protein(D_HUMAN_EYELESS)
fruitfly_eyeless_protein = desktop_read_protein(D_FRUITFLY_EYELESS)
consensus_pax = desktop_read_protein(D_CONSENSUS_PAX)
pam50 = desktop_read_scoring_matrix(D_PAM50)
word_list = desktop_read_words(D_WORD_LIST)

def corresponding_percentage(seq1, seq2):
    """
    seq1 and seq2: two strings with same length
    :return: percentage of corresponding elements in the sequences or None if the length of strings are different
    """
    if len(seq1) != len(seq2):
        return None
    length = len(seq1)
    correspond_num = 0
    for idx in range(length):
        if seq1[idx] == seq2[idx]:
            correspond_num += 1
    return 100.0 * correspond_num / length

def run_question1_3():
    """
    # question 1 -3
    """
    # Compute the local alignments of the sequences of HumanEyelessProtein and FruitflyEyelessProtein
    local_alignment_matrix = student.compute_alignment_matrix(human_eyeless_protein, fruitfly_eyeless_protein, pam50, False)
    local_alignment = student.compute_local_alignment(human_eyeless_protein, fruitfly_eyeless_protein, pam50, local_alignment_matrix)
    (local_score, local_human_alignment, local_fruitfly_alignment) = local_alignment
    print 'score: ', local_score
    print 'human eyeless alignment: ', local_human_alignment
    print 'fruit fly eyeless alignment: ', local_fruitfly_alignment
    # Compare each of the two sequences of the local alignment to consensus sequence.
    # delete dashes in local alignment
    lha_nodash = local_human_alignment.replace('-', '')
    lffa_nodash = local_fruitfly_alignment.replace('-', '')
    # compute global alignment for local human-consensus PAX
    global_alignment_matrix_hc = student.compute_alignment_matrix(lha_nodash, consensus_pax, pam50, True)
    global_alignment_hc = student.compute_global_alignment(lha_nodash, consensus_pax, pam50, global_alignment_matrix_hc)
    # compute global alignment for local fruitfly-consensus PAX
    global_alignment_matrix_ffc = student.compute_alignment_matrix(lffa_nodash, consensus_pax, pam50, True)
    global_alignment_ffc = student.compute_global_alignment(lffa_nodash, consensus_pax, pam50, global_alignment_matrix_ffc)
    print 'local human vs. consensus PAX: ', corresponding_percentage(global_alignment_hc[1], global_alignment_hc[2])
    print 'local fruit fly vs. consensus PAX: ', corresponding_percentage(global_alignment_ffc[1], global_alignment_ffc[2])

# run_question1_3()

# question 4-6
def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Note: local alignment
    seq_x, seq_y: two strings
    :param scoring_matrix: a scoring matrix
    :param num_trials: number of trials
    :return: a dictionary that represents an un-normalized distribution generated
    """
    scoring_distribution = {}
    list_y = list(seq_y)
    for _ in range(num_trials):
        random.shuffle(list_y)
        rand_y = ''.join(list_y)
        local_am = student.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        score = student.compute_local_alignment(seq_x, rand_y, scoring_matrix, local_am)[0]
        scoring_distribution[score] = scoring_distribution.get(score, 0) + 1
    return scoring_distribution

def run_question4():
    """
    save the score_dict and plot the score-distribution bar plot
    """
    num_trials = 1000
    time.clock()
    score_dict = generate_null_distribution(human_eyeless_protein, fruitfly_eyeless_protein, pam50, num_trials)
    savefile = open('score_dict.pkl', 'wb')
    pickle.dump(score_dict, savefile)
    savefile.close()
    print "Time cost: ", int(time.clock()) / 60, 'mins ', int(time.clock()) % 60, 'secs'
    x = []
    y = []
    for key, value in score_dict.items():
        x.append(key)
        y.append(1.0 * value / num_trials)
    plt.bar(x, y, width = 0.5, yerr  = 0.0001)
    plt.xlabel('Scores of local alignment of HumanEyelessProtein and shuffled FruitflyEyelessProtein')
    plt.ylabel('Fraction of total trials')
    plt.title('Distribution of scores with 1000 trials')
    plt.show()

# bar_plot()

def compute_z_zone(score_dict, s):
    """
    score_dict{score: appearence times}
    z_zone z = (s - u) / sigma
    s is the score of the local alignment for the human eyeless protein and the fruitfly eyeless protein
    u is the mean of score_dict
    sigma is the standard deviation of score_dict
    """
    sum_value = 0
    num = 0
    for key, value in score_dict.items():
        sum_value += key * value
        num += value
    u = 1.0 * sum_value / num

    square_deviation = 0
    for key, value in score_dict.items():
        square_deviation += (key - u) ** 2 * value
    sigma = (square_deviation / num) ** 0.5
    return u, sigma, (s - u) / sigma

def run_question5():
    """
    load score_dict and compute z-zone
    """
    openfile = open('score_dict.pkl', 'rb')
    score_dict = pickle.load(openfile)
    print sum(score_dict.values())
    print score_dict
    openfile.close()
    print compute_z_zone(score_dict, 875)

# run_question5()

######################################################
# Part 2 Words with spelling mistakes.

# build scoring matrix for edit distance
alphabet = set([])
for i in range(97, 123):
    alphabet.add(chr(i))
edit_distance_sm = student.build_scoring_matrix(alphabet, 2, 1, 0)

def edit_distance(word_a, word_b):
    """
    return edit distance of word a and word b
    """
    edit_distance_am = student.compute_alignment_matrix(word_a, word_b, edit_distance_sm, True)
    score = student.compute_global_alignment(word_a, word_b, edit_distance_sm, edit_distance_am)[0]
    return len(word_a) + len(word_b) - score


def check_spelling(checked_word, dist, word_list):
    """
    :param dist: allowed edit distance
    returns: a set of all words that are within edit distance dist of the string checked_word.
    """
    similar_word_list = set([])
    for word in word_list:
        if abs(len(word) - len(checked_word)) > dist:
            continue
        if edit_distance(word, checked_word) <= dist:
            similar_word_list.add(word)

    return similar_word_list

def run_question8():
    list1 = check_spelling('humble', 1, word_list)
    print 'humble: ', list1
    print 'length: ', len(list1)
    list2 = check_spelling('firefly', 2, word_list)
    print 'firefly: ', list2
    print 'length: ', len(list2)

# print edit_distance('kitten', 'sitting')
run_question8()
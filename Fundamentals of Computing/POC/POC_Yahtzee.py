"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    scores = {}
    for die in hand:
        if not scores.has_key(die):
            scores[die] = 0
        scores[die] += die
    return max(scores.values())


# print score((1,2,14,7,6,6))

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    total_score = 0
    dice = tuple([die + 1 for die in range(num_die_sides)])
    free_dices = gen_all_sequences(dice, num_free_dice)
    for die in free_dices:
        hand = die + held_dice
        total_score += score(hand)
    return 1.0 * total_score / len(free_dices)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    { {} }

    # 'a' is comming
    { {} } + {{'a'}}

    # 'b' is comming
    { {},{'a'} } + { {'b'},{'a','b'} }

    # 'c' is comming
    { {},{'a'},{'b'},{'a','b'} } + { {'c'}, {'a','c'},{'b','c'},{'a','b','c'} }
    """
    hand_list = [()]
    for item in hand:
        temp_list = []
        for prev_item in hand_list:
            prev_item = list(prev_item)
            prev_item.append(item)
            temp_list.append(tuple(prev_item))
        hand_list += temp_list
    sorted_list = [tuple(sorted(hands)) for hands in hand_list]
    return set(sorted_list)

# print gen_all_holds((3, 2, 3))
# for item in gen_all_holds((1, 2, 3)):
#     print item


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_sequences = gen_all_holds(hand)
    held_dice = ()
    max_expected_val = 0
    for sequence in all_sequences:
        seq_expected_val = expected_value(sequence, num_die_sides, len(hand) - len(sequence))
        if max_expected_val < seq_expected_val:
            held_dice = sequence
            max_expected_val = seq_expected_val
    return (max_expected_val, held_dice)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)








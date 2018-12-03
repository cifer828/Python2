import random
def my_gen_all_holds(hand):
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

all_case = [i + 1 for i in range(8)]

for test_case in gen_all_sequences(all_case, 6):
    sorted_case = sorted(test_case)
    if my_gen_all_holds(sorted_case) != gen_all_holds(sorted_case):
        print sorted_case
        print my_gen_all_holds(sorted_case)
        print gen_all_holds(sorted_case)


# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
tips = ["New Deal?", "Hit or Stand?"]
player_score = 0
dealer_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.card_list = []	# create Hand object

    def __str__(self):
        string = ""
        for card in self.card_list:
            string += " " + str(card)
        return "Hand contains" + string # return a string representation of a hand

    def add_card(self, card):
        self.card_list.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        ace_num = 0
        for card in self.card_list:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                ace_num += 1
        if ace_num == 0:
            return value
        elif value + 10 < 21:
            return value + 10
        else:
            return value
        # compute the value of the hand, see Blackjack video

    def draw(self, canvas, pos):
        step = 0
        for card in self.card_list:
            new_pos = (pos[0] + step * (CARD_SIZE[0] + 30), pos[1])
            step += 1
            card.draw(canvas, new_pos)  # draw a hand on the canvas, use the draw method for cards


# define deck class
class Deck:
    def __init__(self):
        self.card_list = []
        for suit in SUITS:
            for rank in RANKS:
                self.card_list.append(Card(suit, rank))
                # create a Deck object

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.card_list)    # use random.shuffle()

    def deal_card(self):
        return self.card_list.pop()	 # deal a card object from the deck

    def __str__(self):
        string = ""
        for card in self.card_list:
            string += " " + str(card)
        return "Deck contains" + string    # return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, dealer_score
    global player_hand, dealer_hand, deck
    if in_play:
        dealer_score += 1
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    # your code goes here

    in_play = True

def hit():
    global in_play, dealer_score, outcome
    # if the hand is in play, hit the player
    if not in_play:
        return
    player_hand.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        outcome = "You went busted and lose."
        in_play = False
        dealer_score += 1

def stand():
    global in_play, player_score, dealer_score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if not in_play:
        return
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
    # assign a message to outcome, update in_play and score
    in_play = False
    if dealer_hand.get_value() > 21:
        outcome = "Dealer went busted, You win!"
        player_score += 1
    else:
        if dealer_hand.get_value() >= player_hand.get_value():
            dealer_score += 1
            outcome = "You lose."
        else:
            player_score += 1
            outcome = "You win!"

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    player_hand.draw(canvas, [100, 400])
    dealer_hand.draw(canvas, [100, 200])
    canvas.draw_text("Dealer", [100, 180], 30, "Black")
    canvas.draw_text("Player", [100, 380], 30, "Black")
    canvas.draw_text(outcome, [250, 180], 30, "Black")
    canvas.draw_text("Blackjack", [100, 100], 50, 'Aqua')
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [136, 248], CARD_BACK_SIZE)
        tip = tips[1]
    else:
        tip = tips[0]
    canvas.draw_text(tip, [250, 380], 30, "Black")
    canvas.draw_text("Player_score: " + str(player_score), [400, 100], 30, "Black")
    canvas.draw_text("Dealer_score: " + str(dealer_score), [400, 70], 30, "Black")

#initialization frame
frame = simplegui.create_frame("Blackjack", 700, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
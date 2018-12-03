# input will come from buttons and an input field
# all output for the game will be printed in the console


#########################################################
# Just for saving script.
# IDE is CodeSkulptor.
# simplegui is not include in python desktop

import simplegui
import random

num_range = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    global chances
    if num_range == 100:
        chances = 7
    elif num_range == 1000:
        chances = 10
    secret_number = random.randrange(0, num_range)
    print 
    print "New game. Range is from 0 to", num_range
    print "Number of remaining guesses is", chances


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global num_range
    num_range = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global num_range
    num_range = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global chances
    guess = int(guess)
    print     
    print "Guess was ", guess
    
    #Calculate remaining guesses. If you have no chance, start a new game
    chances -= 1
    print "Number of remaining guesses is",chances
    if chances == 0:
        print "You run out of guesses. The number was", secret_number
        new_game()    
        return 
    
    #compare guess to secret_number
    if guess < secret_number:
        print "Hihger!"
    elif guess > secret_number:
        print "Lower!"
    elif guess == secret_number:
        print "Correct!"
        new_game()
    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0,100)", range100, 200)
frame.add_button("Range is [0,1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
frame.start()
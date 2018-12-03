# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    #Restart a game
    global exposed, exposed1, exposed2, card_list, state, set_text
    card_list = range(8) + range(8)
    exposed = [False for _ in range(len(card_list))]
    exposed1 = "inf"
    exposed2 = "inf"
    state = 0
    set_text = 0
    random.shuffle(card_list)

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed1, exposed2, state, set_text, label
    clicking_card = pos[0] / 50
    if not exposed[clicking_card]:
        exposed[clicking_card] = True
        if state == 0:
            exposed1 = clicking_card
            state = 1
        elif state == 1:
            exposed2 = clicking_card
            state = 2
            set_text += 1
        else:
            if card_list[exposed1] != card_list[exposed2]:
                exposed[exposed1] = False
                exposed[exposed2] = False
            exposed1 = clicking_card
            state = 1



# cards are logically 50x100 pixels in size
def draw(canvas):
    label.set_text("Turn = " + str(set_text))
    win = True
    for win_or_not in exposed:
        win = win and win_or_not
    if win:
        label_win.set_text("Good Job!")
    else:
        label_win.set_text("")
    for idx in range(len(card_list)):
        if exposed[idx]:
            canvas.draw_text(str(card_list[idx]), (idx * 50 +10 , 70), 60, "Black")
            canvas.draw_polyline([[idx * 50, 0], [(idx + 1) * 50, 0], [(idx + 1) * 50, 100], [idx * 50, 100]], 2, "Yellow")
        else:
            canvas.draw_polygon([[idx * 50, 0], [(idx + 1) * 50, 0], [(idx + 1) * 50, 100], [idx * 50, 100]], 2, "Yellow", "Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.set_canvas_background("White")
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")
label_win = frame.add_label("")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
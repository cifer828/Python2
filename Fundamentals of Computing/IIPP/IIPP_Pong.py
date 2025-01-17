# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0.0, 0.0]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240)
        ball_vel[1] = -random.randrange(60, 180)
    if direction == LEFT:
        ball_vel[0] = -random.randrange(120, 240)
        ball_vel[1] = -random.randrange(60, 180)

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global GAME_RUNNING
    GAME_RUNNING = False
    spawn_ball(None)
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    score1 = 0
    score2 = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0] / 60
    ball_pos[1] += ball_vel[1] / 60
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = -ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'Red', 'Red')

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel / 4 - HALF_PAD_HEIGHT > 0 and paddle1_pos + paddle1_vel / 4 + HALF_PAD_HEIGHT < HEIGHT:
        paddle1_pos += paddle1_vel

    if paddle2_pos + paddle2_vel / 4 - HALF_PAD_HEIGHT > 0 and paddle2_pos + paddle2_vel / 4 + HALF_PAD_HEIGHT < HEIGHT:
        paddle2_pos += paddle2_vel

    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT],
                        [0, paddle1_pos + HALF_PAD_HEIGHT],
                        [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],
                        [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT]],
                        1, 'white', 'white')
    canvas.draw_polygon([[WIDTH, paddle2_pos - HALF_PAD_HEIGHT],
                        [WIDTH, paddle2_pos + HALF_PAD_HEIGHT],
                        [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT],
                        [WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT]],
                        1, 'white', 'white')

    # determine whether paddle and ball collide
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT and ball_pos[1] > paddle1_pos - HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        else:
            spawn_ball(RIGHT)
            score2 += 1
    if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT and ball_pos[1] > paddle2_pos - HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        else:
            spawn_ball(LEFT)
            score1 += 1
    # draw scores
    canvas.draw_text(str(score1), [150, 50], 30, 'White')
    canvas.draw_text(str(score2), [450, 50], 30, 'White')

def keydown(key):
    global paddle1_vel, paddle2_vel, GAME_RUNNING
    if GAME_RUNNING == False:
        spawn_ball(random.choice([LEFT, RIGHT]))
        GAME_RUNNING = True
    if chr(key) == 'W':
        paddle1_vel = -4
    if chr(key) == 'S':
        paddle1_vel = 4
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -4
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 4

def keyup(key):
    global paddle1_vel, paddle2_vel
    if chr(key) == 'W' or 'S':
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0

def button_handler():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', button_handler, 100)


# start frame
new_game()
frame.start()

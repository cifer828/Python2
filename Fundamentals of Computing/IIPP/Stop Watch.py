# template for "Stopwatch: The Game"
import simplegui

# define global variables
time = 0
interval = 100
integers = 0
tries = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(tenth_time):
    Min = tenth_time / 600
    sec = (tenth_time - Min * 600) / 10
    if sec < 10:
        str_sec = "0" + str(sec)
    else:
        str_sec = str(sec)
    tenth = tenth_time % 10
    return str(Min) + ":" + str_sec + ":" + str(tenth)


# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    global tries
    global is_running
    global integers
    if timer.is_running() == True:
        tries += 1
        if time % 10 == 0:
            integers += 1
    timer.stop()


def reset():
    global time
    global tries
    global integers
    time = 0
    timer.stop()
    tries = 0
    integers = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time += 1

# define draw handler
def draw(canvas):
    str_time = format(time)
    str_reflexes = str(integers) + '/' + str(tries)
    canvas.draw_text(str_time, [100, 150], 36, "White")
    canvas.draw_text(str_reflexes , [250, 30], 30, "Blue")

# create frame
frame = simplegui.create_frame("Home", 300, 300)

# register event handlers
timer = simplegui.create_timer(interval, tick)
frame.set_draw_handler(draw)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

# start frame
frame.start()
# Please remember to review the grading rubric

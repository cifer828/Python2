# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

LEFT = 1
RIGHT = 2
UP = 3

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.acc = 0.1
        self.friction = 0.02

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self,canvas):
        self.update()
        if self.thrust:
            self.image_center[0] = self.image_size[0] * 3 / 2
        else:
            self.image_center[0] = self.image_size[0] / 2
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
#        canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        self.angle += self.angle_vel
        #friction
        self.vel[0] *= 1- self.friction
        self.vel[1] *= 1- self.friction
        #accerlation
        if self.thrust:
            self.vel[0] += angle_to_vector(self.angle)[0] * self.acc
            self.vel[1] += angle_to_vector(self.angle)[1] * self.acc
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT

    def thrusting(self, thrusting):
        self.thrust = thrusting
        if thrusting:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()

    def shoot(self):
        cannon_pos = [self.pos[0] + self.radius * angle_to_vector(self.angle)[0],
                      self.pos[1] + self.radius * angle_to_vector(self.angle)[1]]
        cannon_vel = [self.vel[0] + 2 * angle_to_vector(self.angle)[0],
                      self.vel[1] + 2 * angle_to_vector(self.angle)[1]]
        a_missile = Sprite(cannon_pos, cannon_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)


    def turn(self, direction):
        if direction == LEFT:
            self.angle_vel = -0.05
        elif direction == RIGHT:
            self.angle_vel = 0.05
        elif not direction:
            self.angle_vel = 0


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self, canvas):
        self.update()
        if self.animated:
            self.age += 0.5
            current_index = (self.age % 64) // 1
            self.image_center = [self.image_center[0] + current_index * self.image_size[0], self.image_center[1]]
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
#        canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")

    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        self.age += 0.5
        return self.age >= self.lifespan

    def collide(self, other_object):
        distance = dist(self.pos, other_object.get_position())
        return distance < self.radius + other_object.get_radius()

# helper function for checking collision between group and object
def group_collide(group, other_object):
    flag = False
    for item in set(group):
        if item.collide(other_object):
            an_explosion = Sprite(item.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)
            group.remove(item)
            flag = True
    return flag

# helper function for checking collision between group and group
def group_group_collide(group1, group2):
    num = 0
    for item in set(group1):
        if group_collide(group2, item):
            group1.discard(item)
            num += 1
    return num


# helper function for drawing a group of objects
def process_sprite_group(group, canvas):
    for item in set(group):
        if item.update():
            group.remove(item)
    for an_item in group:
        an_item.draw(canvas)

# click handler for starting a new game
def click(pos):
    global started, timer, lives, score, my_ship
    # initialize ship position, lives and scores
    soundtrack.play()
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    lives = 3
    score = 0
    timer.start()
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True

def draw(canvas):
    global time, lives, score, started, rock_group, missile_group, timer
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # detect collision between missiles and rocks / rocks and ships
    if group_collide(rock_group, my_ship):
        lives -= 1
    score += group_group_collide(rock_group, missile_group) * 10

    # check lives
    if lives <= 0:
        started = False
        rock_group = set([])
        missile_group = set([])

    # draw lives and socres
    canvas.draw_text("Lives: " + str(lives), (20, 45), 20, 'White')
    canvas.draw_text("Scores: " + str(score), (WIDTH - 110, 45), 20, 'White')

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(explosion_group, canvas)

    # update ship and sprites
    my_ship.update()

    # start a new game
    if not started:
        timer.stop()
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())
        soundtrack.rewind()

def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.turn(LEFT)
    elif key == simplegui.KEY_MAP['right']:
        my_ship.turn(RIGHT)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrusting(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def keyup(key):
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        my_ship.turn(None)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrusting(False)

# timer handler that spawns a rock
def rock_spawner():
    pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    vel = [random.random() / 2, random.random() / 2]
    ang_vel = random.random() * random.choice([1, -1]) / 20
    if len(rock_group) < 12:
        a_rock = Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info)
        # make sure the rock isn't too close to my_ship
        if dist(pos, my_ship.get_position()) < a_rock.get_radius() + my_ship.get_radius() + 10:
            return
        rock_group.add(a_rock)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group= set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
from pygame import Surface, PixelArray
from pygame import transform


import computer


WIDTH = 800
HEIGHT = 800
GRID_SIZE = 4 # pixel size of one little square in the game grid


# convert pixel coordinates to grid coords
def screen_to_grid(x, y):
    return round(x / GRID_SIZE), round(y / GRID_SIZE)


trails = PixelArray(Surface(screen_to_grid(WIDTH, HEIGHT)))
bike1 = Actor('bike1')
bike2 = Actor('bike2')
bike1.colour = (252, 186, 3) # yellow / orange
bike2.colour = (0, 255, 255) # cyan

bike1.is_computer = False  # <-- human or AI
bike2.is_computer = True   # <-- human or AI


# maps a direction to (angle, velocity, reverse) tuple
directions = {
    'right': (0,   (GRID_SIZE, 0),  'left'),
    'up':    (90,  (0, -GRID_SIZE), 'down'),
    'left':  (180, (-GRID_SIZE, 0), 'right'),
    'down':  (270, (0, GRID_SIZE),  'up'),
}


# key controls, maps a key to (bike, direction) tuple
controls = {
    keys.UP:    (bike1, 'up'),
    keys.LEFT:  (bike1, 'left'),
    keys.DOWN:  (bike1, 'down'),
    keys.RIGHT: (bike1, 'right'),
    keys.W: (bike2, 'up'),
    keys.A: (bike2, 'left'),
    keys.S: (bike2, 'down'),
    keys.D: (bike2, 'right'),
}


def reset_bikes():
    trails.surface.fill((0, 0, 0)) # black
    
    bike1.pos = (WIDTH + GRID_SIZE) // 3, (HEIGHT + GRID_SIZE) // 3
    bike1.dead = False
    bike1.angle, bike1.velocity, bike1.reverse = directions['right']
    
    bike2.pos = (WIDTH + GRID_SIZE) // 3, 2 * (HEIGHT + GRID_SIZE) // 3
    bike2.dead = False
    bike2.angle, bike2.velocity, bike2.reverse = directions['right']


# Reset the bikes to start
reset_bikes()

##########
# update #
##########

def update():
    if bike1.dead or bike2.dead:
        return

    for bike in (bike1, bike2):
    
        x, y = bike.pos # old pixel coordinates
        i, j = screen_to_grid(x, y) # old grid coordinates
    
        if bike.is_computer:
            old_dir = directions[bike.reverse][2]
            new_dir = computer.calc_direction((i,j), old_dir, trails)
            if new_dir != bike.reverse:
                bike.angle, bike.velocity, bike.reverse = directions[new_dir]

        # move bike
        vx, vy = bike.velocity
        x += vx
        y += vy
        bike.pos = x, y # new pixel coordinates

        i, j = screen_to_grid(x, y) # new grid coordinates
        width, height = trails.shape

        if i < 0 or j < 0 or i >= width or j >= height: 
            # Out of bounds! we crashed
            bike.dead = True
            return
        trail_value = trails[i,j]

        if trail_value:
            # Crash: We've already set this grid square as a trail
            bike.dead = True
        else:
            trails[i,j]= bike.colour

########
# draw #
########

def draw():
    transform.scale(trails.surface, (WIDTH, HEIGHT), screen.surface)
    for bike in (bike1, bike2):
        if bike.dead:
            screen.draw.text(
                'YOU ARE DEREZZED!\nPRESS SPACE TO RESTART',
                center=(WIDTH // 2, 100),
                color=bike.colour,
                fontsize=50,
                fontname="tr2n"
            )
        else:
            bike.draw()

#############
# key press #
#############

def on_key_down(key):
    if bike1.dead or bike2.dead:
        if key is keys.SPACE:
            reset_bikes()

    elif key in controls:
        bike, direction = controls[key]
        if not bike.is_computer and direction != bike.reverse:
            bike.angle, bike.velocity, bike.reverse = directions[direction]
        

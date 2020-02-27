from pygame import PixelArray
import random


def calc_direction(pos, old_dir, trails):
    return collision_avoid(pos, old_dir, trails)
    
    
def dumb(pos, old_dir, trails):
    return 'up'
    
    
def randomly(pos, old_dir, trails):
    if random.random() < 0.1:
        return random.choice(['up', 'down', 'left', 'right'])
    else:
        return old_dir
        
        
def collision_avoid(pos, old_dir, trails):
    i,j = pos
    options = ['up', 'left', 'down', 'right']
    width, height = trails.shape
    
    if j == height-1 or trails[i,j+1] or old_dir == 'up':
        options.remove('down')
    if i == width - 1 or trails[i+1,j] or old_dir == 'left':
        options.remove('right')
    if j == 0 or trails[i,j-1] or old_dir == 'down':
        options.remove('up')
    if i == 0 or trails[i-1,j] or old_dir == 'right':
        options.remove('left')
        
    if old_dir in options and random.random() < 0.95:
        return old_dir
    if len(options) == 0:
        return old_dir
    return random.choice(options)
        
        
        

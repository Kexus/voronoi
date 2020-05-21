import pygame as pg
import numpy as np
import random

WINSIZE = [800, 800]

WHITE = (255,255,255,255)
BLACK = (0, 0, 0, 255)

def gencolor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b, 255)

def index_of_closest(point, locuses):
    min = np.linalg.norm(point - locuses[0])
    mindex = 0
    ds = [min]
    for i in range(1, len(locuses)):
        d = np.linalg.norm(point - locuses[i])
        ds.append(d)
        if min > d:
            min = d
            mindex = i
            
    out = [mindex]
    
    #check for ties
#    for i in range(len(ds)):
#        # epsilon?
#        if ds[i] == min and i != mindex:
#            out.append(i)
            
    return out
    
def main():
    colors = []
    locuses = []
    
    clock = pg.time.Clock()

    pg.init()
    screen = pg.display.set_mode(WINSIZE)
    
    pg.display.set_caption("Voronoi")

    screen.fill(BLACK)
    
    done = 0
    dirty = False
    while not done:
        if dirty:
            if len(locuses) != 0:
                for x in range(WINSIZE[0]):
                    for y in range(WINSIZE[1]):
                        indices = index_of_closest(np.array((x,y)), locuses)
                        if len(indices) > 1:
                            screen.set_at((x,y), WHITE)
                        else:
                            screen.set_at((x,y), colors[indices[0]])
                            
            # show locuses
            for l in locuses:
                pg.draw.circle(screen, WHITE, l, 5)
            dirty = False
                    
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break
            if e.type == pg.MOUSEBUTTONDOWN:
                locuses.append(np.array(pg.mouse.get_pos()))
                colors.append(gencolor())
                dirty= True

        clock.tick(60)
    pg.quit()

if __name__ == "__main__":
    main()
import pygame as pg
import numpy as np
import random
import threading
import time

WINSIZE = [800, 800]
GRAIN = 100

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

    return mindex

def color_rect(x_start, x_end, y_start, y_end, locuses, colors, screen, fork=False):

    if x_start == x_end and y_start == y_end:
        # this is a 1px region, so just color it
        screen.set_at((x_start, y_start), colors[index_of_closest(np.array((x_start, y_start)), locuses)])
    else:
        indices = [None, None, None, None]
        indices[0] = index_of_closest(np.array((x_start, y_start)), locuses)
        indices[1] = index_of_closest(np.array((x_start, y_end)), locuses)
        indices[2] = index_of_closest(np.array((x_end, y_end)), locuses)
        indices[3] = index_of_closest(np.array((x_end, y_start)), locuses)
        
        if indices[0] == indices[1] == indices[2] == indices[3]:
            pg.draw.rect(screen, colors[indices[0]], pg.Rect((x_start, y_start), (x_end-x_start+1, y_end-y_start+1)))
#            pg.display.update()
        elif x_end-x_start <= 2 or y_end-y_start <= 2:
#             screen.set_at((x_start, y_start), colors[indices[0]])
#             screen.set_at((x_start, y_end), colors[indices[1]])
#             screen.set_at((x_end, y_end), colors[indices[2]])
#             screen.set_at((x_end, y_start), colors[indices[3]])
            pg.draw.rect(screen, colors[indices[0]], pg.Rect((x_start, y_start), (x_end-x_start+1, y_end-y_start+1)))
        else:
            # divide region into quadrants and recursively color each one
            x_mid = x_start + (x_end-x_start)//2
            y_mid = y_start + (y_end-y_start)//2
            if fork:
                f0 = threading.Thread(target=color_rect, args=(x_start, x_mid, y_start, y_mid, locuses, colors, screen))
                f1 = threading.Thread(target=color_rect, args=(x_start, x_mid, y_mid+1, y_end, locuses, colors, screen))
                f2 = threading.Thread(target=color_rect, args=(x_mid+1, x_end, y_start, y_mid, locuses, colors, screen))
#                f3 = threading.Thread(target=color_rect, args=(x_mid+1, x_end, y_mid+1, y_end, locuses, colors, screen))
                f0.start()
                f1.start()
                f2.start()
                color_rect(x_mid+1, x_end, y_mid+1, y_end, locuses, colors, screen)
#                f3.start()
                f0.join()
                f1.join()
                f2.join()
#                f3.join()
            else:
                color_rect(x_start, x_mid, y_start, y_mid, locuses, colors, screen)
                color_rect(x_start, x_mid, y_mid+1, y_end, locuses, colors, screen)
                color_rect(x_mid+1, x_end, y_start, y_mid, locuses, colors, screen)
                color_rect(x_mid+1, x_end, y_mid+1, y_end, locuses, colors, screen)
            
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
                # old code to color each pixel individually
#                for x in range(WINSIZE[0]//GRAIN):
#                    for y in range(WINSIZE[1]//GRAIN):
#                        indices = index_of_closest(np.array((x*GRAIN,y*GRAIN)), locuses)
#                        if len(indices) > 1:
#                            screen.set_at((x,y), WHITE)
#                        else:
#                            pg.draw.rect(screen, colors[indices[0]], pg.Rect((x*GRAIN,y*GRAIN), (GRAIN,GRAIN)))
                t1 = time.time()
                color_rect(0, WINSIZE[0]-1, 0, WINSIZE[1]-1, locuses, colors, screen, fork=False)
                print(time.time() - t1)
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

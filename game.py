# standard lib
import random
import json
import pickle
import copy

# third-party lib
import numpy as np
from graphics import *

# local files
import board
import network
import data_loader


SIZE = 4


def main(train=False):
    if train:
        data = data_loader.load_data()
    else:
        data = []
    net = network.Network([16, 10, 4])
    #return
    alive = True
    b = board.Board(SIZE)
    """
    for text based game
    
    for row in b.get_array():
        print(row)
    """

    win = GraphWin("2048", 500, 500, autoflush=False)
    p = Point(50, 50)
    for row in b.get_array():
        for cell in row:
            r = Rectangle(p, Point(p.getX()+100, p.getY()+100))
            r.draw(win)
            if cell != 0:
                t = Text(Point(p.getX()+50, p.getY()+50), cell)
                t.draw(win)
            p.move(100, 0)
        p.move(-400, 100)

    # draw the score
    score = Text(Point(250, 25), "Score: {0}".format(0))
    score.draw(win)

    while alive:
        # pauses to get key press
        key = win.getKey()

        # keep a variable that holds the array before it is changed
        tmp = np.copy(b.get_array())

        # move depending on key press
        if key == "Up":
            b.move("up")
        elif key == "Left":
            b.move("left")
        elif key == "Down":
            b.move("down")
        elif key == "Right":
            b.move("right")
        elif key == "Escape":
            alive = False
            win.close()
        else:
            continue

        data.append([tmp, key])

        # checks whether board changed at all
        different = False
        for row in range(SIZE):
            for col in range(SIZE):
                if tmp[row][col] != b.get_array()[row][col]:
                    different = True
                    break
            if different:
                break

        # only update if the board changed
        if different:
            # new number generator
            rand_x = random.randint(0, SIZE - 1)
            rand_y = random.randint(0, SIZE - 1)
            while b.get_array()[rand_x][rand_y] != 0:
                rand_x = random.randint(0, SIZE - 1)
                rand_y = random.randint(0, SIZE - 1)
            rand_two = random.random()
            if rand_two < 0.95:
                b.get_array()[rand_x][rand_y] = 2
            else:
                b.get_array()[rand_x][rand_y] = 4

            """
            for text based game
            
            print("\n")
            # print array
            for row in b.get_array():
                print(row)
            """

            # erase all items on window
            for item in win.items[:]:
                item.undraw()

            score.setText("Score : {0}".format(b.score))
            score.draw(win)

            # restart drawing from upper left corner
            p = Point(50,50)
            # draw a rectangle for each element in the array
            # draw a number for each non zero element in the array
            for row in b.get_array():
                for cell in row:
                    r = Rectangle(p, Point(p.getX() + 100, p.getY() + 100))
                    r.draw(win)
                    if cell != 0:
                        t = Text(Point(p.getX() + 50, p.getY() + 50), cell)
                        t.draw(win)
                    # move over by a rectangle width
                    p.move(100, 0)
                # reset back four rectangles and down 1 to draw next row
                p.move(-400, 100)
            # update at 30 frames per sec if animation is used
            update(30)

        # pause so it doesn't overrun, unnecessary for gui since it pauses for
        # each keystroke
        #time.sleep(.2)
        else:
            # check if you can make anymore moves
            directions = ["up", "left", "down", "right"]
            for dir in directions:
                tmp_b = copy.deepcopy(b)
                tmp_b.move(dir)
                different = False
                for row in range(SIZE):
                    for col in range(SIZE):
                        if tmp[row][col] != tmp_b.get_array()[row][col]:
                            different = True
                            break
                    if different:
                        break
                if different:
                    break
            if not different:
                alive = False
    if not train:
        file_num = 0
        while os.path.exists("datafile{0}".format(file_num)):
            file_num += 1
        data_loader.save_data(data, 'datafile{0}'.format(file_num))



main()

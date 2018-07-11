import board
import numpy as np
import copy
import random
import data_loader
from graphics import *
import time
import network


def simulate(path):

    data = data_loader.load_data(path)

    win = GraphWin("2048", 500, 500, autoflush=False)

    i = 0
    while i < len(data):
        entry = data[i]
        arr = entry[0]

        arr = data_loader.decode(arr)

        # erase all items on window
        for item in win.items[:]:
            item.undraw()

        # restart drawing from upper left corner
        p = Point(50, 50)
        # draw a rectangle for each element in the array
        # draw a number for each non zero element in the array
        for row in arr:
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

        i += 1

        time.sleep(.2)
    win.getMouse()
    win.close()


"""
epochs is number of times the network is trained
num is the number of files or "batches" that are made per iteration
"""
def generate_sim(epochs, num, folder, nn=None, train=False):

    if nn:
        net = nn
    else:
        net = network.Network([16, 200, 100, 4])
        """
        data = data_loader.load_data("damngoodgame")
        net.stochastic_gradient_descent([data], [np.ndarray([1])], 10, 0.001)
        nn = net
        """
    end_arr = []

    for i in range(num):
        b = board.Board(4)
        data = []
        alive = True
        start = time.time()
        while alive:
            tmp = copy.deepcopy(b.get_array())

            # eliminate invalid moves given board config
            directions = ["up", "down", "left", "right"]
            choices = [0, 1, 2, 3]
            valid = [b.is_valid_move(direc) for direc in directions]

            if nn:
                output = net.feedforward(b.get_array().flatten())
                outMax = 0
                for node in range(len(output)):
                    if output[node] > output[outMax] and valid[node]:
                        outMax = node
                outMax = random.choices(choices, valid*output)
                outMax = outMax[0]
            else:
                outMax = np.random.randint(0, 4)



            direction = [0 for i in range(4)]
            direction[outMax] = 1
            if outMax == 0:
                b.move("up")
            if outMax == 1:
                b.move("down")
            elif outMax == 2:
                b.move("left")
            elif outMax == 3:
                b.move("right")

            # checks whether board changed at all
            different = False
            for row in range(4):
                for col in range(4):
                    if tmp[row][col] != b.get_array()[row][col]:
                        different = True
                        break
                if different:
                    break

            if different:
                start = time.time()
                # new number generator
                rand_x = np.random.randint(0, 4)
                rand_y = np.random.randint(0, 4)
                while b.get_array()[rand_x][rand_y] != 0:
                    rand_x = np.random.randint(0, 4)
                    rand_y = np.random.randint(0, 4)
                rand_two = random.random()
                if rand_two < 0.95:
                    b.get_array()[rand_x][rand_y] = 2
                else:
                    b.get_array()[rand_x][rand_y] = 4
                data.append([copy.deepcopy(b.get_array()), direction])
            else:
                end = time.time()
                if end-start > 1:
                    alive = False

            # check if you can make anymore moves
            if b.is_game_over():
                break

        data_loader.save_data(data, "{0}/file{1}".format(folder, i))

        if len(data):
            end_arr.append(data[-1][0])
    print("batch {0}: generated".format(10 - epochs))
    if train:
        end_score = []
        # for each file, calculate an end score and save them to a list
        # then standardize the scores so they have a mean of 1 and
        for arr in end_arr:
            end_score.append(arr.sum())

        end_score = (end_score-np.mean(end_score))/np.std(end_score)

        # train net over newly made data
        training_data = []
        j = 0
        while os.path.exists("batches{0}/file{1}".format(10-epochs, j)):
            training_data.append(data_loader.load_data(
                "batches{0}/file{1}".format(10-epochs, j)))
            j += 1

        net.stochastic_gradient_descent(training_data, end_score, 5, 0.002)

        if not epochs:
            generate_sim(epochs - 1, num, "result", net, False)
        else:
            generate_sim(epochs - 1, num, "batches{0}".format(10-epochs+1), net, True)


#generate_sim(10, 1000, "batches0", None, True)
#for i in range(30):
#    simulate("batches1/file{0}".format(i))
simulate("batches{0}/file{1}".format(1, 517))
#simulate("over100/file1")
#simulate("bestAIgame")

import pickle
import numpy as np

def save_data(data, path):

    file = open(path, 'wb')
    for entry in data:
        for thing in entry:
            if isinstance(thing, np.ndarray):
                thing = encode(thing)
            else:
                if thing == "Up":
                    thing = np.array([1, 0, 0, 0])
                elif thing == "Down":
                    thing = np.array([0, 1, 0, 0])
                elif thing == "Left":
                    thing = np.array([0, 0, 1, 0])
                elif thing == "Right":
                    thing = np.array([0, 0, 0, 1])
            pickle.dump(thing, file)
    file.close()


def load_data(path):

    data = []
    file = open(path, 'rb')
    try:
        while True:
            entry = []
            entry.append(pickle.load(file).flatten())
            entry.append(pickle.load(file))
            data.append(entry)
    except EOFError:
        pass
    return data

def decode(thing):
    thing = np.reshape(thing, (4, 4))
    for row in range(len(thing)):
        for col in range(len(thing[0])):
                # 17 is 15 + 2 and 15 is the max power of the highest
                # possible value in 2048 given a 4x4 grid and 2 is the power
                # of 4, which is, in the perfect situation, the highest low
                # number you could have
                thing[row][col] = np.round(np.exp2(thing[row][col]*17.0))
                if thing[row][col] == 1:
                    thing[row][col] = 0
    return thing.astype(int)


def encode(thing):
    thing = thing.astype(float)
    for row in range(len(thing)):
        for col in range(len(thing[0])):
            if thing[row][col] != 0:
                # 17 is 15 + 2 and 15 is the max power of the highest
                # possible value in 2048 given a 4x4 grid
                thing[row][col] = np.log2(thing[row][col]) / 17.0
    return thing.flatten()


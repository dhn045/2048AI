import random
import numpy as np
import copy

DOUBLE = 2

class Board:

    def __init__(self, size):
        # initial score is 0
        self.score = 0

        # the array's dimensions are size by size
        self.size = size
        # create a zero filled array of size by size
        self.array = np.array([[0] * size for i in range(size)])

        # generated random "coordinates" to place the first two random twos
        x1 = random.randint(0, size-1)
        y1 = random.randint(0, size-1)
        x2 = random.randint(0, size-1)
        y2 = random.randint(0, size-1)

        # keep generating if they overlap
        while x1 == x2 and y1 == y2:
            x2 = random.randint(0, size-1)
            y2 = random.randint(0, size-1)

        # set the random coordinates to twos
        self.array[x1][y1] = 2
        self.array[x2][y2] = 2

    """
    get_array
    
    returns the objects array
    """
    def get_array(self):
        return self.array

    """
    move
    
    combines all values in the array and then calls shift to shift them
    """
    def move(self, direction):
        if direction == "up":
            # goes top down for each column to combine
            for col in range(0, self.size):
                for row in range(0, self.size):

                    # we only want non zero values to combine
                    if self.array[row][col] == 0:
                        continue

                    # by the time we get to here, tmp_row will be the row
                    # below the first non zero value in the column
                    tmp_row = row + 1

                    # keep searching for a non zero value in the column
                    # as long as tmp_row doesn't exceed size, otherwise
                    # there is only one nonzero value in the column so it
                    # just be shifted later, also using short circuiting
                    # logic to make sure tmp_row is never out of bounds
                    while tmp_row < self.size and self.array[tmp_row][col] == 0:
                        tmp_row += 1

                    # if tmp_row exceeds size, then there is no other
                    # non zero value in the column, so break from loop
                    if tmp_row >= self.size:
                        break

                    # if they were the same value, then combine them
                    if self.array[row][col] == self.array[tmp_row][col]:
                        self.array[row][col] *= DOUBLE
                        self.array[tmp_row][col] = 0
                        self.score += self.array[row][col]

        elif direction == "down":
            # goes bottom up for each column to combine
            for col in range(0, self.size):

                # range to iterate should start from bottom
                # up and decrementing
                for row in range(self.size - 1, -1, -1):

                    # we only want non zero values to combine
                    if self.array[row][col] == 0:
                        continue

                    # by the time we get to here, tmp_row will be the row
                    # above the last non zero value in the column
                    tmp_row = row - 1

                    # keep searching for a non zero value in the column
                    # as long as tmp_row doesn't exceed size, otherwise
                    # there is only one nonzero value in the column so it
                    # just be shifted later, also using short circuiting
                    # logic to make sure tmp_row is never out of bounds
                    while tmp_row >= 0 and self.array[tmp_row][col] == 0:
                        tmp_row -= 1

                    # if tmp_row is below 0, then there is no other
                    # non zero value in the column, so break from loop
                    if tmp_row < 0:
                        break

                    # combine same values
                    if self.array[row][col] == self.array[tmp_row][col]:
                        self.array[row][col] *= DOUBLE
                        self.array[tmp_row][col] = 0
                        self.score += self.array[row][col]

        elif direction == "left":
            # goes left to right to combine, since we are shifted in the
            # "negative" direction as the up, its the same code
            # but adjusted in the horizontal direction
            for row in range(0, self.size):
                for col in range(0, self.size):

                    # we only want nonzero values
                    if self.array[row][col] == 0:
                        continue

                    # by the time this is reached, it will be the
                    # cell just right of the leftmost non zero value
                    tmp_col = col + 1

                    # keep searching for a non zero value in the column
                    # as long as tmp_row doesn't exceed size, otherwise
                    # there is only one nonzero value in the column so it
                    # just be shifted later, also using short circuiting
                    # logic to make sure tmp_row is never out of bounds
                    while tmp_col < self.size and self.array[row][tmp_col] == 0:
                        tmp_col += 1

                    # if tmp_col is above size, then there is no other
                    # non zero value in the column, so break from loop
                    if tmp_col >= self.size:
                        break

                    # combine same values
                    if self.array[row][col] == self.array[row][tmp_col]:
                        self.array[row][col] *= DOUBLE
                        self.array[row][tmp_col] = 0
                        self.score += self.array[row][col]

        elif direction == "right":
            # goes left to right to combine, since we are shifted in the
            # "positive" direction as the down, its the same code
            # but adjusted in the horizontal direction
            for row in range(0, self.size):

                # range to iterate should start from right to left and
                # decrementing
                for col in range(self.size - 1, -1, -1):

                    # we only want non zero values
                    if self.array[row][col] == 0:
                        continue

                    # by the time this is reached, it will be the
                    # cell just left of the rightmost non zero value
                    tmp_col = col - 1

                    # keep searching for a non zero value in the column
                    # as long as tmp_row doesn't exceed size, otherwise
                    # there is only one nonzero value in the column so it
                    # just be shifted later, also using short circuiting
                    # logic to make sure tmp_row is never out of bounds
                    while tmp_col >= 0 and self.array[row][tmp_col] == 0:
                        tmp_col -= 1

                    # if tmp_col is below 0, then there is no other
                    # non zero value in the row, so break from loop
                    if tmp_col < 0:
                        break

                    # combine same values
                    if self.array[row][col] == self.array[row][tmp_col]:
                        self.array[row][col] *= DOUBLE
                        self.array[row][tmp_col] = 0
                        self.score += self.array[row][col]

        self.shift(direction)

    """
    shift
    
    function that takes a board where everything is already combined, and
    shifts to a certain direction to that there are no empty spaces
    in that direction
    """
    def shift(self, direction):
        # collapses each column as a vector upwards
        if direction == "up":
            for col in range(0, self.size):
                working_col = []

                # append all non zero values in the column
                for row in range(0, self.size):
                    if self.array[row][col] != 0:
                        working_col.append(self.array[row][col])

                # append necessary amount of zeros based on size and
                # how many non zero values there were
                for i in range(len(working_col), self.size):
                    working_col.append(0)

                # replace the column with the shifted vector
                self.array[:, col] = working_col

        # collapses each column as a vector downwards
        elif direction == "down":
            for col in range(0, self.size):
                working_col = []

                # append all non zero values in the column
                for row in range(0, self.size):
                    if self.array[row][col] != 0:
                        working_col.append(self.array[row][col])

                # reverse vector to "prepend" zeros since we shift down
                working_col.reverse()

                # append necessary amount of zeros based on size and
                # how many non zero values there were
                for i in range(len(working_col), self.size):
                    working_col.append(0)

                # re-reverse to get the vector we want
                working_col.reverse()

                # replace column with shifted vector
                self.array[:, col] = working_col

        # collapses each row as a vector leftward
        elif direction == "left":
            for row in range(0, self.size):
                working_row = []

                # append all non zero values in the row
                for col in range(0, self.size):
                    if self.array[row][col] != 0:
                        working_row.append(self.array[row][col])

                # append necessary amount of zeros based on size and
                # how many non zero values there were
                for i in range(len(working_row), self.size):
                    working_row.append(0)

                # replace row with shifted row vector
                self.array[row] = working_row

        # collapes each row as a vector rightward
        elif direction == "right":
            for row in range(0, self.size):
                working_row = []

                # append all non zero values in the row
                for col in range(0, self.size):
                    if self.array[row][col] != 0:
                        working_row.append(self.array[row][col])

                # reverse to "prepend" zeros by reversing then appending
                working_row.reverse()

                # append necessary amount of zeros based on size and
                # how many non zero values there were
                for i in range(len(working_row), self.size):
                    working_row.append(0)

                # re-reverse to get vector we want
                working_row.reverse()

                # replace row with shifted row vector
                self.array[row] = working_row

    def is_game_over(self):
        directions = ["up", "down", "left", "right"]
        result = []
        for direc in directions:
            tmp = copy.deepcopy(self)
            tmp.move(direc)
            different = False
            for row in range(4):
                for col in range(4):
                    if self.array[row][col] != tmp.get_array()[row][col]:
                        different = True
                        break
                if different:
                    break
            if different:
                break
        return not different

    """
    returns the move if valid, nothing otherwise
    """
    def is_valid_move(self, move):
        tmp = copy.deepcopy(self)
        tmp.move(move)
        changed = False
        for row in range(4):
            for col in range(4):
                if self.array[row][col] != tmp.get_array()[row][col]:
                    changed = True
                    break
            if changed:
                break
        return int(changed)

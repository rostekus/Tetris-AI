from fileinput import filename
from re import L
from shutil import move
import numpy as np
import pandas as pd
import time


LENGHT = 100000


class Augmentation:
    """
    A class for augmentation of the collected dataset of
    tetris' grids
    ...
    Methods
    -------
    create_holes(mov, filenames,aug = False)
        Function for creating holes in tetris grid.
        Then it saves augmented data to csv file.
    shifting()
        Fucntion shifts every grid downwards 3 times.
    """

    def __init__(self, grids, moves, heights):
        self.grids = grids
        self.moves = moves
        self.heights = heights

    def get_height(self, grid):
        locked = np.zeros(10)
        for i, column in enumerate(grid.T):
            j = 19
            height = 0
            while column[j] and j >= 0:
                height += 1
                j -= 1
            if locked[i] != height:
                locked[i] = height
        return locked

    def create_holes(self):
        moves = ["ROT", "RIGHT", "LEFT", "DOWN"]
        iter = 0
        for mov in moves:

            df = pd.read_csv(self.moves)
            df[df["move"] == mov]

            indeces = np.array(df[df.move == mov].index)

            grids = np.loadtxt(self.grids)
            files_num = 0

            size = grids.size
            n = int(size / (20 * 10))
            grids.resize((n, 20, 10))
            df_aug = pd.DataFrame(index=np.arange(0, LENGHT), columns=["move"])
            df_aug.iloc[:] = mov
            grids_aug = np.zeros(shape=(LENGHT, 200))
            for i, grid in enumerate(grids[indeces]):
                grid_holes = grid.copy()
                heights = self.get_height(grid)
                for i, height in enumerate(heights):
                    if height > 3:
                        for h in range(0, int(height) - 1):
                            grid_holes = grid.copy()
                            grid_holes.T[i][19 - h] = 0

                            grids_aug[iter] = grid_holes.flatten()
                            # grids_aug[iter] = grid_holes
                            iter += 1
                            if iter == LENGHT:
                                assert grids_aug.shape[0] == grids_aug.shape
                                name = time.time()
                                with open(
                                    f"./data/aug/{name}-grids.csv", "a"
                                ) as outfile:
                                    for slice_2d in grids_aug[:iter]:
                                        np.savetxt(
                                            outfile,
                                            slice_2d,
                                            fmt="%i",
                                            delimiter=",",
                                        )
                                df_aug[: iter + 1].to_csv(
                                    f"./data/aug/{name}-moves.csv", index=False
                                )
                                iter = 0
                                grids_aug = np.zeros(shape=(LENGHT, 200))
                                print("saved")
                                files_num += 1
        name = time.time()
        with open(f"./data/aug/{name}-grids.csv", "a") as outfile:
            for slice_2d in grids_aug[:iter]:
                np.savetxt(outfile, slice_2d, fmt="%i", delimiter=",")
        df_aug[:iter].to_csv(f"./data/aug/{name}-moves.csv", index=False)


    # def delete_object(self, grid):
    #     indeces = []
    #     for x, column in enumerate(grid.T):
    #         for y, block in enumerate(column):
    #             height = 0
    #             if block == 1:
    #                 while grid[y][x] == 1:
    #                     height += 1
    #                     if height < 4:
    #                         break
    #                     elif height == 19:
    #                         break
    #                     y += 1
    #                 else:
    #                     indeces.append((x, y))

    def shifting_down(self):
        grids = np.loadtxt(self.grids, delimiter=",")
        size = grids.size
        n = int(size / (20 * 10))
        grids.resize((n, 20, 10))
        df = pd.read_csv(self.moves)
        df_aug = pd.DataFrame(
            index=np.arange(
                LENGHT,
            ),
            columns=["move"],
        )
        grids_aug = np.zeros(shape=(LENGHT, 20, 10))
        id = 0
        for iter, grid in enumerate(grids):
            for i, row in enumerate(grid[::-1], 1):
                procent = np.sum(row, axis=0)
                procent /= 10
                if procent >= 0.60:
                    new_grid = np.zeros((20, 10))
                    new_grid[i:20] = grid[: 20 - i]
                    grids_aug[id] = new_grid

                    df_aug.iloc[id] = df.iloc[iter]
                    id += 1
                    if id % 500 == 0:
                        print("500")
                    if id == LENGHT:
                        name = time.time()
                        print("saved")

                        with open(f"./data/aug/{name}-grids.csv", "a") as outfile:
                            for slice_2d in grids_aug[:iter]:
                                np.savetxt(outfile, slice_2d, fmt="%i", delimiter=",")
                        df_aug[:iter].to_csv(
                            f"./data/aug/{name}-moves.csv", index=False
                        )
                        id = 0
                        grids_aug = np.zeros(shape=(LENGHT, 20, 10))
                else:
                    break

        name = time.time()
        with open(f"./data/aug/{name}-grids.csv", "a") as outfile:
            for slice_2d in grids_aug[:iter]:
                np.savetxt(outfile, slice_2d, fmt="%i", delimiter=",")
        df_aug[:iter].to_csv(f"./data/aug/{name}-moves.csv", index=False)

    def save(self, df):
        df.to_csv(f"data/{time.time()}.csv", index=False)
        df = pd.DataFrame(index=np.arange(0, 500), columns=("grid", "move"), )
        return df, iter

    def get_indeces(self, grid):
        X, Y = np.where(grid == 1)
        indeces = []
        for x, y in zip(X, Y):
            indeces.append((y, x))
        return indeces

    def flip(self):
        grids = np.loadtxt(self.grids, delimiter=",")
        grids = grids.reshape((int(grids.shape[0] / 20), 20, 10))
        moves = pd.read_csv(self.moves)
        heights = pd.read_csv(self.heights)
        flipped_grids = np.zeros(grids.shape)
        flapped_moves = pd.DataFrame(np.zeros(heights.shape))
        for i, grid in enumerate(grids):
            flipped_grids[i] = np.fliplr(grid)
            if moves["move"].iloc[i] == "RIGHT":
                flapped_moves.iloc[i] = "LEFT"
            elif moves["move"].iloc[i] == "LEFT":
                flapped_moves.iloc[i] = "RIGHT"
            else:
                flapped_moves.iloc[i] = moves["move"].iloc[i]
        with open('./data/heightsv2.csv', "w") as outfile:
            np.savetxt(outfile, heights, fmt="%i", delimiter=",")
            outfile.write(b"\n")
            np.savetxt(outfile, np.fliplr(heights), fmt="%i", delimiter=",")
        
        moves_cot = pd.concat([moves, flapped_moves], ignore_index=True)
        moves_cot.to_csv("./data/movesv2.csv")

        with open("./data/gridsv2", "w") as outfile:
            for slice_2d in grids:
                np.savetxt(outfile, slice_2d, fmt="%i", delimiter=",")
            for slice_2d in flipped_grids:
                np.savetxt(outfile, slice_2d, fmt="%i", delimiter=",")

    def get_indeces(self, grid, heights):
        for i, height in enumerate(heights):
            grid.T[i][19-int(height):20] = 0
        X, Y = np.where(grid == 1)
        indeces = []
        for x, y in zip(X, Y):
            indeces.append((y, x))
        return indeces

    def shifting_up(self):
        moves_aug = pd.DataFrame(index=np.arange(0, LENGHT), columns=["move"])
        heights_aug = heights_aug =np.zeros(shape=(LENGHT, 10), dtype =np.int8).astype(np.short)
        grids_aug = np.zeros(shape=(LENGHT ,20, 10)).astype(np.short)

        grids = np.loadtxt(self.grids, delimiter=",",dtype =np.int8).astype(np.short)
        grids = grids.reshape((int(grids.shape[0] / 20), 20, 10))
        moves = pd.read_csv(self.moves)
        heights = np.loadtxt(self.heights, delimiter=',')

        iter = 0
        delete = []
        for item , (grid, move, height) in enumerate(zip(grids, moves['move'], heights)):
            try:
                max_y = 19-np.max(heights[0])
                indeces = self.get_indeces(grid.copy(), height)
                min_y = max(indeces, key = lambda x: x[1])
                diff = max_y -min_y[1]
            except:
                delete.append(item)
                continue
            else:
                if diff <= 0:
                    continue

                for additional_height in range(1, int(diff)-2):
                    grid_up = np.zeros((20, 10))
                    for x,y in indeces:
                        grid_up[y][x] =1
                    for j, col in enumerate(grid_up.T):
                        col[20-int(height[j])-additional_height:20] = 1
                    for i in range(10):
                        for h in range(int((height+additional_height-1)[i])):
                            grid_hole = grid_up.copy()
                            grid_hole[19-h][i] = 0
                            grids_aug[iter] = grid_hole
                            moves_aug['move'][iter] = move
                            heights_aug[iter] = height + 1
                            iter += 1
                            if iter == LENGHT:
                                name = time.time()
                                with open(f"./data/aug/{name}-grids.csv", "a") as outfile:
                                    for slice_2d in grids_aug[:iter]:
                                        np.savetxt(outfile, slice_2d, fmt="%i", delimiter=",")
                                moves_aug[:iter].to_csv(f"./data/aug/{name}-moves.csv", index=False)
                                with open(f"./data/aug/{name}-heights.csv", "a") as outfile:
                                    np.savetxt(outfile, heights_aug[:iter], fmt="%i", delimiter=",")
                                iter = 0
                                moves_aug = pd.DataFrame(index=np.arange(0, LENGHT), columns=["move"])
                                heights_aug =np.zeros(shape=(LENGHT, 10)).astype(np.short)
                                grids_aug = np.zeros(shape=(LENGHT ,20, 10)).astype(np.short)

        name = time.time()
        with open(f"./data/aug/{name}-grids.csv", "a") as outfile:
            for slice_2d in grids_aug[:iter]:
                np.savetxt(outfile, slice_2d, fmt="%i", delimiter=",")
        moves_aug[:iter].to_csv(f"./data/aug/{name}-moves.csv", index=False)
        with open(f"./data/aug/{name}-heights.csv", "a") as outfile:
                                    np.savetxt(outfile, heights_aug[:iter], fmt="%i", delimiter=",")
        
        grids = np.delete(grids,delete)
        moves.drop(delete, inplace=True)
        heights = np.delete(heights, delete)
        with open(f"./data/grids.csv", "a") as outfile:
            for slice_2d in grids:
                np.savetxt(outfile, slice_2d, fmt="%i", delimiter=",")
        moves.to_csv(f"./data/moves.csv", index=False)
        with open(f"./data/aug/heightsV2.csv", "a") as outfile:
            np.savetxt(outfile, heights_aug[:iter], fmt="%i", delimiter=",")

def main():
        au = Augmentation('./data/grids.csv','./data/moves.csv' ,'./data/heights.csv')
        au.flip()
        au.create_holes()
if __name__ == "__main__":
   main()
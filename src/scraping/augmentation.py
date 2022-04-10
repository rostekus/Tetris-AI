from fileinput import filename
from shutil import move
import numpy as np
import config
import pandas as pd
import os.path
from sklearn.utils import shuffle

import time

import re
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

    def create_holes(self, mov, filenames,aug = False):
        moves = ['ROT', 'RIGHT', 'LEFT', 'DOWN']
        iter =0
        for filename in  filenames:
            for mov in moves:
                
                df  = pd.read_csv(f'./data/move.csv')
                df[df["move"] == mov]

                indeces  = np.array(df[df.move ==mov].index)
                
                grids = np.loadtxt(f'./data/grids.csv')
                files_num = 0 

                size = grids.size
                n = int(size/(20*10))
                grids.resize((n,20,10))
                df_aug = pd.DataFrame(index=np.arange(0, LENGHT), columns=["move"])
                df_aug.iloc[:] = mov
                grids_aug = np.zeros(shape=(LENGHT,200))
                for i, grid in enumerate(grids[indeces]):
                    grid_holes = grid.copy()
                    heights = self.get_height(grid)
                    # max_height = max(heights)
                    # min_height = min(heights)
                    for i, height in enumerate(heights):
                        if height >3:
                            for h in range(0, int(height)-1):
                                grid_holes = grid.copy()
                                grid_holes.T[i][19 - h] = 0
                                
                                grids_aug[iter] = grid_holes.flatten()
                                # grids_aug[iter] = grid_holes
                                iter +=1
                                if iter == LENGHT:
                                    name = time.time()
                                    with open(f'./data/aug/{name}-grids.csv', 'a') as outfile:
                                        for slice_2d in grids_aug[:iter]:
                                            np.savetxt(outfile, slice_2d, fmt='%i',delimiter=',')
                                    df_aug[:iter+1].to_csv(f'./data/aug/{name}-moves.csv',index = False )
                                    iter = 0
                                    grids_aug = np.zeros(shape=(LENGHT,200))
                                    print('saved')
                                    files_num +=1
        name = time.time()
        with open(f'./data/aug/{name}-grids.csv', 'a') as outfile:
            for slice_2d in grids_aug[:iter]:
                np.savetxt(outfile, slice_2d, fmt='%i',delimiter=',')
        df_aug[:iter].to_csv(f'./data/aug/{name}-moves.csv',index = False )

    def delete_object(self, grid):
        indeces = []
        for x , column in enumerate(grid.T):
            for y, block in enumerate(column):
                height  = 0
                if block ==1:
                    while grid[y][x] == 1:
                        height +=1
                        if height < 4:
                            break
                        elif height == 19:
                            break
                        y += 1
                    else:
                        indeces.append((x,y))
    
    def shifting(self):
        
        grids = np.loadtxt('/data/grids.csv')
        size = grids.size
        n = int(size/(20*10))
        grids.resize((n,20,10))
        df  = pd.read_csv('/data/move.csv')
        df_aug = pd.DataFrame(index=np.arange(0, LENGHT), columns=["move"])
        grids_aug = np.zeros(shape=(LENGHT,20,10))
        id  = 0
        for iter, grid in enumerate(grids):
            first_three_row = grid[17:20]
            for i, row in enumerate(first_three_row ,1):
                procent = np.sum(row,axis = 0)
                procent /=(10)
                if procent >= 0.75:
                    new_grid = np.zeros((20,10))
                    new_grid[i:20] = grid[:20-i]
                    grids_aug[id] = new_grid
                    df_aug.iloc[id] = df.move.iloc[iter]
                    id += 1
                    if id == LENGHT:
                        name = time.time()
                        with open(f'./data/aug/{name}-grids.csv', 'a') as outfile:
                            for slice_2d in grids_aug[:iter]:
                                np.savetxt(outfile, slice_2d, fmt='%i',delimiter=',')
                        df_aug[:iter+1].to_csv(f'./data/aug/{name}-moves.csv',index = False )
                        id = 0
                        grids_aug = np.zeros(shape=(LENGHT,20,10))
         
        name = time.time()
        with open(f'./data/aug/{name}-grids.csv', 'a') as outfile:
            for slice_2d in grids_aug[:iter]:
                np.savetxt(outfile, slice_2d, fmt='%i',delimiter=',')
        df_aug[:iter].to_csv(f'./data/aug/{name}-moves.csv',index = False )


    def save(self, df):
        df.to_csv(f"data/{time.time()}.csv", index=False)
        df = pd.DataFrame(index=np.arange(0, 500), columns=("grid", "move"))
        return df, iter

    def get_indeces(self, grid):
        X, Y = np.where(grid == 1)
        indeces = []
        for x, y in zip(X, Y):
            indeces.append((y, x))
        return indeces


if __name__ == "__main__":
    au = Augmentation()
    files = os.listdir('./data')
    pattern  = r"(.+)-grids.csv"
    filenames = []
    for file in files:
        find_name = re.search(pattern, file, re.IGNORECASE)
        if find_name:
            filenames.append(find_name.group(1))
    moves = ['ROT', 'RIGHT', 'LEFT', 'DOWN']
    filenames =[0]
    au.create_holes(move,filenames)
    au.shifting()


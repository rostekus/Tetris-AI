from fileinput import filename
import os
import pandas as pd
import re
import glob


class DataBase:
    """
    A class for augmentation of the collected dataset of
    tetris' grids
    ...
    Methods
    -------
    merge(filenames, output = 'grids.csv')
        Function merges all numpy csv filenames
    merge_final(self, grids, moves)
        Function merges final two files for moves
        and grids
    merge_moves(filenames, output = 'moves.csv')
        Function merges all pandas csv filenames
    get(dir)
        Returns all filenemas of grids and moves
    """

    def merge_grids(self, filenames, output="grids.csv"):

        with open(output, "w") as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

    def merge_final(self, grids, moves):
        df = pd.concat(map(pd.read_csv, moves), ignore_index=True)
        df.to_csv("./data/finalmoves.csv", index=False)
        self.merge_grids(grids, "./data/finalgrids.csv")

    def merge_moves(self, filenames, output="moves.csv"):
        df = pd.concat(map(pd.read_csv, filenames), ignore_index=True)
        df.to_csv("output")

    def get(self, dir):
        files = os.listdir(dir)
        import re

        pattern_move = r"(.+)-moves.csv"
        pattern_grid = r"(.+)-grids.csv"
        filemoves = []
        filegrids = []
        for file in files:
            find_move = re.search(pattern_move, file, re.IGNORECASE)
            if find_move:
                filemoves.append(f"{dir}{find_move.group(1)}-moves.csv")

            find_grid = re.search(pattern_grid, file, re.IGNORECASE)
            if find_grid:
                filegrids.append(f"{dir}{find_move.group(1)}-grids.csv")

        return filegrids, filemoves

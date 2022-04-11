from fileinput import filename
import os
import pandas as pd

class DataBase():
    """
    A class for augmentation of the collected dataset of
    tetris' grids
    ...
    Methods
    -------
    merge(filenames, name)
        Function merges all csv filenames 
    merge_final(name):
        Fucntion merges final two files for moves
        and grids
    merge_aug(self)
        merges augemented data to one file   
    """

    def merge(self, filenames, name):

        with open(f'./data/{name}', 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

    def merge_final(self,name):
        filenames = ['data/aug_moves.csv','data/final_moves.csv']
        df = pd.concat(map(pd.read_csv, filenames),ignore_index=True)
        df.to_csv('./data/moves.csv')
        filenames = ['data/aug_grids.csv', 'data/new_grid.csv']
        self.merge(filenames, name)

    def merge_aug(self):
        files = os.listdir('data/aug')
        import re
        pattern  = r"(.+)-moves.csv"
        filenames = []
        for file in files:
            find_name = re.search(pattern, file, re.IGNORECASE)
        if find_name:
             filenames.append(f'./data/aug/{find_name.group(1)}-moves.csv')
    df = pd.concat(map(pd.read_csv, filenames),ignore_index=True)
    df.to_csv('./data/aug_moves.csv')

def main():
    db  = DataBase()
    pattern  = r"(.+)-grids.csv"
    filenames = []
    for file in files:
        find_name = re.search(pattern, file, re.IGNORECASE)
        if find_name:
                filenames.append(f'./data/aug/{find_name.group(1)}-grids.csv') 
    db.merge(filenames,'aug_grids.csv')


if __name__ == "__main__":
    main()




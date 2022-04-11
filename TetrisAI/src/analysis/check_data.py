import pandas as pd
import numpy as np
import cv2
import pandas as pd
from os import listdir
from os.path import isfile, join
class Check:
    def __init__(self, path = './data'):
        self.path =  path


    def foo(self,x):
        try:
            return np.array(eval(x.replace("\n", ",").replace(".", ",")))
        except:
            pass

    def get_grid(self, df):
        # only ROT
        df = df[df['move'] == 'ROT']
        df['grid'] = df['grid'].apply(lambda x : self.foo(x))
        return df.iterrows()
    
    def get_files(self):
        onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        return onlyfiles




    def check_moves(self):
        # files = self.get_files()
        files = '1648588019.3197172.csv'
        for file in files:
            df = pd.read_csv(join('./data', file))
            iter_df = self.get_grid(df)
            for i in range(len(df)):
                try:
                    _, row = next(iter_df)
                    grid, move = row
                except:
                    df.to_csv(f"new.csv", index=False)
                    cv2.destroyAllWindows()

                scale_percent = 1000 # percent of original size
                width = int(10 * scale_percent / 100)
                height = int(20 * scale_percent / 100)
                dim = (width, height)
                
                # resize image
                resized = cv2.resize(grid.astype('float32'), dim, interpolation= cv2.INTER_NEAREST)
                cv2.imshow("Resized image", resized)
                q = cv2.waitKey()
                
                if q== 113:
                    df.to_csv(f"new.csv", index=False)
                    print('SAVED TI {i}')
                    cv2.destroyAllWindows()
                    break

                if q== 3:
                    df['move'][i] = 'RIGHT'

                if q== 1:
                    df['move'][i] = 'DOWN'

                if q== 2:
                    df['move'][i] = 'LEFT'

                if q== 0:
                    df['move'][i] = 'ROT'

                if q == 47:
                    df.drop(i)

                if q == 32:
                    pass


if __name__ == "__main__":
    check =  Check()
    filenames = check.get_files()
    check.check_moves()
    # path = '/Users/rostyslavmosorov/Desktop/tetris_ai/data'    
    # print(len([f for f in listdir(path) if isfile(join(path, f))]))
    
    # combined_csv = pd.concat( [ pd.read_csv(join("./data",f),) for f in filenames ])
    # combined_csv.to_csv( join("./data","combined_csv.csv"), index=False )
    # print('done')
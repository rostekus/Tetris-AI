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
           
            grids = np.loadtxt('/data/grids.csv', delimiter=",")
            grids = grids.reshape((int(grids.shape[0] / 20), 20, 10))
            df = pd.DataFrame(np.zeros(grids.shape[0]))
            for i, grid in enumerate(grids):
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
                    df.iloc[i] = 'RIGHT'

                if q== 1:
                    df.iloc[i] = 'DOWN'

                if q== 2:
                    df.iloc[i] = 'LEFT'

                if q== 0:
                    df.iloc[i] = 'ROT'

                if q == 47:
                    df.drop(i)

                if q == 32:
                    pass
def main():
    check =  Check()
    filenames = check.get_files()
    check.check_moves()


if __name__ == "__main__":
    main()
    # path = '/Users/rostyslavmosorov/Desktop/tetris_ai/data'    
    # print(len([f for f in listdir(path) if isfile(join(path, f))]))
    
    # combined_csv = pd.concat( [ pd.read_csv(join("./data",f),) for f in filenames ])
    # combined_csv.to_csv( join("./data","combined_csv.csv"), index=False )
    # print('done')
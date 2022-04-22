"""
NAME
    scrapping

DESCRIPTION
    This module provides tools for analazying tetris video 
    made by Classic Tetris (https://www.youtube.com/c/ClassicTetris)

"""
import numpy as np
import cv2
import time
# import imutils
import pandas as pd
from os import path
import operator
import argparse
from gui.interacter import interactive_get_contour

LENGHT = 2500
TIME = 4500


class TetrisGrabber:
    """
    A class for grabbing tetris grid from video

    ...

    Attributes
    ----------
    filename : str
        video filename
    name : str
        the name of the animal
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    create_grid
        anylize video frame by frame if it finds
        valid move it saves it to db.

    get_move(grid)
        Function analizes tetris grid with respect
        to previuos one and return the user move
    draw_grid()
        Function draws grid on the image
    find_region()
        Function finds the cordinates of the tetris grid
        in the video
    step(image)
        Obrains the object indeces on tetris grid
    get_grid(image)
        Function turns image of tetris grid to 20x10
        numpy array
    get_probability(A,B)
        Retutn the procentage of common elements in A and B
    get_move()
        Function analyze grid and return predicted move
    clear_grid_from_locked()
        Deletec locked objects from grid
    show_grid_move()
        Upscale 20x10 grid and puts prodicted move in
        the corner of image
    """

    def __init__(self, filename):
        self.filename = filename
        self.locked_first = np.zeros(10)
        self.locked_second = np.zeros(10)
        self.max_y = np.array([5, 1])
        self.min_y = np.array([5, 0])
        self.max_x = np.array([5, 1])
        self.min_x = np.array([5, 0])
        self.height = 0

    def create_grid(self, display= True):

        cap = cv2.VideoCapture(self.filename)
        iter = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, TIME)
        if cap.isOpened() == False:
            print("Error opening video stream or file")
            return
        _, frame = cap.read()
        contour = [[570, 350], [280, 380], [250, 100], [450, 100]]
        contour = interactive_get_contour(contour, frame)
        print(contour)

        top_left_x = min([x[0] for x in contour])
        top_left_y = min([x[1] for x in contour])
        bot_right_x = max([x[0] for x in contour])
        bot_right_y = max([x[1] for x in contour])
        img = frame[top_left_y:bot_right_y, top_left_x:bot_right_x]
        h, w, _ = img.shape
        diff = abs(h - w)
        w = int((w - diff) / 2)

        # create alocation
        # save every LENGHT entries
        df = pd.DataFrame(index=np.arange(0, LENGHT), columns=["move"])
        grids = np.zeros(shape=(LENGHT, 200))
        _, frame = cap.read()
        frame = frame[top_left_y:bot_right_y, top_left_x:bot_right_x]
        first_img = frame[:, 0 : w + 15]
        second_img = frame[:, w + int((diff)) :]
        pxstep = w // 10
        self.draw_grid(first_img, pxstep=pxstep)
        self.draw_grid(second_img, pxstep=pxstep)
        first_grid = self.get_grid(first_img)
        self.get_locked(first_grid)

        obj_grid = self.clear_grid_from_locked(first_grid)

        previuos_indeces_first_obj = self.get_indeces(obj_grid)

        second_grid = self.get_grid(second_img)
        previuos_indeces_second_obj = self.get_indeces(second_grid)
        f = first_grid
        s = second_grid
        self.get_locked(first_grid)

        while cap.isOpened():
            ret, frame = cap.read()
            frame = frame[top_left_y:bot_right_y, top_left_x:bot_right_x]

            if ret == True:

                second_img = frame[:, w + int((diff)) :]
                first_img = frame[:, 15:w]
                pxstep = w // 10

                # self.draw_grid(first_img, pxstep=pxstep)
                # self.draw_grid(second_img, pxstep=pxstep)

                cv2.imshow("Frames", frame)

                indeces_first_obj, first_grid = self.step(first_img)
                indeces_second_obj, second_grid = self.step(second_img, first=False)

                first_move = None
                if (
                    len(indeces_first_obj) == len(previuos_indeces_first_obj)
                    and len(indeces_first_obj) == 4
                ):

                    first_move = self.get_move(
                        previuos_indeces_first_obj, indeces_first_obj
                    )
                if indeces_first_obj:
                    max_block_y = np.array(
                        max(indeces_first_obj, key=operator.itemgetter(1))
                    )
                    min_block_y = np.array(
                        min(indeces_first_obj, key=operator.itemgetter(1))
                    )
                    self.height = max_block_y[1] - min_block_y[1]

                second_move = None
                if (
                    len(indeces_second_obj) == len(previuos_indeces_second_obj)
                    and len(indeces_second_obj) > 2
                ):

                    second_move = self.get_move(
                        previuos_indeces_second_obj, indeces_second_obj
                    )

                if first_move:
                    grids[iter] = first_grid.flatten()
                    df.iloc[iter]["move"] = first_move

                    iter += 1
                    if iter == LENGHT:
                        filename = path.join("./data", f"{time.time()}")
                        with open(f"{filename}-grids.csv", "a") as outfile:
                            for slice_2d in grids:
                                np.savetxt(outfile, slice_2d, fmt="%i", delimiter=",")
                        df.to_csv(f"{filename}-moves.csv", index=False)
                        iter = 0
                a = self.show_grid_move(first_grid, first_move)
                f = self.show_grid_move(second_grid, second_move)
                if display:
                    numpy_horizontal = np.hstack((f, a))
                    cv2.imshow("images", numpy_horizontal)
                    previuos_indeces_second_obj = indeces_second_obj

                if second_move:
                    grids[iter] = second_grid.flatten()
                    df.iloc[iter]["move"] = second_move

                    iter += 1
                    if iter == LENGHT:
                        filename = path.join("./data", f"{time.time()}")

                        with open(f"{filename}-grids.csv", "a") as outfile:
                            for slice_2d in grids:
                                np.savetxt(outfile, slice_2d, fmt="%i", delimiter=",")
                        df.to_csv(f"{filename}-moves.csv", index=False)
                        print(df)
                        iter = 0
                f = first_grid
                s = second_grid
                if iter % 500 == 0 and iter != 0:
                    print(f"SAVED {iter}")
                print(iter)
                saved = False
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    with open(f"{filename}-grids.csv", "a") as outfile:
                        for slice_2d in grids:
                            np.savetxt(outfile, slice_2d, fmt="%i", delimiter=",")
                    df.to_csv(f"{filename}-moves.csv", index=False)
                    break
            else:
                if not saved:
                    with open(f"{filename}-grids.csv", "a") as outfile:
                        for slice_2d in grids:
                            np.savetxt(outfile, slice_2d, fmt="%i", delimiter=",")
                    df.to_csv(f"{filename}-moves.csv", index=False)
                break
        cap.release()
        cv2.destroyAllWindows()

    def step(self, img, first=True):
        grid = self.get_grid(img)
        grid_copy = grid.copy()
        self.get_locked(grid, first=first)
        obj_grid = self.clear_grid_from_locked(grid, first=first)

        indeces_obj = self.get_indeces(obj_grid)
        return indeces_obj, np.array(grid_copy)

    def get_grid(self, img):

        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        resized = imutils.resize(imgray, height=20, width=10)
        if resized.size != 200:
            resized.resize((20, 10))

        _, grid = cv2.threshold(resized, 50, 255, cv2.THRESH_BINARY)

        grid = grid / 255
        grid = np.asarray(grid).astype(np.float32)
        if (
            grid[1][9] == 1
            and grid[2][9] == 1
            and grid[3][9] == 1
            and grid[4][9] == 1
            and grid[5][9] == 0
        ):
            grid[2, 9] = 0
            grid[1, 9] = 0
            grid[3, 9] = 0
            grid[4, 9] = 0
        return grid

    def get_probability(self, A, B):
        common_elements = [
            x for x in set(tuple(x) for x in A) & set(tuple(x) for x in B)
        ]
        return len(common_elements) / len(A)

    def get_move(self, indeces_prev, indeces):

        max_block_y = np.array(max(indeces, key=operator.itemgetter(1)))
        min_block_y = np.array(min(indeces, key=operator.itemgetter(1)))
        max_block_x = np.array(max(indeces, key=operator.itemgetter(0)))
        min_block_x = np.array(min(indeces, key=operator.itemgetter(0)))

        upper = self.max_y - max_block_y
        lower = self.min_y - min_block_y

        self.min_y = min_block_y
        self.max_y = max_block_y

        self.max_x = max_block_x
        self.min_x = min_block_x

        if int(upper[1]) <= -2 and int(lower[1]) <= -2:
            return None
        if np.array_equiv(np.hstack((upper, lower)), [0, 0, 0, 0]):
            return None
        if np.array_equiv(upper, [0, -1]) and np.array_equiv(lower, [0, -1]):
            return "DOWN"
        if (np.array_equiv(upper, [-1, 0]) and np.array_equiv(lower, [-1, 0])) or (
            np.array_equiv(upper, [-1, -1]) and np.array_equiv(lower, [-1, -1])
        ):
            return "RIGHT"
        if (np.array_equiv(upper, [1, 0]) and np.array_equiv(lower, [1, 0])) or (
            np.array_equiv(upper, [1, -1]) and np.array_equiv(lower, [1, -1])
        ):
            return "LEFT"
        if (upper[1] == lower[0]) or (upper[0] == lower[1]):
            if self.height != (max_block_y[1] - min_block_y[1]):
                return "ROT"
        if np.array_equiv(upper, [0, 0]):
            if lower[0] >= -2 and lower[0] <= 2:
                if self.height != (max_block_y[1] - min_block_y[1]):
                    return "ROT"
        if np.array_equiv(lower, [0, 0]):
            if upper[0] >= -2 and upper[0] <= 2:
                if self.height != (max_block_y[1] - min_block_y[1]):
                    return "ROT"
        if upper[0] == upper[1]:
            if lower[0] >= -2 and lower[0] <= 2:
                if self.height != (max_block_y[1] - min_block_y[1]):
                    return "ROT"
        if lower[0] == lower[1]:
            if upper[0] >= -2 and upper[0] <= 2:
                if self.height != (max_block_y[1] - min_block_y[1]):
                    return "ROT"

    def get_indeces(self, grid):
        X, Y = np.where(grid == 1)
        indeces = []
        for x, y in zip(X, Y):
            indeces.append((y, x))
        return indeces

    def clear_grid_from_locked(self, grid, first=True):
        found = []
        if first:
            for col_num, height in enumerate(self.locked_first):
                for i in range(19, 19 - int(height), -1):
                    grid.T[col_num][i] = 0
            for i, row in enumerate(grid):
                if any(row):
                    found.append(i)
            if found:
                if max(found) - min(found) > 4:
                    grid = np.zeros((20, 10))

        else:
            for col_num, height in enumerate(self.locked_second):
                for i in range(19, 19 - int(height), -1):
                    grid.T[col_num][i] = 0
            for i, row in enumerate(grid):
                if any(row):
                    found.append(i)
            if found:
                if max(found) - min(found) > 4:
                    grid = np.zeros((20, 10))

        return grid

    def get_locked(self, grid, first=True):

        for i, column in enumerate(grid.T):
            j = 19
            height = 0
            while column[j] and j >= 0:
                height += 1
                j -= 1
            if first:
                if self.locked_first[i] != height:
                    self.locked_first[i] = height
            else:
                if self.locked_second[i] != height:
                    self.locked_second[i] = height
        return True

    def draw_grid(
        self, img, line_color=(0, 255, 0), thickness=1, type_=cv2.LINE_AA, pxstep=50
    ):
        """
        Draws the grid on the image

        If the argument `sound` isn't passed in, the default Animal
        sound is used.

        Args
        ----------
        img : array
            The image on which the grid will be drawn
        line color : tuple RGB, optional
            Line color (default is Green (0, 255, 0))
        thickness: int, optional
            The thickness of the line in pixels (default is 1)
        type_ : optional
            Type of line (default is cv.LINE_AA)
        pxstep : int, optional
            in pixels (default is 50)
        """

        x = pxstep
        y = pxstep
        z = img.shape[1]
        while x < img.shape[1]:
            cv2.line(
                img,
                (x, 0),
                (x, img.shape[0]),
                color=line_color,
                lineType=type_,
                thickness=thickness,
            )
            x += pxstep

        while y < img.shape[0]:
            cv2.line(
                img,
                (0, y),
                (img.shape[1], y),
                color=line_color,
                lineType=type_,
                thickness=thickness,
            )
            y += pxstep

    def find_region(self, draw=False):
        """
        Function analyzes the video specified in __init__ function.
        Finds the cordinates of the tetris frame
          Args
        ----------
        draw : bool
            Draw frame on the video to check if fucntion
            correctly found tetris grid
        """

        lower_black = np.array([70, 0, 30], dtype=np.uint8)
        upper_black = np.array([85, 255, 255], dtype=np.uint8)
        cap = cv2.VideoCapture(self.filename)
        if cap.isOpened() == False:
            print("Error opening video stream or file")
            return
        while cap.isOpened():
            ret, frame = cap.read()
            if ret == True:

                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                mask = cv2.inRange(hsv, lower_black, upper_black)

                img = cv2.bitwise_and(frame, frame, mask=mask)
                # blur = cv2.GaussianBlur(img, (3, 3), 1)
                edges = cv2.Canny(img, 100, 200)
                kernel = np.ones((2, 2), np.uint8)
                dil = cv2.dilate(edges, kernel, iterations=1)
                cv2.imshow("e", dil)
                contours, hierarchy = cv2.findContours(
                    edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
                )
                if len(contours) != 0:
                    c = max(contours, key=cv2.contourArea)
                    contourImg = cv2.drawContours(frame, c, -1, (0, 255, 0), 3)
                    cv2.imshow("Contours", contourImg)
                # edges = cv2.Canny(mask,100,200)
                # cv2.imshow("Contours", edges)
                # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
                # # dilated = cv2.dilate(edges, kernel)
                # contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                # try:
                #
                #     contourImg = cv2.drawContours(frame, contour, -1, (0,255,0), 3)
                #     # cv2.imshow("Contours", contourImg)
                #     cnts = contour[0]
                #     x,y,w,h = cv2.boundingRect(cnts)
                #     print(x,y)
                #     cv2.circle(frame_,(x,y), 3, (0,0,255), -1)
                #     cv2.circle(frame_,(x+w,y), 3, (0,0,255), -1)
                #     cv2.circle(frame_,(x+w,y+h), 3, (0,0,255), -1)
                #     cv2.circle(frame_,(x,y+h), 3, (0,0,255), -1)
                #     cv2.imshow("Corners of grid", contourImg)

                # except ValueError:
                #     pass

                if cv2.waitKey(25) & 0xFF == ord("q"):

                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()

    def show_grid_move(self, grid, move):
        scale_percent = 5000  # percent of original size
        width = int(10 * scale_percent / 100)
        height = int(20 * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(
            grid.astype("float32"), dim, interpolation=cv2.INTER_NEAREST
        )

        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (20, 50)
        fontScale = 1
        fontColor = (255, 255, 255)
        thickness = 1
        lineType = 2

        cv2.putText(
            resized,
            move,
            bottomLeftCornerOfText,
            font,
            fontScale,
            fontColor,
            thickness,
            lineType,
        )

        return resized


def main():
    parser = argparse.ArgumentParser(description="Scraping module")
    parser.add_argument("-d", action="store_true", help="Display grids", default=False)
    args = vars(parser.parse_args())
    display = args["d"]
    tertis = TetrisGrabber("./video/video.mp4")
    tertis.create_grid(display)


if __name__ == "__main__":
    main()

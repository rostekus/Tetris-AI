![GitHub last commit](https://img.shields.io/tokei/lines/github/rostekus/Tetris-AI)
# Tetris AI
A self-playing Tetris.

## Brief History
I can proudly say that it is the biggest project that I've been working on.
When I started this project I wanted to create RL AI for playing tetris but then I've youtube video when was proposed to scraped data from Classic Tetris World Championship [youtube channel](https://www.youtube.com/c/ClassicTetris) and based on that data, train NN. Author didn't provide any source code so I knew I had to try to implement it. 
This project has taught me a number of things. First of all working with read data isn't as easy as with Iris or MNIST data set.
Secodnly, if we are talking about bigger project than two-three files, it is crutial to be certain that modules which are finished are working correctly since their infuence work of fututr modules. Finally...
During the developtemnt of this project I faced three major problems. The hardest things was to write a algorith for predicting user move based on tetris gris as there are frames where due to high speed game engine for smoothness of gameplay, draws strange figures. Examples:

<img src="/images/strange.png" width="480" >
I came up with three main solutions to that issue:

- detecting type of object (squere, line, Z, L)
- getting cordinates of object and observing its change
- getting the rightmost, leftmost, lowest and uppermost cordinades of object and detect how they change
I decided to use last approach with additional step, program calculates the propability of each cordinates to move in each direction
The UI code for the interactive mode is adapted from interacrer.py from matplotlib page.


## Instalation
Clone the repository
```
git clone https://github.com/rostekus/Tetris-AI
```
Setup
```
cd snake-ai
python3 setup.py install
```
## Usage
If you want just play Tetris game
```
python3 tetris.py
```
On the other hand, if you want to create your dataset, firstly dowloand video, copy it to video folder and name it `video.mp4`.
Than run scrapping module
```
python3 scrapping.py [-d]
```
* The `-d` displays scrapping grids
<img src="/images/scraping.gif" width="480" >


After running the script, select the area of TWO tetris grids as is shown below:

<img src="/images/selection.png" width="480" >

Dataset will be saved to `data` folder. Then you can augment your dataset using `augementation` module.
After that just run `create_db.py` script that will merge all datasets files into two (grids/moves)
## Problem
Aftwr scrapping data I began to train models,I got really high accuracy (about 85%) but after testing models on real Tetris game
this what I got:

As I observed the AI stucks after first 2-3 moves. So i added more examples of grids where average high is relativly low. Unfortunettly what I didn't solve the problem as the accuracy of models dropped to 60%. Screenshot from TensorflowBoard:



## Project Structure
------------

    ├── LICENSE
    ├── README.md
    ├── src
    │   ├── analysis    
    │   │   ├── check_data.py           <- module for checking scrapped data
    │   │   ├── create_db.py            <- creating two files for training from scrapped files
    │   │   ├── model.h5                <- trained model
    │   │   ├── models.ipynb            <- tried models
    │   │   └── notebook.ipynb          <- notebook for training model
    │   ├── game
    │   │   ├── config.py               <- config files containg tetris' figures 
    │   │   ├── tetris.py               <- tetris game
    │   │   └── tetrisTF.py             <- tetris game for keras model
    │   ├── gui
    │   │   └── interacter.py           <- module for interactive selecting area of tetris grid
    │   └── scraping
    │       ├── augmentation.py         <- augementation data, creating holes, shifting grids              
    │       └── scrapping.py            <- scraping data from youtube videos, saving into /data/*.csv
    ├── data                            <- scrapped data from videos
    │   ├── grids.csv
    │   └── moves.csv
    ├── setup.py                        <- setup file
    └── video                           <- folder for videos 
        └── video.mp4

---

 ## License

 [MIT](https://choosealicense.com/licenses/mit/)


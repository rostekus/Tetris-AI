![GitHub last commit](https://img.shields.io/tokei/lines/github/rostekus/Tetris-AI)
# Tetris AI
A self-playing Tetris.

## Brief History
I can proudly say that it is the biggest project that I've been working on.
When I started this project I wanted to create RL AI for playing tetris but then I've youtube video when was proposed to scraped data from Classic Tetris World Championship [youtube channel](https://www.youtube.com/c/ClassicTetris) and based on that data, train NN. Author didn't provide any source code so I knew I had to try to implement it. 
This project has taught me a number of things. First of all working with read data isn't as easy as with Iris or MNIST data set.
Secodnly, if we are talking about bigger project than two-three files, it is crutial to be certain that modules which are finished are working correctly since their infuence work of fututr modules. Finally...
During the developtemnt of this project I faced three major problems:
- The hardest things was to write a algorith for predicting user move based on tetris gris as there are frames where due to high speed game engine for smoothness of gameplay, draws strange figures. Example: 
- 
- change the reward function, what I used was simple idea of Euclidian distance from the snakes head to the fruit

-hhgg



------------

    ├── LICENSE
    ├── README.md
    ├── TetrisAI
    │   ├── __init__.py
    │   └── src
    │       ├── analysis    
    │       │   ├── check_data.py           <- module for checking scrapped data
    │       │   ├── create_db.py            <- creating two files for training from scrapped files
    │       │   ├── model.h5                <- trained model
    │       │   ├── models.ipynb            <- tried models
    │       │   └── notebook.ipynb          <- notebook for training model
    │       ├── game
    │       │   ├── config.py               <- config files containg tetris' figures 
    │       │   ├── tetris.py               <- tetris game
    │       │   └── tetrisTF.py             <- tetris game for keras model
    │       ├── gui
    │       │   └── interacter.py           <- module for interactive selecting area of tetris grid
    │       └── scraping
    │           ├── augmentation.py         <- augementation data, creating holes, shifting grids              
    │           └── scrapping.py            <- scraping data from youtube videos, saving into /data/*.csv
    ├── data                                <- scrapped data from several videos
    │   ├── grids.csv
    │   └── moves.csv
    ├── setup.py                            <- setup file
    └── video                               <- folder for videos 
        └── video.mp4

---

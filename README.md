![GitHub last commit](https://img.shields.io/tokei/lines/github/rostekus/Tetris-AI)
# tetris_ai
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

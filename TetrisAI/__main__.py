import argparse
import os.path
import game
import scraping

def main():
    

    parser = argparse.ArgumentParser(description='Tetris AI')
    group =  parser.add_mutually_exclusive_group()

    group.add_argument('--game', action='store_true', help='Play Tetris')
    group.add_argument('--ai', action='store',
    help='Watch AI play Tetris',
    nargs = '?', const=True)

    parser.add_argument('--scrap',action='store',
    help='Run scrapping',nargs = '?', const='./video/video.mp4', type=str)

    parser.add_argument('--aug', action='store_true')
    
    
    arguments = vars(parser.parse_args())   

    
    if arguments['game']:
        game.tetris.play()

    elif arguments['ai']:
        game.tetrisTF.play()
        if arguments['scrap'] == True:
            game.tetrisTF.play()
        elif isinstance(arguments['scrap'], str):
            if os.path.isfile(arguments['scrap']):
                game.tetrisTF.play( arguments['scrap']) 
            else:
                print('Incorrect file name')
        else:
                print('Incorrect file name')

    elif arguments['scrap']:
        if arguments['scrap'] == True:
            scraping.scrap.TetrisGrabber('/video/video.mp4').create_grid()
        elif isinstance(arguments['scrap'], str):
            if os.path.isfile(arguments['scrap']):
                scraping.scrap.TetrisGrabber(arguments['scrap']).create_grid()
        else:
            print('Incorrect file name')

    elif arguments['aug']:
        scraping.augment.main()




if __name__ == "__main__":
    main()

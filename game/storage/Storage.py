from pygame import Vector2

GAME_WIDTH = 1280
GAME_HEIGHT = 720
RESOLUTION = (GAME_WIDTH, GAME_HEIGHT)
FONT_VALUES = {'font_type': None,
               'font_size': 36}
BLOCK_WIDTH = 30
BLOCK_HEIGHT = 20
BLOCK_SCALE_SIZE = (BLOCK_WIDTH, BLOCK_HEIGHT)
LEFT_MARGIN = 20
BLOCK_DISTANCE_FROM_LATERAL_WALL = BLOCK_WIDTH
BLOCK_STARTING_DISTANCE_FROM_TOP = 20
BLOCK_ENDING_DISTANCE_FROM_TOP = 400
BLOCK_EMPTY_SPACE = 5
BLOCK_EMPTY_SPACE_LIST = [5, 10, 15, 20, 25, 30, 35, 40]
PLAY_OPTION_POSITION = (GAME_WIDTH / 2, GAME_HEIGHT / 2 - 50)
QUIT_OPTION_POSITION = (GAME_WIDTH / 2, GAME_HEIGHT / 2 + 50)
GAME_OVER_POSITION = (GAME_WIDTH / 2, GAME_HEIGHT / 2)
GAME_WON_POSITION = (GAME_WIDTH / 2, GAME_HEIGHT / 2)
CONTINUE_POSITION = (GAME_WIDTH / 2, GAME_HEIGHT / 2 + FONT_VALUES['font_size'] * 2)
DELAY = 100
INTERVAL = 100
BACKGROUND_COLOR = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GAME_TITLE = "DxBall cu buget redus"
BALL_FILENAME = 'silver_ball_32px.png'
BALL_SIZE = 32
PLATE_FILENAME = 'dxball_bar_120x24.png'
PLATE_WIDTH = 120
PLATE_HEIGHT = 24
PLATE_DISTANCE_FROM_BOTTOM = 50
INITIAL_BALL_SPEED = 0

DATA_FOLDER_NAME = 'data'
PSEUDO_DB_FOLDER_NAME = 'pseudo_database'
PLAY_STATE_MUSIC_FILENAME = 'Benny-hill-theme.mp3'
GAME_WON_STATE_MUSIC_FILENAME = 'Cartoon-woohoo.mp3'

BALL_SPEED = 5
PLATE_SPEED = 40

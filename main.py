import pygame
from random import randint
import math

# initializing pygame, without this the game won't open
pygame.init()

# Size of game screen
WIDTH = 900
HEIGHT = 800

# Creating a game screen
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Ping Pong') # Giving the game an actual name

# Colors
DARK_BLUE = (10, 20, 60) # Background
WHITE = (255, 255, 255) # Border

# Border in the middle so paddles can't cross it
"""(WIDTH - BORDER_WIDTH)/2 will center the border directlt in the middle, y = 0 
will start to draw e=rectangle from top, 10 is it's width and it's height should 
be the same as screen height"""
BORDER_WIDTH = 12
BORDER_X_START = (WIDTH - BORDER_WIDTH)/2
BORDER_X_END = (WIDTH + BORDER_WIDTH)/2
BORDER = pygame.Rect(BORDER_X_START, 0, BORDER_WIDTH, HEIGHT)

# Defining at what speed our game runs, so it can run in the same speed in
# most of the computers rather than running faster in stronger computers and in
# slower computers

FPS: int = 60 # Frames Per Second, defining how fast the screen would be drawn

# Loading images so pygame can use them inside the actual game
PADDLE = pygame.image.load('Images/Paddle.png') # -> Will take the file
# path as an argument
BALL = pygame.image.load('Images/Ball.png')

# Decreasing the size of the images, so they would fit

# Defining dimensions in variables, so I can use them inside the RECT class
PADDLE_WIDTH = 90
PADDLE_HEIGHT = 160
BALL_WIDTH = 80
BALL_HEIGHT = 80

# A constant touch value so that the images can touch the border
TOUCH_VALUE_X = 20
TOUCH_VALUE_Y = 10

# Defining the velocity of both paddle and the ball
# In each direction btw the velocity is actually vel*FPS
PADDLE_VEL = 6
BALL_VEL = 3

# Centering the elements
BALL_CENTER_X = (WIDTH - BALL_WIDTH)//2
BALL_CENTER_Y = (HEIGHT - BALL_HEIGHT)//2
PADDLE_CENTER_Y = (HEIGHT - PADDLE_HEIGHT)//2

PADDLE = pygame.transform.scale(PADDLE, (PADDLE_WIDTH, PADDLE_HEIGHT))
BALL = pygame.transform.scale(BALL, (BALL_WIDTH, BALL_HEIGHT))


def draw_window(color: tuple, left_paddle: pygame.Rect,
                right_paddle: pygame.Rect, ball: pygame.Rect) -> None:
    """
    A function to fill the entire background with a given color(e.i. rgb
    values of the color), and draw 3 rectangle objects to represent the
    right, left paddles and the ball which should be in the center. The
    reason why we are using rectangle objects is that, these objects will
    help us to keep track of x, y positions of elements, and by increasing them
    we can create the effect of these objects actually moving.

    :param color: RGB values of the background color, it should be a tuple
    :param right_paddle: A Rect() object, which will model the right paddle,
    with its position value(i.e. right_paddle.x)
    :param left_paddle:  A Rect() object, which will model the left paddle,
    with its position value(i.e. left_paddle.x)
    :param ball: A Rect() object, which will model the ball, and should be
    positioned in the center
    :return: None
    """
    WINDOW.fill(color)  # fills the background with the given color

    # Drawing the right paddle
    """For .blit to work you need to pass an argument which defines the 
    surface area, meaning the object you want to draw, instead of the object 
    which you want to draw you decide to draw an rectangle object error will 
    be raised, because simply python can't understand what do draw. The rect() 
    object however is a simple object, which helps you to keep track of x, 
    y coordinate and maybe collision and etc but I'm not sure yet"""
    # Masking the right paddle with the rectangle.
    WINDOW.blit(PADDLE, (right_paddle.x, right_paddle.y))

    # Drawing the left paddle
    WINDOW.blit(PADDLE, (left_paddle.x, left_paddle.y))

    # Drawing a border in the middle so the paddles can't cross it
    pygame.draw.rect(WINDOW, WHITE, BORDER)

    # Drawing the ball
    WINDOW.blit(BALL, (ball.x, ball.y))

    # updates the python display, basically drawing new stuf
    pygame.display.update()


def move_left_paddle(key_pressed, left_paddle: pygame.Rect) -> None:
    """
    Moves the object using the WASD, in this particular program the
    key_pressed parameter will get all the pressed keys during the loop,
    and the left Rect() object will move this object to the right.
    :param key_pressed: All the keys pressed
    :param left_paddle: The Rect() object which will be moved when the arrow
    keys are pressed
    :return: None
    """
    # Moving the left paddle use WASD without allowing the paddle to go out
    # of the screen
    if key_pressed[pygame.K_w] and left_paddle.y - PADDLE_VEL > 0 - \
            TOUCH_VALUE_Y:
        # Moving up in coordinate pane
        left_paddle.y -= PADDLE_VEL

    if key_pressed[pygame.K_s] and left_paddle.y + PADDLE_VEL + \
            left_paddle.height < TOUCH_VALUE_Y + HEIGHT:
        # Moving down in coordinate pane
        left_paddle.y += PADDLE_VEL

    if key_pressed[pygame.K_a] and left_paddle.x - PADDLE_VEL > 0 - \
            TOUCH_VALUE_X:
        # Moving lef in coordinate pane
        left_paddle.x -= PADDLE_VEL

    if key_pressed[pygame.K_d] and left_paddle.x + PADDLE_VEL + \
            left_paddle.width < TOUCH_VALUE_X + BORDER_X_START:
        # Mowing right in coordinate pane
        left_paddle.x += PADDLE_VEL


def move_right_paddle(key_pressed, right_paddle) -> None:
    """
    Moves the object using teh arrow keys, in this particular program the
    key_pressed parameter will get all the pressed keys during the loop,
    and the right_paddle Rect() object will move this object to the right.
    :param key_pressed: All the keys pressed
    :param right_paddle: The Rect() object which will be moved when the arrow
    keys are pressed
    :return: None
    """
    # Moving right paddle with arrow keys
    if key_pressed[pygame.K_UP] and right_paddle.y - PADDLE_VEL > 0 - \
            TOUCH_VALUE_Y:
        right_paddle.y -= PADDLE_VEL

    if key_pressed[pygame.K_DOWN] and right_paddle.y + PADDLE_VEL + \
            right_paddle.height < HEIGHT + TOUCH_VALUE_Y:
        right_paddle.y += PADDLE_VEL

    if key_pressed[pygame.K_RIGHT] and right_paddle.x + PADDLE_VEL + \
            right_paddle.width < WIDTH + TOUCH_VALUE_X:

        right_paddle.x += PADDLE_VEL

    if key_pressed[pygame.K_LEFT] and right_paddle.x - PADDLE_VEL > \
            BORDER_X_END - TOUCH_VALUE_X:
        right_paddle.x -= PADDLE_VEL


def pause_game() -> None:
    """
    A function to pause the game, when the mouse is clicked.
    :return: None
    """
    paused: bool = True
    while paused:
        # Handling events, to prevent other events from moving the paddles,
        # and breaking the paused state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                paused = False


def random_degree() -> float:
    """
    Returns a random degree, in radians. The domain of the degree is [0, 360]
    :return: A float which contains the randomly chosen x degree with radians.
    :rtype: float
    """
    deg = randint(0, 360)
    return math.radians(deg)


def move_direction(deg: float, distance: int) -> tuple[int, int]:
    """
    Computes the movement in the x and y directions based on given angles
    and a specified distance.
    The function uses the sine and cosine of the given angle (in radians)
    to determine how much the object should move along the x and y axes.
    :param deg: Angle (in radians) used to compute horizontal displacement
    as cos(x) * distance, and vertical displacement as sin(x) * distance.
    :param distance: The amount of distance defined to move the object
    :return: A tuple (length_x, length_y) representing the movement along the x
    and y axes.
    """
    length_x = (distance * math.cos(deg))//1
    length_y = (distance * math.sin(deg))//1
    # Making sure the ball just doesn't move horizontally as cos(x) can be 0.
    # Which will result in no vertical movement
    if length_x == 0:
        length_x = length_y = (distance/math.sqrt(2))//1
    return int(length_x), int(length_y)


def random_ball_movement(ball: pygame.Rect, x: float, distance: int) -> None:
    """
    This function will move the ball (Rect object) simultaneously in random
    vertical and horizontal, directions. It uses move_direction function to
    determine in which direction to move the ball.

    :param ball: A rectangle object which models the ball
    :param x: Angle (in radians) used to compute horizontal and vertical
    displacement within the function move_direction()
    :param distance: The amount of distance defined to move object. It's used
    inside the move_direction() function
    :return: None
    """
    direct_x, direct_y = move_direction(x, distance)
    ball.x += direct_x
    ball.y += direct_y


# Making Sure that the game window is there, by creating the infinite loop
def main() -> None:
    """
    A function in which the main functionalities of the game will be
    written, such as the infinite running loop, score board, quiting and
    wining conditions. The run time is set to 60FPS so that it can run the
    same as in other computers
    """
    left_paddle = pygame.Rect(110, PADDLE_CENTER_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(700, PADDLE_CENTER_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(BALL_CENTER_X, BALL_CENTER_Y, BALL_WIDTH, BALL_HEIGHT)

    click_counter: int = 0
    running: bool = True

    # Defining x and y, so I can use these variables later
    x: None = None
    while running:

        # Defining a speed in which the game is running (e.g. the frames
        # drawn each second)
        delay = pygame.time.Clock() # Creating a clock object
        delay.tick(FPS) # Making the loop take 60fps to run each time

        # Checking all the possible events like press from keyboard exit and etc
        for event in pygame.event.get(): # gets all the events as a list
            # Event for quiting py game
            if event.type == pygame.QUIT:
                running = False # making sure that you can leave the loop
            # Increasing the num_mouse_pressed for using at to pause and play
            # game
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_counter += 1
                if click_counter == 1:
                    # Generating random x and y degrees to move the ball
                    # randomly when the game begins
                    x: float = random_degree()
                else:
                    pause_game()

        # Getting all the pressed keys, so you can add functionality to them
        key_pressed = pygame.key.get_pressed()

        # Using specifically this method, because with this pygame will get
        # the keys even if they are held down, in the other method which I'll
        # write later about(spoiler checking key pressed in the for loop for
        # events)
        move_left_paddle(key_pressed, left_paddle)
        move_right_paddle(key_pressed, right_paddle)

        # Changing the x, y coordinates of the ball
        # For now this will move the ball in the same direction, since the
        # beginning of the game because I haven't added collision and other
        # stuff yet.
        if click_counter:
            random_ball_movement(ball, x, BALL_VEL)

        draw_window(DARK_BLUE, left_paddle, right_paddle, ball)

    pygame.quit() # quiting the game after you leave the loop


if __name__ == '__main__':
    main()

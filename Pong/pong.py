import pygame

#Window class
#  contains the following attributes: width, height, color, win, clock, score
#  initializes the game board with given width, height, and color
#  requires the width, height, and color to be passed
#  functions: update()
class Window():
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color
        self.win = pygame.display.set_mode((width, height))
        self.win.fill(color)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pong")
        self.score = [0,0]

    #updates the pygame display
    def update(self):
        pygame.display.update()


#Ball class
#  contains the following attributes: rect, color, direction, size
#  initializes the ball for pong and controls how it reacts
#  requires surface, dir, size,color
#    surface: Window object
#    dir: the direction the ball is going in, is a list [x pixels, y pixels]
#    size: the size of the ball as it is a square
#    color: color of the ball
#  functions: movingSquare(), draw(), movingDraw(), checkCollide(), checkCollideWithPlayers(), reset()
class Ball():
    def __init__(self, surface, dir, size, color):
        self.rect = pygame.Rect(surface.width//2, surface.height//2, size, size)
        self.color = color
        self.direction = dir
        self.size = size

    #determines where to move the square
    #  requires surface and collided
    #    surface: Window object for game
    #    collided: boolean if ball has collided with either player
    def movingSquare(self, surface, collided):
        #if ball has collided with players, check if abs(speed) is not more than 20
        #  if abs(speed) is less than 20, add increase speed, and bounce ball off player
        if collided:
            self.determinePaddleBonuses()
            self.direction[0] *= -1 # rebound direction

        self.checkForScore(surface) #checks if scoring occurs and handles it

        #check if ball hits top or bottom of gameboard, if so change y direction so it bounces off
        if self.rect.y + self.size >= surface.height or self.rect.y + self.direction[1] <= 0:
            self.direction[1] *= -1

        self.rect.move_ip(self.direction[0], self.direction[1]) # move ball in correct direction

    #determines if there are any bonuses to add to the current direction of the ball
    #  this includes the x speed and the y speed
    def determinePaddleBonuses(self):
        keys = pygame.key.get_pressed() #get keys pressed

        #must be separate so that P1 cannot affect P2's bounce and P2 cannot affect P1's bounce
        #determine which paddle it is hitting, allow player to affect the bounce
        if self.direction[0] < 0:
            #check if speed > -20, then sub 1 on speed
            #change speed of y value
            if keys[pygame.K_w]:
                self.direction[1] -= 5
            elif keys[pygame.K_s]:
                self.direction[1] += 5
            #change speed of x value
            if self.direction[0] > -20:
                self.direction[0] -= 1
        elif self.direction[0] > 0:
            #we know it must be hitting player 2
            #change speed of y value
            if keys[pygame.K_UP]:
                self.direction[1] -= 5
            elif keys[pygame.K_DOWN]:
                self.direction[1] += 5
            #change speed of x value
            if self.direction[0] < 20:
                self.direction[0] += 1

    #checks if the ball is behind a player and has scored
    #  requires surface: Window object
    def checkForScore(self, surface):
        #if score, add to corresponding score, reset the speed to 5, and reset ball's location
        if self.rect.x + self.size >= surface.width:
            surface.score[0] += 1 # Player 1 scored
            self.direction = [5,5]
            self.reset(surface)
        elif self.rect.x + self.direction[0] <= 0:
            surface.score[1] += 1 # Player 2 scored
            self.direction = [-5,5]
            self.reset(surface)

    #draws the ball on the surface with given color
    #  requires surface: Window object, and color
    def draw(self, surface, color):
        pygame.draw.rect(surface.win, color, self.rect)

    #draws and moves the ball
    #  requires surface: Window object, and players: list of Player objects
    def movingDraw(self, surface, players): #, dirx, diry):
        self.draw(surface, surface.color) # draw ball with surface color to erase it
        self.movingSquare(surface, self.checkCollideWithPlayers(players)) # figure out where to move ball to
        self.draw(surface, self.color) # draw ball with ball color to have it reappear

    #checks if there is a collision with given rectangle
    #  requires rect: rectangle object to check if it is colliding with
    #  returns True if there is a collision, False if there is no collision
    def checkCollide(self, rect):
        return self.rect.colliderect(rect)

    #checks if there is a collision with any of the players
    #  requires players: list of Player objects
    #  returns True if there is a collision, False if there is no collision
    def checkCollideWithPlayers(self, players):
        for i in range(len(players)):
            if self.checkCollide(players[i].rect):
                return True
        return False

    #resets the ball back to the middle of the board
    #  requires surface: Window object
    def reset(self, surface):
        self.draw(surface, surface.color) # color over ball's current location to erase it
        self.rect.x = surface.width//2 # floor to keep it an int
        self.rect.y = surface.height//2


#Player class
#  contains the following attributes: surface, width, height, color, number
#  initializes a player for pong and the controls for the player
#  requires surface, width, height, color, number
#    surface: Window object
#    width: width of player paddle
#    height: height of player paddle
#    color: color of player paddle
#    number: player's number (as in player 1 or player 2)
#  functions: draw(), move()
class Player():
    def __init__(self, surface, width, height, color, number):
        if number == 1:
            self.rect = pygame.Rect(0, surface.height//2 - height//2, width, height)
        elif number == 2:
            self.rect = pygame.Rect(surface.width-width, surface.height//2 - height//2, width, height)
        self.color = color
        self.number = number

    #draws the player on the surface with given color
    #  requires surface: Window object, and color
    def draw(self, surface, color):
        pygame.draw.rect(surface.win, color, self.rect)

    #moves the player on the surface based on user input
    #  requires surface: Window object
    #  player 1 uses 'W' and 'S' keys
    #  player 2 uses 'UP_Arrow' and 'DOWN_Arrow' keys
    def move(self, surface):
        keys = pygame.key.get_pressed() #get keys pressed

        self.draw(surface, surface.color) # color over player's current location to erase it

        #determine if Player is 1 or 2, and if they want to go up or down
        if self.number == 1:
            if keys[pygame.K_w]:
                self.rect.move_ip(0, -10) # go up 10 pixels
            elif keys[pygame.K_s]:
                self.rect.move_ip(0, 10) # go down 10 pixels
        elif self.number == 2:
            if keys[pygame.K_UP]:
                self.rect.move_ip(0, -10) # go up 10 pixels
            elif keys[pygame.K_DOWN]:
                self.rect.move_ip(0, 10) # go down 10 pixels

        self.draw(surface, self.color) # redraw player at correct location

#redraws the gameboard to make sure it is the most current gameboard state
#  requires surface: Window object, players: list of Player objects, ball: Ball object
def redrawWindow(surface, players, ball):
    drawScoreboard(surface, ball) # redraw scoreboard

    ball.draw(surface, ball.color) # redraw ball

    for i in range(len(players)):
        players[i].draw(surface, players[i].color) # redraw each player

    # redraw center line
    pygame.draw.line(surface.win, ball.color, (surface.width//2,0), (surface.width//2,surface.height), 5)

#redraws scoreboard
#  requires surface: Window object, ball: Ball object
#    needs ball to determine scoreboard's color
def drawScoreboard(surface, ball):
    scoreStr = f"{surface.score[0]}    {surface.score[1]}"
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render(scoreStr, True, ball.color, surface.color)
    textRect = text.get_rect()
    textRect.center = (surface.width//2, 30)
    surface.win.blit(text, textRect)

#sets up and runs the game
def run():
    #initializing needed game objects
    white = (255,255,255) # players, scoreboard, and line color
    black = (0,0,0) # background color

    pygame.init()
    win = Window(600, 500, black)

    ball = Ball(win, [5,5], 20, white)
    playerOne = Player(win, 25, 100, white, 1)
    playerOne.draw(win, white)
    playerTwo = Player(win, 25, 100, white, 2)
    playerTwo.draw(win, white)

    playersList = [playerOne, playerTwo]

    #running the game
    while True:
        #allow for x button on pygame window to work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit() # stops Segmentation fault from occurring

        pygame.time.delay(20)
        win.clock.tick(45)

        playerOne.move(win)
        playerTwo.move(win)
        ball.movingDraw(win, playersList)

        redrawWindow(win, playersList, ball)

        win.update()


### MAIN METHOD ###
run()

import pygame

#width = 500
#height = 500

class Window():
    def __init__(self, height, width, color):
        self.height = height
        self.width = width
        self.color = color
        self.win = pygame.display.set_mode((width, height))
        self.win.fill(color)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pong Alpha")
        self.score = [0,0]

    def update(self):
        pygame.display.update()



class Cube():
    def __init__(self, color, posx, posy, dir, size):
        self.rect = pygame.Rect(posx, posy, size, size)
        self.color = color
        self.direction = dir
        self.size = size
        #turn posx and posy into list?

    def movingSquare(self, surface):
        if self.rect.x + self.size >= surface.width or self.rect.x + self.direction[0] <= 0:
            self.direction[0] *= -1
        if self.rect.y + self.size >= surface.height or self.rect.y + self.direction[1] <= 0:
            self.direction[1] *= -1
        self.rect.move_ip(self.direction[0], self.direction[1])


    def draw(self, surface): #add color, then can code to choose between background and actual color
        pygame.draw.rect(surface.win, self.color, self.rect) #(0,255,0), self.rect)

    def movingDraw(self, surface): #, dirx, diry):
        pygame.draw.rect(surface.win, surface.color, self.rect)
        self.movingSquare(surface)
        self.draw(surface)
        #pygame.draw.rect(surface, self.color, self.rect) # (0,255,0), self.rect)

    def checkCollide(self, rect):
        return self.rect.colliderect(rect)

class Ball():
    def __init__(self, color, posx, posy, dir, size):
        self.rect = pygame.Rect(posx, posy, size, size)
        self.color = color
        self.direction = dir
        self.size = size
        #turn posx and posy into list?

    def movingSquare(self, surface, collided):
        # need to factor in movement of paddle
        #  create function to check if paddle is moving then factor that in
        if collided:
            if self.direction[0] < 20 and self.direction[0] > -20:
                if self.direction[0] < 0:
                    self.direction[0] -= 1
                else:
                    self.direction[0] += 1
            self.direction[0] *= -1
            #self.direction[1] *=
        #NEED TO CHANGE THIS TO DISPLAY SCORE AND RESET BALL
        if self.rect.x + self.size >= surface.width: #or self.rect.x + self.direction[0] <= 0:
            #self.direction[0] *= -1
            #print("Score P1")
            surface.score[0] += 1
            self.direction[0] = 5
            self.reset(surface)
        elif self.rect.x + self.direction[0] <= 0:
            #print("Score P2")
            surface.score[1] += 1
            self.direction[0] = -5
            self.reset(surface)
        if self.rect.y + self.size >= surface.height or self.rect.y + self.direction[1] <= 0:
            self.direction[1] *= -1
        self.rect.move_ip(self.direction[0], self.direction[1])


    def draw(self, surface): #add color, then can code to choose between background and actual color
        pygame.draw.rect(surface.win, self.color, self.rect) #(0,255,0), self.rect)

    def movingDraw(self, surface, players): #, dirx, diry):
        pygame.draw.rect(surface.win, surface.color, self.rect)
        self.movingSquare(surface, self.checkCollideWithPlayers(players))
        self.draw(surface)
        #pygame.draw.rect(surface, self.color, self.rect) # (0,255,0), self.rect)

    def checkCollide(self, rect):
        return self.rect.colliderect(rect)

    def checkCollideWithPlayers(self, players):
        for i in range(len(players)):
            if self.checkCollide(players[i].rect):
                return True
        return False

    def reset(self, surface):
        pygame.draw.rect(surface.win, surface.color, self.rect)
        self.rect.x = 250
        self.rect.y = 250
        #self.draw(surface)


class Player():
    def __init__(self, posx, posy, width, height, number):
        #self.rect = Cube((255,255,255), 0, 250, 0, 50)
        self.rect = pygame.Rect(posx, posy, width, height)
        self.number = number

    def draw(self, surface):
        #self.rect.draw(surface) [if using cube]
        pygame.draw.rect(surface.win, (255,255,255), self.rect)

    def move(self, surface):
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
            #    pygame.quit()
        keys = pygame.key.get_pressed()

        #for key in keys:
        if self.number == 1:
            if keys[pygame.K_w]:
                pygame.draw.rect(surface.win, (0,0,0), self.rect)
                self.rect.move_ip(0, -10)
                pygame.draw.rect(surface.win, (255,255,255), self.rect)
            elif keys[pygame.K_s]:
                pygame.draw.rect(surface.win, (0,0,0), self.rect)
                self.rect.move_ip(0, 10)
                pygame.draw.rect(surface.win, (255,255,255), self.rect)
        elif self.number == 2:
            if keys[pygame.K_UP]:
                pygame.draw.rect(surface.win, (0,0,0), self.rect)
                self.rect.move_ip(0, -10)
                pygame.draw.rect(surface.win, (255,255,255), self.rect)
            elif keys[pygame.K_DOWN]:
                pygame.draw.rect(surface.win, (0,0,0), self.rect)
                self.rect.move_ip(0, 10)
                pygame.draw.rect(surface.win, (255,255,255), self.rect)


#should make a redrawWindow() instead of drawing in each method
#  should redraw each object again
def redrawWindow(win, players, ball):
    drawScoreboard(win)

    ball.draw(win)
    for i in range(len(players)):
        players[i].draw(win)
    pygame.draw.line(win.win, (255,255,255), (250,0), (250,500), 5)

def drawScoreboard(win):
    scoreStr = f"{win.score[0]}    {win.score[1]}"
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render(scoreStr, True, (255,255,255), (0,0,0))
    textRect = text.get_rect()
    textRect.center = (250, 30)
    win.win.blit(text, textRect)

def run():
    pygame.init()
    win = Window(500, 500, (0,0,0))
    #win = pygame.display.set_mode((width, height))
    #clock = pygame.time.Clock()
    #win.fill((0,0,0))
    #aRect = pygame.Rect(10, 10, 25, 50)
    #aSquare = pygame.Rect(100, 100, 25, 25)
    #movingSquare = pygame.Rect(100, 150, 25, 25)
    #pygame.draw.rect(win.win, (255,255,255), aRect)
    #pygame.draw.rect(win.win, (255,0,0), aSquare)
    #pygame.draw.rect(win, (255,0,0), movingSquare)

    #horiSquare = Cube((0,255,0), 100, 150, [5,0], 25)
    #vertSquare = Cube((0, 0, 255), 200, 100, [0,5], 30)

    #bothSquare = Cube((100, 100, 100), 300, 200, [5,5], 20)

    #pygame.display.update()

    ball = Ball((255,255,255), 250, 250, [5,5], 20)
    playerOne = Player(0, 200, 25, 100, 1)
    playerOne.draw(win)
    playerTwo = Player(475, 200, 25, 100, 2)
    playerTwo.draw(win)

    playersList = [playerOne, playerTwo]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit() # stops Segmentation fault from occurring

        pygame.time.delay(20)
        win.clock.tick(10)
        #pygame.draw.rect(win, (0,0,0), movingSquare)
        # pygame.draw.rect(win, (0,255,0), movingSquare)
        #movingSquare.move_ip(5, 5) # if I wanted to use just the move(), I would need to reassign it to itself
        #pygame.draw.rect(win, (0,255,0), movingSquare)
        #movingSquare(win, movingSquare)

        #movingSquare.movingSquare()
        #movingSquare.draw(win)

        # if horiSquare.rect.x + 25 >= win.width or horiSquare.rect.x - 5 <= 0:
            # horiSquare.direction[0] *= -1
        #horiSquare.movingDraw(win)

        # if vertSquare.rect.y + 25 >= win.height or vertSquare.rect.y - 5 <= 0:
            # vertSquare.direction[1] *= -1
        #vertSquare.movingDraw(win)


        # if bothSquare.rect.x + 25 >= win.width or bothSquare.rect.x - 5 <= 0:
            # bothSquare.direction[0] *= -1
        #bothSquare.movingDraw(win)
        # if bothSquare.rect.y + 25 >= win.height or bothSquare.rect.y - 5 <= 0:
            # bothSquare.direction[1] *= -1
        #bothSquare.movingDraw(win)
        #print("mSquare x:" + str(movingSquare.rect.x))

        playerOne.move(win)
        playerTwo.move(win)
        ball.movingDraw(win, playersList)

        #if bothSquare.checkCollide(playerOne.rect):
        #    print("Collision detected")

        redrawWindow(win, playersList, ball)
        #pygame.display.update()
        win.update()

run()

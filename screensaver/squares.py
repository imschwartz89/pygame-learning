import pygame
import random

# add block randomly or with key press
# add cube(ball) with key press
# need to figure out if i can test lines on rect for collide, because points are too finicky

class Window():
    def __init__(self, height, width, color):
        self.height = height
        self.width = width
        self.color = color
        self.win = pygame.display.set_mode((width, height))
        self.win.fill(color)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Block Bounce")
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

    def movingSquare(self, surface, blockList, cubeList):

        collidedBlock = self.checkBlockColl(blockList)
        collidedCube = self.checkCubeColl(cubeList)

        if collidedBlock != -1:
            #print("collided")
            #collides on bottom or top of Cube
            if blockList[collidedBlock].rect.collidepoint(self.rect.midbottom) or blockList[collidedBlock].rect.collidepoint(self.rect.midtop):
                #self.direction[0] *= -1
                self.direction[1] *= -1
                removeBlock(blockList, collidedBlock, surface)
                #collides on right or left
            elif blockList[collidedBlock].rect.collidepoint(self.rect.midleft) or blockList[collidedBlock].rect.collidepoint(self.rect.midright):
                self.direction[0] *= -1
                removeBlock(blockList, collidedBlock, surface)
        """
        if collidedCube != -1:
            if cubeList[collidedCube].rect.collidepoint(self.rect.midbottom) or cubeList[collidedCube].rect.collidepoint(self.rect.midtop):
                #self.direction[0] *= -1
                self.direction[1] *= -1
                #collides on right or left
            elif cubeList[collidedCube].rect.collidepoint(self.rect.midleft) or cubeList[collidedCube].rect.collidepoint(self.rect.midright):
                self.direction[0] *= -1
        """

        if self.rect.x + self.size >= surface.width or self.rect.x + self.direction[0] <= 0:
            self.direction[0] *= -1
        if self.rect.y + self.size >= surface.height or self.rect.y + self.direction[1] <= 0:
            self.direction[1] *= -1
        self.rect.move_ip(self.direction[0], self.direction[1])


    def draw(self, surface, color): #add color, then can code to choose between background and actual color
        pygame.draw.rect(surface.win, color, self.rect) #(0,255,0), self.rect)

    def movingDraw(self, surface, blockList, cubeList): #, dirx, diry):
        #pygame.draw.rect(surface.win, surface.color, self.rect)
        self.draw(surface, surface.color)
        self.movingSquare(surface, blockList, cubeList)
        self.draw(surface, self.color)
        #pygame.draw.rect(surface, self.color, self.rect) # (0,255,0), self.rect)

    def checkCollide(self, rect):
        return self.rect.colliderect(rect)

    def checkBlockColl(self, blockList):
        for i in range(len(blockList)):
            if self.checkCollide(blockList[i].rect):
                return i
        return -1

    def checkCubeColl(self, cubeList):
        for i in range(len(cubeList)):
            if self != cubeList[i]:
                if self.checkCollide(cubeList[i].rect):
                    return i
        return -1


#block class, other functions?
class Block():
    def __init__(self, color, posx, posy, width, length):
        self.rect = pygame.Rect(posx, posy, width, length)
        self.color = color

    def draw(self, surface, color):
        pygame.draw.rect(surface.win, color, self.rect)


#make random color, make random position, make random size
def addBlock(surface, blockList):
    c = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    x = random.randint(0, surface.width)
    y = random.randint(0, surface.height)
    w = random.randint(50,100)
    h = random.randint(50,100)
    newBlock = Block(c, x, y, w, h)
    blockList.append(newBlock)

#make random color, make random postion, make random size?, random speed/direction
def addCube(surface, cubeList):
    c = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    s = random.randint(10,75)
    x = random.randint(0, surface.width - s)
    y = random.randint(0, surface.height - s)
    d = [random.randint(-10,10), random.randint(-10,10)]
    newCube = Cube(c, x, y, d, s)
    cubeList.append(newCube)

#maybe should just return the block that is removed and it then gets drawed on where it is called
def removeBlock(blockList, index, surface):
    block = blockList.pop(index)
    block.draw(surface, (0,0,0))

def removeCube(cubeList, index, surface):
    cube = cubeList.pop(index)
    cube.draw(surface, (0,0,0))



def drawBlocks(surface, blockList):
    for i in range(len(blockList)):
        blockList[i].draw(surface, blockList[i].color)

def drawCubes(surface, cubeList, blockList):
    for i in range(len(cubeList)):
        cubeList[i].movingDraw(surface, blockList, cubeList)

def run():
    pygame.init()
    win = Window(750, 1000, (0,0,0))
    #win = pygame.display.set_mode((width, height))
    #clock = pygame.time.Clock()
    #win.fill((0,0,0))
    #aRect = pygame.Rect(10, 10, 25, 50)
    #aSquare = pygame.Rect(100, 100, 25, 25)
    #movingSquare = pygame.Rect(100, 150, 25, 25)
    #pygame.draw.rect(win.win, (255,255,255), aRect)
    #pygame.draw.rect(win.win, (255,0,0), aSquare)
    #pygame.draw.rect(win, (255,0,0), movingSquare)
    blkList = []
    cbList = []
    #horiSquare = Cube((0,255,0), 100, 150, [5,0], 25)
    #vertSquare = Cube((0, 0, 255), 200, 100, [0,5], 30)

    #bothSquare = Cube((100, 100, 100), 300, 200, [5,5], 20)

    #blockOne = Block((255, 255, 255), 250, 250, 100, 150)
    addBlock(win, blkList)
    addCube(win, cbList)
    #need to add cubes to list of Cubes to check for collisions (might need to use groups)
    #need to add blocks to list of Blocks to check for collisions

    blockWait = 0
    cubeWait = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit() # stops Segmentation fault from occurring

        pygame.time.delay(20)
        win.clock.tick(20)

        #horiSquare.movingDraw(win, blkList)

        #vertSquare.movingDraw(win, blkList)

        #bothSquare.movingDraw(win, blkList)
        #print("mSquare x:" + str(movingSquare.rect.x))

        if cubeWait == 60:
            addCube(win, cbList)
            if len(cbList) >= 10:
                removeCube(cbList, 0, win)
            cubeWait = 0

        if blockWait == 15:
            addBlock(win, blkList)
            blockWait = 0

        #blkList[0].draw(win, blkList[0].color)
        drawBlocks(win, blkList)
        drawCubes(win, cbList, blkList)

        win.update()
        blockWait += 1
        cubeWait += 1
run()

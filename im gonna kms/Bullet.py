from MyConstants import PLAYER_WIDTH, BULLET_SPEED, BULLET_SIZE, WINDOW_HEIGHT
from myLists import BULLET_LIST



def isInside(pos1, pos2, sample):
    if sample > pos1 and sample < pos2:
        return True
    else:
        return False

class Bullet:
    
    def __init__(self, xPos, yPos, canKillPlayer):
        self.xPos = xPos
        self.yPos = yPos
        self.size = BULLET_SIZE
        self.speed = BULLET_SPEED
        self.canKillPlayer = canKillPlayer
        BULLET_LIST.append(self)

    def __del__(self):
       ## print("Bullet destroyed")
       return

    def draw(self, canvas):
        canvas.create_rectangle(self.xPos, self.yPos, self.xPos + self.size, self.yPos + self.size, fill='white')

    def update(self):
        self.doMovement()
        self.detectOutOfBounds()

    def doMovement(self):
        if self.canKillPlayer == True:
            self.yPos += self.speed
        else:
            self.yPos -= self.speed
    
    def detectCollision(self, object):
        if (isInside(object.xPos, object.xPos + object.width, self.xPos) or isInside(object.xPos, object.xPos + object.width, self.xPos + self.size)) and \
            (isInside(object.yPos, object.yPos + object.width, self.yPos) or isInside(object.yPos, object.yPos + object.width, self.yPos + self.size)):
        
            print("Collision detected!")
            self.handleCollision()
            object.handleCollision()
        
    def detectOutOfBounds(self):
        if self.yPos <= 0 or self.yPos >= WINDOW_HEIGHT:
            if self in BULLET_LIST:
                BULLET_LIST.remove(self)
            # BULLET_LIST.remove(self)
            # self.__del__

    def handleCollision(self):
        if self in BULLET_LIST:
            BULLET_LIST.remove(self)
        # BULLET_LIST.remove(self)
        # self.__del__


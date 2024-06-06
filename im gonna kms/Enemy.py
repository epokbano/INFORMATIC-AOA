from MyConstants import WINDOW_WIDTH, WINDOW_HEIGHT, INTERFACE_WIDTH, ENEMY_WIDTH, PLAYER_WIDTH, FPS_CAP
from Bullet import Bullet
from myLists import ENEMY_LIST, BULLET_LIST


class Enemy:
    def __init__(self, xPos, yPos):
        self.xPos = xPos   
        self.yPos = yPos
        self.width = ENEMY_WIDTH
        self.shootingFrequency = 1
        self.timer = FPS_CAP/self.shootingFrequency
        self.speed = 2
        ENEMY_LIST.append(self)


    def __del__(self):
        print("enemy killed")

    def draw(self, canvas):
        canvas.create_rectangle(self.xPos, self.yPos, self.xPos + self.width, self.yPos + self.width, fill='red')

    def update(self):
        self.doMovement()
        self.tryShooting()
        ## shoot 

    def doMovement(self):
        if self.speed > 0:   ## prawa kolizja
            if (self.rightBoundPos() + self.speed >= WINDOW_WIDTH): 
                self.xPos = WINDOW_WIDTH - self.width ##clip to wall
                self.speed = -self.speed
            else:
                self.xPos += self.speed

        else:           ## lewa kolizja
            if (self.xPos + self.speed <= INTERFACE_WIDTH): 
                self.xPos = INTERFACE_WIDTH
                self.speed = -self.speed
            else:
                self.xPos += self.speed

    def tryShooting(self):
        if self.timer == 0:
            BULLET_LIST.append(Bullet(self.xPos + self.width/2, self.yPos + self.width, True))
            self.timer = FPS_CAP/self.shootingFrequency
        else:
            self.timer -= 1

    def rightBoundPos(self):
        return self.xPos + self.width
    
    def handleCollision(self):
        ENEMY_LIST.remove(self)
        self.__del__
    
    
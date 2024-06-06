import time
from Bullet import Bullet
from MyConstants import WINDOW_WIDTH, WINDOW_HEIGHT, INTERFACE_WIDTH, ENEMY_WIDTH, PLAYER_WIDTH, FPS_CAP
from myLists import BULLET_LIST






class Player:
    def __init__(self, xPos, yPos):
        self.ShootingFrequency = 1
        self.xPos = xPos
        self.yPos = yPos
        self.speed = 5
        self.currentSpeed = 0
        self.gameOver = False
        self.timer = FPS_CAP/self.ShootingFrequency
        self.BulletCount = 1
        self.BulletSpread = False
        self.PlayerHP = 3
        self.width = PLAYER_WIDTH
        self.moveLimit = [False, False]
        self.shootLimit = False
        self.isShooting = False
        self.lastShotTime = 0
        self.shootCooldown = 1



    def draw(self, canvas):
        canvas.create_rectangle(self.xPos, self.yPos, self.xPos + PLAYER_WIDTH, self.yPos + PLAYER_WIDTH, fill='blue')

    def update(self):
        self.doMovement()
        self.tryShooting()
        return
        ## shoot 

    def initiatePlayerMovementSetup(self, root):
        root.bind("<KeyPress-A>", self.onKeyPress)
        root.bind("<KeyPress-a>", self.onKeyPress)
        root.bind("<KeyPress-D>", self.onKeyPress)
        root.bind("<KeyPress-d>", self.onKeyPress)
        root.bind("<KeyPress-X>", self.onKeyPress)
        root.bind("<KeyPress-x>", self.onKeyPress)

        root.bind("<KeyRelease-A>", self.onKeyRelease)
        root.bind("<KeyRelease-a>", self.onKeyRelease)
        root.bind("<KeyRelease-D>", self.onKeyRelease)
        root.bind("<KeyRelease-d>", self.onKeyRelease)
        root.bind("<KeyRelease-X>", self.onKeyRelease)
        root.bind("<KeyRelease-x>", self.onKeyRelease)

    def onKeyPress(self, event):

        keysym = event.keysym.lower()  # Convert to lowercase
        if keysym == 'a':
            if self.moveLimit[0] == False:
                self.moveLimit[0] = True
                self.currentSpeed -= self.speed
                
        if keysym == 'd':
            if self.moveLimit[1] == False:
                self.moveLimit[1] = True
                self.currentSpeed += self.speed
                
        if keysym == 'x':
            # if not self.shootLimit and (currentTime - self.lastShotTime >= self.shootCooldown):
            #     BULLET_LIST.append(Bullet(self.xPos + self.width/2, self.yPos, True))  # Bullet spawning adjusted
            #     self.lastShotTime = currentTime
            #     self.shootLimit = True
            self.isShooting = True
                

    def onKeyRelease(self, event):
        keysym = event.keysym.lower()
        if event.keysym == 'a':
            self.moveLimit[0] = False
            self.currentSpeed += self.speed
            
        if event.keysym == 'd':
            self.moveLimit[1] = False
            self.currentSpeed -= self.speed
            
        if event.keysym == 'x':
            self.isShooting = False


    def doMovement(self):
        ##print("Current speed:", self.currentSpeed)
        if self.currentSpeed >= 0:   ## prawa kolizja
            if (self.rightBoundPos() + self.currentSpeed >= WINDOW_WIDTH): 
                self.xPos = WINDOW_WIDTH - self.width - 1
                print("Clipping right")
            else:
                self.xPos += self.currentSpeed

        elif self.currentSpeed <= 0 :          ## lewa kolizja
            if (self.xPos + self.currentSpeed <= INTERFACE_WIDTH):
                print("Clipping left")
                self.xPos = INTERFACE_WIDTH
            else:
                self.xPos += self.currentSpeed

    def rightBoundPos(self):
        return self.xPos + self.width
    
    def handleCollision(self):
        print("Life before: ", self.PlayerHP)
        # self.PlayerHP -= 0.5
        if self.PlayerHP == 0:
            print("GAME OVER")
            self.triggerGameOver()

    def triggerGameOver(self):
        self.gameOver = True

    def tryShooting(self):
            # if self.shootLimit == False:
            #     if self.timer == 0:
            #         BULLET_LIST.append(Bullet(self.xPos + self.width/2, self.yPos + self.width, True))
            #         self.timer = FPS_CAP/self.ShootingFrequency
            #         self.shootLimit = True
            #     else:
            #         self.timer -= 1
            #         self.shootLimit = True
        currentTime = time.time()
        if self.isShooting and (currentTime - self.lastShotTime >= self.shootCooldown):
            BULLET_LIST.append(Bullet(self.xPos + self.width / 2, self.yPos, False))
            self.lastShotTime = currentTime

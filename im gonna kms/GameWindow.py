import math
import time
import tkinter as tk
from Enemy import Enemy
from MyConstants import WINDOW_WIDTH, WINDOW_HEIGHT, INTERFACE_WIDTH, FPS_CAP, SPAWN_OFFSET_X, SPAWN_OFFSET_Y, ENEMY_WIDTH, ENEMY_DISTANCE_X, ENEMY_DISTANCE_Y
from Player import Player
from myLists import BULLET_LIST, ENEMY_LIST
import sys





class GameWindow:
    def __init__(self, master, width, height):
        self.master = master
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(master, width=width, height=height, bg="BLACK")
        self.canvas.pack()
        self.master.protocol("WM_DELETE_WINDOW", self.stop_game)
        self.playerObject = None
        self.enemyCount = 0
        self.nextWaveTextId = None
        self.textColorTimer = 0
        self.textColor = "white"
        
        
    def stop_game(self):
        self.running = False
        self.master.destroy()

    

    def tick(self):
        
        if len(ENEMY_LIST) == 0:
            if self.enemyCount < 30:
                self.enemyCount += 1
            self.spawnWave(self.enemyCount)
            self.clearBullets()
            self.pauseBetweenWaves(2)
        
        for i in ENEMY_LIST:
            i.update()
        self.playerObject.update()
        for i in BULLET_LIST:
            i.update()
            if i.canKillPlayer:
                i.detectCollision(self.playerObject)
            else:
                for j in ENEMY_LIST:
                    i.detectCollision(j)
        self.textColorTimer += 1
        self.updateTextColor()

    def render(self):
        if self.canvas:
            self.canvas.delete("all")
            self.canvas.create_rectangle(0,0, INTERFACE_WIDTH, WINDOW_HEIGHT, outline= "#FF00FF", fill="grey12")
            
            self.playerObject.draw(self.canvas)

            for i in ENEMY_LIST:
                if i.xPos >= INTERFACE_WIDTH and i.xPos <= WINDOW_WIDTH:
                    i.draw(self.canvas)
            for i in BULLET_LIST:
                i.draw(self.canvas)
            if len(ENEMY_LIST) == 0:
                self.showNextWaveText()
            

    def run(self):
        running = True
        clock = time.time()

        while running:
            
            dt = time.time() - clock
            clock = time.time()

            
            self.tick()
            if self.playerObject.gameOver == True:
                sys.exit(0)

            
            self.render()

            
            if dt < 1/FPS_CAP:
                time.sleep(1/FPS_CAP - dt)


            self.master.update()

        print("Game loop exited")
    
    def initiatePlayer(self):
        self.playerObject = Player(500, 500)
    
    def spawnFullRow(self, xPos, rowNumber):
        for i in range(6):
            x = xPos + i * (SPAWN_OFFSET_X + ENEMY_WIDTH)
            y = SPAWN_OFFSET_Y + rowNumber * (ENEMY_WIDTH + ENEMY_DISTANCE_Y)
            print(f"Spawned enemy at ({x}, {y})")
            Enemy(x, y)  
            # Enemy(xPos + (i)*(SPAWN_OFFSET_X + ENEMY_WIDTH), SPAWN_OFFSET_Y + rowNumber *(ENEMY_WIDTH + ENEMY_DISTANCE_Y))
        print("SPAWNING FULL WAVE")
    
    def spawnPartRow(self, xPos, rowNumber, enemyCount):
        
        print({enemyCount})
        for i in range(enemyCount):
            x = xPos + i * (SPAWN_OFFSET_X + ENEMY_WIDTH)
            y = SPAWN_OFFSET_Y + rowNumber * (ENEMY_WIDTH + ENEMY_DISTANCE_Y)
            print(f"Spawned enemy at ({x}, {y})")
            if x < 800:
                Enemy(x, y)
            else:
                x = 445
                Enemy(x,y)

            # Enemy(xPos + (i -1) *(SPAWN_OFFSET_X + ENEMY_WIDTH), SPAWN_OFFSET_Y + rowNumber *(ENEMY_WIDTH + ENEMY_DISTANCE_Y))
        print("SPAWNING PARTIAL WAVE")
    

    def spawnWave(self, enemy_number):
        # rowCount = math.floor(enemy_number / 6)
        rowCount = enemy_number // 6
        lastRowCount = enemy_number % 6
        xPos = INTERFACE_WIDTH + SPAWN_OFFSET_X

        for i in range(rowCount):
            self.spawnFullRow(xPos, i)
        if lastRowCount > 0:
            self.spawnPartRow(xPos, rowCount, lastRowCount)
        elif rowCount == 0:  
            self.spawnPartRow(xPos, 0, enemy_number)

    def clearBullets(self):
        
        BULLET_LIST.clear()
    def showNextWaveText(self):
        
        if self.nextWaveTextId:
            self.canvas.delete(self.nextWaveTextId)
        text_x = INTERFACE_WIDTH + (WINDOW_WIDTH - INTERFACE_WIDTH) / 2
        text_y = WINDOW_HEIGHT / 2
        self.canvas.create_text(text_x, text_y, text="NEXT WAVE", font=("Helvetica", 36), fill=self.textColor)
        

    def pauseBetweenWaves(self, seconds):
        
        time.sleep(seconds)
        
    
    def updateTextColor(self):
        # Update text color periodically
        if self.textColorTimer % 20 == 0:  
            self.toggleTextColor()
    def toggleTextColor(self):
        
        if self.textColor == "white":
            self.textColor = "red"
        else:
            self.textColor = "white"
        

    
    
    
   


                

        


    

############################# MAIN #############################
# Create the Tkinter window
if __name__ == "__main__":
    print("Start of App")
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Space Invaders made in Poland")
    # root.bind("<KeyPress>", onKeyPress)
    # root.bind("<KeyRelease>", onKeyRelease)

    # Run the game
    game = GameWindow(root, WINDOW_WIDTH, WINDOW_HEIGHT)

    game.initiatePlayer()
    game.playerObject.initiatePlayerMovementSetup(root)
    game.run()


    root.mainloop()


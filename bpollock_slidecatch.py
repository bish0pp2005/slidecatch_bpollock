import pygame, simpleGE, random

class Ram(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("ram.png")
        self.setSize(30, 30)
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(3, 8)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()


class DVD(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("dvd.png")
        self.setSize(60, 60)
        self.position = (320, 400)
        self.moveSpeed = 5
    
    def process(self):
        if self.isKeyPressed(pygame.K_a):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_d):
            self.x += self.moveSpeed
        if self.isKeyPressed(pygame.K_s):
            self.y += self.moveSpeed
        if self.isKeyPressed(pygame.K_w):
            self.y -= self.moveSpeed
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 15"
        

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("smogcity.png")
        
        self.sndRam = simpleGE.Sound("connection.wav")
        self.numRams = 10
        self.score = 0
        self.lblScore = LblScore()  
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 15
        self.lblTime = LblTime()
        self.dvd = DVD(self)
        self.rams = []
        for i in range(self.numRams):
            self.rams.append(Ram(self))
        
        self.sprites = [self.dvd,
                        self.rams,
                        self.lblScore,
                        self.lblTime]
    def process(self):
            for ram in self.rams:
                if ram.collidesWith(self.dvd):
                    ram.reset()
                    self.sndRam.play()
                    self.score += 1
                    self.lblScore.text = f"Score: {self.score}"
                
            self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
            if self.timer.getTimeLeft() < 0:
                print(f"Score: {self.score}")
                self.stop()
class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        
        self.prevScore = prevScore
        
        self.setImage("smogcity.png")
        self.response = "Quit"
        
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "You are a DVD disk",
        "Move with WASD.",
        "Grab as much RAM as you can, before time runs out!"
        ]
        
        self.directions.center = (320, 200)
        self.directions.size = (520, 260)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last score: 0"
        self.lblScore.center = (320, 400)
        
        self.lblScore.text = f"Last score: {self.prevScore}"
        
        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
            
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
            

        
def main():
    keepGoing = True
    lastScore = 0
    while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()
        if instructions.response == "Play":
            game = Game()
            game.start()
            lastScore = game.score
        else: 
            keepGoing = False
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()
# Pygame module for Graphic GUI
import pygame
pygame.init()

def buildWindow():
    """
    Build window is called when a fullscreen window is needed.
    Return a screen as a surface object.
    """
    #screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen = pygame.display.set_mode((320,320),pygame.RESIZABLE)
    return screen

"""
def run():
    clock = pygame.time.Clock()
    
    animationsList = {"idle":40}
    spriteMapDir = "./Sprite/virtualTrainer.PNG"
    spriteImgSize = [64, 64]

    screen = buildWindow()
    #Window is a surface object where all objects should be blit on here first, then be rescaled together and blit onto the screen.
    window = pygame.Surface((512,288))

    #Finding Aspect Ratio
    if screen.get_width()/16 > screen.get_height()/9:
        winWidth = screen.get_height()*16/9
        winHeight = screen.get_height()
        winOffset = [(screen.get_width()-winWidth)/2,0]
    else:
        winWidth = screen.get_width()
        winHeight = screen.get_width()*9/16
        winOffset = [0,(screen.get_height()-winHeight)/2]
    
    trainer = Sprite(animationsList, spriteMapDir, spriteImgSize, window)

    tick = 0
    runBool = True
    while runBool:

        if screen.get_width()/16 > screen.get_height()/9:
            winWidth = screen.get_height()*16/9
            winHeight = screen.get_height()
            winOffset = [(screen.get_width()-winWidth)/2,0]
        else:
            winWidth = screen.get_width()
            winHeight = screen.get_width()*9/16
            winOffset = [0,(screen.get_height()-winHeight)/2]
        
        window.fill((100,100,100))
        trainer.playAnimation([256-trainer.spriteImgSize[0]/2,144-trainer.spriteImgSize[1]/2],round(tick))
        tick += 0.2

        screen.fill((0,0,0))
        newWindow = pygame.transform.scale(window,(winWidth,winHeight))
        screen.blit(newWindow,(winOffset[0],winOffset[1]))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runBool = False
        
        pygame.display.flip()
        clock.tick(60)
                
    pygame.quit()
"""

class Sprite:
    def __init__(self, publicAnimationsList, publicSpriteMapDir, publicSpriteSize, publicScreen):
        """
        Sprite is an object to be displayed on the screen.
          
        publicAnimationsList: This is a list of the names of different animations.
        publicSpriteMapDir: This is the directory of the sprite map.
        publicSpriteSize: This represents the dimension of each sprite.
        publicScreen: Targetted surface object to be drawn on.
        """
        self.screen = publicScreen
        self.animationsList = list(publicAnimationsList.keys())
        
        self.status = self.animationsList[0]
        self.spriteMapDir = publicSpriteMapDir
        self.spriteImgSize = publicSpriteSize
        self.spriteAnimation = self.retrieveSprites(publicAnimationsList)
        

    def retrieveSprites(self, publicAnimationsList):
        """
        Extract sprites from a spriteMap and store them in a dictionary.
        Returns a dictionary with key-value pair of animation names and list of its frames as surface objects.
        Returns null and print "No File found." when spriteMapDir has no accessible file.

        Requirement for Sprite Map, each row has a list of images per set. The order of row should match the order of animationsList.
        """
        try:
            spriteMapImg = pygame.image.load(self.spriteMapDir).convert_alpha()
        except FileNotFoundError:
            print("No File found.")
            return None

        spriteAnimation = {}

        sliderY = 0
        for setName in publicAnimationsList:
            spriteAnimation[setName] = []
            
            for sliderX in range(publicAnimationsList[setName]):
                #cropSprite is initiated
                cropSprite = pygame.Surface((self.spriteImgSize[0], self.spriteImgSize[1]))
                cropSprite = cropSprite.convert_alpha()
                cropSprite.fill((0,0,0,0))
                #cropSprite has cropped spriteMapImg pasted on it, sliderX slides the spriteMapImg to the right and sliderY slides the spriteMapImg down.
                cropSprite.blit(spriteMapImg, (0, 0), (sliderX * self.spriteImgSize[0], sliderY * self.spriteImgSize[1], self.spriteImgSize[0], self.spriteImgSize[1]))
                spriteAnimation[setName].append(cropSprite)

            sliderY += 1
            
        return spriteAnimation

    def playAnimation(self, position, tick):
        """
        Draw an image to the screen.
            
        position: 2D tuple/ 2D list of top right position to be drawn on the screen.
        counter: An integer of the index of image/ current runtime tick.
        """
        lengthList = len(self.spriteAnimation[self.status])
        self.screen.blit(self.spriteAnimation[self.status][tick % lengthList], position)





    

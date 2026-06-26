import pygame
import virtualTrainer
import escapeMenu
import sys


def run():
    clock = pygame.time.Clock()

    #Initialise Virtual Trainer
    animationsList = {"idle":40}
    spriteMapDir = "./Sprite/virtualTrainer.PNG"
    spriteImgSize = (64, 64)

    #Initial Escape Menu
    publicEscMenuDir = "./Sprite/EscapeMenu.png"
    publicEscMenuSize = (256,144)
    publicRetMenuDir = "./Sprite/ReturnButton.png"
    publicRetMenuSize = (118,38)
    publicLeaveDir = "./Sprite/LeaveButton.png"
    publicLeaveSize = (118,38)

    pygame.mouse.set_visible(False)

    screen = virtualTrainer.buildWindow()
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
    
    trainer = virtualTrainer.Sprite(animationsList, spriteMapDir, spriteImgSize, window)
    escMenu = escapeMenu.EscapeMenu(publicEscMenuDir, publicEscMenuSize, publicRetMenuDir, publicRetMenuSize, publicLeaveDir, publicLeaveSize, window)

    tick = 0
    tickIncrement = 0.2
    runBool = True
    returnBool = False
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
        escMenu.playAnimation([256-publicEscMenuSize[0]/2,144-publicEscMenuSize[1]/2])
        tick += tickIncrement

        mouseX = (pygame.mouse.get_pos()[0] - winOffset[0])/winWidth*512
        mouseY = (pygame.mouse.get_pos()[1] - winOffset[1])/winHeight*288
        mousePos = (mouseX, mouseY)
        pygame.draw.rect(window, "Red", pygame.Rect((mousePos),(5,5)))
        
        screen.fill((0,0,0))
        newWindow = pygame.transform.scale(window,(winWidth,winHeight))
        screen.blit(newWindow,(winOffset[0],winOffset[1]))

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                runBool = False
            
            runBool, returnBool = escMenu.escapeMenuUpdate(event, mousePos, runBool, returnBool)
        
        pygame.display.flip()
        clock.tick(60)
                
    pygame.quit()
    sys.exit()

run()

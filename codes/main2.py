import pygame
import virtualTrainer
import escapeMenuCooler as escapeMenu
import sys
import MainMenu
import json
import cv2
import PauseSurface
import Authentication
import AccountInfo
from AnimationSequence import statusUpdate
from imageSurface import getCameraSurface
import firebase_admin

def run():
    pygame.init()

    clock = pygame.time.Clock()

    cred = firebase_admin.credentials.Certificate("Sprite/privateKey.json")
    firebase_admin.initialize_app(cred, {'databaseURL' : "https://easy-fit-storage-default-rtdb.firebaseio.com/" })

    #Initialise Virtual Trainer
    animationsList = {"idle":40,
                      "lieR":11,
                      "lieL":11,
                      "sitUpR":6,
                      "sitUpL":6,
                      "sitDownR":6,
                      "sitDownL":6}
    spriteMapDir = "./Sprite/virtualTrainer.PNG"
    spriteImgSize = (64, 64)

    #Initialise Escape Menu Constants
    publicEscMenuDir = "./Sprite/EscapeMenu.png"
    publicEscMenuSize = (256,144)
    publicRetMenuDir = "./Sprite/ReturnButton.png"
    publicRetMenuSize = (118,38)
    publicLeaveDir = "./Sprite/LeaveButton.png"
    publicLeaveSize = (118,38)

    #Initialise Main Menu Constants
    mainMenuBackgroundImgDir = "./Sprite/Background.PNG"
    menuOverlayImgDir = "./Sprite/MenuOverlay.png"

    #Initialise In-game Constants
    gameBackgroundImgDir = "./Sprite/InGameBg.png"
    gameBackgroundImgSurf = pygame.image.load(gameBackgroundImgDir)

    #Authentication Constant
    authBackgroundImgDir = "./Sprite/AuthBackground.PNG"

    worksetMoveContentDir = "./Sprite/worksetMoveContent.json"

    fontDir = "./Sprite/Monocraft.ttc"
    fontSize = 16
    font = pygame.font.Font(fontDir, fontSize)
    leaderboardContentDir = "./Sprite/leaderboardContent.json"

    worksetMoveFile = open(worksetMoveContentDir, "r")
    worksetMoveContent = json.load(worksetMoveFile)
    worksetMoveFile.close()

    screen = virtualTrainer.buildWindow()
    #Window is a surface object where all objects should be blit on here first, then be rescaled together and blit onto the screen.
    window = pygame.Surface((512,288))

    trainer = virtualTrainer.Sprite(animationsList, spriteMapDir, spriteImgSize, window)
    escMenu = escapeMenu.EscapeMenu(font, publicEscMenuDir, publicEscMenuSize, 
                                    publicRetMenuDir, publicRetMenuSize, 
                                    publicLeaveDir, publicLeaveSize, 
                                    window)
    mainMenuObj = MainMenu.mainMenu(window, mainMenuBackgroundImgDir, menuOverlayImgDir, 
                                    trainer, worksetMoveContent, fontDir)
    
    pauseSurf = PauseSurface.popUp(window, font)
    scoreSurf = PauseSurface.popUp(window, font)
    authSurf = Authentication.loginSurf(window, font, authBackgroundImgDir)
    
    tick = 0
    tickIncrement = 0.3
    runBool = True
    returnBool = False
    pause = False
    scene = 0
    webcam = cv2.VideoCapture(0)
    pointIncrement = 0
    point = 0

    

    accountInfoDir = "./Sprite/accountInfo.json"

    accountInfoFile = open(accountInfoDir, "r")
    accountInfo = json.load(accountInfoFile)
    accountInfoFile.close()

    if accountInfo["loginStatus"] == False:
        scene = -1
    elif Authentication.check(accountInfo["Username"], accountInfo["Password"]):
        scene = 0
        accountSurf = AccountInfo.accountInfoSurf(window, font, accountInfoDir)
    else:
        Authentication.logout(accountInfoDir)
        scene = -1

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

        if not pause or scene == 0:
            tick += tickIncrement

        mouseX = (pygame.mouse.get_pos()[0] - winOffset[0])/winWidth*512
        mouseY = (pygame.mouse.get_pos()[1] - winOffset[1])/winHeight*288
        mousePos = (mouseX, mouseY)
        

        for event in pygame.event.get():
            
            if scene == -1:
                returnBool = False
                scene, username, password = authSurf.update(event, mousePos)

                #authorised
                if scene == 0:
                    accountInfoFile = open(accountInfoDir, "w")
                    accountInfoToWrite = {"loginStatus": True,
                                          "Username" : username,
                                          "Password" : password}
                    json.dump(accountInfoToWrite, accountInfoFile)
                    accountInfoFile.close()

            else:
                runBool, returnBool = escMenu.escapeMenuUpdate(event, mousePos, runBool, returnBool)

            if scene == 0 and not escMenu.onStatus and not scoreSurf.onStatus:
                trainer.status = "idle"
                lastTickOnMainMenu = tick
                scene, sceneName = mainMenuObj.update(event, mousePos)
                tickIncrement = 0.3
                
                if scene == 1:
                    #Started a workout game
                    print(sceneName)
                    point = 0
                    pause = False
                    pauseSurf.onStatus = False
            
            if scoreSurf.onStatus:
                scoreSurf.update(mousePos, event)

            if scene == 1:
                pause = pauseSurf.update(mousePos, event)
                if pause:
                    tickIncrement = 0
                else:
                    tickIncrement = 0.3

            
            if scene == 2:
                scene = accountSurf.update(event, mousePos)

                    
            if event.type == pygame.QUIT:
                runBool = False


        if scene == -1:
            authSurf.playAnimation(mousePos)
            if scene == 0:
                accountSurf = AccountInfo.accountInfoSurf(window, font, accountInfoDir)

        elif scene == 0:
            mainMenuObj.playAnimation(round(tick), mousePos)
            escMenu.playAnimation([256-publicEscMenuSize[0]/2,144-publicEscMenuSize[1]/2],mousePos)

            scoreSurf.playAnimation(mousePos, "point: " + str(point))

            
            
        elif scene == 1:

            window.blit(gameBackgroundImgSurf, (0,0))
            
            cameraSurface = getCameraSurface(webcam)
            cameraSurface = pygame.transform.scale(cameraSurface, (96*cameraSurface.get_width()/cameraSurface.get_height(),96))
            window.blit(cameraSurface, ((window.get_width()-cameraSurface.get_width())*6/7,(window.get_height()-cameraSurface.get_height())/2))
            
            if pause:
                pauseSurf.onStatus = True
                
            
            if not pause:
                point += pointIncrement
                relativeTick, pause, pointIncrement, scene = statusUpdate(worksetMoveContent, sceneName, 
                                                                   tick-lastTickOnMainMenu, tickIncrement, 
                                                                   trainer, webcam)
            
                #game ends
                if scene == 0:
                    scoreSurf.onStatus = True
                    Authentication.uploadScore(point, accountInfoDir)
            
            trainer.playAnimation([window.get_width()/2-trainer.spriteImgSize[0]/2,
                               (window.get_height()-trainer.spriteImgSize[1])*4/5], 
                               relativeTick)
            
            pointSurface = font.render("Point: "+str(point), True, "black")
            window.blit(pointSurface, ((window.get_width() - pointSurface.get_width())/2, 4))

            pauseSurf.playAnimation(mousePos, "Cannot Detect You!")

            escMenu.playAnimation([256-publicEscMenuSize[0]/2,144-publicEscMenuSize[1]/2],mousePos)

            if returnBool:
                scene = 0
                escMenu.onStatus = False

        elif scene == 2:
            
            accountSurf.playAnimation(mousePos)

            


        screen.fill((0,0,0))
        newWindow = pygame.transform.scale(window,(winWidth,winHeight))
        screen.blit(newWindow,(winOffset[0],winOffset[1]))
        
        pygame.display.flip()
        clock.tick(30)

    webcam.release() 
    pygame.quit()
    sys.exit()

run()

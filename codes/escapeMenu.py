import pygame

class EscapeMenu:
    def __init__(self, publicEscMenuDir, publicEscMenuSize, publicRetMenuDir, publicRetMenuSize, publicLeaveDir, publicLeaveSize, publicScreen):
        """
        EscapeMenu is an object to be displayed on the screen.
          
        publicEscMenuDir: This is the directory of the Escape Menu Image.
        publicEscMenuSize: This is the dimension of the Escape Menu Image.
        publicRetMenuDir: This is the directory of the Return Button Image.
        publicRetMenuSize: This is the dimension of the Return Button Image.
        publicLeaveDir: This is the directory of the Leave Button Image.
        publicLeaveSize : This is the dimension of the Leave Button Image.
        publicScreen: Targetted surface object to be drawn on.
        """
        self.onStatus = False
        self.screen = publicScreen
        
        self.image = pygame.image.load(publicEscMenuDir).convert_alpha()
        self.surface = pygame.Surface(publicEscMenuSize)
        self.surface.blit(self.image,pygame.Rect((0,0),publicEscMenuSize))

        self.buttonsImg = {}
        self.buttonsImg["RetMenu"] = pygame.image.load(publicRetMenuDir).convert_alpha()
        self.buttonsImg["Leave"] = pygame.image.load(publicLeaveDir).convert_alpha()

        offsetEscMenu = ((512 - publicEscMenuSize[0])/2, (288 - publicEscMenuSize[1])/2)
        self.buttonsRect = {}
        self.buttonsRect["RetMenu"] = pygame.Rect(((publicEscMenuSize[0] - publicRetMenuSize[0])/2,(publicEscMenuSize[1] - publicRetMenuSize[1])/2),publicRetMenuSize)
        self.buttonsRect["Leave"] = pygame.Rect(((publicEscMenuSize[0] - publicLeaveSize[0])/2,(publicEscMenuSize[1] - publicLeaveSize[1])*4/5),publicLeaveSize)

        self.surface.blit(self.buttonsImg["RetMenu"], self.buttonsRect["RetMenu"])
        self.surface.blit(self.buttonsImg["Leave"], self.buttonsRect["Leave"])

        self.buttonsRect["RetMenu"] = pygame.Rect((offsetEscMenu[0] + (publicEscMenuSize[0] - publicRetMenuSize[0])/2,offsetEscMenu[1] + (publicEscMenuSize[1] - publicRetMenuSize[1])/2),publicRetMenuSize)
        self.buttonsRect["Leave"] = pygame.Rect((offsetEscMenu[0] + (publicEscMenuSize[0] - publicLeaveSize[0])/2,offsetEscMenu[1] + (publicEscMenuSize[1] - publicLeaveSize[1])*4/5),publicLeaveSize)
        
        self.buttonsIsPressed = {}
        self.buttonsIsPressed["RetMenu"] = False
        self.buttonsIsPressed["Leave"] = False
         
    def escapeMenuUpdate(self, event, mousePos, runBool, returnBool):
        """
        escapeMenuUpdate checks for user inputs to the screen and matches to corresponding responses from the Escape Menu.
        It contains features such as:
        Toggle escape menu on and off.
        Check if buttons on Menu is pressed.

        event: retrieve pygame events from pygame.events
        """
        #toggle on/off
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.onStatus = not self.onStatus
                
                if not self.onStatus:
                    for keyName in self.buttonsIsPressed.keys():
                        self.buttonsIsPressed[keyName] = False

        #check for keydown collision with buttons
        elif self.onStatus and event.type == pygame.MOUSEBUTTONDOWN:
            for keyName in self.buttonsRect.keys():
                self.buttonsIsPressed[keyName] = self.buttonsRect[keyName].collidepoint(mousePos)

        elif self.onStatus and event.type == pygame.MOUSEBUTTONUP:
            
            for keyName in self.buttonsIsPressed.keys():
                
                if self.buttonsIsPressed[keyName] and self.buttonsRect[keyName].collidepoint(mousePos):
                    match keyName:
                        case "RetMenu":
                            returnBool = True
                        case "Leave":
                            runBool = False
                self.buttonsIsPressed[keyName] = self.buttonsRect[keyName].collidepoint(mousePos)

        return runBool, returnBool
            
    def playAnimation(self, position):
        """
        Draw an image to the screen.
            
        position: 2D tuple/ 2D list of top right position to be drawn on the screen.
        """
        if self.onStatus:
            self.screen.blit(self.surface, position)

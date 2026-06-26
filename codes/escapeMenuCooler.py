import pygame

class EscapeMenu:
    def __init__(self, font, publicEscMenuDir, publicEscMenuSize, publicRetMenuDir, publicRetMenuSize, publicLeaveDir, publicLeaveSize, publicScreen):
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
        self.menuSize = publicEscMenuSize
        self.surface.blit(self.image,pygame.Rect((0,0),publicEscMenuSize))

        self.buttonsImg = {}
        #self.buttonsImg["Return"] = pygame.image.load(publicRetMenuDir).convert_alpha()
        #self.buttonsImg["Leave"] = pygame.image.load(publicLeaveDir).convert_alpha()

        self.font = font
        self.buttonsImg["Return"] = pygame.Surface(publicRetMenuSize)
        self.buttonsImg["Return"].fill((153, 204, 255))
        text = self.font.render("Return", True, "black")
        self.buttonsImg["Return"].blit(text, ((self.buttonsImg["Return"].get_width() - text.get_width())/2, 
                                              (self.buttonsImg["Return"].get_height() - text.get_height())/2))
        self.buttonsImg["Leave"] = pygame.Surface(publicLeaveSize)
        self.buttonsImg["Leave"].fill((255, 204, 204))
        text = self.font.render("Leave", True, "black")
        self.buttonsImg["Leave"].blit(text, ((self.buttonsImg["Leave"].get_width() - text.get_width())/2, 
                                             (self.buttonsImg["Leave"].get_height() - text.get_height())/2))

        offsetEscMenu = ((512 - publicEscMenuSize[0])/2, (288 - publicEscMenuSize[1])/2)
        self.buttonsRectLocal = {}
        self.buttonsRectLocal["Return"] = pygame.Rect(((publicEscMenuSize[0] - publicRetMenuSize[0])/2,
                                                        (publicEscMenuSize[1] - publicRetMenuSize[1])/2),publicRetMenuSize)
        self.buttonsRectLocal["Leave"] = pygame.Rect(((publicEscMenuSize[0] - publicLeaveSize[0])/2,
                                                      (publicEscMenuSize[1] - publicLeaveSize[1])*9/10),publicLeaveSize)

        self.surface.blit(self.buttonsImg["Return"], self.buttonsRectLocal["Return"])
        self.surface.blit(self.buttonsImg["Leave"], self.buttonsRectLocal["Leave"])

        self.buttonsRect = {}
        self.buttonsRect["Return"] = pygame.Rect((offsetEscMenu[0] + (publicEscMenuSize[0] - publicRetMenuSize[0])/2,
                                                   offsetEscMenu[1] + (publicEscMenuSize[1] - publicRetMenuSize[1])/2),publicRetMenuSize)
        self.buttonsRect["Leave"] = pygame.Rect((offsetEscMenu[0] + (publicEscMenuSize[0] - publicLeaveSize[0])/2,
                                                 offsetEscMenu[1] + (publicEscMenuSize[1] - publicLeaveSize[1])*9/10),publicLeaveSize)
        
        self.buttonsIsPressed = {}
        self.buttonsIsPressed["Return"] = False
        self.buttonsIsPressed["Leave"] = False
         
    def escapeMenuUpdate(self, event, mousePos, runBool, returnBool):
        """
        escapeMenuUpdate checks for user inputs to the screen and matches to corresponding responses from the Escape Menu.
        It contains features such as:
        Toggle escape menu on and off.
        Check if buttons on Menu is pressed.

        event: user input.
        mousePos: mouse position relative to the window.
        runBool: value to be returned, False if the user click leave button.
        returnBool: value to be returned, True if the user click the return button.
        """
        returnBool = False
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
                        case "Return":
                            returnBool = True
                        case "Leave":
                            runBool = False
                    self.onStatus = False
                

        return runBool, returnBool
            
    def playAnimation(self, position, mousePos):
        """
        Draw the the escape menu to the screen.
            
        position: 2D tuple/ 2D list of top right position to be drawn on the screen.
        """
        if self.onStatus:

            self.surface.blit(self.image,pygame.Rect((0,0),self.menuSize))

            for keyName in self.buttonsRect.keys():
                #Check for hovering
                if self.buttonsRect[keyName].collidepoint(mousePos):
                    self.buttonsImg[keyName].fill((0, 64, 128))
                    
                else:
                    self.buttonsImg[keyName].fill((153, 204, 255))

                text = self.font.render(keyName, True, "black")
                self.buttonsImg[keyName].blit(text, ((self.buttonsImg[keyName].get_width() - text.get_width())/2,
                                                     (self.buttonsImg[keyName].get_height() - text.get_height())/2))
                
            self.surface.blit(self.buttonsImg["Return"], self.buttonsRectLocal["Return"])
            self.surface.blit(self.buttonsImg["Leave"], self.buttonsRectLocal["Leave"])

            pygame.draw.rect(self.surface, (153, 51, 51), self.buttonsRectLocal["Return"],2)
            pygame.draw.rect(self.surface, (153, 51, 51), self.buttonsRectLocal["Leave"],2)

            self.screen.blit(self.surface, position)

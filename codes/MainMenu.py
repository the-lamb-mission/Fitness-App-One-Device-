import pygame
from firebase_admin import db

class leaderboardSurf:
    def __init__(self, screen, fontDir):
        """
        searchResult is a class with a surface that display a list of workout 
        from the Workset Move Content File.

        screen: Targetted surface object to be drawn on.
        worksetMoveContent: A dictionary that has the content of the Workset Move Content File.
        fontDir: A string of the directory to a font file.
        """
        
        self.fontSize = 16
        self.gap = 2
        self.font = pygame.font.Font(fontDir, self.fontSize)
        
        searchSurface = pygame.Surface((screen.get_width()*8/10, screen.get_height()*(3/6)*(8/10))).convert_alpha()

        self.database = db.reference("")
        self.content = self.database.get()

        self.leaderboard = {}
        for key, value in self.content.items():
            if "Point" in value.keys():
                self.leaderboard[key] = value["Point"]

        self.leaderboard = dict(sorted(self.leaderboard.items(), key=lambda x:x[1], reverse=True))

        #Creating a dictionary of buttons, key as the name of the workout, value as the Rect object of the button.
        self.buttons = {}
        index = 0
        for key, value in self.leaderboard.items():
            self.buttons[key] = pygame.Rect((self.gap, (self.fontSize + self.gap) * index + self.gap),
                                             (searchSurface.get_width() - self.gap*2, self.fontSize + self.gap))
            index += 1
            if index == 5:
                break
            
        self.Surface = searchSurface

        self.screen = screen
    
    def update(self):
        self.content = self.database.get()

        self.leaderboard = {}
        for key, value in self.content.items():
            if "Point" in value.keys():
                self.leaderboard[key] = value["Point"]

        self.leaderboard = dict(sorted(self.leaderboard.items(), key=lambda x:x[1], reverse=True))

        #Creating a dictionary of buttons, key as the name of the workout, value as the Rect object of the button.
        self.buttons = {}
        index = 0
        for key, value in self.leaderboard.items():
            self.buttons[key] = pygame.Rect((self.gap, (self.fontSize + self.gap) * index + self.gap),
                                             (self.Surface.get_width() - self.gap*2, self.fontSize + self.gap))
            index += 1

            if index == 5:
                break


    def playAnimation(self, mousePos, searchSurfaceOffset):
        """
        Draw the seach surface on to the screen, including the buttons
        and the label of the buttons.

        mousePos: a tuple of position of the mouse
        searchSurfaceOffset: the position of the search surface relative to the window.
        """
        self.Surface.fill((255,255,255,122))
        newMousePos = (mousePos[0] - searchSurfaceOffset[0],mousePos[1] - searchSurfaceOffset[1])
        
        #Check for hovering
        for buttonName in self.buttons.keys():
            if self.buttons[buttonName].collidepoint(newMousePos):
                pygame.draw.rect(self.Surface, "white", self.buttons[buttonName])

        #Draw on to object's local surface
        index = 0
        for key, value in self.leaderboard.items():
            text = self.font.render(key + ": " + str(value), True, "black")
            self.Surface.blit(text, (self.gap, (self.fontSize + self.gap) * index + self.gap))
            index += 1
            
            if index == 5:
                break

        #Display local surface to screen
        self.screen.blit(self.Surface, searchSurfaceOffset) 


class searchResult:
    def __init__(self, screen, worksetMoveContent, fontDir):
        """
        searchResult is a class with a surface that display a list of workout 
        from the Workset Move Content File.

        screen: Targetted surface object to be drawn on.
        worksetMoveContent: A dictionary that has the content of the Workset Move Content File.
        fontDir: A string of the directory to a font file.
        """
        
        self.fontSize = 16
        self.gap = 2
        self.font = pygame.font.Font(fontDir, self.fontSize)
        
        searchSurface = pygame.Surface((screen.get_width()*8/10, screen.get_height()*(3/6)*(8/10))).convert_alpha()

        self.content = worksetMoveContent

        #Creating a dictionary of buttons, key as the name of the workout, value as the Rect object of the button.
        self.buttons = {}
        for index in range(len(self.content.keys())):
            name = list(self.content.keys())[index]
            self.buttons[name] = pygame.Rect((self.gap, (self.fontSize + self.gap) * index + self.gap),
                                             (searchSurface.get_width() - self.gap*2, self.fontSize + self.gap))
            
        self.Surface = searchSurface

        self.screen = screen

    def update(self, event, mousePos, searchSurfaceOffset):
        """
        Checks for user input, return scene number (which redirects to 
        different scene) and which workout user has chosen according to which
        button they have clicked.

        event: user input
        mousePos: a tuple of position of the mouse
        searchSurfaceOffset: the position of the search surface relative to the window.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Adjusted mouse position relative to the search surface
            newMousePos = (mousePos[0] - searchSurfaceOffset[0],mousePos[1] - searchSurfaceOffset[1])
        
            for buttonName in self.buttons.keys():
                if self.buttons[buttonName].collidepoint(newMousePos):
                    return 1, buttonName

        return 0, None

    def playAnimation(self, mousePos, searchSurfaceOffset):
        """
        Draw the seach surface on to the screen, including the buttons
        and the label of the buttons.

        mousePos: a tuple of position of the mouse
        searchSurfaceOffset: the position of the search surface relative to the window.
        """
        self.Surface.fill((255,255,255,122))
        newMousePos = (mousePos[0] - searchSurfaceOffset[0],mousePos[1] - searchSurfaceOffset[1])
        
        #Check for hovering
        for buttonName in self.buttons.keys():
            if self.buttons[buttonName].collidepoint(newMousePos):
                pygame.draw.rect(self.Surface, "white", self.buttons[buttonName])

        #Draw on to object's local surface
        for index in range(len(self.content.keys())):
            name = list(self.content.keys())[index]
            text = self.font.render(name, True, "black")
            self.Surface.blit(text, (self.gap, (self.fontSize + self.gap) * index + self.gap))

        #Display local surface to screen
        self.screen.blit(self.Surface, searchSurfaceOffset)        
        
    
class mainMenu:
    def __init__(self, publicScreen, backgroundImgDir, menuOverlayImgDir, publicVirtualTrainer, worksetMoveContentDir, fontDir):
        """
        mainMenu is a class with surface that display when the scene is 0.
        It is the GUI displayed after user have logged in.

        publicScreen: Targetted surface object to be drawn on.
        backgroundImgDir: A directory to the background image for main menu.
        menuOverlayImgDir: A directory to the overlay image (includes the button icon 
        and title image) for main menu.
        publicVirtualTrainer: A pointer to the virtual trainer object initiated from 
        the main code.
        worksetMoveContentDir: A directory to the work set move content.
        """
        self.screen = publicScreen
        
        self.background = pygame.image.load(backgroundImgDir)

        self.menuOverlay = pygame.image.load(menuOverlayImgDir).convert_alpha()
        
        #bottomBar is the bar with options, seen from the brown bar above.
        self.bottomBar = pygame.Rect((0, self.screen.get_height()*(5/6)),(self.screen.get_width(), self.screen.get_height()*(5/6)))
        self.bottomBarButtons = {"Leaderboard": pygame.Rect((0, self.screen.get_height()*(5/6)),
                                    (self.screen.get_width()/3, self.screen.get_height()*(5/6))),
                                 "Home": pygame.Rect((self.screen.get_width()/3, self.screen.get_height()*(5/6)),
                                    (self.screen.get_width()/3, self.screen.get_height()*(5/6))),
                                 "Search": pygame.Rect((self.screen.get_width()*2/3, self.screen.get_height()*(5/6)),
                                    (self.screen.get_width()/3, self.screen.get_height()*(5/6)))
                                 }
        
        self.virtualTrainer = publicVirtualTrainer

        self.searchSurface = searchResult(self.screen, worksetMoveContentDir, fontDir)
        self.searchSurfaceOffset = ((self.screen.get_width()-self.searchSurface.Surface.get_width())/2,
        (self.screen.get_height()*3/6-self.searchSurface.Surface.get_height())/2+self.screen.get_height()*2/6)

        self.leaderboardSurface = leaderboardSurf(self.screen, fontDir)
        self.leaderboardSurfaceOffset = ((self.screen.get_width()-self.leaderboardSurface.Surface.get_width())/2,
        (self.screen.get_height()*3/6-self.leaderboardSurface.Surface.get_height())/2+self.screen.get_height()*2/6)

        #Default local scene when loaded
        self.scene = "Home"

        self.font = pygame.font.Font(fontDir, 16)
        self.accountButton = {"Rect": pygame.Rect((self.screen.get_width()-64-16, 
                                                 16),
                                                 (64,64)),
                                                 "label": self.font.render("A/C", True, "black")}

        
    def update(self, event, mousePos):
        """
        Checks for user inputs to the screen and matches to corresponding responses in the main menu.
        This return the scene switching by pressing the bottom bar buttons.

        event: user input.
        mousePos: mouse position relative to the window.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            for buttonName in self.bottomBarButtons.keys():
                if self.bottomBarButtons[buttonName].collidepoint(mousePos):
                    self.scene = buttonName
                    if buttonName == "Leaderboard":
                        self.leaderboardSurface.update()

        scene, sceneName = 0, None
        if self.scene == "Search":
            scene, sceneName = self.searchSurface.update(event, mousePos, self.searchSurfaceOffset)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.accountButton["Rect"].collidepoint(mousePos):
                scene = 2
                
        return scene, sceneName
    
    def playAnimation(self, tick, mousePos):
        """
        Fill the screen with the main menu.
            
        tick: the amount of ticks passed since the app has opened.
        mousePos: mouse position relative to the window.
        """
        self.screen.blit(self.background, (0,0))
        pygame.draw.rect(self.screen, "brown", self.bottomBar)
        for button in self.bottomBarButtons.values():
            if button.collidepoint(mousePos):
                pygame.draw.rect(self.screen, "black", button)
        
        match self.scene:
            case "Home":
                self.virtualTrainer.playAnimation([self.screen.get_width()/2-self.virtualTrainer.spriteImgSize[0]/2,
                self.screen.get_height()*2/3-self.virtualTrainer.spriteImgSize[1]*2/3], tick)
                
            case "Leaderboard":
                pass
                #self.leaderboardSurface.playAnimation(mousePos, self.leaderboardSurfaceOffset)

            case "Search":

                self.searchSurface.playAnimation(mousePos, self.searchSurfaceOffset)
        self.screen.blit(self.menuOverlay, (0,0))

        
        if self.accountButton["Rect"].collidepoint(mousePos):
            pygame.draw.rect(self.screen, "grey", self.accountButton["Rect"])
        else:
            pygame.draw.rect(self.screen, "white", self.accountButton["Rect"])
        self.screen.blit(self.accountButton["label"], (self.accountButton["Rect"].centerx - self.accountButton["label"].get_width()/2, 
                                                      self.accountButton["Rect"].centery - self.accountButton["label"].get_height()/2))
        pygame.draw.rect(self.screen, "black", self.accountButton["Rect"], 2)

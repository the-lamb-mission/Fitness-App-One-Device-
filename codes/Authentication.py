import pygame
import string
import json
from firebase_admin import db

def uploadScore(score, accountInfoDir):
    accountInfoFile = open(accountInfoDir, "r")
    username = json.load(accountInfoFile)["Username"]
    accountInfoFile.close()

    database = db.reference(username)
    databaseContent = database.get()

    if "Point" in databaseContent.keys():
        databaseContent["Point"] += score
    else:
        databaseContent["Point"] = score
    
    database.set(databaseContent)

def logout(accountInfoDir):
    """
    delete the account info stored in a local json file.
    Next time the user open the app.

    accountInfoDir: A directory to the local json file that 
    stores account information.
    """
    accountInfoFile = open(accountInfoDir, "w")
    accountInfoToWrite = {"loginStatus": False,
                            "Username" : "",
                            "Password" : ""}
    json.dump(accountInfoToWrite, accountInfoFile)
    accountInfoFile.close()

def check(username, password):
    """
    Go to the online database to check verify user's input of
    username and password is correct.

    Returns True if verify is successful.
    Returns False if verify is unsuccessful.

    username: the username entered at the login username text box.
    password: the password entered at the login password text box.
    """
    print("Checking...")

    if type(username) == str:
        database = db.reference(username)
        databaseContent = database.get()
        
        if databaseContent != None:
            if password == databaseContent["Password"]:
                print("Found!")
                return True
            
        print("Not found!")
    return False

def register(username, password):
    """
    Check if chosen username has been registered.
    If chosen username has been registered, return False.
    If not, create an account and upload it into the database and
    return True.

    username: the username entered at the register username text box.
    password: the password entered at the register password text box.
    """
    database = db.reference(username)
    databaseContent = database.get()
    
    if databaseContent == None:
        database.set({"Password": password})
        return True
    
    print("Username Taken")
    return False


class loginSurf:

    def __init__(self, screen, font, authBackgroundImgDir):
        """
        loginSurf is a class with a surface that includes textboxes for entering
        username and password and a functional submit button to allow users to login 
        and register an account.

        screen: Targetted surface object to be drawn on.
        font: 
        """
        self.screen = screen
        self.surface = pygame.image.load(authBackgroundImgDir)
        self.font = font

        rawTitleSurf = font.render("Easy Fit - Authentication", True, "white")
        rawTitleSurf = pygame.transform.scale(rawTitleSurf,(rawTitleSurf.get_width() *1.5,rawTitleSurf.get_height()*1.5))
        #Shadow
        shadowTitleSurf = font.render("Easy Fit - Authentication", True, "black")
        shadowTitleSurf = pygame.transform.scale(shadowTitleSurf,(shadowTitleSurf.get_width() *1.5, shadowTitleSurf.get_height()*1.5))
        #Combine word with shadow
        self.titleSurf = pygame.Surface((rawTitleSurf.get_width(), rawTitleSurf.get_height()+3)).convert_alpha()
        self.titleSurf.fill((0,0,0,0))
        self.titleSurf.blit(shadowTitleSurf, (0, 3))
        self.titleSurf.blit(rawTitleSurf, (0, 0))

        loginUsername = {"Rect": pygame.Rect(((screen.get_width()-128)/4, 
                                        (screen.get_height()-32)*3/7),
                                        (128,32)),
                    "text": "",
                    "label": font.render("Login Username", True, "white")}
        
        loginPassword = {"Rect": pygame.Rect(((screen.get_width()-128)/4, 
                                        (screen.get_height()-32)*4/6),
                                        (128,32)),
                    "text": "",
                    "label": font.render("Password", True, "white")}
        
        regUsername = {"Rect": pygame.Rect(((screen.get_width()-128)*3/4, 
                                        (screen.get_height()-32)*3/7),
                                        (128,32)),
                    "text": "",
                    "label": font.render("Register Username", True, "white")}
        
        regPassword = {"Rect": pygame.Rect(((screen.get_width()-128)*3/4, 
                                        (screen.get_height()-32)*4/6),
                                        (128,32)),
                    "text": "",
                    "label": font.render("Password", True, "white")}
        
        self.textBoxes = [loginUsername, loginPassword, regUsername, regPassword]

        self.loginSubmitButton = {"Rect": pygame.Rect(((screen.get_width()-128)/4, 
                                        (screen.get_height()-32)*5/6),
                                        (96,32)),
                                "label": font.render("Submit", True, "black")}
        
        self.regSubmitButton = {"Rect": pygame.Rect(((screen.get_width()-128)*3/4, 
                                        (screen.get_height()-32)*5/6),
                                        (96,32)),
                                "label": font.render("Submit", True, "black")}
                    

        self.onWhichTextbox = ""

    def update(self, event, mousePos):
        """
        

        event: user input
        mousePos: mouse position relative to the window
        """
        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.loginSubmitButton["Rect"].collidepoint(mousePos):
                if check(self.textBoxes[0]["text"], self.textBoxes[1]["text"]):
                    username = self.textBoxes[0]["text"]
                    password = self.textBoxes[1]["text"]

                    for textBox in self.textBoxes:
                        textBox["text"] = ""
                    return 0, username, password
            
            if self.regSubmitButton["Rect"].collidepoint(mousePos):
                if self.textBoxes[2]["text"] != "" and self.textBoxes[3]["text"] != "":
                    if register(self.textBoxes[2]["text"], self.textBoxes[3]["text"]):
                        username = self.textBoxes[2]["text"]
                        password = self.textBoxes[3]["text"]

                        for textBox in self.textBoxes:
                            textBox["text"] = ""

                        return 0, username, password
                    else:
                        self.textBoxes[2]["text"] = ""

            clickedTextBox = False
            for button in self.textBoxes:
                if button["Rect"].collidepoint(mousePos):
                    self.onWhichTextbox = button
                    clickedTextBox = True
            
            if clickedTextBox == False:
                self.onWhichTextbox = ""

        if event.type == pygame.KEYDOWN and self.onWhichTextbox != "":
            if event.key == pygame.K_BACKSPACE:
                self.onWhichTextbox["text"] = self.onWhichTextbox["text"][0:-1]
            elif event.unicode in string.ascii_letters or event.unicode == " " or event.unicode.isdigit():
                self.onWhichTextbox["text"] += event.unicode
        
        return -1, None, None

    def playAnimation(self, mousePos):
        self.screen.fill((102, 153, 255))
        self.screen.blit(self.surface, (0,0))

        self.screen.blit(self.titleSurf, ((self.screen.get_width()-self.titleSurf.get_width())/2, 
                                          (self.screen.get_height()-self.titleSurf.get_height())/5))

        for button in self.textBoxes:
            pygame.draw.rect(self.screen, (255,255,255), button["Rect"])

        for button in self.textBoxes:

            if button["Rect"].collidepoint(mousePos):
                pygame.draw.rect(self.screen, (230, 230, 255), button["Rect"])

            self.screen.blit(button["label"], (button["Rect"].x + (button["Rect"].w - button["label"].get_width())/2, 
                                        button["Rect"].y - button["label"].get_height() - 2))
            
        if self.onWhichTextbox != "":
            pygame.draw.rect(self.screen, (194, 194, 214), self.onWhichTextbox["Rect"])

        for button in self.textBoxes:

            pygame.draw.rect(self.screen, "black", button["Rect"], 2)

            rawTextSurf = self.font.render(button["text"], True, "black")
            textSurf = pygame.Surface((min(rawTextSurf.get_width(), button["Rect"].w-2), rawTextSurf.get_height())).convert_alpha()
            textSurf.fill((0,0,0,0))
            textSurf.blit(rawTextSurf, (0,0))
            self.screen.blit(textSurf, (button["Rect"].x+2, 
                                        button["Rect"].y + (button["Rect"].h-textSurf.get_height())/2))
            
        if self.loginSubmitButton["Rect"].collidepoint(mousePos):
            pygame.draw.rect(self.screen, (255, 77, 77), self.loginSubmitButton["Rect"])
        else:
            pygame.draw.rect(self.screen, (238, 204, 255), self.loginSubmitButton["Rect"])
        self.screen.blit(self.loginSubmitButton["label"], (self.loginSubmitButton["Rect"].centerx - self.loginSubmitButton["label"].get_width()/2, 
                                                      self.loginSubmitButton["Rect"].centery - self.loginSubmitButton["label"].get_height()/2))
        pygame.draw.rect(self.screen, "black", self.loginSubmitButton["Rect"], 2)
                
        if self.regSubmitButton["Rect"].collidepoint(mousePos):
            pygame.draw.rect(self.screen, (255, 77, 77), self.regSubmitButton["Rect"])
        else:
            pygame.draw.rect(self.screen, (238, 204, 255), self.regSubmitButton["Rect"])
        self.screen.blit(self.regSubmitButton["label"], (self.regSubmitButton["Rect"].centerx - self.regSubmitButton["label"].get_width()/2, 
                                                      self.regSubmitButton["Rect"].centery - self.regSubmitButton["label"].get_height()/2))
        pygame.draw.rect(self.screen, "black", self.regSubmitButton["Rect"], 2)
                
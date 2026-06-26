import pygame
import json
import Authentication

class accountInfoSurf:
    def __init__(self, screen, font, accountInfoDir):

        self.screen = screen

        self.accountInfoDir = accountInfoDir

        accountInfoFile = open(accountInfoDir, "r")
        accountInfoContent = json.load(accountInfoFile)
        accountInfoFile.close()

        self.username = accountInfoContent["Username"]
        self.password = accountInfoContent["Password"]

        self.surface = pygame.Surface((self.screen.get_width(), 
                                       self.screen.get_height()))
        
        self.surface.fill((153, 187, 255))
        self.surface.blit(font.render("Account Info", True, "black"), (16, 16))
        self.surface.blit(font.render("Username: " + self.username, True, (51, 51, 153)), (16, 16+18*1))
        self.surface.blit(font.render("Password: " + self.password, True, (51, 51, 153)), (16, 16+18*2))

        self.leaveButton = {"Rect": pygame.Rect(((screen.get_width()-128)*3/4, 
                                                 (screen.get_height()-32)*5/6),
                                                 (96,32)),
                                                 "label": font.render("Leave", True, "black")}
        
        self.logoutButton = {"Rect": pygame.Rect(((screen.get_width()-128)*3/4, 
                                                 (screen.get_height()-32)*4/6),
                                                 (96,32)),
                                                 "label": font.render("Logout", True, "black")}

    def update(self, event, mousePos):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.leaveButton["Rect"].collidepoint(mousePos):
                return 0
            
            if self.logoutButton["Rect"].collidepoint(mousePos):
                Authentication.logout(self.accountInfoDir)
                return -1
        
        return 2
            
    def playAnimation(self, mousePos):

        self.screen.blit(self.surface, (0,0))

        if self.leaveButton["Rect"].collidepoint(mousePos):
            pygame.draw.rect(self.screen, "grey", self.leaveButton["Rect"])
        else:
            pygame.draw.rect(self.screen, "white", self.leaveButton["Rect"])
        self.screen.blit(self.leaveButton["label"], (self.leaveButton["Rect"].centerx - self.leaveButton["label"].get_width()/2, 
                                                      self.leaveButton["Rect"].centery - self.leaveButton["label"].get_height()/2))
        pygame.draw.rect(self.screen, "black", self.leaveButton["Rect"], 2)

        if self.logoutButton["Rect"].collidepoint(mousePos):
            pygame.draw.rect(self.screen, "grey", self.logoutButton["Rect"])
        else:
            pygame.draw.rect(self.screen, "white", self.logoutButton["Rect"])
        self.screen.blit(self.logoutButton["label"], (self.logoutButton["Rect"].centerx - self.logoutButton["label"].get_width()/2, 
                                                      self.logoutButton["Rect"].centery - self.logoutButton["label"].get_height()/2))
        pygame.draw.rect(self.screen, "black", self.logoutButton["Rect"], 2)


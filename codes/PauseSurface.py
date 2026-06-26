import pygame

class popUp:
    def __init__(self, screen, font):
        self.screen = screen
        
        self.surface = pygame.Surface((256,144))
        self.surface.fill((141, 177, 179))
        self.font = font

        self.buttonLabel = font.render("Back", True, "Black")
        
        self.fullRect = pygame.Rect(((screen.get_width()-self.surface.get_width())/2,
                                 (screen.get_height()-self.surface.get_height())/2),
                                (256,144))

        self.buttonRect = pygame.Rect(((screen.get_width()-128)/2,
                                 screen.get_height()/2),
                                (128,32))

        self.onStatus = False
        
    def update(self, mousePos, event):
        if self.onStatus:
            if (self.buttonRect.collidepoint(mousePos) and event.type == pygame.MOUSEBUTTONDOWN):
                self.onStatus = False
                return False
            else:
                return True
        return False
        
    def playAnimation(self, mousePos, text):
        if self.onStatus:
            self.surface.fill((141, 177, 179))

            warningLabel = self.font.render(text, True, "black")
            self.surface.blit(warningLabel, ((self.surface.get_width()-warningLabel.get_width())/2, 4))

            self.screen.blit(self.surface, (self.fullRect.centerx - self.surface.get_width()/2,
                                            self.fullRect.centery - self.surface.get_height()/2))
            pygame.draw.rect(self.screen, "black", self.fullRect, 2)
            
            if self.buttonRect.collidepoint(mousePos):
                pygame.draw.rect(self.screen, (204, 0, 0), self.buttonRect)
            else:
                pygame.draw.rect(self.screen, (255, 204, 204), self.buttonRect)
            pygame.draw.rect(self.screen, "black", self.buttonRect, 2)

            self.screen.blit(self.buttonLabel, (self.buttonRect.centerx - self.buttonLabel.get_width()/2,
                                                self.buttonRect.centery - self.buttonLabel.get_height()/2))
            

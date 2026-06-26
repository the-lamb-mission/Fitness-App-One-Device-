import pygame
import sys

class Slider:
    def __init__(self, screen, sliderBarPos, sliderBarSize, sliderBallPos, sliderBallSize):
        
        self.screen = screen
        self.ballUpdate = False
        self.ball = pygame.Rect(sliderBallPos,sliderBallSize)
        self.bar = pygame.Rect(sliderBarPos,sliderBarSize)


    def update(self, mousePos):
        pygame.draw.rect(self.screen,"black",self.bar)
        
        if self.ballUpdate:
            self.ball.update((min(max(mousePos[0]-self.ball.size[0]/2,self.bar.left),self.bar.right),self.bar.centery - self.ball.size[1]/2),self.ball.size)
        pygame.draw.rect(self.screen,"white",self.ball)

        return (self.ball.left - self.bar.left)/self.bar.size[0]






def test():
    screen = pygame.display.set_mode((500,500))

    sliderBarPos = (50,249)
    sliderBarSize = (400,2)
    sliderBallPos = (50,240)
    sliderBallSize = (20,20)
    
    slider = Slider(screen, sliderBarPos, sliderBarSize, sliderBallPos, sliderBallSize)

    sliderVal = 0
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and slider.ball.collidepoint(pygame.mouse.get_pos()):
                slider.ballUpdate = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                slider.ballUpdate = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print(sliderVal)
        
        screen.fill((0,0,0))
        sliderVal = slider.update(pygame.mouse.get_pos())
        slider.ball.size = (20+100*sliderVal,20+100*sliderVal)
        
        pygame.display.flip()
        

    pygame.quit()
    sys.exit()



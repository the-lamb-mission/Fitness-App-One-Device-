import numpy
import cv2
import pygame

def getCameraSurface(webcam):
    ret, frame = webcam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = numpy.rot90(frame)
    return pygame.surfarray.make_surface(frame)


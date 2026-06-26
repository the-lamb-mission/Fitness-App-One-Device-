import math
import checkPose

def statusUpdate(jsonContent, worksetName, tick, tickIncrement, virtualTrainer, webcam):
    pause = False
    points = 0
    checkIdentifiers = list(jsonContent[worksetName]["CheckPose"].keys())
    
    for animation in jsonContent[worksetName]["AnimationSequences"]:
        
        if animation not in checkIdentifiers:
            
            #animations
            relativeTick = tick 
            tick -= len(virtualTrainer.spriteAnimation[animation])
            
            if tick < 0:                
                virtualTrainer.status = animation
                break
        else:
            #check
            tick -= tickIncrement
            if tick < 0:
                pause, points, cameraInput = checkPose.returnPoints(webcam,
                                                                    jsonContent[worksetName]["RequiredBodyParts"],
                                                                    jsonContent[worksetName]["CheckPose"][animation])
                break
    if tick > 0:
        virtualTrainer.status = "idle"
        scene = 0
    else:
        scene = 1

            
    return math.floor(relativeTick), pause, points, scene


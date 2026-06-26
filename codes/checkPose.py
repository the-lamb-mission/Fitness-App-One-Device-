from videoInput2 import videoInput
import math

def returnPoints(webcam, requiredBodyParts, relationship):
    output = videoInput(webcam, requiredBodyParts)
    if output == None:
        print("No Source")
        return True, 0, False
    elif type(output) == list:
        print("NO required parts", output)
        return True, 0, True
    else:
        print("success")
        
        basePointX = output[relationship[1]][0]
        basePointY = output[relationship[1]][1]

        firstPointDiffX = output[relationship[0]][0] - basePointX
        firstPointDiffY = output[relationship[0]][1] - basePointY
        
        secondPointDiffX = output[relationship[2]][0] - basePointX
        secondPointDiffY = output[relationship[2]][1] - basePointY
        
        if firstPointDiffX != 0:
            angle1 = abs(math.degrees(math.atan(firstPointDiffY/firstPointDiffX)))
        else:
            angle1 = 90
        if secondPointDiffX != 0:
            angle2 = abs(math.degrees(math.atan(secondPointDiffY/secondPointDiffX)))
        else:
            angle2 = 90

        actualAngle = angle1+angle2
        desiredAngle = relationship[3]

        if abs(desiredAngle - actualAngle) < 10:
            point = 10
        elif abs(desiredAngle - actualAngle) < 30:
            point = 7
        elif abs(desiredAngle - actualAngle) < 50:
            point = 3
        else:
            point = 0
        print(point)
        return False, point, True

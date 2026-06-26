import cv2
import time

def readNetwork():
    """
    Reads file and returns a network object.
    If the file cannot be found, it returns None.
    """
    protoFile = "videoInputAssets/deploy_coco.prototxt"
    weightsFile = "videoInputAssets/pose_iter_440000.caffemodel"
    
    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
    #net = cv2.dnn.readNetFromTensorflow("videoInputAssets/graph_opt.pb")

    return net

def retrieveWebcam(camera):
    """
    retrieveWebcam returns an image read from the webcam if the webcam is accessible.
    It will return None if the image cannot be read.

    camera: An object initiated from cv2.VideoCapture().
    """
    imgBool, image = camera.read()
    if imgBool:
        return image
        #return cv2.imread("videoInputAssets/images.jpeg")
    else:
        return None

def getPoints(output, bodyParts, frameWidth, frameHeight, threshold):
    """
    Takes in the output from net.forward() and returns the points estimated by the network.
    
    points: A list (ordered by bodyParts) of tuple of positions relative to the actual image according to frameWidth and frameHeight.
    If there is no confident estimation of the position, the value for that bodyPart will be 0.

    Input:
    output: A ndarray from net.forward()
    bodyParts: A constant of dictionary that contains key-pair values of body part names and their order.
    frameWidth: The width of the actual image.
    frameHeight: The height of the actual image.
    threshold: A constant of a float between 0 and 1. The minimum confidence needed for the estimation to be valid.
    """
    
    points = []
    for bodyPartsId in range(len(bodyParts)):

        #probability Distribution of the output.
        probDist = output[0, bodyPartsId, :, :]
        
        confidence = cv2.minMaxLoc(probDist)[1]
        point = cv2.minMaxLoc(probDist)[3]

        #print(list(bodyParts.keys())[bodyPartsId], confidence, (frameWidth * point[0]) / output.shape[3])

        #Validating the point with its confidence
        if confidence > threshold:
            
            #translating points from blob of image to actual image location
            x = (frameWidth * point[0]) / output.shape[3]
            y = (frameHeight * point[1]) / output.shape[2]
            
            points.append((int(x), int(y)))
            
        else:
            points.append(0)
            
    return points

def videoInput(webcam, requiredBodyParts):
    """
    Video Input gets the webcam to check if the body parts required is visible, and returns the body parts position if they are available.

    requiredBodyParts: A list of names of body parts that is required for the workout to check.

    Output:
    A Dictionary of body parts as name and the value as the location of the body part within the webcam frame.
    Return 0 if not all body parts are visible in the frame.
    Return None if the webcam source is not available.
    """
    #Setting up constants
    thr = 0.05
    bodyParts= { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }
    # read network into memory
    net = readNetwork()
    
    #Validating webcam input
    if type(retrieveWebcam(webcam)) != None:
        frame = retrieveWebcam(webcam)
        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        #Specify dimension of image
        inWidth = 368
        inHeight = 368
        #Convert frame to suitable format
        inp = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)

        #Returning joint positions from inputting image into Network
        net.setInput(inp)
        output = net.forward()
        points = getPoints(output, bodyParts, frameWidth, frameHeight, thr)
        #print(points)
        #Validating each bodyPart
        labelledPoints = {}
        unavailableBodyParts = []
        for bodyPart in requiredBodyParts:
            index = bodyParts[bodyPart]
            #print(bodyPart, index, points[index])
            if points[index] != 0:
                labelledPoints[bodyPart] = points[index]
            else:
                unavailableBodyParts.append(bodyPart)
        if len(unavailableBodyParts) != 0:
            
            return unavailableBodyParts
            #print("success?")
        return labelledPoints
    else:
        #Error Handling
        print("Error - Webcam Source is not available.")
        return None
    
def main():
    print("Connecting...")
    
    webcam = cv2.VideoCapture(0)
    requiredBodyParts = ["Nose"]
    input("Connected! Type anything to proceed.")
    start = time.time()
    print(videoInput(webcam, requiredBodyParts))
    duration = time.time() - start
    print(round(duration,2))
    webcam.release()




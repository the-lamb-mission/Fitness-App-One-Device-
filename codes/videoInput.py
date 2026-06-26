import cv2

def readNetwork():
    """
    Reads file and returns a network object.
    If the file cannot be found, it returns None.
    """
    protoFile = "videoInputAssets/pose_deploy_linevec_faster_4_stages.prototxt"
    weightsFile = "videoInputAssets/pose_iter_160000.caffemodel"

    try:
        net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
    except FileNotFoundError:
        return None

    return net

def retrieveWebcam(camera):
    imgBool, image = camera.read()
    if imgBool:
        return image
    else:
        return None

def getPoints(out, BODY_PARTS, frameWidth, frameHeight, thr):
    points = []
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponding body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv2.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]

        # Add a point if it's confidence is higher than threshold.
        if conf > thr:
            points.append((int(x), int(y)))
        else:
            points.append(0)
    return points
    
def annotate(POSE_PAIRS, BODY_PARTS, frame, points):
    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert(partFrom in BODY_PARTS)
        assert(partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]
        
        if points[idFrom] and points[idTo]:
            cv2.line(frame, points[idFrom], points[idTo], (255, 74, 0), 3)
            cv2.ellipse(frame, points[idFrom], (4, 4), 0, 0, 360, (255, 255, 255), cv2.FILLED)
            cv2.ellipse(frame, points[idTo], (4, 4), 0, 0, 360, (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, str(idFrom), points[idFrom], cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, str(idTo), points[idTo], cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, cv2.LINE_AA)

    return frame


def main():
    inWidth = 368
    inHeight = 368

    thr = 0.5 

    net = readNetwork()

    BODY_PARTS = {"Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                      "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                      "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                      "Background": 15}

    POSE_PAIRS = [["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                  ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                  ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                  ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"]]

    webcam = cv2.VideoCapture(0)
    
    frame = retrieveWebcam(webcam)
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]

    inp = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inp)
    out = net.forward()
    
    while True:
        if type(retrieveWebcam(webcam)) != None:
            frame = retrieveWebcam(webcam)
            #frame = cv2.imread("videoInputAssets/download.jpg")
            frameWidth = frame.shape[1]
            frameHeight = frame.shape[0]
            
            inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)
            net.setInput(inpBlob)
            output = net.forward()
            points = getPoints(output, BODY_PARTS, frameWidth, frameHeight, thr)
            
            new = annotate(POSE_PAIRS, BODY_PARTS, frame, points)
            cv2.imshow('frame', new)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("No Image Available")
    webcam.release()
main()


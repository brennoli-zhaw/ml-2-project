import os
from PIL import Image
import cv2
import mediapipe as mp
import math
import base64



# Open a video capture object (0 for the default camera)

#this function will split your video into single images, making it easier to obtain training data 
def extractFramesFromVideo(videoPath, outputPath = "dataCreation/createdImages", everyFrames = 8):
    if outputPath[-1] == "/":
        outputPath = outputPath[:-1]
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    # guideline hand recognition: https://medium.com/@lota.pipeline/hand-recognition-with-python-guide-with-code-samples-a0b17f4cd813
    # Initialize MediaPipe Hands module
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Initialize MediaPipe Drawing module for drawing landmarks
    mp_drawing = mp.solutions.drawing_utils
    
    files = os.listdir(outputPath)
    vidcap = cv2.VideoCapture(videoPath)
    success,image = vidcap.read()
    count = 0
    while success:
        #cv2.imwrite("frames/frame%d.jpg" % count, image)
        success,image = vidcap.read()
        if not success:
            continue
        # Convert the frame to RGB format
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the frame to detect hands
        results = hands.process(frame_rgb)
        
        # Check if hands are detected
        if results.multi_hand_landmarks and count % everyFrames == 0:
            #we add files length just so no files are overwritten
            cv2.imwrite(outputPath + "/frame%d.jpg" % (count + len(files)), image)
            print('write a new image: ', success)
        
        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        count += 1

    # Release the video capture object and close the OpenCV windows
    vidcap.release()
    cv2.destroyAllWindows()

#this function will create a series of images from the images in the input folder
#note if you create folders or files that are not images, this function will fail and throw an error
#seriesLength is the amount of images that will be combined in one series, a negative value will result in an error
def createImageSeries(inputPath = "dataCreation/createdImages", outputPath = "dataCreation/createdImageSeries", reverse=False, seriesLength = 4, imageWidth = 639, imageHeight = 360, spacerWidth = 10):
    if outputPath[-1] == "/":
        outputPath = outputPath[:-1]
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    if not os.path.exists(inputPath):
        print("Input path does not exist")
        return
    files = os.listdir(inputPath)
    counter = 0
    continueTill = -1
    if reverse:
        files.reverse()
    for i in range(0, len(files)):
        # Check if the series length is reached, to avoid out of bounds error
        # we will not create a series if the series length is not reached
        if i + seriesLength >= len(files):
            break
        #adding to i doesn't skip images, this is a workaround to skip images
        if i < continueTill:
            continue
        # Create a new image with white background
        new_image = Image.new('RGB',(seriesLength * imageWidth + spacerWidth * (seriesLength - 1), imageHeight), (255,255,255))
        for j in range(0, seriesLength):
            image_file = Image.open(inputPath + "/" + files[i + j])
            image = image_file.resize((imageWidth, imageHeight))
            new_image.paste(image,(j * (imageWidth + spacerWidth),0))
        #we add files length just so no files are overwritten
        new_image.save(outputPath + "/imageSeries%d.jpg" % (counter + len(files)))
        counter += 1
        # to generate at least some series that can be used for training, we will overlap the series
        continueTill = math.ceil(seriesLength / 1.5) - 1 + i

#gets all images in the folder ImageSeriesToUse, returns a list of base64 encoded images or the path to the images
def getTrainingImages(toBase64 = True):
    path = "ImageSeriesToUse"
    images = []
    os.path.exists(path)
    files = os.listdir(path)
    for file in files:
        if file.endswith(".jpg"):
            if toBase64:
                with open(path + "/" + file, "rb") as imageFile:
                    images.append(base64.b64encode(imageFile.read()).decode('utf-8'))
            else:
                images.append(path + "/" + file)
    return images

#encodes an image to base64
def encodeImage(imagePath : str):
    with open(imagePath, "rb") as imageFile:
        return base64.b64encode(imageFile.read()).decode('utf-8')

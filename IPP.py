### Importing required modules ###
import streamlit as st
from PIL import Image
import numpy as np
import cv2
import mediapipe as mp
from fer import FER
from matplotlib import pyplot as plt
import dlib

st.set_page_config(page_title="Photo ID Validator",layout="centered")
st.title("Photo ID Validator")
st.markdown("Upload a photo to check if it meets official photo ID requirements.")

uploaded_file=st.file_uploader("Upload your photo (JPG or PNG)", type=["jpg", "jpeg", "png"])
face_detector=mp.solutions.face_detection.FaceDetection(model_selection=1,min_detection_confidence=0.5)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r'./shape_predictor_68_face_landmarks/shape_predictor_68_face_landmarks.dat')
#model_selection is 0 or 1 (0 for webcam or phone images, 1 for widerange and all kind of images). This param can be possibly adjusted in future
#min_detection_confidence, higher value like 0.7-0.75 for better image quality but 0.5 is balanced for low resolution images

emotion_detector=FER()
### Import and loading basic models complete ###

### Validation functions ###
def Dimensions(image):
    height=image.shape[0]
    width=image.shape[1]
    if height<=531 and width<=413 :
        result={"pass":True,"feedback":f"Image dimensions are correct, Found: ({width}x{height}px),  Max Allowed:(413x531px)."}
        return result
    result={"pass":False,"feedback":f"Image size is ({width}x{height}px). Required: 413x531 px."}
    return result

def Background(image,threshold=0.3,tolerance=30):
    # threshold: atleast 30% of the pixels should be white to pass the image with white background
    
    # tolerance: The allowable deviation from perfect white (255,255,255) for a pixel to still be counted as white.
    
    white=np.array([255,255,255])
    diff=np.abs(image-white) ### subtracting values of white from image, if perfect white array will be like [0,0,0], if not: a tolerance of upto 30 points is considered white.
    mask=np.all(diff<=tolerance,axis=-1)  #True where pixel is close to white

    total_while=np.sum(mask)/mask.size
    
    if total_while>=threshold:
        result={"pass":True,"feedback":f"Image has {total_while:.2f} white background (OK)."}
    else:
        result={"pass":False,"feedback":f"Image has only {total_while:.2f} white background (Too low)."}
    return result

def Face_Positioning(image):
    results = face_detector.process(image)
    if results.detections:
        result= {"pass":True,"feedback":"Face detected looking at camera."}
        return result
    result={"pass":False,"feedback":"No face detected or not facing camera."}
    return result

def shoulders_visible(image):
    face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.1,5)
    # print(faces)
    if len(faces) == 0:
        result={"pass":False,"feedback":"No face detected."}
        return result
    h=faces[0][3] ### Taking out h for height of the face
    img_height=image.shape[0]
    
    face_ratio=h/img_height

    if face_ratio<0.6:  #If face occupies less than ~60% of height
        result={"pass":True,"feedback":"Shoulders are likely visible."}
    else:
        result={"pass":False,"feedback":"Face is too close - shoulders not visible."}
    return result

def ears_unobstructed(image):
    face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.1,5)
    # print(faces)
    if len(faces)==0:
        result={"pass":False,"feedback": "No face detected."}
        return result

    w=faces[0][2] ### Taking out only w for width of the face
    img_width=image.shape[1]
    face_width_ratio=w/img_width

    if face_width_ratio>0.10: #if face covers >20% of image width
        return {"pass":True,"feedback":"Ears are likely unobstructed."}
    else:
        return {"pass":False,"feedback":"Ears may be obstructed or not fully visible."}
    
def Expression(image):
    try:
        ##generating top emotion in the image with a score in a tuple output ex: ("neutral",1.0)
        emotion = emotion_detector.top_emotion(image)
        # print(emotion)
        if emotion and emotion[0]=='neutral':
            result={"pass":True,"feedback": "Expression is neutral."}
            return result
        result={"pass":False,"feedback":f"Detected expression: {emotion[0]}."}
        return result
    except:
        # print("Not able to analyze")
        result={"pass":False,"feedback":"Could not analyze expression."}
        return result

# def Accessories(image):
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY) ## Converting to grayscale
    
    ##Loading pre-trained haarcascade model which is trained on eyes detection
    eye_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglass.xml') 
    eyes=eye_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)
    #scaleFactor: Lower is more accurate but slower.
    #minNeighbors: Higher value=fewer false positives,but may miss some eyes.

    # print(eyes)
    if len(eyes)>=2:
        result={"pass":False,"feedback":"Possible glasses detected. Please remove them."}
        return result
    
    #NOTE: head covering detection is not robust here—would need segmentation/classification
    result={"pass":True,"feedback":"No visible glasses or head covering."}
    return result

def accessories2(image):

## Source : https://github.com/siddh30/Glasses-Detection/tree/main
# Get the facial landmark coordinates for the nasal area
# Crop the Image base on these landmarks
# Convert the image into black and white (White being the background and black being the details)
# Look of the presence a nasal strip in the nose (A strip of 0s (black pixels))
# If present than the subject is wearing glasses

    img_array = np.array(image)
    if len(detector(img_array))==0:
        result={"pass":False,"feedback":"No face detected for accessory check."}
        return result

    rect=detector(img_array)[0] ## taking first face for detection
    sp=predictor(img_array,rect) ## predicting 68 coordinates on the image
    landmarks=np.array([[p.x,p.y] for p in sp.parts()]) ## converting 68 coordinates to x and y using numpy

    nose_bridge_x=[]
    nose_bridge_y=[]

    for i in [27,28,29,30,31,33,34,35]:  ### Coordinates on nose, if something on nose is obstructing most likely glasses
        nose_bridge_x.append(landmarks[i][0])
        nose_bridge_y.append(landmarks[i][1])

    x_min=min(nose_bridge_x)
    x_max=max(nose_bridge_x)
    y_min=landmarks[20][1] ### eye brow
    y_max=landmarks[30][1] ### to lower nose area

    img_crop = img_array[y_min:y_max,x_min:x_max] ## cropping according to coordinates
    img_blur=cv2.GaussianBlur(np.array(img_crop),(3,3),sigmaX=0,sigmaY=0) ## for smoothening
    edges=cv2.Canny(image=img_blur,threshold1=100,threshold2=200) ## for judgement of intensity? edge detection?
    edges_center=edges.T[int(len(edges.T)/2)]


    ### if white if found most likely a glass
    if 255 in edges_center:
        result={"pass":False,"feedback":"Possible glasses or accessories detected!"}
    else:
        result={"pass": True,"feedback": "No glassed or acessories detected!"}
    return result

### End of validation functions ###

#Checks when image is uploaded
if uploaded_file:
    image=Image.open(uploaded_file).convert("RGB") #Converting file into RGB layers
    image=np.array(image) #making array containing all the infromation about all the pixels
    st.image(image,caption="Uploaded Image", use_container_width=True) # printing image uploaded on the UI

    ### Running validation ###
    with st.spinner("Validating photo..."):
        results={
            "Dimensions": Dimensions(image),
            "Background": Background(image),
            "Face Presence": Face_Positioning(image),
            "Ears presence": ears_unobstructed(image),
            "Shoulders Presence": shoulders_visible(image),
            "Expression": Expression(image),
            "Accessories": accessories2(image)
        }

    ### Final results
    st.subheader("Validation Report")
    for check,result in results.items():
        if result["pass"]:
            icon="✅"
        else:
            icon="❌"
        st.markdown(f"{icon} {check} — {result['feedback']}")

    if all(i["pass"] for i in results.values()):
        st.success("This photo passed all the validation checks!")
    else:
        st.warning("Some checks failed. Please review the feedback!")

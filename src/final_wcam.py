

import argparse
#from pyzbar.pyzbar import decode
from PIL import Image

import sys
import time

import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils
import serial
import time
import argparse
print(cv2.__version__)









# print alailable serial ports list of computer
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        print("{}: {}".format(port, desc))






# argumnet parsing here
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", required=True,
   help = "com port of arduino")
ap.add_argument("-c", "--cam", required=False,type=int, default=0,
    help = "s 0 default camera 1 webcam")
args = vars(ap.parse_args())


port = args['port']
camera_number = args['cam']
baud = 115200



current_color   = None
current_side    = 0

_CURRENT_GREEN   = "GREEN"
_CURRENT_RED     = "RED"
_CURRENT_YELLOW  = "YELLOW"




_EXTRA_PER_CAR = 5

_GREEN_TIME = 10
_RED_TIME = 15
_YELLOW_TIME = 3



serialPort = serial.Serial(port, baud, timeout=1)
if serialPort.isOpen():
    print(serialPort.name + ' is open...')

serialPort.rts = False
serialPort.dtr = False


def detectVehicles(image, model):
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    # Initialize the object detection model
    options = ObjectDetectorOptions(
        num_threads=8,
        score_threshold=0.3,
        max_results=10,
        enable_edgetpu= bool(False))
      
    detector = ObjectDetector(model_path=model, options=options)


    #image = cv2.imread(image_path)
    detections = detector.detect(image)
    
    image, detected_classes = utils.visualize(image, detections)
    print(detected_classes)
    
    if len(detections) > 0:
        return image, detected_classes
        
    return image, None




seconds = 0
seconds_last = 0
tick = False
last_update = 0

colorLight = (0,0,0)
colorLingtStr =  "off"
countDown = 0
nextUpdate = 0

side1_extra_time = 0


webcam = cv2.VideoCapture(camera_number)
detected_classes = 0

while True:
    detected_classes = []
    # Loop until the camera is working
    rval = False
    while(not rval):
        # Put the image from the webcam into 'img'
        (rval, img) = webcam.read()
        if(not rval):
            print("Failed to open webcam. Trying again...")


    img, detected_classes = detectVehicles(img,'vehicle-ambu-car.tflite2')
    

    
    orgCircle = (20, 20)
    cirSize =   20 
    
    
    car_no = 0
    seconds = int(time.perf_counter())
    
    ambulance = False


    if not detected_classes is None:
        car_no = len(detected_classes)
        for detect in detected_classes:
            if detect.__contains__("ambulance"):
                ambulance = True
                


   

        
    
    if seconds_last != seconds:
        seconds_last = seconds
        tick = True
    
    if ambulance :
        current_color = _CURRENT_GREEN
        last_update = seconds
        current_side = 1
        print("SIDE 1 GREEN ","SIDE 2 RED   ")
        colorLight   = (0,255,0)
        colorLingtStr = 'green'
        serialPort.write("GREEN1 RED2\n".encode('ascii'))


    side1_extra_time = car_no*_EXTRA_PER_CAR



    
    if tick and not ambulance:
        tick = False
        print("tick: ",seconds)
        if current_color is None:
            current_color = _CURRENT_GREEN
            last_update = seconds
            current_side = 1
            print("SIDE 1 GREEN ","SIDE 2 RED   ")
            colorLight   = (0,255,0)
            colorLingtStr = 'green'
            nextUpdate = (last_update + _GREEN_TIME + side1_extra_time) 
            serialPort.write("GREEN1 RED2\n".encode('ascii'))
            
        
            
        if current_color ==  _CURRENT_GREEN and current_side == 1 and nextUpdate < seconds:
            #CHANGE TO YELLOW
            current_color = _CURRENT_YELLOW
            last_update = seconds
            print("SIDE 1 YELLOW","SIDE 2 YELLOW")
            colorLight = (0,234,255)
            colorLingtStr = 'yellow'
            serialPort.write("YELLOW1 YELLOW2\n".encode('ascii'))
            nextUpdate = (last_update + _YELLOW_TIME) 
            
        
        if current_color ==  _CURRENT_YELLOW and current_side == 1 and nextUpdate < seconds:
            #CHANGE TO RED
            current_color = _CURRENT_RED
            last_update = seconds
            print("SIDE 1 RED   ","SIDE 2 GREEN ")
            colorLight = (0,0,255)
            colorLingtStr = 'red'
            serialPort.write("RED1 GREEN2\n".encode('ascii'))
            nextUpdate = (last_update + _RED_TIME ) 
            
            
        if current_color ==  _CURRENT_RED and current_side == 1 and nextUpdate < seconds:
            #CHANGE TO YELLOW
            current_color = _CURRENT_YELLOW
            last_update = seconds
            current_side  = 2
            print("SIDE 1 YELLOW","SIDE 2 YELLOW")
            colorLight = (0,234,255)
            colorLingtStr = 'yellow'
            serialPort.write("YELLOW1 YELLOW2\n".encode('ascii'))
            nextUpdate = (last_update + _YELLOW_TIME ) 
            
            
        if current_color ==  _CURRENT_YELLOW and current_side == 2 and nextUpdate < seconds:
            #CHANGE TO GREEN
            current_color = _CURRENT_GREEN
            last_update = seconds
            current_side = 1
            print("SIDE 1 GREEN ","SIDE 2 RED   ")
            colorLight = (0,255,0)
            colorLingtStr = 'green'
            serialPort.write("GREEN1 RED2\n".encode('ascii'))
            nextUpdate = (last_update + _GREEN_TIME + side1_extra_time) 
                
                
            
            
        #print("color", colorLight)
    
        countDown = nextUpdate-seconds
        #print('Coundown', countDown)
        
        #file_contents = json.loads('{"vehicles":"'+str(car_no)+'","countdown":"'+str(countDown)+'","light":"'+colorLingtStr+'"}')
        
    print('{"vehicles":"'+str(car_no)+'","countdown":"'+str(countDown)+'","light":"'+colorLingtStr+'"}')
    
        
    cv2.circle(img,orgCircle, cirSize, colorLight, -1)  

    font = cv2.FONT_HERSHEY_SIMPLEX 
    # org 
    org = (40, 25) 
    # fontScale 
    fontScale = 1
    # Blue color in BGR 
    color = (255, 0, 0) 
    # Line thickness of 2 px 
    thickness = 2
    #+", Seconds: "+str(seconds)
    img = cv2.putText(img, "Vehicles:"+str(car_no), org, font,  
                   fontScale, color, thickness, cv2.LINE_AA)
    
    posContdwn = (15,25)
    if countDown > 9:
        posContdwn = (10,25)
    
    img = cv2.putText(img,str(countDown), posContdwn, font,  
                   .5, color, 1, cv2.LINE_AA)


    cv2.imshow('Click & Press C to capture', img)

    Key = cv2.waitKey(1)
    if Key == 27:
        cv2.destroyAllWindows()
        break
    
    

    
    
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    